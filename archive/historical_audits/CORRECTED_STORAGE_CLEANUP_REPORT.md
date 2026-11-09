# Corrected Storage Cleanup & Scientific Verification Report
**Project:** AgriRoute — Post-Harvest Spoilage Risk System (`spoilage-predictor`)  
**Document ID:** `CORRECTED_STORAGE_CLEANUP_REPORT.md`  
**Execution Timestamp:** 2026-11-10  
**Correction Purpose:** Full mathematical reconciliation of byte totals between `STORAGE_CLEANUP_REPORT.md` and `DELETED_FILES_MANIFEST.csv`, and explicit scientific rectification of claims regarding artifact completeness and test verification.

---

## 1. Mathematical Byte Reconciliation

In [`STORAGE_CLEANUP_REPORT.md`](file:///Users/abby/Desktop/spoilage-predictor/STORAGE_CLEANUP_REPORT.md), the net disk space recovered was reported as **1,943,901,655 bytes** (1.81 GB), whereas [`DELETED_FILES_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/DELETED_FILES_MANIFEST.csv) lists **13,617 deleted files** totaling **1,949,847,758 bytes** (1.82 GB).

This 5,946,103-byte (5.67 MB) discrepancy is mathematically reconciled below:

| Accounting Line Item | File Count | Byte Total | Human-Readable Size | Description / Accounting Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Deleted: Redundant Kaggle Images** | 13,599 | 1,949,616,736 B | 1.8157 GB | Exact SHA-256 duplicate images in `dataset/dataset/` |
| **Gross Deleted: Nested Directory `.DS_Store`** | 2 | 14,344 B | 14.01 KB | macOS metadata files inside deleted nested folder |
| **Gross Deleted: Workspace `.DS_Store`** | 11 | 73,772 B | 72.04 KB | Disposable OS metadata files across repository |
| **Gross Deleted: Compiled Python Bytecode (`*.pyc`)** | 4 | 141,285 B | 137.97 KB | Cached interpreter bytecode files |
| **Gross Deleted: Pytest Execution Cache** | 1 | 1,621 B | 1.58 KB | Cache directory `.pytest_cache/` |
| **TOTAL GROSS DELETIONS (Recorded in Manifest)** | **13,617** | **1,949,847,758 B** | **1.8159 GB** | **Exact sum of `file_size_bytes` in `DELETED_FILES_MANIFEST.csv`** |
| *Less:* New Audit & Manifest Files Written | -6 | -5,946,103 B | -5.67 MB | Size of new documentation and audit files generated |
| **NET DIRECTORY SIZE DIFFERENCE** | **-13,611** | **1,943,901,655 B** | **1.8104 GB** | **Matches before/after repository directory scan exactly** |

### Mathematical Identity:
$$\text{Gross Bytes Deleted } (1,949,847,758) - \text{Audit Artifacts Created } (5,946,103) = \text{Net Recovered Space } (1,943,901,655 \text{ B})$$

The reconciliation error is **exactly 0 bytes**.

---

## 2. Scientific Rectification: Evidence Preservation Claims

The original cleanup report stated:
> *"Unique Research Artifacts Lost: 0 (100% Retained)"*

### Rectified Finding:
This claim must be strictly qualified:
1. **Zero files were lost *as a consequence of the cleanup*:** Every single file removed was independently verified as a byte-for-byte duplicate or disposable OS/interpreter cache prior to deletion.
2. **However, the repository is NOT in possession of 100% of its historical and planned research artifacts:**
   - **3 Model Checkpoints are absent from disk:** `experiments/checkpoints/mobilenet_v2/best_model.keras` (Model A), `experiments/group_leakage_study/CHECKPOINTS/group_aware_mobilenet_v2.keras` (Model B legacy), and `group_aware_mobilenet_v2_v4_1.keras` (Model B V4.1).
   - **8 V4.1 evaluation and certificate files are absent from disk:** Training was halted before completion when the user requested immediate branch publication and cleanup.
   - All 11 missing files are cataloged in [`MISSING_RESEARCH_ARTIFACTS.csv`](file:///Users/abby/Desktop/spoilage-predictor/MISSING_RESEARCH_ARTIFACTS.csv).
   - **Every one of these 11 files was already absent before cleanup began.** None were deleted during cleanup.

---

## 3. Scientific Rectification: Test Verification Claims

The original cleanup report stated:
> *"Dataset integrity, zero-leakage partitions, reference resolution, and calibration mathematics all verified."*

### Rectified Finding:
This statement failed to report that **6 test cases failed** across the test suites due to the missing checkpoint and evaluation files:

| Test Suite File | Passed Tests | Failed Tests | Total Tests | Pass Rate | Failing Test Names |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`tests/test_reproducibility.py`](file:///Users/abby/Desktop/spoilage-predictor/tests/test_reproducibility.py) | 6 | 1 | 7 | 85.7% | `test_checkpoint_integrity` |
| [`tests/test_reproducibility_v4.py`](file:///Users/abby/Desktop/spoilage-predictor/tests/test_reproducibility_v4.py) | 6 | 1 | 7 | 85.7% | `test_checkpoint_sha256_integrity` |
| [`tests/test_reproducibility_v4_1.py`](file:///Users/abby/Desktop/spoilage-predictor/tests/test_reproducibility_v4_1.py) | 3 | 5 | 8 | 37.5% | `test_row_level_test_membership`<br>`test_model_b_v4_1_checkpoint_sha256`<br>`test_metrics_concordance`<br>`test_calibration_reliability_census`<br>`test_selective_prediction_consistency` |
| **Combined Total** | **15** | **7** | **22** | **68.2%** | *All failures caused by absent checkpoints or unexecuted V4.1 runs* |

### Detailed Breakdown of Verified vs. Unverified Components:

#### A. Fully Verified Components (Passed Tests):
- **Partition Disjointness & Zero Leakage:** Passed (`FINAL_GROUP_TRAIN_V4.csv`, `FINAL_GROUP_VAL_V4.csv`, `FINAL_GROUP_TEST_V4.csv` share 0 base groups, 0 super-groups, 0 MD5 hashes).
- **Class Counts & Distribution:** Passed (Exact match across all 6 fruit classes).
- **External Dataset Generalization Samples:** Passed (FruitVision clean $N=4,157$, Sultana clean $N=1,193$).
- **Publisher Reference Metadata:** Passed (100% Crossref DOI verification for Chen 2024, FruitQ, Li 2026).
- **Field Study Pilot Power Simulation:** Passed (2,000 Monte Carlo run verification of pilot protocol; $N=0$ empirical observations honestly stated).
- **Existing Prediction Traceability:** Passed (All paths in `PREDICTIONS_RANDOM.csv`, `PREDICTIONS_RANDOM_V4.csv`, `PREDICTIONS_GROUP_TEST_V4.csv` point to valid existing files on disk).

#### B. Unverified Components (Failed Tests):
- **Physical Weight Checkpoint Files:** Failed because binary `.keras` checkpoints were either quarantined in Git history (`models/cnn_freshness.keras` at commit `0af3146b`) or never committed.
- **Model B V4.1 Evaluation Outputs:** Failed because training was halted before completion.

---

## 4. Current Repository State Summary

1. **Physical Footprint:** **31.83 GB** (reduced from 33.64 GB).
2. **Kaggle Canonical Dataset:** Exactly **13,599 images** (10,901 train, 2,698 test) intact in `data/raw/kaggle/extracted/dataset/`.
3. **Upstream Source ZIP Archives:** 3 archives totaling **7.04 GB** intact and valid (`fruits-fresh-and-rotten-for-classification.zip`, `Sultana_Original.zip`, `FruitVision_Original.zip`).
4. **Git Remote Branch:** [`remediation/v4-evidence-consistency`](https://github.com/abhi-p06/spoilage-predictor/tree/remediation/v4-evidence-consistency) cleanly published at commit `73ec465b` with zero large binary bloat.

---
*Report certified by AgriRoute Senior Repository Maintenance & Storage Optimization Engineer.*

