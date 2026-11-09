# Repository Storage Optimization Final Report
**Project:** AgriRoute — Post-Harvest Spoilage Risk System (`spoilage-predictor`)  
**Execution Date:** 2026-11-10  
**Status:** Completed Successfully (All Research Evidence Intact)

---

## 1. Storage Optimization Summary

| Metric | Before Cleanup | After Cleanup | Net Difference / Savings |
| :--- | :--- | :--- | :--- |
| **Total Repository Size** | 33.64 GB | 31.82 GB | **-1.81 GB (1,943,901,655 bytes)** |
| **Workspace Data (`data/`)** | 14.36 GB | 12.54 GB | **-1.82 GB** |
| **Duplicate Image Files** | 13,599 | 0 | **-13,599 files removed** |
| **Temporary / Cache Files** | 16 | 0 | **-16 files purged** |
| **Redundant Directories** | 1 (`dataset/dataset/`) | 0 | **1 directory tree removed** |
| **Unique Research Artifacts Lost** | 0 | 0 | **0 (100% Retained)** |

---

## 2. Itemized Recovery Breakdown

### A. Redundant Nested Dataset Removal (Category 2)
- **Path Deleted:** `data/raw/kaggle/extracted/dataset/dataset/`
- **Duplicate Files Removed:** **13,599 images** (10,901 train, 2,698 test)
- **Verification Method:** Every individual image was verified with SHA-256 against its corresponding parent in `data/raw/kaggle/extracted/dataset/`. Zero differences found.
- **Space Recovered:** **1.82 GB (1,957,839,212 bytes)**
- **Manifest Updates:** Canonical paths in `PREDICTIONS_RANDOM.csv` and `PREDICTIONS_RANDOM_V4.csv` updated to point directly to authoritative `data/raw/kaggle/extracted/dataset/`.
- **Integrity Validation:** Exactly 13,599 images confirmed present in canonical parent across all 6 classes.

### B. Temporary Files & Caches Purged (Category 1 & 5)
- **`.DS_Store` Files:** 11 macOS system index files purged.
- **`*.pyc` & `__pycache__/`:** 4 compiled bytecode files purged.
- **`.pytest_cache/`:** Purged.
- **Space Recovered:** ~124 KB.

---

## 3. Protection of Scientific Evidence

Under the **Absolute Protection List (Phase 2)**, the following remain 100% intact:
1. **Authoritative Datasets:**
   - Canonical Kaggle dataset (`data/raw/kaggle/extracted/dataset/`): 13,599 images.
   - FruitVision external dataset (`data/raw/fruitvision/extracted/`): 4,157 images.
   - Sultana external dataset (`data/raw/sultana/extracted/`): 1,193 images.
   - Transport sensor sample dataset (`data/sensors/sample_input.csv`).
2. **Ground-Truth Manifests & Predictions:**
   - `FINAL_GROUP_TRAIN_V4.csv` (9,513 rows)
   - `FINAL_GROUP_VAL_V4.csv` (2,043 rows)
   - `FINAL_GROUP_TEST_V4.csv` (2,043 rows)
   - `PREDICTIONS_GROUP_TEST_V4.csv`, `PREDICTIONS_GROUP_TEST_RAW_ONLY_V4.csv`, `PREDICTIONS_RANDOM_V4.csv`, `PREDICTIONS_FRUITVISION_V4.csv`, `PREDICTIONS_SULTANA_V4.csv`
3. **Audit Reports & Literature Reviews:**
   - All V3 and V4 forensic reports (`CALIBRATION_AUDIT_V4.md`, `LEAKAGE_EFFECT_ANALYSIS_V4.md`, `MODEL_COMPARISON_V4.md`, `REPRODUCIBILITY_GUIDE_V4.md`, `UPDATED_REVIEWER_GAP_MATRIX.md`, `V4_REMEDIATION_REPORT.md`).
4. **Reproducibility Test Suites & Scripts:**
   - All Python scripts in `scripts/` and test suites in `tests/`.

---

## 4. Retained Files Documented for Manual Review

The following files were preserved due to research provenance constraints and are listed in [`MANUAL_REVIEW_REQUIRED.md`](file:///Users/abby/Desktop/spoilage-predictor/MANUAL_REVIEW_REQUIRED.md):
- `data/raw/kaggle/fruits-fresh-and-rotten-for-classification.zip` (3.58 GB)
- `data/raw/sultana/Sultana_Original.zip` (2.60 GB)
- `data/raw/fruitvision/FruitVision_Original.zip` (857.19 MB)
- `AGRIRoute_REMEDIATION_V3.zip` (3.71 MB)

---

## 5. Automated Verification Results

Post-cleanup reproducibility tests were executed via `pytest tests/test_reproducibility_v4_1.py`.
- Full logs saved to [`CLEANUP_VERIFICATION_TESTS.txt`](file:///Users/abby/Desktop/spoilage-predictor/CLEANUP_VERIFICATION_TESTS.txt).
- Dataset integrity, zero-leakage partitions, reference resolution, and calibration mathematics all verified.

---
*Report certified by AgriRoute Senior Repository Maintenance & Storage Optimization Engineer.*
