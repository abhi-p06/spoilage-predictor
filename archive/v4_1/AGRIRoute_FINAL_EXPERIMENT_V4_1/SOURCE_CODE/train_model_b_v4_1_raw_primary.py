"""
scripts/train_model_b_v4_1_raw_primary.py
=========================================
Primary Experiment: Train MobileNetV2 strictly on the 1,057 original raw images (is_raw == 1).

Dataset partitions:
- Training: FINAL_GROUP_TRAIN_V4_1.csv filtered by is_raw == 1 (N = 1,057)
- Validation: FINAL_GROUP_VAL_V4_1.csv filtered by is_raw == 1 (N = 227)
- Testing: FINAL_GROUP_TEST_V4_1.csv filtered by is_raw == 1 (N = 227, unobserved during training)

Data Augmentation:
- Online augmentation strictly applied to training images only:
  RandomFlip("horizontal"), RandomRotation(0.15), RandomZoom((-0.10, 0.10)), RandomContrast(0.10)
- Validation and testing remain completely unaugmented.

Model:
- Base: MobileNetV2 pretrained on ImageNet
- Head: GlobalAveragePooling2D -> Dropout(0.3) -> Dense(6, softmax)
- Phase 1: Frozen backbone (10 epochs), AdamW(lr=1e-3, wd=1e-4), label smoothing 0.05
- Phase 2: Fine-tuning from layer 100 (up to 20 epochs), AdamW(lr=1e-4, wd=1e-4), label smoothing 0.05
- Early stopping: patience=5 on val_loss
- Checkpoint: group_aware_mobilenet_v2_v4_1.keras (best val_loss) and MODEL_B_V4_1_CHECKPOINT.keras
"""

import os
import sys
import time
import json
import shutil
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
ROOT_CKPT_PATH = PROJECT_ROOT / "MODEL_B_V4_1_CHECKPOINT.keras"
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

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

def verify_and_load_raw_manifest(manifest_path: Path, expected_raw_count: int, name: str) -> pd.DataFrame:
    assert manifest_path.exists(), f"Manifest {manifest_path} not found!"
    df = pd.read_csv(manifest_path)
    df_raw = df[df["is_raw"] == 1].copy().reset_index(drop=True)
    
    # Verify count
    assert len(df_raw) == expected_raw_count, f"{name} expected {expected_raw_count} raw images, got {len(df_raw)}"
    
    # Verify every file exists on disk
    missing_files = []
    for fp in df_raw["filepath"]:
        p = Path(fp)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        if not p.exists():
            missing_files.append(str(p))
    assert len(missing_files) == 0, f"{name} has {len(missing_files)} missing image files: {missing_files[:5]}"
    print(f"✅ {name}: Verified exactly {len(df_raw)} raw images (is_raw == 1) present on disk.")
    return df_raw

def build_dataset(df_subset: pd.DataFrame, is_training: bool = False):
    file_paths = []
    for fp in df_subset["filepath"]:
        p = Path(fp)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        file_paths.append(str(p))
    labels = df_subset["label_idx"].values.astype(np.int32)

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
        ds = ds.shuffle(buffer_size=min(len(file_paths), 1500), seed=SEED, reshuffle_each_iteration=True)
    ds = ds.map(process_image, num_parallel_calls=4)
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(1)
    return ds, len(df_subset)

def main():
    print("==================================================================")
    print("🚀 AgriRoute Primary Experiment: Raw-Only ImageNet Fine-Tuning")
    print("==================================================================")
    set_seed(SEED)

    train_manifest = PROJECT_ROOT / "FINAL_GROUP_TRAIN_V4_1.csv"
    val_manifest = PROJECT_ROOT / "FINAL_GROUP_VAL_V4_1.csv"
    test_manifest = PROJECT_ROOT / "FINAL_GROUP_TEST_V4_1.csv"

    # 1. Manifest Verification
    print("\n--- Verifying Exact Raw Image Counts (is_raw == 1) ---")
    df_train_raw = verify_and_load_raw_manifest(train_manifest, 1057, "Training Partition")
    df_val_raw = verify_and_load_raw_manifest(val_manifest, 227, "Validation Partition")
    df_test_raw = verify_and_load_raw_manifest(test_manifest, 227, "Testing Partition (Unobserved)")

    # 2. Build Datasets
    print("\n--- Building Data Pipelines ---")
    print("Training: Online augmentation enabled.")
    print("Validation: Pure unaugmented raw screenshots.")
    train_ds, n_train = build_dataset(df_train_raw, is_training=True)
    val_ds, n_val = build_dataset(df_val_raw, is_training=False)
    print(f"Train batches: {len(df_train_raw)//BATCH_SIZE + 1} | Val batches: {len(df_val_raw)//BATCH_SIZE + 1}")

    # 3. Model Architecture Instantiation
    print("\n--- Instantiating MobileNetV2 (ImageNet Pretrained) ---")
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
    model = models.Model(inputs=inputs, outputs=outputs, name="agriroute_mobilenet_v2_v4_1_primary")

    # 4. Callbacks
    cb_checkpoint = callbacks.ModelCheckpoint(
        filepath=str(CKPT_PATH),
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    )
    cb_early_stop = callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    cb_reduce_lr = callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=3,
        min_lr=1e-6,
        verbose=1
    )
    cb_csv_logger = callbacks.CSVLogger(str(HISTORY_PATH), append=False)

    start_time = time.time()

    # 5. Phase 1: Feature extraction (Backbone frozen, 10 epochs)
    print("\n--- Phase 1: Feature Extraction (Backbone Frozen, 10 epochs) ---")
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
        epochs=10,
        callbacks=[cb_checkpoint, cb_early_stop, cb_reduce_lr, cb_csv_logger],
        verbose=2
    )

    # 6. Phase 2: Fine-Tuning (Top layers from layer 100, up to 20 epochs)
    print("\n--- Phase 2: Fine-Tuning Top Layers from Layer 100 (Epochs 11-30) ---")
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
        initial_epoch=10,
        epochs=30,
        callbacks=[cb_checkpoint, cb_early_stop, cb_reduce_lr, cb_csv_logger_append],
        verbose=2
    )

    total_duration = time.time() - start_time
    print(f"\n✅ Training completed in {total_duration:.1f} seconds ({total_duration/60:.2f} minutes).")

    # Verify best checkpoint
    assert CKPT_PATH.exists(), f"Checkpoint {CKPT_PATH} not found!"
    sha256_hash = compute_sha256(CKPT_PATH)
    file_size = CKPT_PATH.stat().st_size

    # Copy to project root as MODEL_B_V4_1_CHECKPOINT.keras
    shutil.copy2(CKPT_PATH, ROOT_CKPT_PATH)
    print(f"✅ Copied checkpoint to {ROOT_CKPT_PATH}")

    print(f"\nBest Checkpoint: {CKPT_PATH}")
    print(f"File Size: {file_size:,} bytes")
    print(f"SHA-256:  {sha256_hash}")

    # Write SHA report
    with open(SHA_REPORT_PATH, "w") as f:
        f.write(f"MODEL_B_V4_1_CHECKPOINT_SHA256: {sha256_hash}\n")
        f.write(f"FILENAME: group_aware_mobilenet_v2_v4_1.keras\n")
        f.write(f"ROOT_CHECKPOINT_ALIAS: MODEL_B_V4_1_CHECKPOINT.keras\n")
        f.write(f"FILE_SIZE_BYTES: {file_size}\n")
        f.write(f"TRAINING_TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n")
        f.write(f"TRAIN_SAMPLES_RAW_ONLY: {n_train}\n")
        f.write(f"VAL_SAMPLES_RAW_ONLY: {n_val}\n")
        f.write(f"TEST_SAMPLES_RAW_ONLY: {len(df_test_raw)}\n")

    # Write Model Configuration JSON
    config_dict = {
        "model_name": "agriroute_mobilenet_v2_v4_1_primary",
        "architecture": "MobileNetV2",
        "weights_init": "imagenet",
        "num_classes": 6,
        "classes": CLASSES,
        "input_shape": list(INPUT_SHAPE),
        "seed": SEED,
        "batch_size": BATCH_SIZE,
        "training_mode": "raw_screenshots_only_online_augmentation",
        "raw_train_samples": n_train,
        "raw_val_samples": n_val,
        "raw_test_samples": len(df_test_raw),
        "phase1_epochs": 10,
        "phase1_lr": 0.001,
        "phase2_epochs": 20,
        "phase2_lr": 0.0001,
        "fine_tune_start_layer": 100,
        "label_smoothing": 0.05,
        "weight_decay": 1e-4,
        "train_manifest": "FINAL_GROUP_TRAIN_V4_1.csv (is_raw == 1)",
        "val_manifest": "FINAL_GROUP_VAL_V4_1.csv (is_raw == 1)",
        "test_manifest": "FINAL_GROUP_TEST_V4_1.csv (is_raw == 1)",
        "checkpoint_filename": "group_aware_mobilenet_v2_v4_1.keras",
        "checkpoint_root_alias": "MODEL_B_V4_1_CHECKPOINT.keras",
        "checkpoint_sha256": sha256_hash,
        "checkpoint_size_bytes": file_size,
        "training_timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    }
    with open(CKPT_DIR / "model_b_v4_1_config.json", "w") as f:
        json.dump(config_dict, f, indent=2)
    with open(PROJECT_ROOT / "model_b_v4_1_config.json", "w") as f:
        json.dump(config_dict, f, indent=2)
    print(f"✅ Generated model configuration JSON at {PROJECT_ROOT / 'model_b_v4_1_config.json'}")

    # Load and inspect history
    df_hist = pd.read_csv(HISTORY_PATH)
    best_epoch = df_hist.loc[df_hist["val_loss"].idxmin()]

    # Write Markdown training report
    with open(TRAINING_REPORT_PATH, "w") as f:
        f.write(f"""# Model B (V4.1) Primary Training Report: Raw-Only ImageNet Fine-Tuning

**Model Identifier:** `agriroute_mobilenet_v2_v4_1_primary`  
**Checkpoint Path:** `experiments/group_leakage_study/CHECKPOINTS/group_aware_mobilenet_v2_v4_1.keras`  
**Root Alias:** `MODEL_B_V4_1_CHECKPOINT.keras`  
**SHA-256 Checksum:** `{sha256_hash}`  
**Training Date:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}  
**Total Training Duration:** {total_duration:.1f} seconds ({total_duration/60:.2f} minutes)  

---

## 1. Experimental Design & Partition Rigor

- **Primary Experiment Mandate:** Trained strictly on original fruit specimen screenshots identified by `is_raw == 1`.
- **Training Partition:** Exactly 1,057 raw screenshots from `FINAL_GROUP_TRAIN_V4_1.csv`.
- **Validation Partition:** Exactly 227 unaugmented raw screenshots from `FINAL_GROUP_VAL_V4_1.csv` (used solely for early stopping and temperature scaling).
- **Test Partition:** Exactly 227 unaugmented raw screenshots from `FINAL_GROUP_TEST_V4_1.csv` (completely unobserved during training and tuning).
- **Online Augmentation:** Applied during runtime strictly to the 1,057 training images (RandomFlip, RandomRotation(0.15), RandomZoom(0.10), RandomContrast(0.10)). Validation and test remain unaugmented.

---

## 2. Hyperparameter Configuration

| Hyperparameter | Phase 1 (Feature Extraction) | Phase 2 (Fine-Tuning) |
| :--- | :--- | :--- |
| **Backbone Trainability** | Frozen (`trainable=False`) | Layers 100–154 Trainable (Layers 0–99 Frozen) |
| **Optimizer** | AdamW (`weight_decay=1e-4`) | AdamW (`weight_decay=1e-4`) |
| **Learning Rate** | $1.0 \\times 10^{-3}$ | $1.0 \\times 10^{-4}$ (with `ReduceLROnPlateau(factor=0.2, patience=3)`) |
| **Loss Function** | Categorical Crossentropy (`label_smoothing=0.05`) | Categorical Crossentropy (`label_smoothing=0.05`) |
| **Batch Size** | 32 | 32 |
| **Epochs Scheduled** | 10 | 20 (epochs 11 to 30) |
| **Early Stopping** | Patience = 5 on `val_loss` | Patience = 5 on `val_loss` |
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

