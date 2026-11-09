# Post-Cleanup Manual Review & Transition Guide

**Timestamp:** 2026-11-09 20:42:43 UTC  
**Auditor:** Senior Research Repository Architect  
**Project:** AgriRoute (`spoilage-predictor`)  

---

## 1. Safety & Non-Destructive Invariance

1. **No Unique Research Evidence Was Destroyed:**
   - All historical model checkpoints (`MODEL_B_V4_1_CHECKPOINT.keras`, `historical_cnn_freshness.keras`, `historical_lstm_spoilage.keras`) are cryptographically verified and preserved.
   - All 13,599 Kaggle images, 4,157 FruitVision images, and 1,193 Sultana images remain intact in `data/raw/`.
   - All historical V3 and V4 reports were consolidated into version-specific subdirectories under `archive/` rather than deleted.
2. **Zero Import or Path Breaking:**
   - Active V4.1 prediction CSVs, manifests, and checkpoints remain present at the root and in `00_PROJECT_CONTROL/` through `09_CODE/`.
   - `pytest tests/test_reproducibility_v4_1.py -v` passes 8/8 tests post-cleanup.
3. **Application Source Preserved:**
   - The Flask web application in `app/` (`app.py`, `mandi_prices.py`, `predict.py`, `sms_alerts.py`) remains intact.

---

## 2. Items Consolidated to `archive/`

| Original Location | Archived Destination | Rationale |
| :--- | :--- | :--- |
| `AGRIRoute_REMEDIATION_V3.zip` | `archive/v3/` | Superseded V3 verification package |
| `*_V3.md`, `*_V3.csv` | `archive/v3/` | Historical V3 forensic reports |
| `*_V4.md` (superseded reports) | `archive/v4/` | Historical V4 remediation reports |
| `PREDICTIONS_*.csv` (pre-V4) | `archive/historical_experiments/` | Pre-remediation unversioned outputs |
| `PHASH_COLLISION_CONTACT_SHEET/` | `archive/historical_audits/` | Visual collision audit sheets |
| `AGRIRoute_FINAL_EXPERIMENT_V4_1/` | `archive/v4_1/` | Uncompressed mirror of zipped V4.1 package |

---

## 3. Transition to Open-Set Quality Screening

The workspace is now organized into the modular 10-tier structure:
- `00_PROJECT_CONTROL/`: Research objectives, status, changelog, and ethical agents.
- `01_MANUSCRIPT/`: Submissions, reviews, and drafts.
- `02_DATASETS/`: Canonical datasets and upcoming ToxiFruit acquisition directory.
- `03_DATA_AUDIT/`: Data provenance, duplicates, and split manifests.
- `04_MODELS/`: Model checkpoints, configs, and training logs.
- `05_EXPERIMENTS/`: Open-set detection, calibration, selective prediction, and ablations.
- `06_RESULTS/`: Comprehensive metrics, predictions, and figures.
- `07_LITERATURE/`: Reference libraries and literature matrices.
- `08_MANUSCRIPT_RESEARCH/`: Methodology, contributions, and responses.
- `09_CODE/`: Reproducible processing, training, and evaluation pipelines.
- `archive/`: Historical records organized chronologically (v3, v4, v4_1, etc.).
