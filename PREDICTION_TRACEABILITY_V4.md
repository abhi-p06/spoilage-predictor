# Prediction Traceability & Schema Audit Report (V4)

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Reproducibility Auditor:** Lead Scientific Reproducibility Engineer  
**Document ID:** `PREDICTION_TRACEABILITY_V4.md`  
**Execution Timestamp:** 2026-11-09  
**Git Branch:** `remediation/v4-evidence-consistency`  
**Associated Scripts:** [`scripts/master_inference_and_calibration_v4.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/master_inference_and_calibration_v4.py)

---

## 1. Executive Summary & V4 Enhancements

In accordance with independent auditor requirements, AgriRoute V4 introduces a fully unified prediction schema that eliminates ambiguity between raw logits, uncalibrated softmax scores, and temperature-scaled probabilities.

Every sample across all five evaluation partitions is traceable to its physical image file on disk, its 32-character hexadecimal MD5 hash, its 64-character SHA-256 checkpoint provenance, its native pre-softmax logits, its raw softmax confidence scores, and its validation-calibrated probabilities.

---

## 2. Authoritative Prediction Inventory (V4)

| CSV Table Name | Evaluated Backbone | Checkpoint SHA-256 | Source Corpus & Partition | Sample Count ($N$) | MD5 Verified | Calibrated Probs Included |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: |
| [`PREDICTIONS_RANDOM_V4.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_RANDOM_V4.csv) | Model A (Historical) | `6d7f61d368a7...` | Kaggle Random Internal Test | 4,090 | 100% | YES ($T^*=1.3157$) |
| [`PREDICTIONS_GROUP_TEST_V4.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_GROUP_TEST_V4.csv) | Model B (Group-Aware) | `3bdda4572ba1...` | Kaggle Group Test (All 9 Variants) | 2,043 | 100% | YES ($T^*=0.4905$) |
| [`PREDICTIONS_GROUP_TEST_RAW_ONLY_V4.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_GROUP_TEST_RAW_ONLY_V4.csv) | Model B (Group-Aware) | `3bdda4572ba1...` | Kaggle Group Test (Raw Base Only) | 227 | 100% | YES ($T^*=0.4905$) |
| [`PREDICTIONS_FRUITVISION_V4.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_FRUITVISION_V4.csv) | Model B (Group-Aware) | `3bdda4572ba1...` | FruitVision V2 Clean Test | 4,157 | 100% | YES ($T^*=0.4905$) |
| [`PREDICTIONS_SULTANA_V4.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_SULTANA_V4.csv) | Model B (Group-Aware) | `3bdda4572ba1...` | Sultana et al. Clean Test | 1,193 | 100% | YES ($T^*=0.4905$) |

---

## 3. Standardized 37-Column V4 Schema

Every generated V4 prediction table strictly implements the following standardized schema:

### Provenance & Identifiers (Columns 1–11)
1. `sample_id` (string): Standardized sample ID formatted as `{PARTITION}_{INDEX:04d}`.
2. `dataset_name` (string): Source dataset name (`Kaggle_FreshRotten`, `FruitVision`, `Sultana`).
3. `split_name` (string): Split partition name (`historical_random_test`, `group_aware_test`, `external_test`).
4. `model_name` (string): Model identifier (`Model_A_Historical_Random` or `Model_B_Group_Aware`).
5. `relative_path` (string): Portable POSIX relative path from repository root.
6. `filename` (string): File basename on disk.
7. `base_filename` (string): Base screenshot filename after prefix stripping (`N/A_EXTERNAL` for external datasets).
8. `base_group_id` (string): Group ID matching `BASE_IMAGE_GROUP_AUDIT.csv`.
9. `variant_type` (string): Transformation category (`raw_screenshot`, `rotation`, `translation`, etc.).
10. `is_raw` (integer): `1` for original unaugmented screenshot, `0` for affine variant.
11. `md5` (string): 32-character hexadecimal MD5 checksum of the image file on disk.

### Ground Truth & Decision (Columns 12–19)
12. `ground_truth_label` (string): Class string name (`fresh_apple`, `rotten_banana`, etc.).
13. `ground_truth_idx` (integer): Integer class target ($0 \dots 5$).
14. `predicted_label` (string): Predicted class string from $\operatorname{argmax} P(y \mid x)$.
15. `predicted_idx` (integer): Predicted integer target ($0 \dots 5$).
16. `max_confidence` (float): Maximum raw softmax probability $\max_k P(y=k \mid x)$.
17. `tau_threshold` (float): Uncertainty-aware decision threshold ($\tau = 0.9000$).
18. `decision` (string): `ACCEPTED` if $\max_k P(y=k \mid x) \ge \tau$, else `ABSTAINED`.
19. `temperature_T` (float): Validation-fitted temperature scaling parameter applied.

### Raw Softmax Probabilities (Columns 20–25)
20–25. `prob_{class_name}` (6 float columns): Raw softmax probabilities summing to 1.0.

### Calibrated Probabilities (Columns 26–31)
26–31. `prob_cal_{class_name}` (6 float columns): Temperature-scaled softmax probabilities $\operatorname{softmax}(z / T)$ summing to 1.0.

### Native Pre-Softmax Logits (Columns 32–37)
32–37. `logit_{class_name}` (6 float columns): Pre-softmax dense layer activation values $z = W h + b$.

---

## 4. Selective Prediction Operating Points at $\tau = 0.90$

Calculated directly from the predictions tables without approximation:

### 4.1 FruitVision External Benchmark ($N=4,157$)
- **Total Test Cohort:** 4,157 samples
- **Coverage ($\kappa$):** **$25.11\%$** (1,044 accepted samples)
- **Abstention Rate ($1 - \kappa$):** **$74.89\%$** (3,113 samples routed to human inspector)
- **Accepted Subset Accuracy:** **$95.69\%$** (999 correct / 1,044 accepted)
- **Accepted Subset Error Rate:** **$4.31\%$** (45 errors)

### 4.2 Sultana External Benchmark ($N=1,193$)
- **Total Test Cohort:** 1,193 samples
- **Coverage ($\kappa$):** **$23.81\%$** (284 accepted samples)
- **Abstention Rate ($1 - \kappa$):** **$76.19\%$** (909 samples routed to human inspector)
- **Accepted Subset Accuracy:** **$82.04\%$** (233 correct / 284 accepted)
- **Accepted Subset Error Rate:** **$17.96\%$** (51 errors)

### 4.3 Scientific Reporting Guideline
The 95.69% accuracy applies exclusively to the 25.11% high-confidence operating subset. The overall zero-shot accuracy across all 4,157 samples is 67.33%. The system is presented as an automated screening filter for high-volume packhouses rather than an autonomous replacement for human inspectors.

