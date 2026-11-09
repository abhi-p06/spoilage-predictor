"""
scripts/train_model_b_v4_1.py
=============================
Phase 2: Retrains Model B (group_aware_mobilenet_v2_v4_1.keras) from a fresh ImageNet initialization.

Trained strictly on: FINAL_GROUP_TRAIN_V4.csv (9,513 images, 1,052 super-groups)
Validated strictly on: FINAL_GROUP_VAL_V4.csv (2,043 images, 226 super-groups)
Never observes test partition: FINAL_GROUP_TEST_V4.csv (2,043 images, 226 super-groups)

Protocol:
- Base architecture: MobileNetV2 pretrained on ImageNet
- Classification head: GlobalAveragePooling2D -> Dropout(0.3) -> Dense(6, softmax)
- Phase 1: Frozen backbone (5 epochs), AdamW(lr=1e-3, wd=1e-4), label smoothing 0.05
- Phase 2: Fine-tuning from layer 100 (up to 10 epochs), AdamW(lr=1e-4, wd=1e-4), label smoothing 0.05
- Early stopping: patience=3 on val_loss
- Checkpoint: group_aware_mobilenet_v2_v4_1.keras (best val_loss)
"""

import os
import sys
import time
import json
import random
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.applications import mobilenet_v2

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CKPT_DIR = PROJECT_ROOT / "experiments" / "group_leakage_study" / "CHECKPOINTS"
CKPT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR = PROJECT_ROOT / "experiments" / "group_leakage_study" / "TRAINING_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PATH = CKPT_DIR / "group_aware_mobilenet_v2_v4_1.keras"
HISTORY_PATH = LOG_DIR / "group_aware_training_history_v4_1.csv"
SHA_REPORT_PATH = PROJECT_ROOT / "MODEL_B_V4_1_CHECKPOINT_SHA256.txt"
TRAINING_REPORT_PATH = PROJECT_ROOT / "MODEL_B_V4_1_TRAINING_REPORT.md"

CLASSES = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]
NUM_CLASSES = 6
INPUT_SHAPE = (224, 224, 3)
BATCH_SIZE = 32
SEED = 42

def set_seed(seed=42):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

def build_dataset(manifest_path: Path, is_training: bool = False):
    df = pd.read_csv(manifest_path)
    file_paths = []
    for fp in df["filepath"]:
        p = Path(fp)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        file_paths.append(str(p))
    labels = df["label_idx"].values.astype(np.int32)

    aug_layers = []
    if is_training:
        aug_layers.append(layers.RandomFlip("horizontal"))
        aug_layers.append(layers.RandomRotation(0.15))
        aug_layers.append(layers.RandomZoom((-0.10, 0.10)))
        aug_layers.append(layers.RandomContrast(0.10))
    aug_model = tf.keras.Sequential(aug_layers) if aug_layers else None

    def process_image(path_tensor, label_tensor):
        img_bytes = tf.io.read_file(path_tensor)
        img = tf.image.decode_image(img_bytes, channels=3, expand_animations=False)
        img = tf.image.resize(img, [INPUT_SHAPE[0], INPUT_SHAPE[1]])
        img.set_shape([INPUT_SHAPE[0], INPUT_SHAPE[1], 3])
        if aug_model is not None:
            img = aug_model(img, training=True)
        img = mobilenet_v2.preprocess_input(img)
        target = tf.one_hot(label_tensor, NUM_CLASSES)
        return img, target

    ds = tf.data.Dataset.from_tensor_slices((file_paths, labels))
    if is_training:
        ds = ds.shuffle(buffer_size=min(len(file_paths), 2000), seed=SEED, reshuffle_each_iteration=True)
    ds = ds.map(process_image, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(BATCH_SIZE)
    if not is_training:
        ds = ds.cache()
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds, len(df)

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

def main():
    print("==================================================================")
    print("🚀 AgriRoute Phase 2: Fresh ImageNet Fine-Tuning of Model B (V4.1)")
    print("==================================================================")
    set_seed(SEED)

    train_manifest = PROJECT_ROOT / "FINAL_GROUP_TRAIN_V4.csv"
    val_manifest = PROJECT_ROOT / "FINAL_GROUP_VAL_V4.csv"
    assert train_manifest.exists() and val_manifest.exists()

    print(f"Loading data from frozen manifests...")
    train_ds, n_train = build_dataset(train_manifest, is_training=True)
    val_ds, n_val = build_dataset(val_manifest, is_training=False)
    print(f"Train samples: {n_train} | Val samples: {n_val}")

    # Fresh instantiation with ImageNet weights
    print("\nInstantiating fresh MobileNetV2 with ImageNet base weights...")
    base_model = mobilenet_v2.MobileNetV2(
        input_shape=INPUT_SHAPE,
        include_top=False,
        weights="imagenet",
        pooling="avg"
    )
    inputs = layers.Input(shape=INPUT_SHAPE, name="input_tensor")
    x = base_model(inputs)
    x = layers.Dropout(0.3, name="top_dropout")(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax", name="predictions", dtype="float32")(x)
    model = models.Model(inputs=inputs, outputs=outputs, name="agriroute_mobilenet_v2_v4_1")

    # Callbacks
    cb_checkpoint = callbacks.ModelCheckpoint(
        filepath=str(CKPT_PATH),
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    )
    cb_early_stop = callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1
    )
    cb_reduce_lr = callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )
    cb_csv_logger = callbacks.CSVLogger(str(HISTORY_PATH), append=False)

    start_time = time.time()

    # Phase 1: Feature extraction (Backbone frozen, 5 epochs)
    print("\n--- Phase 1: Feature Extraction (Backbone Frozen, 5 epochs) ---")
    base_model.trainable = False
    opt_p1 = optimizers.AdamW(learning_rate=0.001, weight_decay=1e-4)
    model.compile(
        optimizer=opt_p1,
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.05),
        metrics=["accuracy"]
    )

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=5,
        callbacks=[cb_checkpoint, cb_early_stop, cb_reduce_lr, cb_csv_logger],
        verbose=2
    )

    # Phase 2: Fine-Tuning (Top layers from layer 100, up to 10 epochs)
    print("\n--- Phase 2: Fine-Tuning Top Layers from Layer 100 (Epochs 6-15) ---")
    base_model.trainable = True
    for layer in base_model.layers[:100]:
        layer.trainable = False

    print(f"Total base layers: {len(base_model.layers)} | Trainable layers: {len([l for l in base_model.layers if l.trainable])}")

    opt_p2 = optimizers.AdamW(learning_rate=0.0001, weight_decay=1e-4)
    model.compile(
        optimizer=opt_p2,
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.05),
        metrics=["accuracy"]
    )

    cb_csv_logger_append = callbacks.CSVLogger(str(HISTORY_PATH), append=True)
    model.fit(
        train_ds,
        validation_data=val_ds,
        initial_epoch=5,
        epochs=15,
        callbacks=[cb_checkpoint, cb_early_stop, cb_reduce_lr, cb_csv_logger_append],
        verbose=2
    )

    total_duration = time.time() - start_time
    print(f"\n✅ Training completed in {total_duration:.1f} seconds ({total_duration/60:.2f} minutes).")

    # Verify best checkpoint
    assert CKPT_PATH.exists(), f"Checkpoint {CKPT_PATH} not found!"
    sha256_hash = compute_sha256(CKPT_PATH)
    file_size = CKPT_PATH.stat().st_size
    print(f"\nBest Checkpoint: {CKPT_PATH}")
    print(f"File Size: {file_size:,} bytes")
    print(f"SHA-256:  {sha256_hash}")

    # Write SHA report
    with open(SHA_REPORT_PATH, "w") as f:
        f.write(f"MODEL_B_V4_1_CHECKPOINT_SHA256: {sha256_hash}\n")
        f.write(f"FILENAME: group_aware_mobilenet_v2_v4_1.keras\n")
        f.write(f"FILE_SIZE_BYTES: {file_size}\n")
        f.write(f"TRAINING_TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n")
        f.write(f"TRAIN_SAMPLES: {n_train}\n")
        f.write(f"VAL_SAMPLES: {n_val}\n")

    # Load and inspect history
    df_hist = pd.read_csv(HISTORY_PATH)
    best_epoch = df_hist.loc[df_hist["val_loss"].idxmin()]

    # Write Markdown training report
    with open(TRAINING_REPORT_PATH, "w") as f:
        f.write(f"""# Model B (V4.1) Training Report: ImageNet Transfer Learning on Post-pHash Merged Split

**Model Identifier:** `agriroute_mobilenet_v2_v4_1`  
**Checkpoint Path:** `experiments/group_leakage_study/CHECKPOINTS/group_aware_mobilenet_v2_v4_1.keras`  
**SHA-256 Checksum:** `{sha256_hash}`  
**Training Date:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}  
**Total Training Duration:** {total_duration:.1f} seconds ({total_duration/60:.2f} minutes)  

---

## 1. Provenance and Initialization

- **Pretrained Weights:** ImageNet (`mobilenet_v2.MobileNetV2(weights="imagenet", include_top=False, pooling="avg")`).
- **Classification Head:** Global Average Pooling (1280-d) $\\to$ `Dropout(p=0.3)` $\\to$ `Dense(6, activation="softmax", dtype="float32")`.
- **Initialization Rule Compliance:** Genuinely retrained from ImageNet initialization; legacy Model B weights were **not** reused.
- **Dataset Partition:** Strictly trained on `FINAL_GROUP_TRAIN_V4.csv` ($N=9,513$ images, 1,052 super-groups). Model selection and early stopping conducted strictly on `FINAL_GROUP_VAL_V4.csv` ($N=2,043$ images, 226 super-groups). The final test partition `FINAL_GROUP_TEST_V4.csv` remained completely unobserved.

---

## 2. Hyperparameter Configuration

| Hyperparameter | Phase 1 (Feature Extraction) | Phase 2 (Fine-Tuning) |
| :--- | :--- | :--- |
| **Backbone Trainability** | Frozen (`trainable=False`) | Layers 100–154 Trainable (Layers 0–99 Frozen) |
| **Optimizer** | AdamW (`weight_decay=1e-4`) | AdamW (`weight_decay=1e-4`) |
| **Learning Rate** | $1.0 \\times 10^{-3}$ | $1.0 \\times 10^{-4}$ (with `ReduceLROnPlateau(factor=0.2, patience=2)`) |
| **Loss Function** | Categorical Crossentropy (`label_smoothing=0.05`) | Categorical Crossentropy (`label_smoothing=0.05`) |
| **Batch Size** | 32 | 32 |
| **Epochs Scheduled** | 5 | 10 (epochs 6 to 15) |
| **Data Augmentation** | Random Flip (Horizontal), Random Rotation (0.15), Random Zoom (0.10), Random Contrast (0.10) | Identical |
| **Input Preprocessing** | `mobilenet_v2.preprocess_input` ($[-1, 1]$) | `mobilenet_v2.preprocess_input` ($[-1, 1]$) |
| **Random Seed** | 42 | 42 |

---

## 3. Training Trajectory & Convergence

- **Best Validation Epoch:** Epoch {int(best_epoch['epoch']) + 1}
- **Best Validation Loss:** {best_epoch['val_loss']:.4f}
- **Validation Accuracy at Best Epoch:** {best_epoch['val_accuracy']*100:.2f}%
- **Training Accuracy at Best Epoch:** {best_epoch['accuracy']*100:.2f}%

### Complete Epoch History
```csv
{df_hist.to_csv(index=False)}
```

---

## 4. Software Environment Manifest
- **Platform:** macOS Darwin (Apple Silicon M4, Metal GPU PluggableDevice)
- **TensorFlow Version:** {tf.__version__}
- **NumPy Version:** {np.__version__}
- **Pandas Version:** {pd.__version__}
""")

    print(f"✅ Generated {SHA_REPORT_PATH}")
    print(f"✅ Generated {TRAINING_REPORT_PATH}")

if __name__ == "__main__":
    main()
