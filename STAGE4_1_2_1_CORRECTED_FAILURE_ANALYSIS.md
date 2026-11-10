# STAGE 4.1.2.1 — CORRECTED FAILURE AND ERROR DIAGNOSTIC REPORT

**Document Type:** Forensic Diagnostic Audit  
**Author:** Independent Research Methodologist & Scientific Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** FULLY RECONCILED — ALL CONFUSION COUNTS & GUARDRAILS APPLIED  

---

## 1. Executive Summary

This report establishes the finalized diagnostic error analysis of the frozen Model B V4.1 vision backbone across $N = 13,465$ local benchmark images evaluated under the Stage 4.0.3 external evaluation protocol.

Every confusion cell, support count, and percentage in this document has been verified by direct calculation from `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`. All older intermediate counts are formally superseded.

---

## 2. Partition B External Known Shift: Source-Stratified Diagnostic Decomposition

Partition B evaluates known species (Apple, Banana, Orange) under external retail environments across **5,350 total images** sourced from **FruitVision** ($N = 4,157$) and **Sultana** ($N = 1,193$).

### Table 1: Source-Stratified Diagnostic Performance on Partition B

$$\text{Balanced Accuracy} = \frac{1}{6} \sum_{c=0}^5 \text{Recall}_c$$

| Class / Species Group | Pooled Partition B ($N=5,350$) | FruitVision B ($N=4,157$) | Sultana B ($N=1,193$) | Primary Diagnostic Finding |
| :--- | :---: | :---: | :---: | :--- |
| **Fresh Apple** | **32.12%** (310/965) | **22.75%** (174/765) | **68.00%** (136/200) | Severe false-rot misclassification on FruitVision |
| **Rotten Apple** | **37.35%** (310/830) | **34.29%** (216/630) | **47.00%** (94/200) | Misclassification into Rotten Orange |
| **Fresh Banana** | **77.64%** (736/948) | **79.28%** (593/748) | **71.50%** (143/200) | Mild over-prediction of decay |
| **Rotten Banana** | **99.40%** (826/831) | **99.68%** (629/631) | **98.50%** (197/200) | High fidelity; invariant contrastive markings |
| **Fresh Orange** | **87.53%** (828/946) | **96.95%** (730/753) | **50.78%** (98/193) | Accuracy drop on Sultana desaturated oranges |
| **Rotten Orange** | **77.95%** (647/830) | **84.44%** (532/630) | **57.50%** (115/200) | Underestimation of rot on Sultana oranges |
| **Top-1 Accuracy** | **68.36%** (3,657/5,350) | **69.14%** (2,874/4,157) | **65.63%** (783/1,193) | Domain drop: $-28.56$ pp vs. Primary Partition A |
| **Balanced Accuracy** | **68.66%** | **69.56%** | **65.55%** | Mean recall across 6 classes |

---

## 3. Reconciled Confusion Breakdowns and Misclassification Counts

### 3.1 FruitVision Fresh Apple Confusion Breakdown (Support = 765)

Out of 765 Fresh Apple images in FruitVision B:
- **Correct Fresh Apple Predictions:** **174** ($22.75\%$)
- **Rotten Apple Predictions:** **345** ($45.10\%$)
- **Rotten Orange Predictions:** **242** ($31.63\%$)
- **Fresh Orange Predictions:** **2** ($0.26\%$)
- **Rotten Banana Predictions:** **2** ($0.26\%$)
- **Sum of Predictions:** $174 + 345 + 242 + 2 + 2 = \mathbf{765}$ ($100.00\%$)

**Observational Diagnosis:** 
In FruitVision B, $587$ out of $765$ fresh apples ($76.73\%$) are predicted as Rotten ($345$ Rotten Apple, $242$ Rotten Orange). Observed visual features in these images include pronounced lenticels, natural varietal russeting (rough corky patches), and localized specular highlights under commercial point-source lighting. We hypothesize that MobileNetV2's early convolutional filters correlate these high-contrast surface textures with necrotic decay lesions.

### 3.2 Sultana Fresh Orange Confusion Breakdown (Support = 193)

Out of 193 Fresh Orange images in Sultana B:
- **Correct Fresh Orange Predictions:** **98** ($50.78\%$)
- **Rotten Orange Predictions:** **71** ($36.79\%$)
- **Rotten Apple Predictions:** **15** ($7.77\%$)
- **Fresh Apple Predictions:** **9** ($4.66\%$)
- **Sum of Predictions:** $98 + 71 + 15 + 9 = \mathbf{193}$ ($100.00\%$)

**Observational Diagnosis:**
In Sultana B, $71$ fresh oranges ($36.79\%$) are predicted as Rotten Orange, and $24$ ($12.44\%$) are predicted as Apple ($15$ Rotten Apple, $9$ Fresh Apple). Visual inspection reveals lower color saturation, pale greenish-yellow peel coloration, and non-uniform surface shading in Sultana specimens, which overlap with yellow apple pericarps and aged citrus textures.

---

## 4. Treatment Condition Shift Diagnostic: Dataset-Labelled Formalin Condition

Partition C evaluates 1,917 images from FruitVision labelled as subjected to a chemical preservation treatment condition (formalin immersion).

### 4.1 Observational Scope and Limitations of the Vision Model
- **Evaluated Condition:** Specimens in Partition C are labelled as treated with formalin (an aqueous fixative that inhibits biological autolysis).
- **Observed Surface Characteristics:** In the evaluated dataset, treated specimens exhibit intact pericarps, preserved pigmentation, and absent macroscopic fungal decay.
- **Model Behavior:** Because the visual appearance of treated fruit closely matches fresh natural fruit, Model B V4.1 assigns high confidence to Fresh classes.

### Table 2: Treatment Condition Shift Rejection Metrics (Cohort B: FruitVision B vs. FruitVision C)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,917$ (Treatment-Labelled Knowns)

| Detector | AUROC | Operational UFAR ($\tau_{95}$) | Operational UFAR-Fresh ($\tau_{95}$) | Percentage of Accepted Treated Images Labelled Fresh |
| :--- | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 58.77% | 50.29% | **37.09%** | 73.76% |
| **Energy Baseline** | 53.13% | 53.94% | **44.03%** | 81.63% |
| **ODIN Baseline** | 56.73% | 47.84% | **36.83%** | 76.99% |
| **Dual-Gate Cascade** | 53.96% | 52.63% | **42.83%** | 81.38% |

> [!CAUTION]
> **Specific Empirical Finding:** Under the locked validation threshold ($\tau_{95}$), **$821$ out of $1,917$ images ($42.83\%$)** of treatment-labelled fruits are accepted by Dual-Gate and assigned a Fresh model class. 
> 
> **Scientific Limitation:** This result demonstrates that within the evaluated dataset and model architecture, standard broadband RGB imagery does not reliably distinguish formalin-treated fruit from natural fresh fruit. This finding provides an empirical rationale for integrating complementary non-optical sensors (such as volatile organic compound gas sensors) in post-harvest screening.

---

## 5. Source-Stratified Semantic Shift: Interpretive Hypotheses

Comparing within-source semantic shift between FruitVision (Cohort A) and Sultana (Cohort D):

### Table 3: Semantic Shift Across Independent External Cohorts

| Stratified Cohort | Unseen Species Evaluated | Energy AUROC | Dual-Gate AUROC (Proxy) | Dual-Gate UFAR ($\tau_{95}$) | Dual-Gate UFAR-Fresh ($\tau_{95}$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Cohort A (Within-FV)** | Grape, Mango | **81.57%** | **80.93%** | **16.07%** | **10.48%** |
| **Cohort D (Within-Sultana)**| Grape, Guava, Jujube, Pomegranate, Strawberry | **67.52%** | **66.68%** | **34.90%** | **22.65%** |

### Proposed Interpretive Hypotheses:
1. **FruitVision Cohort A Hypothesis:**
   In FruitVision D1, unseen species (Mango, Grape) possess distinct morphological outlines (oblong mango shapes and clustered grape berries) that differ clearly from the spherical geometry of apples and oranges.
2. **Sultana Cohort D Hypothesis:**
   In Sultana D1, the unseen cohort includes **Guava** and **Jujube**. We hypothesize that the reduced discrimination ($\text{Energy AUROC } = 67.52\%$) is driven by morphological resemblance: Guavas and Jujubes are spherical, green, and smooth-skinned, presenting visual profiles that overlap with green apples and immature citrus fruits.

---

## 6. Retrospective Coverage-Risk Analysis (Selective Classification)

### Table 4: Retrospective Coverage-Risk on Partition B ($N = 5,350$)

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

