# AgriRoute V4.1 Reproducible Experiment Evidence Package

**Repository:** `spoilage-predictor`  
**Paper ID:** 1345 (*ICMLDE 5.0*, Target: *Procedia Computer Science*)  
**Package Version:** V4.1 (Post-pHash Merged Split Retraining & Unified Evaluation)  
**Date:** 2026-11-10  

---

## 1. Executive Summary

This package contains the complete, unvarnished, empirically verified reproducibility artifacts for **Model B (V4.1)**. 

### Key Audit Findings & Methodology Repairs
1. **Primary Experiment Mandate:** Model B has been trained strictly on the 1,057 original fruit specimen screenshots identified by `is_raw == 1` from `FINAL_GROUP_TRAIN_V4_1.csv`, with online data augmentation applied during training only.
2. **Zero Leakage & Partition Disjointness:** Validation ($N=227$ raw images) and Testing ($N=227$ raw images) remain completely unaugmented. 0 supergroup leakage, 0 binary MD5 duplicates across partitions, and 100% co-location of confirmed pHash near-duplicates.
3. **Dual Reporting Hierarchy:** Primary metrics are reported on the unaugmented raw screenshots ($N=227$, **96.92% Accuracy**, **0.9687 Macro F1**), with secondary concordant robustness evaluation on all 2,043 transformed variants (**95.30% Accuracy**, **0.9519 Macro F1**).
4. **Historical Artifact Preservation:** Pre-revision historical CNN and LSTM weights have been recovered directly from Git object blobs without overwriting active models.

---

## 2. Directory Layout

```
AGRIRoute_FINAL_EXPERIMENT_V4_1/
├── README.md                                 # This reproduction guide
├── PACKAGE_FILES_MANIFEST_SHA256.csv         # Cryptographic SHA-256 catalog of all files
├── TEST_REPORT.txt                           # Full pytest run and audit ledger
├── CHECKPOINTS/
│   ├── MODEL_B_V4_1_CHECKPOINT.keras         # Freshly retrained Model B (9,715,984 bytes)
│   ├── group_aware_mobilenet_v2_v4_1.keras   # Checkpoint mirror
│   ├── historical_cnn_freshness.keras        # Recovered historical CNN (25,802,251 bytes)
│   ├── historical_lstm_spoilage.keras       # Recovered historical LSTM (3,795,422 bytes)
│   ├── MODEL_B_V4_1_CHECKPOINT_SHA256.txt     # Cryptographic certificate
│   └── model_b_v4_1_config.json              # Architecture & training hyperparameters
├── MANIFESTS/
│   ├── FINAL_GROUP_TRAIN_V4_1.csv            # Training partition (N = 9,513; 1,057 raw)
│   ├── FINAL_GROUP_VAL_V4_1.csv              # Validation partition (N = 2,043; 227 raw)
│   ├── FINAL_GROUP_TEST_V4_1.csv             # Test partition (N = 2,043; 227 raw)
│   ├── GROUP_SPLIT_MANIFEST_MERGED_V4.csv    # Master supergroup mapping (N = 13,599)
│   ├── fruitvision_clean.csv                 # Clean external FruitVision benchmark (N = 4,157)
│   └── sultana_clean.csv                     # Clean external Sultana benchmark (N = 1,193)
├── PREDICTIONS_AND_METRICS/
│   ├── MODEL_B_V4_1_PREDICTIONS.csv          # Authoritative 37-column test predictions (N = 2,043)
│   ├── MODEL_B_V4_1_METRICS.json             # Primary (N=227) and secondary (N=2,043) metrics
│   ├── MODEL_B_V4_1_CALIBRATION.json         # Temperature scaling & ECE/Brier metrics
│   ├── MODEL_B_V4_1_RELIABILITY_TABLE.csv    # 10 uniform calibration bins
│   ├── MODEL_B_V4_1_SELECTIVE_RESULTS.json   # Selective prediction at tau = 0.90
│   ├── MODEL_B_V4_1_EXTERNAL_RESULTS.json    # Zero-shot FruitVision and Sultana benchmarks
│   ├── AUTHORITATIVE_EXPERIMENT_REGISTRY_V4_1.csv # Master experiment register
│   ├── TEST_REPORT.txt                       # Test suite verification log
│   ├── UPDATED_REFERENCE_VERIFICATION.csv    # Official verified bibliographic metadata
│   └── FIELD_STUDY_SIMULATION_POWER.json     # Power analysis and field study pilot truth
├── SOURCE_CODE/
│   ├── train_model_b_v4_1_raw_primary.py     # Primary raw-only training pipeline
│   ├── train_model_b_v4_1.py                 # Full partition training script
│   ├── evaluate_model_b_v4_1.py              # Unified evaluation and benchmarking pipeline
│   ├── rebuild_data_splits_v4_1.py           # Split regeneration and leakage audit script
│   ├── build_authoritative_registry_v4_1.py  # Register assembly script
│   └── assemble_final_package_v4_1.py        # Packaging script
└── tests/
    └── test_reproducibility_v4_1.py          # Automated verification test suite (8/8 tests)
```

---

## 3. Verified Performance Summary

| Condition | Dataset | Samples ($N$) | Accuracy | Macro F1 | ROC-AUC (OvR) | PR-AUC (Macro) | ECE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary (Raw Only)** | Kaggle Sealed Test | 227 | **96.92%** | **0.9687** | **0.9979** | **0.9903** | 0.0525 |
| **Secondary (All Variants)**| Kaggle Sealed Test | 2,043 | **95.30%** | **0.9519** | **0.9965** | **0.9841** | 0.0520 |
| **Selective ($	au=0.90$)** | Kaggle Sealed Test | 1,459 accepted | **99.38%** | — | — | — | (Coverage: 71.41%) |
| **External Generalization** | Mendeley FruitVision| 4,157 | **69.14%** | **0.6675** | **0.9522** | **0.7844** | 0.0638 |
| **External Generalization** | Sultana et al. (2022)| 1,193 | **65.63%** | **0.6577** | **0.9032** | **0.7188** | 0.0612 |

---

## 4. How to Verify

From the package directory or workspace root, execute the automated pytest suite:

```bash
pytest tests/test_reproducibility_v4_1.py -v
```

All 8/8 tests will verify partition disjointness, row-level membership, SHA-256 checksums, mathematical concordance, calibration census, selective prediction coverage, publisher references, and pilot power constraints.
