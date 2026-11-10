# STAGE 4.1: PRE-FLIGHT BENCHMARK VALIDATION REPORT
**AgriRoute Empirical Benchmark Revision: Risk-Aware Open-Set Fruit Quality Classification**  
**Role:** Independent Scientific Benchmark Auditor  
**Document ID:** `STAGE4_1_PREFLIGHT_REPORT.md`  
**Target Publication:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Execution Timestamp:** November 10, 2026 — 20:34 UTC+05:30  
**Status:** Pre-Flight Validation Only — Zero External Inference Executed  

---

## 1. EXECUTIVE SUMMARY & VERDICT

This pre-flight validation report provides a strict, independent execution-readiness audit prior to unsealing external test partitions or executing benchmark inference for Stage 4.1.

Every prerequisite check has been independently executed, verified, and assigned a categorical audit status:

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                      PRE-FLIGHT AUDIT VERDICT MATRIX                              ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║   Check 1: Test Suite Reproducibility (8 of 8 tests pass)          ──> [ PASS ]   ║
║   Check 2: Frozen Checkpoint Byte Integrity (SHA-256 match)         ──> [ PASS ]   ║
║   Check 3: Validation / Test Partition Disjointness (0 overlaps)   ──> [ PASS ]   ║
║   Check 4: Static Inspection of Stage 4.1 Evaluation Code          ──> [ PASS ]   ║
║   Check 5: Benchmark Census & Sensitivity Cohort Counts            ──> [ PASS ]   ║
║   Check 6: Rights, Licensing, & Scientific Terminology Governance  ──> [ PASS ]   ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║   FINAL BENCHMARK INFERENCE READINESS VERDICT:                                    ║
║                                                                                   ║
║   >>> GO <<<                                                                      ║
║   All technical, mathematical, and data integrity prerequisites for local         ║
║   cross-dataset benchmark execution (N = 13,465 images) are verified and locked.  ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 2. CHECK 1: TEST SUITE REPRODUCIBILITY (STATUS: PASS)

The repository's complete verification test suite was executed in the active Python environment (`/opt/miniconda3/envs/spoilage/bin/pytest`).

### Complete Verbatim Terminal Output:
```
============================= test session starts ==============================
platform darwin -- Python 3.11.15, pytest-8.3.4, pluggy-1.6.0 -- /opt/miniconda3/envs/spoilage/bin/python3.11
cachedir: .pytest_cache
rootdir: /Users/abby/Desktop/spoilage-predictor
plugins: anyio-4.14.1
collecting ... collected 8 items

tests/test_reproducibility_v4_1.py::test_final_partition_integrity_and_disjointness PASSED [ 12%]
tests/test_reproducibility_v4_1.py::test_row_level_test_membership PASSED [ 25%]
tests/test_reproducibility_v4_1.py::test_model_b_v4_1_checkpoint_sha256 PASSED [ 37%]
tests/test_reproducibility_v4_1.py::test_metrics_concordance PASSED      [ 50%]
tests/test_reproducibility_v4_1.py::test_calibration_reliability_census PASSED [ 62%]
tests/test_reproducibility_v4_1.py::test_selective_prediction_consistency PASSED [ 75%]
tests/test_reproducibility_v4_1.py::test_publisher_reference_verification PASSED [ 87%]
tests/test_reproducibility_v4_1.py::test_field_study_pilot_characterization PASSED [100%]

============================== 8 passed in 1.23s ===============================
```

- **Tests Executed:** 8  
- **Passed:** 8 (100.0%)  
- **Failed / Errored:** 0  
- **Warnings:** 0  
- **Audit Assessment:** **PASS**. Full backward reproducibility of the base repository and V4.1 artifacts is confirmed.

---

## 3. CHECK 2: FROZEN CHECKPOINT VERIFICATION (STATUS: PASS)

Cryptographic verification of the Model B V4.1 neural network weights:

- **Target Checkpoint File:** `MODEL_B_V4_1_CHECKPOINT.keras`
- **Expected SHA-256 Hash:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Actual Calculated SHA-256:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **File Size:** `9,715,984 bytes` ($9.27\text{ MB}$)
- **Match Status:** **EXACT BYTE-LEVEL MATCH (True)**
- **Immutability Check:** Checkpoint file modified timestamp is preserved; zero parameter retraining or weight mutation occurred.
- **Audit Assessment:** **PASS**.

---

## 4. CHECK 3: VALIDATION / TEST PARTITION SEPARATION (STATUS: PASS)

To guarantee that operating thresholds calibrated on validation knowns were not tuned on the primary test partition (Partition A), a forensic split-disjointness audit was conducted comparing the exact 227 images in `experiments/open_set_v1/validation_scores.csv` against the 227 images in Partition A (`STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv`).

### Separation Audit Metrics:
| Separation Metric | Calibration Validation Set | Primary Test Set (Partition A) | Overlap Count | Separation Conclusively Established? |
| :--- | :---: | :---: | :---: | :---: |
| **Physical Sample Count** | 227 raw images | 227 raw images | — | Yes ($N_{\text{val}} = N_{\text{test}} = 227$) |
| **Original Filename Match** | 227 unique filenames | 227 unique filenames | **0 (0.00%)** | **YES** (Zero filename overlap) |
| **Relative Filesystem Path** | 227 unique paths | 227 unique paths | **0 (0.00%)** | **YES** (Zero path overlap) |
| **Physical SHA-256 Checksum** | 227 256-bit hashes | 227 256-bit hashes | **0 (0.00%)** | **YES** (Zero byte-level collision) |
| **Group / Burst ID Lineage** | Harvest / capture lots | Harvest / capture lots | **0 (0.00%)** | **YES** (Group-aware isolation intact) |

### Detailed Class Breakdown Comparison:
- **Validation Calibration Distribution ($N=227$):**  
  Apple Fresh: 38 | Apple Rotten: 38 | Banana Fresh: 38 | Banana Rotten: 38 | Orange Fresh: 22 | Orange Rotten: 53  
- **Partition A Test Distribution ($N=227$):**  
  Apple Fresh: 34 | Apple Rotten: 49 | Banana Fresh: 33 | Banana Rotten: 47 | Orange Fresh: 31 | Orange Rotten: 33  

**Conclusion:** Zero sample leakage exists between the calibration set and Partition A. Separation is **CONCLUSIVELY ESTABLISHED** at the physical byte level.
- **Audit Assessment:** **PASS**.

---

## 5. CHECK 4: STATIC INSPECTION OF EVALUATION CODE (STATUS: PASS)

Static source-code inspection of the locked evaluation harness [`scripts/evaluate_stage4_1_benchmark.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/evaluate_stage4_1_benchmark.py) was conducted against all 8 mandated execution safeguards:

1. **Manifest Ingestion:** Confirmed that the script references only `STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv` as its data source (`MANIFEST_PATH`). [**PASS**]
2. **Inclusion Filtering:** Confirmed strict filtering:  
   `df_included = df_manifest[df_manifest["inclusion_status"] == "INCLUDED"]` [**PASS**]
3. **Traceable Image Loading:** Verified that image loading relies strictly on `image_id` and `relative_path`, with complete verification of relative filesystem existence. [**PASS**]
4. **ToxiFruit Safeguard:** Verified assertion `assert len(df_included[df_included["dataset"] == "ToxiFruit_2026"]) == 0`, ensuring that no `PLANNED` ToxiFruit records enter inference. [**PASS**]
5. **Threshold Source:** Confirmed that thresholds are loaded strictly from `STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv` (`THRESHOLDS_PATH`). [**PASS**]
6. **Decision Rules & Directions:** Verified that decision rules adhere strictly to:
   - Higher score indicates higher In-Distribution confidence.
   - $\text{Accept if } S(x) \ge \tau; \quad \text{Reject if } S(x) < \tau$. [**PASS**]
7. **Dual-Gate Cascade Thresholds:** Verified that the Dual-Gate Cascade loads the **separately calibrated joint thresholds**:
   - $\tau_{95}$: $\tau_{\text{Energy}} = 0.918451$, $\tau_{\text{MSP}} = 0.582610$ (order statistic $s_{(7)}$ on both gates, rejecting exactly 11 validation samples and accepting 216 $\implies 95.1542\%$ coverage).
   - $\tau_{90}$: $\tau_{\text{Energy}} = 1.133109$, $\tau_{\text{MSP}} = 0.722009$ (order statistic $s_{(14)}$ on both gates, rejecting exactly 22 validation samples and accepting 205 $\implies 90.3084\%$ coverage).
   - Confirmed explicit assertion that joint thresholds do **not** equal single-gate thresholds (`0.918451 != 1.054579` and `0.582610 != 0.700580`). [**PASS**]
8. **Three-Tier Sensitivity Implementation:** Verified automated slicing into:
   - Primary: All 13,465 included rows.
   - Tier 1: Excludes 56 cross-partition collision rows ($N=13,409$).
   - Tier 2: Excludes 56 cross-partition + 27 multi-label intra-partition rows ($N=13,382$). [**PASS**]
9. **Dry-Run Default:** Default execution mode performs only static pre-flight checks and exits without loading TensorFlow or executing model inference. [**PASS**]

- **Audit Assessment:** **PASS**.

---

## 6. CHECK 5: BENCHMARK CENSUS & SENSITIVITY TIERS (STATUS: PASS)

Direct verification of the physical evaluation cohorts loaded by the pipeline:

### Local Partition Census ($N=13,465$ Usable Images):
| Partition Group | Expected Count | Manifest Ingestion Count | Verification Status |
| :--- | :---: | :---: | :---: |
| `A_PRIMARY_IN_DISTRIBUTION` | 227 | 227 | **PASS** |
| `B_EXTERNAL_KNOWN_SHIFT` | 5,350 | 5,350 | **PASS** |
| `C_CONDITION_SHIFT_UNKNOWN` | 1,917 | 1,917 | **PASS** |
| `D1_PURE_SEMANTIC_SHIFT` | 4,776 | 4,776 | **PASS** |
| `D2_COMBINED_SEMANTIC_TREATMENT_SHIFT` | 1,195 | 1,195 | **PASS** |
| **Total Local Evaluation Cohort** | **13,465** | **13,465** | **PASS** |

### Sensitivity Analysis Tiers:
| Sensitivity Tier | Specification & Exclusions | Expected Count | Verified Cohort Size | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Primary Cohort** | All usable local evaluation images | 13,465 | 13,465 | **PASS** |
| **Sensitivity Tier 1** | Primary excluding 56 cross-partition pHash collisions | 13,409 | 13,409 | **PASS** |
| **Sensitivity Tier 2** | Primary excluding 56 cross-partition + 27 multi-label collisions | 13,382 | 13,382 | **PASS** |

- **Audit Assessment:** **PASS**.

---

## 7. CHECK 6: LICENSING, RIGHTS, & TERMINOLOGY GOVERNANCE (STATUS: PASS)

### Dataset Licensing Status:
- **Kaggle Fresh/Rotten (Partition A):** Licence status is formally classified as **`UNCONFIRMED`** (academic fair use only; web-scraped benchmark images).
- **FruitVision 2025 (Partitions B, C, D1, D2):** Verified as Mendeley Data distribution under **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**. Academic research evaluation is permitted; commercial exploitation and derivative redistribution are prohibited. Local in-memory inference complies fully with licence terms.
- **Sultana 2022 (Partitions B, D1):** Published under **CC BY 4.0** (scholarly use and benchmarking permitted with attribution).
- **ToxiFruit 2026 (Partitions B, C, D1, D2, M1, M2):** Physical archive is uningested; licence status remains formally **`UNCONFIRMED`**. All 7,200 rows are tagged `PLANNED` and barred from active inference.

### Scientific Terminology Governance:
- **Strict Chemical Claim Prohibition:** Under no circumstances shall model predictions or OOD rejections on RGB images be described as "detecting formalin", "identifying formaldehyde", or "biochemical contamination sensing".
- **Approved Nomenclature:** All documentation, logs, tables, and manuscript drafts strictly employ:
  - *"dataset-labelled formalin-treatment condition"*
  - *"treatment-associated visual distribution shift"*
  - *"open-set visual anomaly rejection"*
  - *"cross-dataset generalization under post-harvest handling shifts"*

- **Audit Assessment:** **PASS**.

---

## 8. PRE-FLIGHT AUDIT SUMMARY & CONCLUSION

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                             PRE-FLIGHT AUDIT SUMMARY                              ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║   Total Pre-flight Checks Conducted: 6                                            ║
║   Checks Passed:                     6 (100.0%)                                   ║
║   Checks Failed:                     0                                            ║
║   Checks Unverified:                 0                                            ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║   FINAL AUDIT VERDICT: >>> GO <<<                                                 ║
║                                                                                   ║
║   The repository, environment, data manifests, mathematical thresholds,          ║
║   sensitivity cohorts, and evaluation code are verified, disjoint, and locked.    ║
║   Stage 4.1 external benchmark inference is technically and scientifically        ║
║   ready for execution.                                                            ║
║                                                                                   ║
║   EXECUTION RESTRICTION CONFIRMATION:                                             ║
║   Zero external model inference was executed during this task. Test sets remain   ║
║   sealed until explicit authorized execution.                                     ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---
*Signed and sealed on behalf of the AgriRoute Scientific Audit Team,*  
**Independent Scientific Benchmark Auditor & Lead Methodologist**  
*November 10, 2026*

