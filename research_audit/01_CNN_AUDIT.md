# Forensic Audit 01: Computer Vision & MobileNetV2 Freshness Classifier

> **Audit Date:** 2026-11-09  
> **Auditor:** Independent Scientific Auditor  
> **Target System:** AgriRoute Image Freshness Module  
> **Primary Script:** `notebooks/01_cnn_training.py` (and `train_all.py` Stage 1)  
> **Execution Log:** `logs/cnn_training.log` (Git commit `0af3146`)  
> **Manuscript Claim:** MobileNetV2 achieves 97.22% accuracy across fresh and spoiling produce.

---

## 1. Executive Summary & Verdict

| Parameter | Audit Finding | Classification |
|---|---|---|
| **Reported Metric** | 97.22% Accuracy | `REPOSITORY-REPORTED` |
| **Exact Source of 97.22%** | Epoch 5 checkpoint restore; scalar `compile_metrics: 0.9722` in `logs/cnn_training.log` | `VERIFIED` |
| **Per-Class Metrics / Confusion Matrix** | **Never computed or evaluated**; script crashed on line 396 (`KeyError: 'accuracy'`) | `UNSUPPORTED` |
| **Dataset Origin** | Kaggle `sriramr/fruits-fresh-and-rotten-for-classification` | `VERIFIED` |
| **Produce Species in Dataset** | **Apple, Banana, Orange only (3 species)** | `VERIFIED` |
| **Manuscript Scope Claim** | Claims coverage of **Apple, Banana, Tomato, Mango (4 species)**; Tomato & Mango absent | `UNSUPPORTED` |
| **Split & Leakage Hygiene** | Pre-divided Kaggle `train/` and `test/` folders; `test_ds` used as validation during training | `CRITICAL DEFECT` |
| **Model Weights Availability** | Deleted from working tree in git commit `568fd604b6` | `DEFECTIVE` |

---

## 2. Dataset Provenance & Class Distribution

### 2.1 Upstream Origin
The dataset was downloaded via `download_dataset.py` from Kaggle:
- **Dataset Slug:** `sriramr/fruits-fresh-and-rotten-for-classification`
- **Total Image Count:** 13,599 images (10,901 train, 2,698 test)
- **Format:** RGB PNG and JPEG images of varying resolutions (standardized to $224 \times 224 \times 3$)

### 2.2 Class & Partition Counts
From `notebooks/01_cnn_training.py` (lines 92–112) and `logs/cnn_training.log`:

| Class Name on Disk | Category | Train Count | Test Count | Total Count |
|---|---|---|---|---|
| `freshapples` | Apple (Fresh) | 1,693 | 395 | 2,088 |
| `rottenapples` | Apple (Rotten) | 2,342 | 601 | 2,943 |
| `freshbanana` | Banana (Fresh) | 1,581 | 381 | 1,962 |
| `rottenbanana` | Banana (Rotten) | 2,224 | 530 | 2,754 |
| `freshoranges` | Orange (Fresh) | 1,466 | 388 | 1,854 |
| `rottenoranges` | Orange (Rotten) | 1,595 | 403 | 1,998 |
| **Total** | **6 Classes / 3 Produce Types** | **10,901** | **2,698** | **13,599** |

### 2.3 The "Four Produce Types" Discrepancy
- The manuscript (Abstract, Section I, Table I, and Web App UI) claims AgriRoute supports **Apple, Banana, Tomato, and Mango**.
- `download_dataset.py` explicitly states in its docstring (lines 16–17):
  ```python
  # We keep only apple, banana; tomato/mango images need a second dataset.
  ```
- **Finding:** No tomato or mango images were ever downloaded, trained on, or evaluated. The vision model has **zero learned parameters for Tomato and Mango**. When tested on Tomato or Mango in the web app, the model either evaluates out-of-distribution features on an apple/banana backbone or executes the random MD5 fallback.

---

## 3. Data Preprocessing & Augmentation Pipeline

### 3.1 Preprocessing Pipeline
Defined in `notebooks/01_cnn_training.py` lines 151–158:
```python
@tf.function
def load_and_preprocess(path, label):
    raw = tf.io.read_file(path)
    img = tf.image.decode_png(raw, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = tf.cast(img, tf.float32) / 255.0
    return img, label
```
In the model architecture (lines 255–256), MobileNetV2's built-in scaling is applied:
```python
x = keras.applications.mobilenet_v2.preprocess_input(inputs * 255.0)
```
This scales pixel values to $[-1.0, 1.0]$ as expected by pre-trained ImageNet weights.

### 3.2 Augmentation Layers
Defined in lines 161–173 (applied exclusively during training when `augment_data=True`):
- `layers.RandomFlip("horizontal")`
- `layers.RandomRotation(0.15)` ($\pm 15\%$)
- `layers.RandomZoom(0.10)` ($\pm 10\%$)
- `layers.RandomBrightness(0.10)` ($\pm 10\%$)
- `layers.RandomContrast(0.10)` ($\pm 10\%$)

**Audit Assessment:** The augmentation parameters are physically conservative and domain-appropriate; they avoid color distortions that would artificially mimic fungal rot.

---

## 4. Architecture & Training Regimen

### 4.1 Neural Network Topology
From `notebooks/01_cnn_training.py` lines 227–264:
- **Base Network:** `keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights="imagenet")`
- **Pooling:** `layers.GlobalAveragePooling2D(name="gap")` (1,280 features)
- **Dense Layer:** `layers.Dense(256, activation="relu", name="fc1")`
- **Regularization:** `layers.Dropout(0.4, name="dropout")`
- **Output Layer:** `layers.Dense(1, activation="sigmoid", name="freshness_score")`
- **Total Parameters:** 2,585,025
  - Base MobileNetV2: 2,257,984
  - Classification Head: 327,041

### 4.2 Two-Stage Transfer Learning Protocol

| Phase | Target Layers | Trainable Params | Initial LR | Epochs | Early Stopping Patience |
|---|---|---|---|---|---|
| **Phase 1: Head Only** | Base frozen; only `fc1` and output trained | 328,193 | $1 \times 10^{-3}$ | Up to 10 | 4 epochs (monitored `val_accuracy`) |
| **Phase 2: Fine-Tuning** | Last 30 layers of MobileNetV2 unfrozen | 1,539,969 | $1 \times 10^{-4}$ | Up to 10 | 5 epochs (monitored `val_accuracy`) |

- **Loss Function:** `binary_crossentropy`
- **Optimizer:** `Adam` with `ReduceLROnPlateau` (factor=0.5, patience=2–3, min_lr=$10^{-7}$)
- **Batch Size:** 32

---

## 5. The Exact Source of the Reported 97.22% Accuracy

The figure of **97.22%** in the manuscript originates from `logs/cnn_training.log` (generated from git commit `0af3146`):

1. During Phase 2 fine-tuning, training proceeded through 10 epochs.
2. At **Epoch 5**, the validation accuracy reached its peak:
   ```text
   Epoch 5: val_accuracy improved from 0.96887 to 0.97220, saving model to .../cnn_freshness.keras
   ```
3. At Epoch 10, early stopping triggered:
   ```text
   Epoch 10: early stopping
   Restoring model weights from the end of the best epoch: 5.
   ── Test Set Results ─────────────────────────────────
     loss        : 0.0792
     compile_metrics: 0.9722
   ```
4. **The Critical Crash:** Immediately following line 395, line 396 executed:
   ```python
   val_acc = dict(zip(metrics_names, test_results))["accuracy"]
   ```
   Under Keras 3.x, `best_model.metrics_names` contained `['loss', 'compile_metrics']` instead of `'accuracy'`. The script crashed with:
   ```text
   KeyError: 'accuracy'
   ```
5. **Consequence:** 
   - Lines 404–422 (calculating `classification_report`, `confusion_matrix`, per-class precision, recall, and F1-score) **never executed**.
   - The reported 97.22% is simply the scalar `compile_metrics: 0.9722` printed to stdout before the crash.

---

## 6. Critical Methodological Defects

### Defect 1: Validation / Test Set Snooping
In `notebooks/01_cnn_training.py`:
- `train_ds` was built from `TRAIN_DIR` (10,901 images).
- `test_ds` was built from `TEST_DIR` (2,698 images).
- In both Phase 1 (line 294) and Phase 2 (line 339):
  ```python
  history = model.fit(train_ds, validation_data=test_ds, callbacks=callbacks, ...)
  ```
- `ModelCheckpoint` monitored `val_accuracy` (which was computed on `test_ds`).
- The best checkpoint restored was chosen because it performed best on `test_ds`.
- Then, on line 390, the model was evaluated on `test_ds` again to claim a "test accuracy" of 97.22%.
- **Finding:** The test partition was used directly as the validation set for model selection and early stopping. There was **no un-snooped, held-out test set**.

### Defect 2: Near-Duplicate / Video Frame Leakage
The Kaggle `fruits-fresh-and-rotten-for-classification` dataset is known in the computer vision literature to contain consecutive video frames of rotating fruits on turn-tables. Because images were split randomly rather than by fruit identity or capture session, identical fruit instances appear in both `train/` and `test/` with mere degree-scale rotations. This identity leakage artificially inflates benchmark accuracy.

### Defect 3: Deletion of Checkpoints
In commit `568fd604b6`, `models/cnn_freshness.keras` was deleted. As a result, the repository in its current state cannot perform visual inference and must rely on the heuristic fallback:
```python
# predict.py line 159-161
seed = int(hashlib.md5(str(image_path).encode()).hexdigest(), 16) % (2**31)
rng = np.random.default_rng(seed)
return float(rng.uniform(0.45, 0.90))
```

---

## 7. Audit Recommendations for Revision

1. **Fix Keras 3 Evaluation Crash:** Replace line 396 with robust metric dictionary extraction:
   ```python
   metric_dict = dict(zip(best_model.metrics_names, test_results))
   val_acc = metric_dict.get("accuracy", metric_dict.get("compile_metrics", 0.0))
   ```
2. **Implement Group-Aware Split:** Enforce perceptual hashing (pHash) and deduplication so no near-duplicate fruit instances cross the train/validation/test boundary.
3. **Partition into True Train / Val / Test (70 / 15 / 15):** Never tune hyperparameters or early-stop on the final test set.
4. **Report Multi-Backbone Benchmark with 95% CIs:** Retrain and compare MobileNetV2, EfficientNetB0, and ResNet50 using 1,000 bootstrap iterations.
5. **Rectify Produce Scope in Manuscript:** Explicitly disclose that visual freshness models currently cover Apple, Banana, and Orange, with Tomato and Mango designated as future work or integrated via secondary public datasets.

