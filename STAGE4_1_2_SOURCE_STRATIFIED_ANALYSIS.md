# STAGE 4.1.2 — SOURCE-STRATIFIED OPEN-SET BENCHMARK ANALYSIS

**Document Type:** Methodological Research Deliverable  
**Auditor:** Independent Research Methodologist & Scientific Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** COMPLETE — RECONCILED AGAINST AUTHORITATIVE MANIFEST  

---

## 1. Executive Summary & Research Rationale

In Stage 4.1.1, the evaluation of external known species (Partition B, $N = 5,350$ images) and unseen species (Partition D1, $N = 4,776$ images) pooled records across two independent repositories: **FruitVision** and **Sultana**. 

While pooling provided a broad external test suite, it introduced cross-repository confounding: differences in camera sensors, studio versus retail illumination, and background environments between FruitVision and Sultana could act as spurious discriminators.

To achieve rigorous scientific isolation, this Stage 4.1.2 report executes a **source-stratified decomposition** across the existing 13,465 image-level prediction records. We evaluate four strictly within-repository cohorts:
- **Cohort A:** FruitVision Known Species ($N = 4,157$) vs. FruitVision Unseen Species ($N = 2,776$)
- **Cohort B:** FruitVision Known Species ($N = 4,157$) vs. FruitVision Preserved Known Species ($N = 1,917$)
- **Cohort C:** FruitVision Known Species ($N = 4,157$) vs. FruitVision Combined-Shift Unknowns ($N = 1,195$)
- **Cohort D:** Sultana Known Species ($N = 1,193$) vs. Sultana Unseen Species ($N = 2,000$)

All metrics are computed directly from the frozen prediction manifest (`STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`) and are synchronized with [`STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv).

---

## 2. Source-Stratified Cohort Provenance and Image Censuses

### Table 1: Source-Stratified Cohort Decomposition

| Cohort Identifier | ID Anchor Source ($N_{\text{id}}$ Images) | OOD Evaluation Source ($N_{\text{ood}}$ Images) | Shift Mechanism Evaluated |
| :--- | :--- | :--- | :--- |
| **Cohort A** | **FruitVision B** ($N = 4,157$)<br>Apple: 1,395, Banana: 1,379, Orange: 1,383 | **FruitVision D1** ($N = 2,776$)<br>Grape: 1,383, Mango: 1,393 | Within-repository pure semantic shift (natural ambient conditions) |
| **Cohort B** | **FruitVision B** ($N = 4,157$)<br>Apple: 1,395, Banana: 1,379, Orange: 1,383 | **FruitVision C** ($N = 1,917$)<br>Apple: 641, Banana: 660, Orange: 616 | Within-repository preservative condition shift (formalin treatment) |
| **Cohort C** | **FruitVision B** ($N = 4,157$)<br>Apple: 1,395, Banana: 1,379, Orange: 1,383 | **FruitVision D2** ($N = 1,195$)<br>Grape: 587, Mango: 608 | Within-repository combined semantic & treatment shift |
| **Cohort D** | **Sultana B** ($N = 1,193$)<br>Apple: 400, Banana: 400, Orange: 393 | **Sultana D1** ($N = 2,000$)<br>Grape: 400, Guava: 400, Jujube: 400, Pomegranate: 400, Strawberry: 400 | Within-repository semantic shift across diverse tropical/sub-tropical cultivars |

> [!WARNING]
> **Methodological Disclaimer:** Evaluating within a shared repository reduces macro-level dataset discrepancy (e.g., image resolution and regional sourcing). However, it does **not** guarantee identical camera hardware, focal distance, or illumination across different collection batches. Image records must not be described as independent physical specimens.

---

## 3. Closed-Set Baseline Performance: FruitVision B vs. Sultana B

Before evaluating open-set rejection, we examine closed-set classification accuracy stratified by source:

### Table 2: Source-Stratified Closed-Set Performance on Known Classes

| Metric / Class | Pooled Partition B ($N=5,350$) | FruitVision B ($N=4,157$) | Sultana B ($N=1,193$) | Source Delta ($\Delta_{\text{FV} - \text{Sult}}$) |
| :--- | :---: | :---: | :---: | :---: |
| **Top-1 Accuracy** | **68.36%** | **69.14%** | **65.63%** | $+3.51$ pp |
| **Macro-Averaged F1** | **67.28%** | **66.75%** | **65.77%** | $+0.98$ pp |
| Fresh Apple Recall | 32.12% | 22.75% ($n=765$) | 68.00% ($n=200$) | $-45.25$ pp |
| Rotten Apple Recall | 37.35% | 34.29% ($n=630$) | 47.00% ($n=200$) | $-12.71$ pp |
| Fresh Banana Recall | 77.64% | 79.28% ($n=748$) | 71.50% ($n=200$) | $+7.78$ pp |
| Rotten Banana Recall | 99.40% | 99.68% ($n=631$) | 98.50% ($n=200$) | $+1.18$ pp |
| Fresh Orange Recall | 87.53% | 96.95% ($n=753$) | 50.78% ($n=193$) | $+46.17$ pp |
| Rotten Orange Recall | 77.95% | 84.44% ($n=630$) | 57.50% ($n=200$) | $+26.94$ pp |

### Methodological Observations:
- **FruitVision Asymmetry:** In FruitVision B, the model achieves near-perfect recall on Fresh Orange ($96.95\%$) and Rotten Banana ($99.68\%$), but collapses on Fresh Apple ($22.75\%$). Observed visual features in FruitVision apples include strong specular highlights and russeting, which the network misclassifies as rotten lesions.
- **Sultana Asymmetry:** In Sultana B, Fresh Apple recall is significantly higher ($68.00\%$), but Fresh Orange recall drops to $50.78\%$ due to subdued color saturation and different citrus cultivars.

---

## 4. Source-Stratified Open-Set Results

All detector scores are oriented such that higher values denote in-distribution (ID) likelihood. 
- **Operational UFAR ($\tau_{95}$):** The empirical false alarm rate evaluated at the locked validation threshold $\tau_{95}^{\text{val}}$.
- **Retrospective FPR@95% TPR:** The false alarm rate when the operating threshold is chosen post-hoc to accept exactly 95.0% of that specific ID cohort.
- **Dual-Gate Note:** Continuous AUROC, AUPR, and OSCR are computed from the linear margin proxy $S_{\text{proxy}} = (S_E - \tau_E) + (S_M - \tau_M)$, while operational metrics reflect the discrete cascade decision rule.

### Table 3: Cohort A — FruitVision B vs. FruitVision D1 (Within-FV Semantic Shift)
$N_{\text{id}} = 4,157$ (Known: Apple, Banana, Orange) vs. $N_{\text{ood}} = 2,776$ (Unseen: Grape, Mango)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 72.42% | 82.04% | 59.91% | 27.23% | 82.74% | 18.84% | 41.88% | 55.92% |
| **Energy Baseline** | **81.57%** | **88.36%** | **72.19%** | **13.18%** | **68.84%** | **7.64%** | 41.42% | **61.28%** |
| **ODIN Baseline** | 72.30% | 81.58% | 57.46% | 17.94% | 87.43% | 7.20% | 47.27% | 56.32% |
| **Mahalanobis** | 81.41% | 87.65% | 68.83% | 32.67% | 79.00% | 18.62% | 20.01% | 54.35% |
| **OpenMax** | 72.46% | 83.85% | 55.91% | 18.80% | 91.28% | 11.96% | 43.32% | 57.26% |
| **Dual-Gate Cascade** | **80.93%** | **87.98%** | **71.54%** | **16.07%** | **69.27%** | **10.48%** | 41.98% | **61.11%** |

*Findings:* When semantic shift is evaluated entirely within FruitVision, Energy and Dual-Gate achieve strong discrimination ($\text{AUROC} > 80.9\%$). Energy rejects **$86.82\%$** of unseen fruits (UFAR = $13.18\%$) under the locked operational threshold, with only $7.64\%$ falsely accepted as Fresh.

---

### Table 4: Cohort B — FruitVision B vs. FruitVision C (Within-FV Condition Shift: Formalin Preservative)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,917$ (Treatment-Labelled Knowns)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 58.77% | 78.59% | 36.73% | 50.29% | 92.85% | 37.09% | 41.88% | 47.62% |
| **Energy Baseline** | 53.13% | 71.25% | 33.41% | 53.94% | 94.42% | 44.03% | 41.42% | 43.45% |
| **ODIN Baseline** | 56.73% | 76.89% | 36.60% | 47.84% | 91.13% | 36.83% | 47.27% | 46.35% |
| **Mahalanobis** | 47.91% | 67.53% | 29.60% | 80.70% | 98.07% | 50.50% | 20.01% | 32.67% |
| **OpenMax** | 55.35% | 75.43% | 33.60% | 50.60% | 95.20% | 40.06% | 43.32% | 45.77% |
| **Dual-Gate Cascade** | 53.96% | 72.03% | 33.99% | 52.63% | 94.16% | 42.83% | 41.98% | 44.23% |

*Findings:* All detectors exhibit near-random AUROC ($47.9\%\text{--}58.8\%$). Formalin preservation maintains surface visual characteristics, causing the vision model to accept $>50\%$ of chemically preserved fruit, with **$42.83\%$** accepted and classified as Fresh under Dual-Gate. This establishes the strict physical boundary of RGB computer vision for food-safety monitoring.

---

### Table 5: Cohort C — FruitVision B vs. FruitVision D2 (Within-FV Combined Shift)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,195$ (Preserved Grape & Mango)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 76.47% | 92.18% | 47.85% | 22.26% | 76.40% | 19.16% | 41.88% | 58.01% |
| **Energy Baseline** | **84.72%** | **95.41%** | **56.71%** | **6.86%** | **64.94%** | **4.94%** | 41.42% | **62.92%** |
| **ODIN Baseline** | 78.11% | 93.17% | 43.32% | 10.46% | 83.85% | 7.28% | 47.27% | 59.69% |
| **Mahalanobis** | 80.08% | 93.82% | 47.10% | 41.26% | 78.49% | 27.70% | 20.01% | 53.42% |
| **OpenMax** | 77.22% | 93.25% | 39.71% | 10.38% | 88.12% | 7.95% | 43.32% | 59.62% |
| **Dual-Gate Cascade** | **84.16%** | **95.18%** | **57.63%** | **9.54%** | **63.18%** | **7.28%** | 41.98% | **62.74%** |

*Findings:* When semantic shift is combined with chemical preservation, semantic features dominate. Energy achieves $84.72\%$ AUROC and rejects $93.14\%$ of samples (UFAR = $6.86\%$).

---

### Table 6: Cohort D — Sultana B vs. Sultana D1 (Within-Sultana Semantic Shift)
$N_{\text{id}} = 1,193$ (Known: Apple, Banana, Orange) vs. $N_{\text{ood}} = 2,000$ (Unseen: Grape, Guava, Jujube, Pomegranate, Strawberry)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 59.77% | 53.25% | 67.96% | 41.10% | 94.30% | 26.80% | 45.85% | 43.11% |
| **Energy Baseline** | **67.52%** | **57.10%** | **76.35%** | **34.15%** | **83.50%** | **21.45%** | 41.74% | **46.62%** |
| **ODIN Baseline** | 60.02% | 52.76% | 67.88% | 28.75% | 94.25% | 15.50% | 54.40% | 42.62% |
| **Mahalanobis** | **68.15%** | **59.17%** | **77.07%** | 65.65% | 81.20% | 37.35% | 16.18% | 42.01% |
| **OpenMax** | 64.38% | 57.23% | 70.56% | 35.50% | 94.75% | 22.30% | 43.76% | 45.59% |
| **Dual-Gate Cascade** | 66.68% | 56.54% | 75.47% | 34.90% | 84.60% | 22.65% | 44.01% | 46.54% |

*Findings:* Semantic separation within Sultana is significantly more difficult than within FruitVision ($\text{Energy AUROC } = 67.52\%$ vs. $81.57\%$). Inspection of Sultana D1 reveals that **Guava** and **Jujube** are round, green pomes/drupes that share high visual and structural similarity with green apples and unripe oranges, causing elevated false alarm rates ($34.15\%$ UFAR under Energy).

---

## 5. Synthesis: Cross-Source Comparison of Semantic Shift

Comparing Cohort A (Within-FruitVision) and Cohort D (Within-Sultana) against the Pooled Benchmark:

$$\text{Within-FruitVision AUROC (Energy): } \mathbf{81.57\%}$$
$$\text{Pooled B-vs-D1 AUROC (Energy): } \mathbf{76.04\%}$$
$$\text{Within-Sultana AUROC (Energy): } \mathbf{67.52\%}$$

### Key Insights:
1. **Repository Heterogeneity Matters:** Pooling FruitVision and Sultana yielded an intermediate AUROC ($76.04\%$) that obscured the stark difference between FruitVision's distinctive species ($81.57\%$) and Sultana's visually confounding species ($67.52\%$).
2. **Morphological Mimicry Dominates:** The drop in Sultana performance is driven by morphological mimicry (guavas resembling apples) rather than camera artifacts.
3. **Dual-Gate Robustness:** Across both repositories, the Dual-Gate Cascade consistently tracks Energy within $\le 0.84$ pp of AUROC while enforcing a strict two-stage operational safety boundary.

---

*Delivered as part of Stage 4.1.2. Reconciled data available in `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`.*

