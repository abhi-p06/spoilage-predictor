# STAGE 4.1.1 — REVISED FAILURE AND ERROR ANALYSIS

**Document Type:** Forensic Diagnostic Audit  
**Author:** Independent Scientific Benchmark Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** RECONCILED AGAINST 13,465 IMAGE-LEVEL PREDICTIONS  

---

## 1. Executive Overview

This report presents a forensic failure analysis of the frozen Model B V4.1 checkpoint (`MODEL_B_V4_1_CHECKPOINT.keras`, SHA-256: `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`) across the 13,465 local benchmark images evaluated in Stage 4.1.

Every metric, percentage, confusion cell, and error breakdown in this report has been verified by direct recalculation from `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`. All older unverified figures from previous preliminary reports are formally superseded.

---

## 2. Partition B External Known Shift: Class-Wise Accuracy Re-Computation

Partition B evaluates known species (Apple, Banana, Orange) under external retail and ambient environment shifts from the independent FruitVision repository ($N = 5,350$). 

Whereas the model achieves **$96.92\%$ top-1 accuracy** ($96.87\%$ Macro-F1) on Partition A (in-distribution test partition, $N = 227$), its accuracy collapses to **$68.36\%$** ($67.28\%$ Macro-F1) on Partition B.

### Table 1: Verified Class-Wise and Species-Wise Performance on Partition B ($N = 5,350$)

| Class / Species Group | Ground Truth Support ($N$) | Correct Predictions ($n$) | Class Accuracy (%) | Primary Misclassification Mode |
| :--- | :---: | :---: | :---: | :--- |
| **Fresh Apple** | 965 | 310 | **32.12%** | Rotten Apple (40.73%), Rotten Orange (26.42%) |
| **Rotten Apple** | 830 | 310 | **37.35%** | Rotten Orange (43.49%), Fresh Apple (18.92%) |
| **Fresh Banana** | 948 | 736 | **77.64%** | Rotten Banana (21.84%) |
| **Rotten Banana** | 831 | 826 | **99.40%** | Fresh Banana (0.36%) |
| **Fresh Orange** | 946 | 828 | **87.53%** | Rotten Orange (9.83%), Fresh Apple (0.95%) |
| **Rotten Orange** | 830 | 647 | **77.95%** | Fresh Orange (12.77%), Rotten Apple (8.43%) |
| **Aggregate: Apple** | 1,795 | 620 | **34.54%** | Severe confusion between fresh/rotten and with orange |
| **Aggregate: Banana** | 1,779 | 1,562 | **87.80%** | High fidelity; asymmetric bias toward rotten |
| **Aggregate: Orange** | 1,776 | 1,475 | **83.05%** | Robust recognition; slight decay underestimation |
| **Overall Partition B** | **5,350** | **3,657** | **68.36%** | **Overall Domain Degradation: $-28.56$ pp vs. Partition A** |

---

## 3. Complete Empirical Confusion Matrix (Partition B)

The cross-tabulation of true labels versus top-1 model predictions across all 5,350 Partition B samples reveals the precise pathways of diagnostic failure:

### Table 2: 6-Class Confusion Matrix on Partition B (Rows = Ground Truth, Columns = Predicted)

```
                       Predicted Class
True Class           0:FA    1:FB    2:FO    3:RA    4:RB    5:RO    Total    Class Recall
0: Fresh Apple        310       0       5     393       2     255      965          32.12%
1: Fresh Banana         0     736       0       3     207       2      948          77.64%
2: Fresh Orange         9       0     828      16       0      93      946          87.53%
3: Rotten Apple       157       0       0     310       2     361      830          37.35%
4: Rotten Banana        0       3       0       0     826       2      831          99.40%
5: Rotten Orange        7       0     106      70       0     647      830          77.95%
-----------------------------------------------------------------------------------------
Total Predicted       483     739     939     792   1,037   1,360    5,350          68.36%
```

### Key Diagnostic Observations:
1. **Fresh Apple Collapse ($32.12\%$):**
   Out of 965 true fresh apples, only 310 are correctly classified. A staggering **$67.15\%$ (648 images)** are predicted as **Rotten** ($393$ as Rotten Apple, $255$ as Rotten Orange). The model exhibits an extreme false-positive spoilage bias on retail apples.
2. **Rotten Apple Cross-Species Confusion ($37.35\%$):**
   Out of 830 rotten apples, $361$ ($43.49\%$) are classified as **Rotten Orange**, exceeding the correct class count ($310$).
3. **Banana Asymmetry:**
   Rotten banana classification is near-perfect ($99.40\%$, only 5 errors out of 831). However, fresh bananas suffer a $21.84\%$ false-rot rate ($207$ fresh bananas misclassified as rotten). The model's latent decision boundary is heavily tilted toward the rotten class for bananas.

---

## 4. Botanical, Physical, and Optical Drivers of Classification Failure

### 4.1 The Apple Failure Mode: Russeting, Cultivar Shift, and Specular Lighting
The catastrophic accuracy drop on apples ($34.54\%$ aggregate) stems from three compounding domain discrepancies:
- **Cultivar and Morphology Shift:** The primary training partition (Kaggle) consists predominantly of uniform, studio-photographed red/green apples (e.g., Red Delicious, Granny Smith) with smooth pericarps. In contrast, FruitVision captures commercial supermarket fruit (Fuji, Gala, Honeycrisp) exhibiting pronounced natural striations, lenticels, and russeting (corky brown patches). MobileNetV2's convolutional filters interpret natural varietal striations as fungal lesions or necrotic decay.
- **Retail Lighting Specularity:** Studio training images utilized diffuse lighting against solid backdrops. FruitVision images were acquired under overhead commercial fluorescent and LED supermarket luminaires. Point-source lighting creates concentrated specular reflections and adjacent high-contrast shadow fringes on curved apple surfaces, which convolutional kernels register as surface pitting and soft rot.
- **Chromatic Convergence with Orange:** Bi-colored apples (yellow-red blush) under warm illumination exhibit chromatic feature vectors overlapping with textured orange pericarps, causing $255$ fresh apples and $361$ rotten apples to be misclassified as Rotten Orange.

### 4.2 The Banana Robustness Mechanism: Melanin Melanogenesis
In contrast to apples, bananas achieved $87.80\%$ aggregate accuracy and $99.40\%$ on rotten specimens. The biochemical degradation of *Musa acuminata* involves enzymatic browning driven by polyphenol oxidase (PPO), which synthesizes high-contrast, black insoluble melanin pigments. These dark lesions form stark, high-frequency spatial gradients against yellow background skin that remain unmistakable regardless of background, illumination, or camera sensor.

### 4.3 Citrus Flavedo and Pericarp Resilience
Fresh oranges maintained $87.53\%$ accuracy. The bright carotenoid pigmentation and distinctive pebbled texture of citrus flavedo provide highly invariant spatial-color signatures. The primary failure mode for oranges was underestimation of internal soft rot when external rind discoloration was subtle ($12.77\%$ rotten oranges predicted fresh).

---

## 5. Condition Shift Failure Mode: Formalin Preservative Immersion (Partition C)

Partition C evaluated 1,917 images from FruitVision labelled as subjected to chemical treatment (formalin immersion). 

### 5.1 Physical Nature of the Formalin Condition
- Formalin is an aqueous solution of formaldehyde gas ($37\%$ $CH_2O$). It is an agricultural preservative that halts enzymatic autolysis and microbial proliferation by cross-linking amino acid functional groups in cellular proteins.
- **Optical Invisibility in RGB:** Formaldehyde immersion maintains the visual freshness of the fruit pericarp. It does not alter optical reflectance across the visible spectrum ($400\text{--}700\text{ nm}$). An RGB image cannot detect chemical contamination or cross-linked proteins without spectroscopic or chemical assays.

### 5.2 Dangerous False Acceptance (UFAR-Fresh)
Because the preserved fruits look pristine, Model B V4.1 predicts them as "Fresh" with high confidence. When applying the locked operational thresholds ($\tau_{95}$):

| Detector | Empirical UFAR ($\tau_{95}$) | UFAR-Fresh ($\tau_{95}$) | Percentage of Accepted Fruit Labelled "Fresh" |
| :--- | :---: | :---: | :---: |
| **MSP Baseline** | 50.29% | **37.09%** | 73.76% |
| **Energy Baseline** | 53.94% | **44.03%** | 81.63% |
| **ODIN Baseline** | 47.84% | **36.83%** | 76.99% |
| **Mahalanobis** | 80.70% | **50.50%** | 62.58% |
| **OpenMax** | 50.60% | **40.06%** | 79.17% |
| **Dual-Gate Cascade** | 52.63% | **42.83%** | 81.38% |

**Supply Chain Risk Interpretation:**
Under the Dual-Gate Cascade, **$42.83\%$ (821 out of 1,917 images)** of formalin-treated fruits are accepted by the OOD gate and classified as **Fresh**. In an automated agricultural routing pipeline, these chemically treated fruits would be passed into the human consumption supply chain.

> [!CAUTION]
> **Scientific Disclosure:** RGB computer vision alone **cannot** serve as a food safety gate for chemical preservatives or adulterants. The manuscript must explicitly warn against claiming chemical safety verification from standard vision sensors.

---

## 6. Selective Classification and Coverage-Risk Tradeoff

Although domain shift degrades full-cohort accuracy on Partition B to $68.36\%$, the continuous detector scores allow the system to **abstain** on uncertain predictions, trading throughput (coverage) for precision (reduced risk).

### Table 3: Empirical Coverage-Risk Tradeoff on Partition B ($N = 5,350$)

$$\text{Risk}(\tau) = \frac{\sum_{i \in \text{Accepted}} \mathbb{I}(\hat{y}_i \neq y_i)}{N_{\text{Accepted}}}$$

| Target Coverage | MSP Risk | Energy Risk | ODIN Risk | Mahalanobis Risk | OpenMax Risk | Dual-Gate Risk |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10.0%** (Top 535 images) | **1.31%** | 3.18% | 2.43% | 28.04% | **1.50%** | 2.80% |
| **20.0%** (Top 1,070 images) | **4.86%** | 5.33% | 5.33% | 26.82% | **2.80%** | 4.67% |
| **30.0%** (Top 1,605 images) | 7.48% | 7.60% | 7.85% | 28.85% | **5.23%** | 6.92% |
| **40.0%** (Top 2,140 images) | 10.42% | 9.95% | 10.42% | 30.79% | **9.02%** | 9.63% |
| **50.0%** (Top 2,675 images) | 13.79% | 12.93% | 14.02% | 32.71% | **12.19%** | 12.37% |
| **60.0%** (Top 3,210 images) | 17.63% | 16.48% | 17.41% | 34.80% | **16.14%** | 16.29% |
| **70.0%** (Top 3,745 images) | 21.79% | 20.45% | 20.88% | 36.05% | **20.21%** | 20.13% |
| **80.0%** (Top 4,280 images) | 25.42% | 24.67% | 24.56% | 36.29% | **24.60%** | 24.60% |
| **90.0%** (Top 4,815 images) | 28.47% | 28.56% | 28.31% | 34.52% | **28.37%** | 28.25% |
| **100.0%** (All 5,350 images) | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** |

### Key Empirical Findings:
1. **Monotonic Risk Reduction:** For MSP, Energy, ODIN, OpenMax, and Dual-Gate, error rate falls monotonically as coverage decreases. At $50\%$ coverage, error is cut by more than half (from $31.64\%$ down to $\sim 12.3\%$). At $20\%$ coverage, error is less than $5\%$.
2. **Mahalanobis Failure on Covariate Shift:** Feature-space Mahalanobis distance fails completely under external retail shift (maintaining $>26\%$ risk even at $10\%$ coverage). Feature centroids calibrated on studio images are severely shifted by background and illumination variations.
3. **Operational Utility:** In real-world agricultural dispatch, routing decisions can be restricted to high-confidence operational envelopes (e.g., $60\%$ coverage yielding $>83\%$ accuracy), routing abstained samples to manual inspection stations.

---

## 7. Conclusions for the Manuscript

1. **Acknowledge the Domain Gap:** The manuscript must honestly report the $68.36\%$ accuracy on Partition B, attributing it directly to apple cultivar and lighting shifts.
2. **Highlight Selective Classification:** Present the coverage-risk curve as proof that the model's confidence scores are well-ordered, enabling robust selective classification in production.
3. **Clarify Formalin Limits:** Frame the Partition C evaluation as a demonstration of the intrinsic limits of RGB imaging for biochemical fixatives, justifying multimodal sensor fusion (e.g., VOC / gas sensors) in holistic post-harvest systems.

