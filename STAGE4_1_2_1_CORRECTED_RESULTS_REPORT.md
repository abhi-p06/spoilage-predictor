# STAGE 4.1.2.1 — CORRECTED BENCHMARK RESULTS AND STATISTICAL AUDIT REPORT

**Document Type:** Primary Scientific Benchmark Deliverable  
**Author:** Independent Research Methodologist & Scientific Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** FULLY RECONCILED — ALL STAGE 4.1.2.1 CORRECTIONS APPLIED  

---

## 1. Executive Summary & Benchmark Image Census

This report establishes the finalized, mathematically reconciled empirical results of the frozen Model B V4.1 vision backbone across $N = 13,465$ local benchmark images evaluated under the Stage 4.0.3 external evaluation protocol.

Every numeric value in this report is calculated directly from `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` and is fully concordant with:
1. `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv` (60 rows)
2. `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv` (72 rows)
3. `STAGE4_1_2_1_FINAL_CLAIMS_LEDGER.csv` (16 verified claims)
4. `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` (64 rows)

### Table 1: Final Benchmark Image Census and Upstream Provenance

| Partition Code | Partition Designation | Upstream Source Repositories | Image Count ($N$) | Evaluation Function |
| :--- | :--- | :--- | :---: | :--- |
| **Partition A** | Primary In-Distribution (ID Test) | Primary Kaggle Archive | 227 | Benchmark closed-set baseline; Primary ID anchor |
| **Partition B** | External Known Shift | FruitVision ($N=4,157$) + Sultana ($N=1,193$) | 5,350 | External domain shift; Secondary ID anchor |
| **Partition C** | Treatment-Labelled Condition Shift | FruitVision (Preserved Knowns) | 1,917 | OOD Condition Shift (Chemical fixative treatment) |
| **Partition D1** | Unseen-Species External Cohort | FruitVision ($N=2,776$) + Sultana ($N=2,000$) | 4,776 | OOD Unseen Species (Natural ambient conditions) |
| **Partition D2** | Combined Shift Unknowns | FruitVision (Preserved Unseen Species) | 1,195 | OOD Combined Shift (Preserved unknown species) |
| **Total Cohort**| **Complete Evaluation Benchmark** | **All Local Partitions** | **13,465** | **Fully Audited Primary Test Suite** |

> [!NOTE]
> **Image Count vs. Specimen Count:** Records are designated as **Image Counts**. Image records cannot be assumed to represent statistically independent biological units. All bootstrap confidence intervals are conditional on image-level resampling exchangeability.

**Model Checkpoint Integrity:**
- Checkpoint Path: `MODEL_B_V4_1_CHECKPOINT.keras`
- SHA-256: `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` (Verified Frozen)
- Regression Suite: 8 of 8 passed (`pytest tests/test_reproducibility_v4_1.py`)

---

## 2. Closed-Set Classification Performance (Partitions A & B)

Closed-set evaluation measures the model's accuracy on known classes (Apple, Banana, Orange $\times$ Fresh, Rotten) under laboratory conditions (Partition A) versus external retail conditions (Partition B).

### Table 2: Reconciled Closed-Set Performance Comparison

$$\text{Balanced Accuracy} = \frac{1}{6} \sum_{c=0}^5 \text{Recall}_c$$

| Metric | Partition A (ID Test, $N=227$) | Partition B (Pooled External, $N=5,350$) | FruitVision B ($N=4,157$) | Sultana B ($N=1,193$) |
| :--- | :---: | :---: | :---: | :---: |
| **Top-1 Accuracy** | **96.92%** | **68.36%** | **69.14%** | **65.63%** |
| **Macro-Averaged F1** | **96.87%** [94.11%, 98.68%] | **67.28%** [66.12%, 68.32%] | **66.75%** [65.34%, 68.01%] | **65.77%** [63.29%, 68.13%] |
| **Balanced Accuracy** | **97.09%** [94.57%, 98.98%] | **68.66%** [67.43%, 69.69%] | **69.56%** [68.30%, 70.58%] | **65.55%** [63.02%, 67.99%] |

### Table 3: Reconciled Class-Wise Performance on Partition B ($N = 5,350$)

| Class Name | Ground Truth ($N$) | Correct ($n$) | Class Accuracy (%) | Primary Misclassification Mode |
| :--- | :---: | :---: | :---: | :--- |
| **Fresh Apple** | 965 | 310 | **32.12%** | Rotten Apple ($40.73\%$), Rotten Orange ($26.42\%$) |
| **Rotten Apple** | 830 | 310 | **37.35%** | Rotten Orange ($43.49\%$), Fresh Apple ($18.92\%$) |
| **Fresh Banana** | 948 | 736 | **77.64%** | Rotten Banana ($21.84\%$) |
| **Rotten Banana** | 831 | 826 | **99.40%** | Fresh Banana ($0.36\%$) |
| **Fresh Orange** | 946 | 828 | **87.53%** | Rotten Orange ($9.83\%$), Fresh Apple ($0.95\%$) |
| **Rotten Orange** | 830 | 647 | **77.95%** | Fresh Orange ($12.77\%$), Rotten Apple ($8.43\%$) |
| **Species: Apple** | 1,795 | 620 | **34.54%** | Confusion between fresh/rotten and with orange |
| **Species: Banana** | 1,779 | 1,562 | **87.80%** | High fidelity; asymmetric bias toward rotten |
| **Species: Orange** | 1,776 | 1,475 | **83.05%** | Robust recognition; slight decay underestimation |
| **Total Cohort** | **5,350** | **3,657** | **68.36%** | **Overall Domain Degradation: $-28.56$ pp** |

---

## 3. Source-Stratified Open-Set Detection Benchmarks

Evaluating strictly within shared repositories eliminates cross-repository macro-confounding:

### 3.1 Cohort A: FruitVision B vs. FruitVision D1 (Within-FV Semantic Shift)
$N_{\text{id}} = 4,157$ (Known: Apple, Banana, Orange) vs. $N_{\text{ood}} = 2,776$ (Unseen: Grape, Mango)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 72.42% | 82.04% | 59.91% | 27.23% | 82.74% | 18.84% | 41.88% | 55.92% |
| **Energy Baseline** | **81.57%** | **88.36%** | **72.19%** | **13.18%** | **68.84%** | **7.64%** | 41.42% | **61.28%** |
| **ODIN Baseline** | 72.30% | 81.58% | 57.46% | 17.94% | 87.43% | 7.20% | 47.27% | 56.32% |
| **Mahalanobis** | 81.41% | 87.65% | 68.83% | 32.67% | 79.00% | 18.62% | 20.01% | 54.35% |
| **OpenMax** | 72.46% | 83.85% | 55.91% | 18.80% | 91.28% | 11.96% | 43.32% | 57.26% |
| **Dual-Gate Cascade** | **80.93%** | **87.98%** | **71.54%** | **16.07%** | **69.27%** | **10.48%** | 41.98% | **61.11%** |

*Methodological Note:* Dual-Gate AUROC (80.93%) is computed via the continuous linear margin proxy $S_{\text{proxy}} = (S_E - \tau_E) + (S_M - \tau_M)$ and is classified as an exploratory metric.

---

### 3.2 Cohort B: FruitVision B vs. FruitVision C (Within-FV Treatment Condition Shift)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,917$ (Treatment-Labelled Knowns)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 58.77% | 78.59% | 36.73% | 50.29% | 92.85% | 37.09% | 41.88% | 47.62% |
| **Energy Baseline** | 53.13% | 71.25% | 33.41% | 53.94% | 94.42% | 44.03% | 41.42% | 43.45% |
| **ODIN Baseline** | 56.73% | 76.89% | 36.60% | 47.84% | 91.13% | 36.83% | 47.27% | 46.35% |
| **Mahalanobis** | 47.91% | 67.53% | 29.60% | 80.70% | 98.07% | 50.50% | 20.01% | 32.67% |
| **OpenMax** | 55.35% | 75.43% | 33.60% | 50.60% | 95.20% | 40.06% | 43.32% | 45.77% |
| **Dual-Gate Cascade** | 53.96% | 72.03% | 33.99% | 52.63% | 94.16% | 42.83% | 41.98% | 44.23% |

*Diagnostic Finding:* Under the locked validation threshold ($\tau_{95}$), **$821$ out of $1,917$ images ($42.83\%$)** of treatment-labelled fruits are accepted by Dual-Gate and assigned a Fresh model class. This demonstrates that in the evaluated dataset and model, RGB imagery alone does not reliably separate formalin-treated fruit from natural fresh fruit.

---

### 3.3 Cohort C: FruitVision B vs. FruitVision D2 (Within-FV Combined Shift)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,195$ (Preserved Grape & Mango)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 76.47% | 92.18% | 47.85% | 22.26% | 76.40% | 19.16% | 41.88% | 58.01% |
| **Energy Baseline** | **84.72%** | **95.41%** | **56.71%** | **6.86%** | **64.94%** | **4.94%** | 41.42% | **62.92%** |
| **ODIN Baseline** | 78.11% | 93.17% | 43.32% | 10.46% | 83.85% | 7.28% | 47.27% | 59.69% |
| **Mahalanobis** | 80.08% | 93.82% | 47.10% | 41.26% | 78.49% | 27.70% | 20.01% | 53.42% |
| **OpenMax** | 77.22% | 93.25% | 39.71% | 10.38% | 88.12% | 7.95% | 43.32% | 59.62% |
| **Dual-Gate Cascade** | **84.16%** | **95.18%** | **57.63%** | **9.54%** | **63.18%** | **7.28%** | 41.98% | **62.74%** |

---

### 3.4 Cohort D: Sultana B vs. Sultana D1 (Within-Sultana Semantic Shift)
$N_{\text{id}} = 1,193$ (Known: Apple, Banana, Orange) vs. $N_{\text{ood}} = 2,000$ (Unseen: Grape, Guava, Jujube, Pomegranate, Strawberry)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 59.77% | 53.25% | 67.96% | 41.10% | 94.30% | 26.80% | 45.85% | 43.11% |
| **Energy Baseline** | **67.52%** | **57.10%** | **76.35%** | **34.15%** | **83.50%** | **21.45%** | 41.74% | **46.62%** |
| **ODIN Baseline** | 60.02% | 52.76% | 67.88% | 28.75% | 94.25% | 15.50% | 54.40% | 42.62% |
| **Mahalanobis** | **68.15%** | **59.17%** | **77.07%** | 65.65% | 81.20% | 37.35% | 16.18% | 42.01% |
| **OpenMax** | 64.38% | 57.23% | 70.56% | 35.50% | 94.75% | 22.30% | 43.76% | 45.59% |
| **Dual-Gate Cascade** | 66.68% | 56.54% | 75.47% | 34.90% | 84.60% | 22.65% | 44.01% | 46.54% |

*Interpretive Hypothesis on Cohort D:* The reduced discrimination in Sultana D1 ($\text{Energy AUROC } = 67.52\%$ vs. $81.57\%$ in FruitVision) is hypothesized to stem from morphological resemblance: Guava and Jujube present spherical, green visual profiles that overlap with green apples and citrus fruits.

---

## 4. Source-Stratified Bootstrap Confidence Intervals (95% CI)

Stratified bootstrap resampling was executed with $B = 1,000$ replicates, random seed 42, stratified across known classes and OOD species/condition groups.

### Table 4: Key Source-Stratified 95% Confidence Intervals

| Cohort / Task | Detector | Point Estimate | Bootstrap Mean | 95% Confidence Interval | Methodological Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Cohort A AUROC** | Energy | **81.57%** | 81.58% | [80.73%, 82.38%] | Within-FV Semantic Shift |
| **Cohort A AUROC** | Dual-Gate | **80.93%** | 80.94% | [80.09%, 81.82%] | Exploratory linear margin proxy |
| **Cohort A UFAR** | Energy | **13.18%** | 13.19% | [12.00%, 14.34%] | Locked operational threshold tau95 |
| **Cohort A UFAR-Fresh** | Dual-Gate | **10.48%** | 10.49% | [9.44%, 11.53%] | Accepted OOD assigned Fresh class |
| **Cohort B AUROC** | Energy | **53.13%** | 53.10% | [51.58%, 54.58%] | Treatment Condition Shift |
| **Cohort B AUROC** | Dual-Gate | **53.96%** | 53.93% | [52.42%, 55.43%] | Exploratory linear margin proxy |
| **Cohort B UFAR-Fresh** | Dual-Gate | **42.83%** | 42.82% | [40.69%, 44.97%] | 821/1,917 accepted as Fresh |
| **Cohort D AUROC** | Energy | **67.52%** | 67.52% | [65.92%, 69.11%] | Within-Sultana Semantic Shift |
| **Cohort D AUROC** | Dual-Gate | **66.68%** | 66.67% | [65.04%, 68.32%] | Exploratory linear margin proxy |
| **Cohort D UFAR-Fresh** | Dual-Gate | **22.65%** | 22.65% | [20.95%, 24.40%] | Accepted OOD assigned Fresh class |
| **FruitVision B Top-1 Acc** | Model B V4.1 | **69.14%** | 69.13% | [68.08%, 70.17%] | Known classes ($N=4,157$) |
| **FruitVision B Bal-Acc** | Model B V4.1 | **69.56%** | 69.52% | [68.30%, 70.58%] | Mean recall across 6 classes |
| **Sultana B Top-1 Acc** | Model B V4.1 | **65.63%** | 65.63% | [63.03%, 68.15%] | Known classes ($N=1,193$) |
| **Sultana B Bal-Acc** | Model B V4.1 | **65.55%** | 65.55% | [63.02%, 67.99%] | Mean recall across 6 classes |

---

## 5. Source-Stratified pHash Sensitivity Analysis

We evaluated metrics across three sensitivity tiers defined by perceptual hash collisions:
- **Primary Cohort:** All images.
- **Tier 1:** Excludes 56 cross-partition pHash collision images.
- **Tier 2:** Additionally excludes 27 intra-partition multi-label collision images.

### Table 5: Maximum Metric Shifts Across pHash Sensitivity Tiers

| Metric Evaluated | Maximum Shift ($\Delta_{\max}$) | Bound Assessment |
| :--- | :---: | :--- |
| **AUPR-OUT** | **0.70 pp** | Exceeds $0.50$ pp threshold ($\Delta_{\max} = 0.70$ pp) |
| **Retrospective FPR@95** | **0.57 pp** | Exceeds $0.50$ pp threshold ($\Delta_{\max} = 0.57$ pp) |
| **Operational UFAR ($\tau_{95}$)** | **0.53 pp** | Exceeds $0.50$ pp threshold ($\Delta_{\max} = 0.53$ pp) |
| **Operational UFAR-Fresh ($\tau_{95}$)** | **0.30 pp** | Strictly bounded $\le 0.30$ pp |
| **AUROC** | **0.22 pp** | Strictly bounded $\le 0.22$ pp |
| **AUPR-IN** | **0.16 pp** | Strictly bounded $\le 0.16$ pp |
| **OSCR** | **0.15 pp** | Strictly bounded $\le 0.15$ pp |
| **Operational KRR ($\tau_{95}$)** | **0.09 pp** | Strictly bounded $\le 0.09$ pp |

> [!WARNING]
> **Audit Finding on Metric Stability:** While AUROC ($\le 0.22$ pp), AUPR-IN ($\le 0.16$ pp), UFAR-Fresh ($\le 0.30$ pp), KRR ($\le 0.09$ pp), and OSCR ($\le 0.15$ pp) remain strictly below 0.50 pp, **AUPR-OUT shifts by up to 0.70 pp, retrospective FPR@95 shifts by up to 0.57 pp, and operational UFAR shifts by up to 0.53 pp**. The manuscript must not claim universal stability below 0.5 pp across all metrics.

---

## 6. Retrospective Coverage-Risk Analysis (Selective Classification)

### Table 6: Retrospective Coverage-Risk on Partition B ($N = 5,350$)

| Target Coverage | MSP Risk | Energy Risk | ODIN Risk | Mahalanobis Risk | OpenMax Risk | Dual-Gate Risk (Proxy) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10.0%** | **1.31%** | 3.18% | 2.43% | 28.04% | **1.50%** | 2.80% |
| **20.0%** | **4.86%** | 5.33% | 5.33% | 26.82% | **2.80%** | 4.67% |
| **30.0%** | 7.48% | 7.60% | 7.85% | 28.85% | **5.23%** | 6.92% |
| **50.0%** | 13.79% | 12.93% | 14.02% | 32.71% | **12.19%** | 12.37% |
| **70.0%** | 21.79% | 20.45% | 20.88% | 36.05% | **20.21%** | 20.13% |
| **100.0%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** |

*Methodological Clarification:* This coverage-risk analysis is a **retrospective diagnostic upper bound** computed by ranking existing test scores. It does **not** represent prospective deployment guarantees, which must be governed by fixed validation-calibrated operating thresholds.

---

*Delivered as part of Stage 4.1.2.1. Reconciled metrics available in `STAGE4_1_2_1_FINAL_CLAIMS_LEDGER.csv`.*

