# AgriRoute Scientific Reproducibility Guide (V4 Evidence Package)

**Target Publication:** Procedia Computer Science  
**Conference:** ICMLDE 5.0 (Paper ID: 1345)  
**Package Version:** V4 (Authoritative Reproducibility & Audit Bundle)  
**Date:** November 2026  
**Git Branch:** `remediation/v4-evidence-consistency`  

---

## 1. Executive Summary & V4 Integrity Standards

This guide provides instructions for independently verifying and reproducing all empirical results reported in the AgriRoute remediation evidence package (V4).

Under strict scientific integrity guidelines:
1. **Zero Fabrication:** Every metric reported in `AUTHORITATIVE_EXPERIMENT_REGISTRY_V4.csv` is derived directly from raw model inferences stored in authoritative prediction CSVs.
2. **Deterministic Checkpoint Integrity:** Model checkpoints are verified using SHA-256 hashes against original model weights.
3. **Quarantine of Unsupported Baselines:** No synthetic or simulated baselines (e.g., synthetic BiLSTM sensor traces or uncheckpointed EfficientNet/ResNet models) are presented as verified experimental evidence. Only verified, checkpointed vision runs are admitted into the active registry.
4. **Transparent Sample Accounting:** Excluded external samples are documented with byte-level MD5 deduplication manifests.

---

## 2. Hardware and Software Environment

The evaluation pipeline was executed on Apple Silicon (M4, 16 GB Unified Memory) running macOS Darwin.

### Python Environment Manifest
- **Python:** 3.11.15
- **TensorFlow:** 2.16.2 (with `tensorflow-metal` pluggable device acceleration)
- **Scikit-learn:** 1.9.0
- **Pandas:** 2.2.3
- **NumPy:** 1.26.4
- **ImageHash:** 4.3.1
- **Pillow:** 10.4.0
- **PyTest:** 8.3.4
- **SciPy:** 1.14.1

### Installation via Conda / UV
```bash
# Create dedicated reproduction environment
conda create -n agriroute_v4 python=3.11 -y
conda activate agriroute_v4

# Install core machine learning and scientific libraries
pip install tensorflow==2.16.2 tensorflow-metal scikit-learn pandas numpy pillow imagehash scipy pytest openpyxl
```

---

## 3. Verified Model Checkpoints

Two authoritative TensorFlow/Keras model checkpoints are included in the package under `CHECKPOINTS/`:

| Model Identifier | Architecture | Checkpoint Filename | SHA-256 Hash | Model File Size |
| :--- | :--- | :--- | :--- | :--- |
| **Model A** | MobileNetV2 | `best_model.keras` | `6d7f61d368a74130ddb932df4c42b75fd9efcbeeab192f3912db0e94f753e2b9` | 9,715,772 bytes |
| **Model B** | MobileNetV2 | `group_aware_mobilenet_v2.keras` | `3bdda4572ba117bef65f707fdc520a12498667f0043d4d1822194cecee5d7689` | 9,723,964 bytes |

### Hash Verification Command
```bash
shasum -a 256 CHECKPOINTS/best_model.keras
shasum -a 256 CHECKPOINTS/group_aware_mobilenet_v2.keras
```

---

## 4. Master Inference & Calibration Pipeline Execution

To recompute all model predictions, pre-softmax dense logits, raw softmax confidences, validation-fitted temperature scaling, ECE calibration bins, and the experiment registry directly from source:

```bash
# Execute master inference pipeline (takes ~2 minutes on GPU/MPS)
python scripts/master_inference_and_calibration_v4.py
```

### Critical Preprocessing Specification
Both Model A and Model B were pre-trained and fine-tuned using MobileNetV2 native input preprocessing:
$$\mathbf{x}_{\text{norm}} = \frac{\mathbf{x}}{127.5} - 1.0 \in [-1, 1]$$
*Auditor Note on V3 Anomaly Resolution:* In V3, an auxiliary calibration script mistakenly evaluated models using `rescale=1./255` ($[0, 1]$), creating an input distribution mismatch that falsely inflated ECE. In V4, all inference steps consistently use `tf.keras.applications.mobilenet_v2.preprocess_input`, restoring true probability calibration performance:
- Model A: ECE = 0.01164 (uncalibrated) $\to$ 0.01745 (calibrated, $T^*=1.3157$)
- Model B: ECE = 0.05942 (uncalibrated) $\to$ 0.01157 (calibrated, $T^*=0.4905$)

---

## 5. Perceptual Hash Collision Review & Super-Group Partitioning

To reproduce the perceptual hash collision audit and super-group partition generation:

```bash
python scripts/investigate_and_merge_phash.py
```

### Outputs Produced:
1. `PHASH_REVIEW/PHASH_CANDIDATE_AUDIT.csv`: Complete forensic audit of all 8 candidate collision pairs ($H \le 10$).
2. `PHASH_REVIEW/pair_01_review.png` through `pair_08_review.png`: Visual multi-panel diagnostic contact sheets.
3. `GROUP_SPLIT_MANIFEST_MERGED_V4.csv`: Consolidated partition manifest containing 1,504 super-groups with 100% zero cross-partition leakage.

---

## 6. Prospective Field Study Statistical Power Analysis

To recompute the statistical power and cluster design effects for the prospective agricultural field evaluation protocol:

```bash
python scripts/calculate_field_study_power.py
```

### Key Statistical Parameters:
- Total Planned Fruit Lots: $K = 40$ shipment consignments (10 fruits per consignment = 400 tracked fruits; 200 sacrificial fruits for destructive firmness testing = 600 total fruits).
- Intra-Cluster Correlation ($\text{ICC}$): $0.12$ ($\text{VIF} = 1 + (10 - 1) \times 0.12 = 2.08$).
- Target Odds Ratio: $\text{OR} = 2.2$.
- Statistical Power: $58.23\%$ under binary thresholding; $>80\%$ requires $\text{OR} \ge 2.8$ or $K \ge 65$ shipments.
- Current Field Validation Data Status: $N = 0$ (prospective study protocol only; empirical observations have not been gathered).

---

## 7. Automated Test Suite Execution

A fully automated test suite (`tests/test_reproducibility_v4.py`) validates the entire evidence package across 7 core integrity dimensions:

```bash
pytest tests/test_reproducibility_v4.py -v | tee TEST_REPORT.txt
```

### Suite Verification Scope:
1. `test_manifest_integrity`: Validates 13,599 manifest entries, 32-character hexadecimal MD5 hashes, and 1,504 super-groups.
2. `test_checkpoint_sha256_integrity`: Verifies byte lengths ($>9$ MB) and exact SHA-256 signatures for Model A and Model B.
3. `test_dataset_exclusion_accounting`: Reconciles external duplicate image exclusions (28 in FruitVision, 7 in Sultana).
4. `test_super_group_partition_separation`: Asserts zero set intersection between train, validation, and test super-groups.
5. `test_prediction_schema_compliance`: Confirms 37 standard columns across all 7 prediction tables, validates class label alignment, and asserts probability sum invariants ($\sum p_i = 1.0 \pm 10^{-3}$).
6. `test_registry_metric_concordance`: Recomputes Accuracy, Macro F1, ROC-AUC, PR-AUC, ECE, and NLL from raw predictions and verifies concordance with `AUTHORITATIVE_EXPERIMENT_REGISTRY_V4.csv`.
7. `test_portable_paths_validity`: Verifies that file paths in prediction manifests are fully portable relative paths.

---

## 8. Directory Structure of V4 Reproduction Bundle

```
AGRIRoute_REMEDIATION_V4/
├── README_FOR_CHATGPT.md                         <- Executive orientation for external auditors
├── REPRODUCIBILITY_GUIDE_V4.md                   <- This complete step-by-step reproduction guide
├── V4_REMEDIATION_REPORT.md                      <- Forensic summary across all 10 remediation areas
├── AUTHORITATIVE_EXPERIMENT_REGISTRY_V4.csv       <- Authoritative master registry (11 benchmark rows)
├── GROUP_SPLIT_MANIFEST_MERGED_V4.csv            <- 13,599-row partition manifest (1,504 super-groups)
├── BASE_IMAGE_GROUP_AUDIT.csv                    <- 1,511 base image family audit
├── CALIBRATION_AUDIT_V4.md                       <- Temperature scaling and reliability bin analysis
├── PREDICTION_TRACEABILITY_V4.md                 <- 37-column prediction schema and data dictionary
├── LEAKAGE_EFFECT_ANALYSIS_V4.md                 <- Rigorous within-test performance analysis
├── FIELD_STUDY_PROTOCOL_V4.md                    <- 600-fruit observational cohort protocol
├── UPDATED_REVIEWER_GAP_MATRIX_V4.md             <- Authoritative 12-item reviewer response matrix
├── REFERENCE_VERIFICATION_V4.csv                 <- 25-item verified scholarly bibliography
├── REFERENCES.bib                                <- Verified BibTeX file
├── TEST_REPORT.txt                               <- Automated pytest execution log (100% passing)
├── CHECKPOINTS/                                  <- Verified Keras model weights
│   ├── best_model.keras                          (Model A: SHA-256 6d7f...)
│   └── group_aware_mobilenet_v2.keras             (Model B: SHA-256 3bdd...)
├── PREDICTIONS/                                  <- Authoritative 37-column prediction tables
│   ├── PREDICTIONS_RANDOM_V4.csv                 (Model A Historical Random Test, N=4,090)
│   ├── PREDICTIONS_GROUP_TEST_V4.csv             (Model B Group Test All Variants, N=2,043)
│   ├── PREDICTIONS_GROUP_TEST_RAW_ONLY_V4.csv    (Model B Group Test Raw Screenshots, N=227)
│   ├── PREDICTIONS_FRUITVISION_V4.csv            (Model B FruitVision External Test, N=4,157)
│   ├── PREDICTIONS_FRUITVISION_MODEL_A_V4.csv    (Model A FruitVision External Test, N=4,157)
│   ├── PREDICTIONS_SULTANA_V4.csv                (Model B Sultana External Test, N=1,193)
│   └── PREDICTIONS_SULTANA_MODEL_A_V4.csv        (Model A Sultana External Test, N=1,193)
├── DATASET_EXCLUSION_MANIFESTS/                  <- Forensic duplicate exclusion manifests
│   ├── FRUITVISION_EXCLUSION_MANIFEST.csv        (28 identical MD5 duplicates)
│   ├── FRUITVISION_INCLUSION_MANIFEST.csv        (4,157 clean test samples)
│   ├── SULTANA_EXCLUSION_MANIFEST.csv            (7 identical MD5 duplicates)
│   ├── SULTANA_INCLUSION_MANIFEST.csv            (1,193 clean test samples)
│   └── EXCLUSION_AUDIT_REPORT.md                 (Forensic deduplication methodology)
├── PHASH_REVIEW/                                 <- Near-duplicate collision audit & visual evidence
│   ├── PHASH_CANDIDATE_AUDIT.csv                 (8 audited candidate collision pairs)
│   └── pair_01_review.png ... pair_08_review.png (Diagnostic visual contact sheets)
├── TRAINING_LOGS/                                <- Epoch-by-epoch training logs
│   ├── historical_random_training_history.csv    (Model A training history)
│   └── group_aware_training_history.csv          (Model B training history)
└── SOURCE_CODE/                                  <- Executable scripts and test harnesses
    ├── master_inference_and_calibration_v4.py
    ├── investigate_and_merge_phash.py
    ├── calculate_field_study_power.py
    ├── build_dataset_exclusion_manifests.py
    ├── rebuild_reference_verification_v4.py
    └── test_reproducibility_v4.py
```

