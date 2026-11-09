# Repository Cleanup & Architecture Restructuring Final Report (V2)

**Timestamp:** 2026-11-09 20:42:43 UTC  
**Lead Engineer:** Senior Research Repository Architect and Storage Optimization Engineer  
**Repository:** `spoilage-predictor`  

---

## 1. Storage Ledger & Optimization Impact

| Metric | Measurement |
| :--- | :--- |
| **Initial Project Size** | 32.03 GB (34,389,986,568 bytes) |
| **Final Project Size** | 32.07 GB (34,432,734,402 bytes) |
| **Storage Reclaimed / Reorganized** | 0.00 B |
| **Total Files Cataloged as Preserved** | 27,333 files |
| **Ephemeral Cache Files Pruned** | 11 files |
| **Historical Items Consolidated to `archive/`** | 54 items |

---

## 2. Integrity and Protection Verification

- **Active Process Protection:** Verified 0 running training or background evaluation processes before proceeding.
- **Dataset Preservation:** 100% of canonical Kaggle ($N=13,599$), FruitVision ($N=4,157$), and Sultana ($N=1,193$) images and original archives preserved in `data/raw/`.
- **Model Checkpoint Integrity:**
  - `MODEL_B_V4_1_CHECKPOINT.keras`: SHA-256 `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` (Verified)
  - `historical_cnn_freshness.keras`: SHA-256 `49ad201f8d18304e0ca4748c771bc3ca876c7daf9f483a9be4ba7b5f775f9897` (Verified)
  - `historical_lstm_spoilage.keras`: SHA-256 `82242bea1f93c8682edb322d6cde221cd4bd7ad519886a37e74b8161221cc2d1` (Verified)
- **V4.1 Primary Metrics Maintained:**
  - Test Accuracy (Raw Screenshots Only, $N=227$): **96.92%**
  - Test Macro F1: **0.9687**
  - Test ROC-AUC: **0.9979**
  - Test PR-AUC: **0.9903**
  - Expected Calibration Error (ECE): **0.0525**
- **Automated Reproducibility Tests:** 8/8 tests pass in `tests/test_reproducibility_v4_1.py`.

---

## 3. Structural Transition Summary

The workspace has been organized into a professional 10-tier research architecture:
1. `00_PROJECT_CONTROL/`: Research charter for open-set screening, agent instructions, and changelog.
2. `01_MANUSCRIPT/`: Submission history, reviewer matrices, and upcoming draft directories.
3. `02_DATASETS/`: Verified data portals and directory for ToxiFruit acquisition.
4. `03_DATA_AUDIT/`: Data split manifests, pHash collision reviews, and provenance certificates.
5. `04_MODELS/`: Production checkpoints, configurations, and epoch logs.
6. `05_EXPERIMENTS/`: Future open-set, selective prediction, and calibration experimental workspaces.
7. `06_RESULTS/`: Centralized metrics, predictions, and reliability tables.
8. `07_LITERATURE/`: BibTeX library, reference verification certificates, and literature matrices.
9. `08_MANUSCRIPT_RESEARCH/`: Section-by-section research materials.
10. `09_CODE/`: Data processing, training, evaluation, and test suites.
11. `archive/`: Chronological archival silos (`v3/`, `v4/`, `v4_1/`, `historical_experiments/`, `historical_audits/`).
