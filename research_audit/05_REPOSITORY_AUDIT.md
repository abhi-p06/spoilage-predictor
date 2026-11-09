# Forensic Audit 05: Repository Architecture, Dependencies & Reproducibility

> **Audit Date:** 2026-11-09  
> **Auditor:** Independent Scientific Auditor  
> **Target Repository:** `https://github.com/abhi-p06/spoilage-predictor`  
> **Audited Git Commit:** `455b129`  
> **Scope:** Code completeness, dependency viability, execution friction, and out-of-the-box reproducibility.

---

## 1. Executive Summary & Verdict

| Dimension | Finding | Status |
|---|---|---|
| **Out-of-the-Box Execution** | Web application starts cleanly via `python app/app.py` | `VERIFIED` |
| **Model Weights Availability** | Checkpoints deleted in commit `568fd604b6`; app operates 100% on fallbacks | `CRITICAL DEFECT` |
| **CNN Training Script** | Crashes on line 396 (`KeyError: 'accuracy'`) under modern Keras 3 | `BROKEN SCRIPT` |
| **Script Format Discrepancy** | `train_all.py` outputs `.h5` files, but `predict.py` expects `.keras` files | `INCONSISTENT` |
| **Raw Dataset Availability** | Image dataset is gitignored and not committed; requires Kaggle API download | `EXTERNAL DEPENDENCY` |
| **Reproducibility of Results** | **Cannot reproduce manuscript results from clean checkout** | `NON-REPRODUCIBLE` |

---

## 2. File-by-File Inventory & Integrity Status

| Path | Size (Bytes) | Role | Integrity Status | Key Defects & Observations |
|---|---|---|---|---|
| `README.md` | 9,472 | Documentation | `OVERCLAIMED` | Claims AUC=1.000 and 97.22% without disclosing synthetic leakage or deleted weights. |
| `requirements.txt` | 922 | Dependencies | `PARTIALLY PINNED` | Pins major versions (`tensorflow>=2.15.0`, `xgboost>=2.0.0`), but unpinned sub-dependencies cause Keras 3 metric key breaks. |
| `.env.example` | 1,497 | Config Template | `VALID` | Well-documented template for Twilio and Kaggle credentials. |
| `download_dataset.py` | 3,386 | Kaggle Downloader | `FUNCTIONAL` | Works if Kaggle token provided; falsely claims Tomato/Mango exist in dataset. |
| `generate_sensor_data.py` | 6,274 | Synthetic Data Gen | `FUNCTIONAL` | Works deterministically with seed 42; generates trivial disjoint distributions. |
| `train_all.py` | 19,633 | Pipeline Runner | `INCONSISTENT` | Saves `.h5` format, breaking `predict.py` which searches for `.keras`. |
| `notebooks/01_cnn_training.py` | 13,842 | CNN Training | `CRASHES` | Crashes at line 396 on test evaluation (`KeyError: 'accuracy'`). |
| `notebooks/02_lstm_training.py` | 9,842 | LSTM Training | `FUNCTIONAL` | Trains BiLSTM; hits val_auc=1.000 at Epoch 1 due to disjoint data. |
| `notebooks/03_fusion_training.py` | 12,410 | XGBoost Training | `FUNCTIONAL` | Trains XGBoost on 10,000 synthetic rows with circular Beta leakage. |
| `app/app.py` | 11,849 | Flask Web Server | `FUNCTIONAL` | Runs on port 5000; correctly serves templates and static assets. |
| `app/predict.py` | 13,874 | Inference Engine | `DEFECTIVE (FALLBACK)` | Operates 100% via heuristic fallback because model directory is empty. |
| `app/mandi_prices.py` | 8,837 | Price Client | `FUNCTIONAL` | Works when key present; falls back cleanly to MD5 generator. |
| `app/sms_alerts.py` | 4,772 | SMS Client | `FUNCTIONAL` | Threaded asynchronous Twilio dispatch; fails gracefully if credentials absent. |
| `app/templates/index.html` | 28,142 | UI Frontend | `FUNCTIONAL` | Responsive UI with Leaflet map and OSRM route fetcher. |
| `app/templates/result.html` | 17,998 | Result Dashboard | `FUNCTIONAL` | Renders risk gauges, route details, and mandi price cards. |
| `data/sensors/sample_input.csv` | 668 | Fixture Data | `VALID` | 24-hour sequence fixture for app testing. |
| `models/` | 0 | Model Storage | `EMPTY` | Directory deleted in git commit `568fd604b6`. |

---

## 3. Dependency & Environment Analysis

### 3.1 Pinned Environment Test
The environment `/opt/miniconda3/envs/spoilage` contains:
- `Python`: 3.11.15
- `TensorFlow`: 2.16.2
- `Keras`: 3.14.1
- `XGBoost`: 3.2.0
- `scikit-learn`: 1.7.2
- `Flask`: 3.1.2

### 3.2 Keras 3 Incompatibility
In TensorFlow 2.16+ / Keras 3+, `model.evaluate()` returns compiled metric keys prefixed or aggregated as `compile_metrics`. In `notebooks/01_cnn_training.py` line 396:
```python
val_acc = dict(zip(metrics_names, test_results))["accuracy"]
```
Because `'accuracy'` is not in `metrics_names` (which contains `['loss', 'compile_metrics']`), execution halts with an unhandled exception. Any automated CI runner attempting to reproduce the notebook will fail.

### 3.3 File Extension Mismatch
- `train_all.py` (lines 28–30):
  ```python
  CNN_PATH  = MODEL_DIR / "cnn_freshness.h5"
  LSTM_PATH = MODEL_DIR / "lstm_spoilage.h5"
  ```
- `app/predict.py` (lines 32–33):
  ```python
  CNN_PATH  = MODEL_DIR / "cnn_freshness.keras"
  LSTM_PATH = MODEL_DIR / "lstm_spoilage.keras"
  ```
- **Consequence:** If a user runs `python train_all.py` to train all models from scratch, the web app will **still fail to find the models**, because it checks for `.keras` while `train_all.py` produced `.h5`.

---

## 4. Git Forensic Trace: The Deleted Checkpoints

In git commit `568fd604b6` (Sat Aug 15 18:44:11 2026), the author committed:
```text
Author: abhi-p06
Commit: 568fd604b6b6cbd12b4d77e7915afad3b0d437e3
Subject: update app, templates, requirements; add mandi prices, sms alerts, reports
```
In this commit, the author removed:
- `models/cnn_freshness.keras` (25.8 MB)
- `models/lstm_spoilage.keras` (3.8 MB)
- `models/lstm_scaler.pkl` (742 bytes)
- `data/sensors/sensor_logs.csv` (4,001 lines)
- `logs/cnn_training.log` (156 lines)

**Why were they deleted?** Likely to prevent GitHub repository bloat or avoid pushing large binary files over git without Git LFS. However, this left the repository in a state where cloning and running `python app/app.py` runs purely on random fallbacks.

---

## 5. Audit Recommendations for Revision

1. **Unify Model Extensions:** Standardize all scripts on `.keras` (the modern Keras v3 native format).
2. **Patch Metric Key Extraction:** Update line 396 across all training scripts to safely handle both Keras 2 and Keras 3 metric dictionary conventions.
3. **Commit Lightweight / Compressed Artifacts or LFS:**
   - Commit `lstm_scaler.pkl` and `fusion_xgb.pkl` (both $< 1$ MB).
   - Host `cnn_freshness.keras` on Hugging Face Model Hub or GitHub Releases with an automated download script in `app/predict.py`.
4. **Automated Reproducibility Script:** Create a clean `reproduce_all.py` script that verifies environment dependencies, downloads required datasets, trains models with fixed random seeds, and generates all publication tables deterministically.

