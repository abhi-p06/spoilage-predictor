# STAGE 4.1.1 — REVISED BENCHMARK RESULTS AND STATISTICAL AUDIT REPORT

**Document Type:** Primary Scientific Benchmark Deliverable  
**Author:** Independent Scientific Benchmark Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** FULLY RECONCILED AGAINST PRIMARY PREDICTION MANIFEST  

---

## 1. Executive Summary and Benchmark Cohort Census

This report establishes the verified, fully reconciled empirical results of the frozen Model B V4.1 vision backbone across $N = 13,465$ local benchmark images evaluated under the Stage 4.0.3 external evaluation protocol.

Every numeric value reported in this document is derived by direct calculation from `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` and is completely concordant with:
1. `STAGE4_1_1_RECONCILED_PARTITION_METRICS.csv` (38 rows)
2. `STAGE4_1_1_RECONCILED_CONFIDENCE_INTERVALS.csv` (40 rows)
3. `STAGE4_1_1_RECONCILED_SENSITIVITY_ANALYSIS.csv` (108 rows)

### Table 1: Final Benchmark Evaluation Cohort Census

| Partition Code | Partition Designation | Primary Upstream Source | Specimen Count ($N$) | Evaluation Function |
| :--- | :--- | :--- | :---: | :--- |
| **Partition A** | Primary In-Distribution (ID Test) | Primary Kaggle Archive | 227 | Benchmark closed-set baseline; Primary ID anchor |
| **Partition B** | External Known Shift | FruitVision (Apple, Banana, Orange) | 5,350 | External domain shift; Secondary ID anchor |
| **Partition C** | Condition-Shift Formalin Knowns | FruitVision (Preserved Knowns) | 1,917 | OOD Condition Shift (Chemical fixative treatment) |
| **Partition D1** | Pure Semantic Shift Unknowns | FruitVision + Sultana (Unseen Species) | 4,776 | OOD Semantic Shift (Natural ambient conditions) |
| **Partition D2** | Combined Semantic & Treatment Shift | FruitVision (Preserved Unseen Species) | 1,195 | OOD Combined Shift (Preserved unknown species) |
| **Total Cohort**| **Complete Evaluation Benchmark** | **All Local Partitions** | **13,465** | **Fully Audited Primary Test Suite** |

**Model Checkpoint Integrity:**
- Checkpoint Path: `MODEL_B_V4_1_CHECKPOINT.keras`
- SHA-256: `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` (Verified Byte-Identical)
- Reproducibility Test Suite: 8 of 8 passed (`pytest tests/test_reproducibility_v4_1.py`)

---

## 2. Closed-Set Classification Performance (Partitions A & B)

Closed-set evaluation measures the model's accuracy on known classes (Apple, Banana, Orange $\times$ Fresh, Rotten) under laboratory conditions (Partition A) versus real-world retail market conditions (Partition B).

### Table 2: Closed-Set Performance Comparison

| Metric | Partition A (ID Test, $N=227$) | Partition B (External Known, $N=5,350$) | Domain Shift Delta ($\Delta$) |
| :--- | :---: | :---: | :---: |
| **Top-1 Accuracy** | **96.92%** | **68.36%** | $-28.56$ pp |
| **Macro-Averaged F1** | **96.87%** [94.11%, 98.81%] | **67.28%** [66.12%, 68.39%] | $-29.59$ pp |
| **Balanced Accuracy** | **96.43%** | **68.67%** | $-27.76$ pp |

### Table 3: Reconciled Class-Wise Performance on Partition B ($N = 5,350$)

| Class Name | Support ($N$) | Correct ($n$) | Class Accuracy (%) | Primary Misclassification Mode |
| :--- | :---: | :---: | :---: | :--- |
| **Fresh Apple** | 965 | 310 | **32.12%** | Rotten Apple ($40.73\%$), Rotten Orange ($26.42\%$) |
| **Rotten Apple** | 830 | 310 | **37.35%** | Rotten Orange ($43.49\%$), Fresh Apple ($18.92\%$) |
| **Fresh Banana** | 948 | 736 | **77.64%** | Rotten Banana ($21.84\%$) |
| **Rotten Banana** | 831 | 826 | **99.40%** | Fresh Banana ($0.36\%$) |
| **Fresh Orange** | 946 | 828 | **87.53%** | Rotten Orange ($9.83\%$), Fresh Apple ($0.95\%$) |
| **Rotten Orange** | 830 | 647 | **77.95%** | Fresh Orange ($12.77\%$), Rotten Apple ($8.43\%$) |
| **Species: Apple** | 1,795 | 620 | **34.54%** | Severe confusion between fresh/rotten and with orange |
| **Species: Banana** | 1,779 | 1,562 | **87.80%** | High fidelity; asymmetric bias toward rotten |
| **Species: Orange** | 1,776 | 1,475 | **83.05%** | Robust recognition; slight decay underestimation |
| **Total Cohort** | **5,350** | **3,657** | **68.36%** | **Overall Domain Degradation: $-28.56$ pp** |

---

## 3. Reconciled Open-Set Benchmark Results (All 6 Pairs)

All detector scores are oriented such that higher scores denote in-distribution (ID) likelihood. 
- **Operational UFAR ($\tau_{95}$):** The false alarm rate evaluated at the locked validation threshold $\tau_{95}^{\text{val}}$.
- **Retrospective FPR@95% TPR:** The empirical false alarm rate when the operating threshold is chosen post-hoc to accept exactly $95.0\%$ of that specific ID test partition.
- **Dual-Gate Note:** Continuous AUROC, AUPR, and OSCR for Dual-Gate are computed using the joint margin proxy $S_{\text{proxy}} = (S_E - \tau_E) + (S_M - \tau_M)$, while operational metrics (UFAR, UFAR-Fresh, KRR) reflect the discrete cascade decision rule.

### Benchmark 1: Partition A vs. Partition C (ID Known vs. Formalin Known)
$N_{\text{id}} = 227, N_{\text{ood}} = 1,917$ (Evaluating preservative condition shift from baseline studio data)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 90.63% | 47.93% | 98.92% | 50.29% | 56.96% | 37.09% | 6.61% | 88.75% |
| **Energy Baseline** | 84.09% | 47.36% | 97.80% | 53.94% | 43.51% | 44.03% | 2.20% | 82.20% |
| **ODIN Baseline** | 89.11% | 43.34% | 98.71% | 47.84% | 55.76% | 36.83% | 8.37% | 87.21% |
| **Mahalanobis** | 85.43% | 48.01% | 97.43% | 80.70% | 69.69% | 50.50% | 2.20% | 83.33% |
| **OpenMax** | 87.69% | 48.27% | 98.39% | 50.60% | 43.19% | 40.06% | 3.52% | 85.67% |
| **Dual-Gate Cascade** | 85.35% | 47.18% | 98.01% | 52.63% | 45.54% | 42.83% | 4.41% | 83.30% |

---

### Benchmark 2: Partition A vs. Partition D1 (ID Known vs. Pure Semantic Shift Unknowns)
$N_{\text{id}} = 227, N_{\text{ood}} = 4,776$ (Evaluating unseen species against baseline studio data — Confounded Shift)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 93.70% | 62.46% | 99.68% | 33.04% | 40.35% | 22.17% | 6.61% | 92.17% |
| **Energy Baseline** | 97.55% | 78.47% | 99.88% | 21.96% | 12.02% | 13.42% | 2.20% | 94.75% |
| **ODIN Baseline** | 94.66% | 60.10% | 99.72% | 22.47% | 31.22% | 10.68% | 8.37% | 92.93% |
| **Mahalanobis** | 94.81% | 69.31% | 99.72% | 46.48% | 36.18% | 26.47% | 2.20% | 92.20% |
| **OpenMax** | 95.83% | 72.80% | 99.78% | 25.80% | 16.79% | 16.29% | 3.52% | 93.47% |
| **Dual-Gate Cascade** | 97.50% | 77.66% | 99.87% | 23.95% | 14.11% | 15.58% | 4.41% | 94.75% |

---

### Benchmark 3: Partition A vs. Partition D2 (ID Known vs. Combined Semantic & Treatment Shift)
$N_{\text{id}} = 227, N_{\text{ood}} = 1,195$ (Evaluating preserved unseen species against baseline studio data)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 96.02% | 91.18% | 98.99% | 22.26% | 27.87% | 19.16% | 6.61% | 94.08% |
| **Energy Baseline** | 99.46% | 98.44% | 99.88% | 6.86% | 1.17% | 4.94% | 2.20% | 96.38% |
| **ODIN Baseline** | 96.89% | 93.25% | 99.12% | 10.46% | 16.90% | 7.28% | 8.37% | 94.55% |
| **Mahalanobis** | 95.95% | 92.23% | 98.18% | 41.26% | 26.36% | 27.70% | 2.20% | 92.87% |
| **OpenMax** | 99.04% | 96.81% | 99.80% | 10.38% | 5.52% | 7.95% | 3.52% | 96.10% |
| **Dual-Gate Cascade** | 99.38% | 97.97% | 99.87% | 9.54% | 3.18% | 7.28% | 4.41% | 96.38% |

---

### Benchmark 4: Partition B vs. Partition C (External Known Shift vs. Formalin Knowns)
$N_{\text{id}} = 5,350, N_{\text{ood}} = 1,917$ (Evaluating preservative condition shift within the external FruitVision domain)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 57.98% | 81.96% | 30.34% | 50.29% | 93.69% | 37.09% | 42.77% | 45.96% |
| **Energy Baseline** | 52.57% | 75.30% | 28.12% | 53.94% | 94.00% | 44.03% | 41.50% | 41.63% |
| **ODIN Baseline** | 55.54% | 80.32% | 30.06% | 47.84% | 92.12% | 36.83% | 48.86% | 44.23% |
| **Mahalanobis** | 50.10% | 75.05% | 25.41% | 80.70% | 98.17% | 50.50% | 19.16% | 33.16% |
| **OpenMax** | 55.18% | 79.19% | 28.53% | 50.60% | 94.57% | 40.06% | 43.42% | 44.24% |
| **Dual-Gate Cascade** | 53.31% | 75.98% | 28.52% | 52.63% | 93.90% | 42.83% | 42.43% | 42.39% |

---

### Benchmark 5: Partition B vs. Partition D1 (External Known Shift vs. Pure Semantic Shift Unknowns)
$N_{\text{id}} = 5,350, N_{\text{ood}} = 4,776$ (Isolated Semantic Shift across external retail domains)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 67.82% | 70.18% | 61.62% | 33.04% | 87.56% | 22.17% | 42.77% | 51.99% |
| **Energy Baseline** | 76.04% | 79.91% | 71.92% | 21.96% | 74.90% | 13.42% | 41.50% | 56.87% |
| **ODIN Baseline** | 68.30% | 68.96% | 60.49% | 22.47% | 90.49% | 10.68% | 48.86% | 52.49% |
| **Mahalanobis** | 73.74% | 78.77% | 70.16% | 46.48% | 79.79% | 26.47% | 19.16% | 48.75% |
| **OpenMax** | 69.08% | 71.02% | 59.61% | 25.80% | 92.94% | 16.29% | 43.42% | 53.82% |
| **Dual-Gate Cascade** | 75.43% | 79.49% | 71.26% | 23.95% | 76.09% | 15.58% | 42.43% | 56.74% |

---

### Benchmark 6: Partition B vs. Partition D2 (External Known Shift vs. Combined Semantic & Treatment)
$N_{\text{id}} = 5,350, N_{\text{ood}} = 1,195$ (Combined semantic and treatment shift within external domain)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 75.74% | 93.53% | 40.75% | 22.26% | 78.41% | 19.16% | 42.77% | 56.52% |
| **Energy Baseline** | 84.97% | 96.38% | 51.46% | 6.86% | 63.60% | 4.94% | 41.50% | 61.82% |
| **ODIN Baseline** | 76.86% | 94.18% | 35.59% | 10.46% | 85.86% | 7.28% | 48.86% | 57.67% |
| **Mahalanobis** | 80.86% | 95.34% | 40.55% | 41.26% | 79.67% | 27.70% | 19.16% | 53.08% |
| **OpenMax** | 77.86% | 94.69% | 34.89% | 10.38% | 86.36% | 7.95% | 43.42% | 58.67% |
| **Dual-Gate Cascade** | 84.23% | 96.15% | 52.19% | 9.54% | 62.59% | 7.28% | 42.43% | 61.58% |

---

## 4. Deep Methodological Analysis: Confounded vs. Isolated Semantic Shift

A central contribution of this benchmark is dissecting the difference between **Benchmark 2 ($A \text{ vs } D1$)** and **Benchmark 5 ($B \text{ vs } D1$)**:

$$\text{Energy AUROC: } \quad A \text{ vs } D1 = 97.55\% \quad \longleftrightarrow \quad B \text{ vs } D1 = 76.04\% \quad (\Delta = -21.51 \text{ pp})$$
$$\text{Dual-Gate AUROC: } \quad A \text{ vs } D1 = 97.50\% \quad \longleftrightarrow \quad B \text{ vs } D1 = 75.43\% \quad (\Delta = -22.07 \text{ pp})$$

### Why Do These Two Benchmarks Differ?
1. **$A \text{ vs } D1$ Confounds Semantic and Domain Shift:**
   In $A \text{ vs } D1$, the ID samples ($A$) originate from the curated Kaggle laboratory dataset (uniform background, standard camera), whereas the OOD samples ($D1$) originate from external sources (FruitVision and Sultana). The neural network easily separates $A$ from $D1$ based on non-semantic covariate artifacts (background texture, sensor noise floor, color balance, compression signatures). This inflates the AUROC to near-perfection ($>97\%$).
2. **$B \text{ vs } D1$ Isolates Genuine Semantic Shift:**
   In $B \text{ vs } D1$, both the ID samples ($B$, known apples/bananas/oranges) and the majority of OOD samples ($D1$, unknown mangoes/grapes) originate from the **same external repository (FruitVision)**. By evaluating within the same retail market domain, camera sensor and environmental variations are held constant. This isolates true semantic discrimination. Under this fair test, open-set discrimination drops to $\approx 75\text{--}76\%$.

> [!IMPORTANT]
> Standard OOD literature routinely evaluates lab-curated ID data against external OOD datasets, reporting spuriously optimistic performance. AgriRoute's dual-anchor protocol ($A \text{ vs } D1$ vs. $B \text{ vs } D1$) rigorously exposes this dataset fingerprinting bias.

---

## 5. Statistical Validation: 95% Bootstrap Confidence Intervals

Confidence intervals were calculated via non-parametric stratified bootstrap ($B = 1,000$ iterations, random seed $42$, image-level resampling unit).

> [!NOTE]
> Because biological specimen independence cannot be established across multiple camera captures of the same fruit lots, these intervals are strictly conditional on the image-level exchangeability assumption.

### Table 4: Key Performance Metrics with 95% Confidence Intervals

| Benchmark Task | Detector | Full-Sample Point Estimate | Bootstrap Mean | 95% Confidence Interval | Methodological Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Macro-F1 (Partition A)** | Model B V4.1 | **96.87%** | 96.75% | [94.11%, 98.81%] | $N=227$; High precision in-distribution |
| **Macro-F1 (Partition B)** | Model B V4.1 | **67.28%** | 67.28% | [66.12%, 68.39%] | $N=5,350$; Statistically locked domain drop |
| **AUROC: A vs C** | MSP | **90.63%** | 90.61% | [87.91%, 93.24%] | Preservative shift vs. lab baseline |
| **AUROC: A vs C** | Energy | **84.09%** | 84.04% | [81.81%, 86.34%] | Log-sum-exp baseline |
| **AUROC: A vs C** | Dual-Gate | **85.35%** | 85.37% | [83.29%, 87.57%] | Linear margin proxy |
| **AUROC: A vs D1** | Energy | **97.55%** | 97.56% | [96.59%, 98.37%] | Confounded semantic shift |
| **AUROC: A vs D1** | Dual-Gate | **97.50%** | 97.49% | [96.64%, 98.27%] | Confounded semantic shift |
| **AUROC: B vs C** | Energy | **52.57%** | 52.52% | [50.97%, 54.06%] | Near random guess under retail shift |
| **AUROC: B vs C** | Dual-Gate | **53.31%** | 53.29% | [51.88%, 54.76%] | Near random guess under retail shift |
| **AUROC: B vs D1** | Energy | **76.04%** | 76.03% | [75.16%, 76.90%] | Isolated semantic shift |
| **AUROC: B vs D1** | Dual-Gate | **75.43%** | 75.45% | [74.53%, 76.31%] | Isolated semantic shift |
| **UFAR-Fresh: A vs C** | Dual-Gate | **42.83%** | 42.85% | [40.69%, 44.97%] | Critical food-safety false acceptance |
| **UFAR-Fresh: B vs D1**| Dual-Gate | **15.58%** | 15.59% | [14.59%, 16.60%] | Unseen fruits falsely accepted as Fresh |

---

## 6. Sensitivity Analysis Across Data Integrity Tiers

Sensitivity analysis was executed across all three data integrity tiers defined in Stage 4.0.3:
1. **Primary Cohort ($N = 13,465$):** Full cleaned evaluation manifest.
2. **Tier 1 ($N = 13,409$):** Excludes 56 images with cross-partition perceptual hash collisions.
3. **Tier 2 ($N = 13,382$):** Excludes 83 images with cross-partition and intra-partition multi-label pHash collisions.

### Table 5: Maximum Observed Variation Across All 108 Sensitivity Rows

$$\Delta_{\max} = \max_{\text{Tiers}} (\text{Metric}) - \min_{\text{Tiers}} (\text{Metric})$$

| Metric Evaluated | Maximum Shift ($\Delta_{\max}$) | Bound in Percentage Points | Methodological Finding |
| :--- | :---: | :---: | :--- |
| **AUPR-OUT** | **0.70 pp** | $\le 0.70$ pp | Most sensitive metric; bounded $< 1.0$ pp |
| **Empirical UFAR ($\tau_{95}$)** | **0.53 pp** | $\le 0.53$ pp | Highly stable operating false alarm rate |
| **UFAR-Fresh ($\tau_{95}$)** | **0.30 pp** | $\le 0.30$ pp | Resilient safety metric across tiers |
| **AUPR-IN** | **0.23 pp** | $\le 0.23$ pp | Insensitive to duplicate pruning |
| **AUROC** | **0.19 pp** | $\le 0.19$ pp | Rank-order stability preserved across all pairs |
| **OSCR** | **0.14 pp** | $\le 0.14$ pp | Open-set classification rate virtually identical |
| **ID Rejection Rate (KRR)** | **0.06 pp** | $\le 0.06$ pp | Locked operational coverage invariant |

**Scientific Conclusion on Sensitivity:**
All evaluated metrics exhibit extreme stability across tiers ($\Delta_{\max} \le 0.70$ percentage points across all 108 rows). Data cleaning did not induce cherry-picking or metric instability.

---

## 7. Compliance with Scientific Integrity Rules

1. **Strictly Observational Terminology:**
   - Formalin-treated specimens are designated as *"dataset-labelled formalin-treatment condition"*.
   - UFAR-Fresh is formally defined as *"the proportion of OOD images accepted by the detector and assigned a Fresh model class"*.
   - No claim is made that RGB images detect formaldehyde or chemical preservatives.
2. **No Data Fabrication:**
   - 100% of reported values trace to `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`.
   - Six-class logits and probabilities were held in transient execution RAM during inference and not serialized to disk; this storage limitation is transparently documented in the reproducibility audit.

