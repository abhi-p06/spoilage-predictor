#!/usr/bin/env python
# coding: utf-8

# # Notebook 01 — CNN Freshness Classifier
# **Architecture:** MobileNetV2 (transfer learning, ImageNet weights)  
# **Task:** Binary classification — fresh (0) vs rotten (1)  
# **Dataset:** Kaggle `sriramr/fruits-fresh-and-rotten-for-classification` (~13 000 PNG images)  
# **Target:** val_accuracy > 85%  
# **Output:** `models/cnn_freshness.h5`  
# 
# **Dataset class folders (actual names on disk):**
# ```
# train/  freshapples/  freshbanana/  freshoranges/
#         rottenapples/ rottenbanana/ rottenoranges/
# test/   (same structure)
# ```
# 
# **Training strategy (two phases):**
# 1. Freeze the MobileNetV2 base → train only the classification head for 10 epochs.
# 2. Unfreeze the last 30 layers of the base → fine-tune end-to-end at a lower LR for 10 epochs.

# ## 1 — Imports & Configuration

# In[1]:


import os
import warnings
from pathlib import Path

# Suppress TF info logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print(f"TensorFlow version : {tf.__version__}")
print(f"Keras version      : {keras.__version__}")
print(f"GPU / Metal devices: {tf.config.list_physical_devices('GPU')}")


# In[ ]:


# ── Paths ─────────────────────────────────────────────────────────────────────
# Notebook lives at  spoilage-predictor/notebooks/
# PROJECT_ROOT is    spoilage-predictor/
PROJECT_ROOT = Path().resolve().parent

# Kaggle extracts to:  data/images/dataset/dataset/train  &  .../test
# (verified on disk after download)
DATA_DIR   = PROJECT_ROOT / "data" / "images" / "dataset" / "dataset"
TRAIN_DIR  = DATA_DIR / "train"     # lowercase — actual folder name on disk
TEST_DIR   = DATA_DIR / "test"      # lowercase — actual folder name on disk
MODEL_DIR  = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "cnn_freshness.h5"

assert TRAIN_DIR.exists(), f"Train dir not found: {TRAIN_DIR}\nCheck dataset was downloaded correctly."
assert TEST_DIR.exists(),  f"Test dir not found: {TEST_DIR}"

# ── Hyper-parameters ──────────────────────────────────────────────────────────
IMG_SIZE    = (224, 224)
BATCH_SIZE  = 32
EPOCHS_HEAD = 10          # Phase 1: head only
EPOCHS_FINE = 10          # Phase 2: fine-tune
LR_HEAD     = 1e-3
LR_FINE     = 1e-4
AUTOTUNE    = tf.data.AUTOTUNE
SEED        = 42

print(f"Train dir : {TRAIN_DIR}")
print(f"Test dir  : {TEST_DIR}")
print(f"Model out : {MODEL_PATH}")


# ## 2 — Dataset Verification

# In[ ]:


def count_images(root: Path) -> pd.DataFrame:
    """Count images (.png / .jpg) per subdirectory under root."""
    rows = []
    for subdir in sorted(root.iterdir()):
        if not subdir.is_dir():
            continue
        imgs = list(subdir.glob("*.png")) + list(subdir.glob("*.jpg"))
        rows.append({"class": subdir.name, "count": len(imgs)})
    return pd.DataFrame(rows)

train_counts = count_images(TRAIN_DIR)
test_counts  = count_images(TEST_DIR)

print("Training images per class:")
print(train_counts.to_string(index=False))
print(f"  Total train: {train_counts['count'].sum():,}")

print("\nTest images per class:")
print(test_counts.to_string(index=False))
print(f"  Total test : {test_counts['count'].sum():,}")


# ## 3 — tf.data Pipeline with Augmentation

# In[ ]:


def get_label(class_name: str) -> int:
    """
    Map Kaggle class folder names to binary freshness label.
    Folders starting with 'fresh'  → 0  (fresh / high freshness score)
    Folders starting with 'rotten' → 1  (rotten)
    Works for: freshapples, freshbanana, freshoranges,
               rottenapples, rottenbanana, rottenoranges
    """
    return 0 if class_name.startswith("fresh") else 1

def build_file_list(split_dir: Path):
    """Return (file_paths, labels) for all images under split_dir."""
    file_paths, labels = [], []
    for subdir in sorted(split_dir.iterdir()):
        if not subdir.is_dir():
            continue
        label = get_label(subdir.name)
        for img_path in list(subdir.glob("*.png")) + list(subdir.glob("*.jpg")):
            file_paths.append(str(img_path))
            labels.append(label)
    return file_paths, labels

train_paths, train_labels = build_file_list(TRAIN_DIR)
test_paths,  test_labels  = build_file_list(TEST_DIR)

print(f"Train: {len(train_paths):,} images  (fresh={train_labels.count(0):,}, rotten={train_labels.count(1):,})")
print(f"Test : {len(test_paths):,} images   (fresh={test_labels.count(0):,},  rotten={test_labels.count(1):,})")


# In[ ]:


@tf.function
def load_and_preprocess(path, label):
    """Read → decode PNG → resize → normalise to [0,1]."""
    raw = tf.io.read_file(path)
    img = tf.image.decode_png(raw, channels=3)
    img = tf.image.resize(img, IMG_SIZE)
    img = tf.cast(img, tf.float32) / 255.0
    return img, label

# Augmentation applied only during training
augment_layer = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.10),
    layers.RandomBrightness(0.10),
    layers.RandomContrast(0.10),
], name="augmentation")

@tf.function
def augment(img, label):
    img = augment_layer(img, training=True)
    return img, label

def make_dataset(paths, labels, augment_data=False, shuffle=False):
    """
    Build a tf.data.Dataset from file path lists.

    Parameters
    ----------
    paths        : list[str]
    labels       : list[int]  — 0=fresh, 1=rotten
    augment_data : bool — apply augmentation (training only)
    shuffle      : bool
    """
    ds = tf.data.Dataset.from_tensor_slices(
        (paths, tf.cast(labels, tf.int32))
    )
    if shuffle:
        ds = ds.shuffle(buffer_size=len(paths), seed=SEED, reshuffle_each_iteration=True)
    ds = ds.map(load_and_preprocess, num_parallel_calls=AUTOTUNE)
    if augment_data:
        ds = ds.map(augment, num_parallel_calls=AUTOTUNE)
    ds = ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)
    return ds

train_ds = make_dataset(train_paths, train_labels, augment_data=True,  shuffle=True)
test_ds  = make_dataset(test_paths,  test_labels,  augment_data=False, shuffle=False)

print("Datasets ready.")
for imgs, lbls in train_ds.take(1):
    print(f"  Batch shape : {imgs.shape}  Labels shape: {lbls.shape}")
    print(f"  Pixel range : [{imgs.numpy().min():.2f}, {imgs.numpy().max():.2f}]")


# In[ ]:


class_names = ["Fresh", "Rotten"]
fig, axes = plt.subplots(2, 5, figsize=(14, 6))
for imgs, lbls in train_ds.take(1):
    for i, ax in enumerate(axes.flat):
        ax.imshow(imgs[i].numpy())
        ax.set_title(class_names[int(lbls[i])], fontsize=10,
                     color='green' if lbls[i] == 0 else 'red')
        ax.axis('off')
plt.suptitle("Sample Training Batch (augmented)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(PROJECT_ROOT / "notebooks" / "sample_batch.png", dpi=100, bbox_inches='tight')
plt.show()


# ## 4 — Build MobileNetV2 Model

# In[ ]:


def build_model(trainable_base: bool = False) -> keras.Model:
    """
    MobileNetV2-based binary freshness classifier.

    Architecture
    ------------
    MobileNetV2 base (ImageNet weights, 224×224×3)
    → GlobalAveragePooling2D
    → Dense(256, relu) + Dropout(0.4)
    → Dense(1, sigmoid)   [1=rotten → freshness_score = 1 - output]

    Parameters
    ----------
    trainable_base : False = Phase 1 (frozen base)
                     True  = Phase 2 (last 30 layers unfrozen)
    """
    base = keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )
    base.trainable = False

    if trainable_base:
        for layer in base.layers[-30:]:
            layer.trainable = True

    inputs  = keras.Input(shape=(*IMG_SIZE, 3), name="image_input")
    # MobileNetV2 expects [-1, 1] — preprocess_input scales from [0,1]
    x = keras.applications.mobilenet_v2.preprocess_input(inputs * 255.0)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dense(256, activation="relu", name="fc1")(x)
    x = layers.Dropout(0.4, name="dropout")(x)
    outputs = layers.Dense(1, activation="sigmoid", name="freshness_score")(x)

    return keras.Model(inputs, outputs, name="cnn_freshness")

model = build_model(trainable_base=False)
model.summary(line_length=90)


# ## 5 — Phase 1: Train Head Only (frozen base)

# In[ ]:


model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LR_HEAD),
    loss="binary_crossentropy",
    metrics=["accuracy", keras.metrics.AUC(name="auc")]
)

callbacks_phase1 = [
    keras.callbacks.EarlyStopping(
        monitor="val_accuracy", patience=4,
        restore_best_weights=True, verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=2,
        min_lr=1e-6, verbose=1
    ),
]

print(f"Phase 1: Training classification head for up to {EPOCHS_HEAD} epochs…")
history_p1 = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=EPOCHS_HEAD,
    callbacks=callbacks_phase1,
    verbose=1,
)


# ## 6 — Phase 2: Fine-tune Last 30 Base Layers

# In[ ]:


# Rebuild with unfrozen layers, transfer Phase 1 weights
model_ft = build_model(trainable_base=True)
model_ft.set_weights(model.get_weights())

trainable_count = sum(1 for l in model_ft.layers if l.trainable)
print(f"Trainable layers in Phase 2: {trainable_count}")

model_ft.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LR_FINE),
    loss="binary_crossentropy",
    metrics=["accuracy", keras.metrics.AUC(name="auc")]
)

callbacks_phase2 = [
    keras.callbacks.EarlyStopping(
        monitor="val_accuracy", patience=5,
        restore_best_weights=True, verbose=1
    ),
    keras.callbacks.ModelCheckpoint(
        filepath=str(MODEL_PATH),
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=3,
        min_lr=1e-7, verbose=1
    ),
]

print(f"Phase 2: Fine-tuning for up to {EPOCHS_FINE} epochs…")
history_p2 = model_ft.fit(
    train_ds,
    validation_data=test_ds,
    epochs=EPOCHS_FINE,
    callbacks=callbacks_phase2,
    verbose=1,
)


# ## 7 — Training Curves

# In[ ]:


def merge_histories(h1, h2):
    """Concatenate two Keras History dicts."""
    merged = {}
    for key in h1.history:
        merged[key] = h1.history[key] + h2.history.get(key, [])
    return merged

hist    = merge_histories(history_p1, history_p2)
ep_range = range(1, len(hist["accuracy"]) + 1)
p1_end   = len(history_p1.history["accuracy"])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(ep_range, hist["accuracy"],     lw=2, color="#0F6E56", label="Train Acc")
ax1.plot(ep_range, hist["val_accuracy"], lw=2, color="#F59E0B", linestyle="--", label="Val Acc")
ax1.axvline(p1_end, color='grey', ls=':', alpha=0.7, label='Fine-tune start')
ax1.axhline(0.85,   color='red',  ls='--', alpha=0.5, label='Target 85%')
ax1.set(title="Accuracy", xlabel="Epoch", ylabel="Accuracy")
ax1.legend(); ax1.grid(alpha=0.3)

ax2.plot(ep_range, hist["loss"],     lw=2, color="#0F6E56", label="Train Loss")
ax2.plot(ep_range, hist["val_loss"], lw=2, color="#F59E0B", linestyle="--", label="Val Loss")
ax2.axvline(p1_end, color='grey', ls=':', alpha=0.7, label='Fine-tune start')
ax2.set(title="Loss", xlabel="Epoch", ylabel="Binary Cross-Entropy")
ax2.legend(); ax2.grid(alpha=0.3)

plt.suptitle("CNN Training History — Phase 1 + Phase 2", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(PROJECT_ROOT / "notebooks" / "cnn_training_curves.png", dpi=120, bbox_inches='tight')
plt.show()


# ## 8 — Evaluation (Accuracy + Confusion Matrix)

# In[ ]:


best_model = keras.models.load_model(MODEL_PATH)

test_results  = best_model.evaluate(test_ds, verbose=0)
metrics_names = best_model.metrics_names
print("── Test Set Results ─────────────────────────────────")
for name, val in zip(metrics_names, test_results):
    print(f"  {name:<12}: {val:.4f}")

val_acc = dict(zip(metrics_names, test_results))["accuracy"]
target  = "✅ TARGET MET" if val_acc >= 0.85 else "⚠️  Below target"
print(f"\nval_accuracy = {val_acc:.4f}  ({target} — target ≥ 0.85)")


# In[ ]:


y_pred_prob = best_model.predict(test_ds, verbose=0).flatten()
y_pred      = (y_pred_prob >= 0.5).astype(int)
y_true      = np.array(test_labels)

print("Classification Report:")
print(classification_report(y_true, y_pred, target_names=["Fresh", "Rotten"]))

cm = confusion_matrix(y_true, y_pred)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
            xticklabels=["Fresh", "Rotten"],
            yticklabels=["Fresh", "Rotten"],
            ax=ax, linewidths=0.5)
ax.set(title="Confusion Matrix — CNN Freshness Classifier",
       xlabel="Predicted", ylabel="True")
plt.tight_layout()
plt.savefig(PROJECT_ROOT / "notebooks" / "cnn_confusion_matrix.png", dpi=120, bbox_inches='tight')
plt.show()


# ## 9 — Save Model & Inference Sanity Check

# In[ ]:


# ModelCheckpoint already saved the best model during training.
# This cell re-saves explicitly and confirms the path.
best_model.save(MODEL_PATH)
print(f"✅  Model saved → {MODEL_PATH}")
print(f"    File size  : {MODEL_PATH.stat().st_size / 1e6:.1f} MB")

print("\nOutput mapping:")
print("  raw sigmoid output ∈ [0,1]  where  1=rotten, 0=fresh")
print("  predict.py uses: freshness_score = 1 − raw")
print("  → freshness_score = 1.0  means perfectly fresh")
print("  → freshness_score = 0.0  means completely rotten")

# Quick single-image inference test
sample_img_path = train_paths[0]
raw_bytes = tf.io.read_file(sample_img_path)
img = tf.image.decode_png(raw_bytes, channels=3)
img = tf.image.resize(img, IMG_SIZE)
img = tf.cast(img, tf.float32) / 255.0
img = tf.expand_dims(img, 0)   # (1, 224, 224, 3)
raw_pred    = float(best_model.predict(img, verbose=0)[0][0])
freshness   = 1.0 - raw_pred
print(f"\nSample inference → raw={raw_pred:.3f}  freshness_score={freshness:.3f}")
print(f"  True label : {'Fresh' if train_labels[0]==0 else 'Rotten'}")

