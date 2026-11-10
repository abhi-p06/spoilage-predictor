# STAGE 4.1.2 — REVISED FAILURE AND DOMAIN SHIFT DIAGNOSTIC REPORT

**Document Type:** Forensic Diagnostic Audit  
**Auditor:** Independent Research Methodologist & Scientific Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** RECONCILED WITH SOURCE-STRATIFIED EVIDENCE & CLAIMS AUDIT  

---

## 1. Executive Summary

This report delivers a forensic failure diagnosis of the frozen Model B V4.1 vision backbone across $N = 13,465$ local benchmark images.

Building upon the Stage 4.1.1 baseline, this Stage 4.1.2 revision incorporates **source-stratified failure decomposition** across FruitVision and Sultana repositories, enforces strict observational language, and explicitly separates physical optical constraints from speculative biochemical mechanisms.

---

## 2. Partition B External Known Shift: Source-Stratified Diagnostic Decomposition

Partition B evaluates known species (Apple, Banana, Orange) under external retail environments across **5,350 total images** sourced from two upstream repositories: **FruitVision** ($N = 4,157$) and **Sultana** ($N = 1,193$).

While aggregate accuracy across the pooled 5,350 images is **$68.36\%$** ($67.28\%$ Macro-F1), source stratification reveals striking repository-level divergences:

### Table 1: Source-Stratified Class-Wise Performance on Partition B

| Class Name | Pooled Partition B ($N=5,350$) | FruitVision B ($N=4,157$) | Sultana B ($N=1,193$) | Primary Diagnostic Failure Mode |
| :--- | :---: | :---: | :---: | :--- |
| **Fresh Apple** | **32.12%** (310/965) | **22.75%** (174/765) | **68.00%** (136/200) | Extreme false-rot misclassification on FruitVision |
| **Rotten Apple** | **37.35%** (310/830) | **34.29%** (216/630) | **47.00%** (94/200) | Cross-species misclassification into Rotten Orange |
| **Fresh Banana** | **77.64%** (736/948) | **79.28%** (593/748) | **71.50%** (143/200) | Mild over-prediction of senescence |
| **Rotten Banana** | **99.40%** (826/831) | **99.68%** (629/631) | **98.50%** (197/200) | High fidelity; invariant dark lesion patterns |
| **Fresh Orange** | **87.53%** (828/946) | **96.95%** (730/753) | **50.78%** (98/193) | Collapse on Sultana desaturated citrus specimens |
| **Rotten Orange** | **77.95%** (647/830) | **84.44%** (532/630) | **57.50%** (115/200) | Underestimation of rot on Sultana oranges |
| **Overall Partition B** | **68.36%** (3,657/5,350) | **69.14%** (2,874/4,157) | **65.63%** (783/1,193) | Domain drop: $-28.56$ pp vs. Primary Partition A |

---

## 3. Forensic Diagnosis of Visual Failure Modes

### 3.1 The Apple Anomaly: Surface Texture and Illumination Interactions
- **Visual Evidence in FruitVision ($22.75\%$ Fresh Apple Recall):**
  Out of 765 fresh apples in FruitVision B, $356$ ($46.54\%$) were misclassified as Rotten Apple and $229$ ($29.93\%$) as Rotten Orange. Observed visual features in these images include pronounced corky lenticels, natural varietal russeting, and sharp specular glare caused by overhead retail lighting. In diffuse studio training data (Kaggle), apples exhibited smooth, uniform pericarps. The convolutional feature extractors interpret high-contrast specular reflections and localized russeting as soft-rot necrotic lesions.
- **Visual Evidence in Sultana ($68.00\%$ Fresh Apple Recall):**
  In Sultana B, fresh apple recall is substantially higher ($68.00\%$). Sultana images feature diffuse ambient illumination and more uniform apple pericarps, substantially reducing false-rot triggers.

### 3.2 The Orange Anomaly: Chromatic Divergence between Repositories
- **FruitVision Robustness ($96.95\%$ Fresh Orange Recall):**
  FruitVision oranges exhibit high color saturation and classic citrus flavedo texture, which aligns well with the training distribution.
- **Sultana Drop ($50.78\%$ Fresh Orange Recall):**
  In Sultana B, fresh orange recall drops to $50.78\%$, with $38$ images misclassified as Fresh Apple and $42$ as Rotten Orange. Visual inspection indicates lower color saturation, pale yellow-greenish peel tones, and different regional citrus cultivars that overlap with yellow apple pericarps.

### 3.3 The Banana Invariance: Contrastive Melanogenesis
Across both repositories, Rotten Banana achieved near-flawless recall ($99.68\%$ in FruitVision, $98.50\%$ in Sultana). Senescent bananas exhibit stark, high-contrast dark patches (enzymatic melanogenesis) against a yellow background. These high-frequency spatial gradients are robust to lighting and sensor domain shifts.

---

## 4. Preservative Condition Shift Failure Mode (Partition C)

Partition C evaluates 1,917 images from FruitVision labelled as subjected to chemical treatment (formalin immersion).

### 4.1 Physical and Optical Constraints of RGB Imaging
- **Chemical Nature:** Formalin is an aqueous solution of formaldehyde ($CH_2O$) that preserves structural cellular integrity by cross-linking proteins, inhibiting microbial decay.
- **Optical Invisibility:** Formalin immersion preserves the visual color, geometry, and surface texture of fresh fruit. It does not alter optical reflectance in the visible light spectrum ($400\text{--}700\text{ nm}$).
- **Diagnostic Outcome:** Without spectroscopic or biochemical data, RGB models evaluate preserved fruits as visually fresh.

### Table 2: Treatment Condition Shift Rejection Metrics (Cohort B: FruitVision B vs. FruitVision C)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,917$ (Treatment-Labelled Knowns)

| Detector | AUROC | Operational UFAR ($\tau_{95}$) | Operational UFAR-Fresh ($\tau_{95}$) | Percentage of Accepted Treated Fruit Labelled Fresh |
| :--- | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 58.77% | 50.29% | **37.09%** | 73.76% |
| **Energy Baseline** | 53.13% | 53.94% | **44.03%** | 81.63% |
| **ODIN Baseline** | 56.73% | 47.84% | **36.83%** | 76.99% |
| **Dual-Gate Cascade** | 53.96% | 52.63% | **42.83%** | 81.38% |

> [!CAUTION]
> **Food Safety Implication:** Under the Dual-Gate Cascade, **$42.83\%$ (821 images)** of formalin-treated fruits are accepted by the vision gate and routed as **Fresh**. RGB vision **cannot** serve as a standalone barrier against chemical adulterants. This finding provides empirical motivation for integrating multimodal volatile organic compound (VOC) gas sensors into holistic post-harvest systems.

---

## 5. Source-Stratified Semantic Shift: Morphological Mimicry

Comparing within-repository semantic shift across Cohort A (FruitVision) and Cohort D (Sultana):

### Table 3: Semantic Shift Across Independent External Cohorts

| Stratified Cohort | Unseen Species Evaluated | Energy AUROC | Dual-Gate AUROC | Dual-Gate UFAR ($\tau_{95}$) | Dual-Gate UFAR-Fresh ($\tau_{95}$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Cohort A (Within-FV)** | Grape, Mango | **81.57%** | **80.93%** | **16.07%** | **10.48%** |
| **Cohort D (Within-Sultana)**| Grape, Guava, Jujube, Pomegranate, Strawberry | **67.52%** | **66.68%** | **34.90%** | **22.65%** |

### Morphological Analysis:
1. **FruitVision Cohort A ($81.57\%$ AUROC):**
   Mangoes possess an asymmetric oblong morphology, and grapes exhibit clustered spherical geometries with distinct branch pedicels. These structural shapes differ markedly from apples, bananas, and oranges, enabling effective rejection.
2. **Sultana Cohort D ($67.52\%$ AUROC):**
   Sultana's unseen cohort includes **Guava** and **Jujube**. These species are spherical, green, and smooth-skinned, visually and structurally mimicking green apples and immature oranges. Consequently, the detector falsely accepts $34.90\%$ of unseen Sultana fruits, with $22.65\%$ accepted and misclassified as Fresh.

---

## 6. Retrospective Selective Classification (Diagnostic Coverage-Risk)

Although domain shift degrades full-cohort accuracy on Partition B to $68.36\%$, model confidence scores enable effective selective abstention:

### Table 4: Retrospective Coverage-Risk on Partition B ($N = 5,350$)

| Target Coverage | MSP Risk | Energy Risk | ODIN Risk | Mahalanobis Risk | OpenMax Risk | Dual-Gate Risk (Proxy) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10.0%** | **1.31%** | 3.18% | 2.43% | 28.04% | **1.50%** | 2.80% |
| **20.0%** | **4.86%** | 5.33% | 5.33% | 26.82% | **2.80%** | 4.67% |
| **30.0%** | 7.48% | 7.60% | 7.85% | 28.85% | **5.23%** | 6.92% |
| **50.0%** | 13.79% | 12.93% | 14.02% | 32.71% | **12.19%** | 12.37% |
| **70.0%** | 21.79% | 20.45% | 20.88% | 36.05% | **20.21%** | 20.13% |
| **100.0%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** |

*Methodological Distinction:* This coverage-risk tradeoff represents a **retrospective diagnostic upper bound**. It confirms that detector confidence scores correlate with diagnostic correctness, permitting operational dispatch systems to abstain on low-confidence images and route them to manual inspection stations.

---

*Delivered as part of Stage 4.1.2. Reconciled metrics available in `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`.*

