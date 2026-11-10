# Pipeline Reproducibility & Integrity Audit Report

**Experiment Directory:** `experiments/open_set_v1/`  
**Document ID:** `reproducibility_report.md`  
**Execution Timestamp:** November 10, 2026  
**Auditor:** Lead ML Research Engineer & Scientific Reproducibility Auditor  

---

## 1. Executive Summary

This report certifies the forensic integrity, numerical determinism, and data isolation of the Stage 3.1 baseline infrastructure pipeline. All operations were executed read-only against the frozen Model B V4.1 checkpoint.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              REPRODUCIBILITY CENSUS                                    │
├─────────────────────────────────────────┬──────────────────────┬───────────────────────┤
│ Check Item                              │ Required Standard    │ Verified State        │
├─────────────────────────────────────────┼──────────────────────┼───────────────────────┤
│ Checkpoint Pre-Execution SHA-256        │ 4a12f354...          │ Verified Match        │
│ Checkpoint Post-Execution SHA-256       │ 4a12f354...          │ 100% Byte-Identical   │
│ Training Raw Partition Row Count        │ Exactly 1,057        │ Exactly 1,057         │
│ Validation Raw Partition Row Count      │ Exactly 227          │ Exactly 227           │
│ Offline Augmented Variants in Training  │ Exactly 0            │ 0 (8,456 Excluded)    │
│ Offline Augmented Variants in Validation│ Exactly 0            │ 0 (1,816 Excluded)    │
│ NaN / Inf Values in Features            │ 0                    │ 0                     │
│ NaN / Inf Values in Logits              │ 0                    │ 0                     │
│ NaN / Inf Values in Probabilities       │ 0                    │ 0                     │
│ Primary Test Set Inspection             │ 0 samples            │ 0 (Completely Sealed) │
│ External Dataset Inspection             │ 0 samples            │ 0 (Completely Sealed) │
└─────────────────────────────────────────┴──────────────────────┴───────────────────────┘
```

---

## 2. Checkpoint Immutability Audit

- **Checkpoint File Path:** `MODEL_B_V4_1_CHECKPOINT.keras`
- **Pre-Execution Checksum:**
  `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Post-Execution Checksum:**
  `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Byte Delta:** Exactly $0$ bytes.
- **Verification:** Loading the checkpoint via `tf.keras.models.load_model(..., compile=False)` and building in-memory feature extractors leaves the serialized HDF5/Keras zip package completely untouched.

---

## 3. Data Partitioning & Alignment Verification

### 3.1 Training Array Alignment (`train_features.npz`)
- **File Size:** 3,528,096 bytes.
- **Keys:** `image_ids`, `labels`, `class_names`, `features`, `logits`, `probs`.
- **Dimensions:**
  - `features`: $(1057, 1280)$
  - `logits`: $(1057, 6)$
  - `probs`: $(1057, 6)$
  - `labels`: $(1057,)$
  - `image_ids`: $(1057,)$
- **Alignment:** Every row $i$ in `train_features.npz` strictly corresponds to row $i$ in `FINAL_GROUP_TRAIN_V4_1.csv` filtered by `is_raw == 1`.
- **Class Breakdown:**
  - `rotten_apple`: 229
  - `rotten_banana`: 213
  - `fresh_apple`: 163
  - `rotten_orange`: 156
  - `fresh_banana`: 152
  - `fresh_orange`: 144
  Total: 1,057 raw images.

### 3.2 Validation Array Alignment (`validation_features.npz`)
- **File Size:** 770,072 bytes.
- **Keys:** `image_ids`, `labels`, `class_names`, `features`, `logits`, `probs`.
- **Dimensions:**
  - `features`: $(227, 1280)$
  - `logits`: $(227, 6)$
  - `probs`: $(227, 6)$
  - `labels`: $(227,)$
  - `image_ids`: $(227,)$
- **Alignment:** Every row $i$ in `validation_features.npz` strictly corresponds to row $i$ in `FINAL_GROUP_VAL_V4_1.csv` filtered by `is_raw == 1`.
- **Class Breakdown:**
  - `rotten_apple`: 49
  - `rotten_banana`: 46
  - `fresh_apple`: 35
  - `fresh_banana`: 33
  - `rotten_orange`: 33
  - `fresh_orange`: 31
  Total: 227 raw images.

---

## 4. Numerical Health of Baseline Score Functions

All five baseline scorers evaluated on validation samples were checked for numerical anomalies:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        VALIDATION SCORE FUNCTION NUMERICAL CENSUS                      │
├─────────────────────────┬──────────────┬──────────────┬──────────────┬─────────────────┤
│ Score Name              │ Min Value    │ Mean Value   │ Max Value    │ NaN / Inf Count │
├─────────────────────────┼──────────────┼──────────────┼──────────────┼─────────────────┤
│ score_msp               │ 0.4225       │ 0.9226       │ 0.9998       │ 0               │
│ score_energy_id         │ -0.6278      │ 2.4590       │ 4.9080       │ 0               │
│ score_odin              │ 0.1668       │ 0.1673       │ 0.1675       │ 0               │
│ score_mahalanobis_id    │ -49.6105     │ -27.8712     │ -17.9042     │ 0               │
│ score_openmax_id        │ 0.3204       │ 0.9313       │ 0.9997       │ 0               │
│ score_calibrated_conf   │ 0.4225       │ 0.9226       │ 0.9998       │ 0               │
└─────────────────────────┴──────────────┴──────────────┴──────────────┴─────────────────┘
```

- **Health:** Zero NaNs, zero infinities, zero out-of-bound probabilities across all 227 validation samples.

---

## 5. Test Partition Sealing Certification

The Lead Scientific Reproducibility Auditor formally certifies that:
1. `FINAL_GROUP_TEST_V4_1.csv` was **NEVER opened, read, or evaluated** during this stage.
2. FruitVision, ToxiFruit, and Sultana datasets were **NEVER accessed or evaluated**.
3. All baseline parameters (centroids, covariance, Weibull parameters, temperature) were fitted strictly on training or validation sets.
4. No threshold tuning on external anomalies has taken place.

---
*Certified by Lead ML Research Engineer and Reproducibility Auditor.*

