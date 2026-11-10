# STAGE 4.1.1 — SCIENTIFIC REPRODUCIBILITY AUDIT AND VERIFICATION REPORT

**Document Type:** Formal Scientific Audit & Change-Control Verification  
**Auditor:** Independent Scientific Benchmark Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** COMPLETED — CONDITIONAL GO FOR MANUSCRIPT SUBMISSION  

---

## 1. Executive Summary

This audit constitutes the comprehensive forensic reconciliation of Stage 4.1 benchmark inference for AgriRoute's computer vision backbone (`Model B V4.1`). 

The audit evaluated 13,465 image-level prediction records across five distinct partitions (Partitions A, B, C, D1, D2), reconciling all statistical discrepancies between the primary prediction manifest (`STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`), partition metrics, confidence intervals, sensitivity analyses, and academic reporting texts.

### Deliverables Reconciled and Validated:
1. `STAGE4_1_1_RECONCILED_PARTITION_METRICS.csv` (38 benchmark rows; 100% verified against primary predictions)
2. `STAGE4_1_1_RECONCILED_CONFIDENCE_INTERVALS.csv` (40 rows; point estimates 100% matched to primary sample)
3. `STAGE4_1_1_RECONCILED_SENSITIVITY_ANALYSIS.csv` (108 rows; exact percentage point deviations computed)
4. `STAGE4_1_1_DUALGATE_SCORE_AUDIT.md` (Forensic trace of continuous proxy formula and cascade decision rules)
5. `STAGE4_1_1_REVISED_RESULTS_REPORT.md` (Primary empirical results and statistical benchmark presentation)
6. `STAGE4_1_1_REVISED_FAILURE_ANALYSIS.md` (Forensic diagnosis of domain shift and botanical/optical failure modes)
7. `STAGE4_1_1_REPRODUCIBILITY_AUDIT.md` (This document)

---

## 2. Checkpoint and Environment Cryptographic Verification

The vision model evaluated in Stage 4.1 was verified prior to and following inference:

- **Model File:** `MODEL_B_V4_1_CHECKPOINT.keras`
- **File Size:** 9,715,984 bytes
- **Expected SHA-256:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Computed SHA-256:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Integrity Status:** **EXACT MATCH (VERIFIED FROZEN)**
- **Weight Modification:** NONE (Zero retraining, zero fine-tuning, zero post-hoc weight adjustment)

### Test Suite Execution
The automated regression and reproducibility suite was executed via pytest:
```bash
pytest tests/test_reproducibility_v4_1.py
```
**Result:** 8 passed in 1.10s (100% pass rate; zero failures, zero regressions).

---

## 3. Forensic Trace of Identified Discrepancies and Their Resolutions

### 3.1 Dual-Gate Continuous Score Formulation
- **Issue:** The image-level prediction artifact contained scalar scores for individual detectors and boolean acceptance flags for Dual-Gate, but no continuous column titled `score_dualgate`.
- **Forensic Investigation:** Inspection of `scripts/run_stage4_1_benchmark.py` (lines 459–464) confirmed that an explicit continuous proxy formula was defined during execution:
  $$S_{\text{DualGate}}(x) = \left(S_{\text{Energy}}(x) - \tau_{E, 95}\right) + \left(S_{\text{MSP}}(x) - \tau_{M, 95}\right)$$
- **Audit Findings:** 
  1. The recovered formula produces 100% numerical concordance with the AUROC, AUPR-IN, AUPR-OUT, and OSCR metrics reported in `STAGE4_1_PARTITION_METRICS.csv`.
  2. The formula represents an unweighted sum of margins across disparate numerical scales ($S_{\text{Energy}} \in [-4.8, 8.4]$ vs. $S_{\text{MSP}} \in [0.17, 1.0]$), meaning ranking is dominated by the Energy component.
- **Resolution:** Fully documented in `STAGE4_1_1_DUALGATE_SCORE_AUDIT.md`. Operational metrics (UFAR, UFAR-Fresh, KRR) remain the primary deployment benchmarks, and continuous metrics are reported with transparent disclosure.

### 3.2 Partition B Class-Wise and Species-Wise Accuracy Re-Computation
- **Issue:** Earlier preliminary draft reports cited unverified class-wise figures on Partition B.
- **Forensic Investigation:** Accuracy was recomputed directly from `ground_truth_label_idx` and `top1_pred_idx` in `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`.
- **Verified Values:**
  - Fresh Apple: $310 / 965 =$ **$32.12\%$**
  - Rotten Apple: $310 / 830 =$ **$37.35\%$**
  - Fresh Banana: $736 / 948 =$ **$77.64\%$**
  - Rotten Banana: $826 / 831 =$ **$99.40\%$**
  - Fresh Orange: $828 / 946 =$ **$87.53\%$**
  - Rotten Orange: $647 / 830 =$ **$77.95\%$**
  - Species Aggregates: Apple = **$34.54\%$**, Banana = **$87.80\%$**, Orange = **$83.05\%$**
  - Overall Partition B: $3,657 / 5,350 =$ **$68.36\%$**
- **Resolution:** All draft markdown reports have been updated to reflect these verified numbers.

### 3.3 Resolution of AUPR-IN Discrepancies on A-vs-D2 and B-vs-C
- **Issue:** AUPR-IN values in `STAGE4_1_FINAL_RESULTS_REPORT.md` differed from `STAGE4_1_PARTITION_METRICS.csv`.
- **Forensic Diagnosis:** The draft markdown report had incorporated intermediate numbers from an early pilot execution.
- **Resolution:** Reconciled in `STAGE4_1_1_RECONCILED_PARTITION_METRICS.csv` and `STAGE4_1_1_REVISED_RESULTS_REPORT.md`. Both documents now share identical verified full-sample values:
  - Benchmark 3 (A vs D2): MSP = $91.18\%$, Energy = $98.44\%$, ODIN = $93.25\%$, Mahalanobis = $92.23\%$, OpenMax = $96.81\%$, Dual-Gate = $97.97\%$.
  - Benchmark 4 (B vs C): MSP = $81.96\%$, Energy = $75.30\%$, ODIN = $80.32\%$, Mahalanobis = $75.05\%$, OpenMax = $79.19\%$, Dual-Gate = $75.98\%$.

### 3.4 Variable Bleed in Bootstrap Confidence Interval Calculation
- **Issue:** Point estimates in `STAGE4_1_CONFIDENCE_INTERVALS.csv` differed slightly from `STAGE4_1_PARTITION_METRICS.csv` (e.g., A vs C MSP AUROC was $90.65\%$ in CI vs. $90.63\%$ in Metrics).
- **Forensic Diagnosis:** In `scripts/run_stage4_1_benchmark.py`, the loop evaluating sensitivity tiers (`for tier_name, t_df in tiers.items():`) terminated on Tier 2 ($N = 13,382$). The subsequent bootstrap block used the lingering variables `df_A` and `df_C`, thereby bootstrapping from Tier 2 rather than the Primary Cohort ($N = 13,465$).
- **Resolution:** `STAGE4_1_1_RECONCILED_CONFIDENCE_INTERVALS.csv` was recomputed strictly on the Primary Cohort. Point estimates now match the metrics table exactly.

### 3.5 Correction of Sensitivity Analysis Claims
- **Issue:** The preliminary results report asserted that all metrics varied by $\le 0.10\%$.
- **Forensic Diagnosis:** Evaluating all 108 rows in `STAGE4_1_SENSITIVITY_ANALYSIS.csv` reveals that while AUROC shifted by at most $0.19$ pp, AUPR-OUT shifted by up to $0.70$ pp and UFAR shifted by up to $0.53$ pp.
- **Resolution:** Stated with mathematical precision in percentage points in `STAGE4_1_1_RECONCILED_SENSITIVITY_ANALYSIS.csv` and `STAGE4_1_1_REVISED_RESULTS_REPORT.md`.

### 3.6 Investigation of the Empty `fpr95_empirical` Column
- **Issue:** In `STAGE4_1_PARTITION_METRICS.csv`, the column `fpr95_empirical` was empty/NaN for open-set rows.
- **Forensic Diagnosis:** In `scripts/run_stage4_1_benchmark.py`, closed-set rows were populated with key `"fpr95_empirical": "N/A"`, while open-set rows were populated with key `"empirical_ufar_tau95": f"{ufar_95*100:.2f}%"`. This discrepancy caused pandas to instantiate two disjoint columns.
- **Resolution:** Reconciled in `STAGE4_1_1_RECONCILED_PARTITION_METRICS.csv` by cleanly separating:
  1. `empirical_ufar_tau95`: Operational false alarm rate at locked validation threshold.
  2. `fpr95_retrospective`: Standard academic benchmark false alarm rate at $95\%$ test ID TPR.

---

## 4. Prediction-Output Traceability (6-Class Logits and Probabilities)

- **Audit Query:** Are full 6-dimensional logit and probability vectors available in cached inference artifacts?
- **Forensic Inspection:** 
  `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` stores:
  - `ground_truth_label_idx`
  - `top1_pred_idx`
  - `top1_pred_class`
  - `top1_pred_prob`
  - `score_msp`, `score_energy`, `score_odin`, `score_mahalanobis`, `score_openmax`
  - Binary acceptance flags
- **Storage Finding:** During inference execution in `scripts/run_stage4_1_benchmark.py`, full 6-class vectors (`all_logits`, `all_probs`) were held in transient RAM memory to calculate the five scalar scores and top-1 predictions, and were not serialized to disk.
- **Scientific Integrity Decision:** In accordance with research ethics rules, no synthetic logit vectors will be fabricated. The limitation is documented transparently. The saved image-level top-1 predictions and scalar detector scores provide complete reproducibility for all reported benchmark metrics.

---

## 5. Final Manuscript Verdict and Recommendations

### **FINAL VERDICT: CONDITIONAL GO**

The benchmark data, model checkpoint, and statistical analyses are approved for incorporation into the revised AgriRoute manuscript (*Procedia Computer Science*), subject to the following mandatory conditions:

1. **Adopt Reconciled Tables Exclusively:**
   All tables, charts, and inline text in the manuscript must draw strictly from `STAGE4_1_1_RECONCILED_PARTITION_METRICS.csv` and `STAGE4_1_1_RECONCILED_CONFIDENCE_INTERVALS.csv`.
2. **Mandatory Reporting of Domain Shift:**
   The paper must transparently report the drop from $96.92\%$ (Partition A) to $68.36\%$ (Partition B) as a central finding demonstrating the necessity of open-set abstention in real-world agricultural logistics.
3. **Dual-Gate Cascade Methodological Clarification:**
   Present the Dual-Gate Cascade primarily as a fixed-threshold operational deployment filter. When citing AUROC/OSCR, explicitly note that they are derived from an unweighted boundary-margin proxy.
4. **Strict Observational Language:**
   Preserve observational wording regarding chemical treatments ("dataset-labelled formalin-treatment condition"). Frame UFAR-Fresh as a critical limitation of RGB imaging that motivates multimodal sensor fusion.
5. **Acknowledge Resampling Assumption:**
   State clearly that bootstrap confidence intervals are conditional on image-level resampling exchangeability.

---

*Forensic Audit Complete. All deliverables sealed and verified.*

