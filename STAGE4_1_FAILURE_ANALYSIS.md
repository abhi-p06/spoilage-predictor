# STAGE 4.1: FORENSIC FAILURE ANALYSIS REPORT
**AgriRoute Empirical Benchmark: Risk-Aware Open-Set Fruit Quality Classification**  
**Target Publication:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Document ID:** `STAGE4_1_FAILURE_ANALYSIS.md`  
**Execution Timestamp:** November 10, 2026 — 20:50 UTC+05:30  
**Status:** Post-Inference Failure Audit ($N = 13,465$ Images Verified)  

---

## 1. EXECUTIVE SUMMARY: THE CENTRAL BENCHMARK PARADOX

This failure analysis report investigates the biological, textural, and covariate mechanisms responsible for false acceptances and false rejections across the 13,465 local evaluation images processed by frozen Model B V4.1.

Our empirical benchmark exposes a profound **scientific paradox** in agricultural computer vision:
1. **High In-Distribution Efficacy:** In laboratory settings against clean known produce (Partition A), Model B V4.1 achieves **$96.92\%$ closed-set accuracy** (Macro-F1: $96.87\%$). Against uncharacterized exotic botanical species under natural conditions (Partition D1 and D2), energy-based and dual-gate detectors achieve exceptional AUROC values of **$97.50\% - 99.46\%$**.
2. **Catastrophic Chemical Shielding (Partition C):** When known commercial species are subjected to hazardous chemical treatment (dilute formalin immersion), detectors experience a severe failure mode: **$52.63\%$ of formalin-treated fruits pass undetected** at the nominal $\tau_{95}$ operating threshold. Critically, **$42.83\%$ of formalin-treated fruits are accepted and specifically misclassified as commercial "Fresh" produce (UFAR-Fresh)**.
3. **Severe Citrus Pericarp Confounding:** In *Citrus sinensis* (Orange), **$93.83\%$ of formalin-treated fruits fool the Dual-Gate detector**, with **$93.18\%$ erroneously labeled as pristine fresh oranges**. The thick, waxy, oil-gland-rich citrus pericarp preserves surface visual aesthetics despite chemical immersion, demonstrating conclusively that conventional RGB imaging cannot function as a chemical safety assurance mechanism.
4. **Domain-Shift Abstention Spikes (Partition B):** When tested on valid commercial fruits photographed in authentic market and field conditions (Partition B), closed-set accuracy drops to **$68.36\%$**, and the detector triggers false alarms on **$42.43\%$** of valid commercial produce, with fresh apples suffering an unsustainable **$79.27\%$ abstention rate**.

---

## 2. PARTITION C FAILURE AUDIT: FORMALIN-MIXED KNOWN SPECIES

Partition C comprises 1,917 physical images of known commercial fruit species (Apple, Banana, Orange) photographed following preservative chemical immersion protocols.

### 2.1 Detector Performance Comparison on Partition C ($N=1,917$)

| OOD Detector | Total False Acceptances (UFAR $\tau_{95}$) | False Acceptance into "Fresh" (UFAR-Fresh $\tau_{95}$) | AUROC vs Primary ID Knowns ($A \text{ vs } C$) | AUROC vs External Knowns ($B \text{ vs } C$) |
| :--- | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 964 ($50.29\%$) | 711 ($37.09\%$) | $90.63\%$ | $57.98\%$ |
| **Energy Baseline** | 1,034 ($53.94\%$) | 844 ($44.03\%$) | $84.09\%$ | $52.57\%$ |
| **ODIN Baseline** | 917 ($47.84\%$) | 706 ($36.83\%$) | $89.11\%$ | $55.54\%$ |
| **Ledoit-Wolf Mahalanobis** | 1,547 ($80.70\%$) | 968 ($50.50\%$) | $85.43\%$ | $50.10\%$ |
| **OpenMax (Weibull $\alpha=2$)** | 970 ($50.60\%$) | 768 ($40.06\%$) | $87.69\%$ | $55.18\%$ |
| **Dual-Gate Cascade (Joint $\tau_{95}$)** | **1,009 ($52.63\%$)** | **821 ($42.83\%$)** | **$85.35\%$** | **$53.31\%$** |

### 2.2 Species-Level Dissection of Dual-Gate Failure Rates

```
                          PARTITION C FALSE ACCEPTANCE RATES BY BOTANICAL SPECIES
                          
   Botanical Taxon            Total Usable   False Acceptances (UFAR)   Catastrophic UFAR-Fresh
  ─────────────────────────────────────────────────────────────────────────────────────────────
   Apple (Malus domestica)         641         104 (16.22%)               21 ( 3.28%)   <-- Strong Rejection
   Banana (Musa acuminata)         660         327 (49.55%)              226 (34.24%)   <-- Moderate Leakage
   Orange (Citrus sinensis)        616         578 (93.83%)              574 (93.18%)   <-- Complete Collapse
  ─────────────────────────────────────────────────────────────────────────────────────────────
   Total Partition C             1,917       1,009 (52.63%)              821 (42.83%)
```

### 2.3 Biological & Textural Failure Mechanisms
1. **The Thick-Pericarp Citrus Shield (Orange):**
   - *Observation:* 574 out of 616 formalin-treated oranges ($93.18\%$) are classified as `fresh_orange` with high detector confidence.
   - *Biological Mechanism:* The outer flavedo of *Citrus sinensis* consists of a dense cuticle containing essential oil cavities (limonene pockets) and carotenoid pigments supported by a fibrous, spongy, pectin-rich albedo. When immersed in aqueous formaldehyde, the hydrophobic cuticle prevents rapid tissue collapse, cellular maceration, or immediate enzymatic browning. As a result, the fruit retains its spherical geometry, saturated orange hue, and surface gloss.
   - *Model Bias:* To MobileNetV2's inverted residual blocks, a formalin-dipped orange exhibits high-contrast edge gradients and standard citrus color channels, yielding logit values indistinguishable from unadulterated orchard-fresh oranges ($S_{\text{MSP}} > 0.90$).
2. **Peel Thickness vs. Surface Degradation (Apple vs. Banana):**
   - *Apple:* The thin epicuticular wax layer of *Malus domestica* reacts to chemical dip protocols with micro-fissuring, irregular lenticel spotting, and accelerated superficial scald. The detector successfully captures these anomalous textural perturbations, keeping false acceptances to a modest **$16.22\%$** (and catastrophic fresh misclassifications to only **$3.28\%$**).
   - *Banana:* *Musa acuminata* displays intermediate behavior ($49.55\%$ FA). Immersion delays typical polyphenol oxidase (PPO) melanin spotting (senescent freckling), resulting in an artificially uniform yellow peel that the network frequently misinterprets as prime commercial freshness.

---

## 3. PARTITION D1 FAILURE AUDIT: PURE SEMANTIC SHIFT

Partition D1 evaluates $N=4,776$ physical images of uncharacterized exotic botanical species undergoing natural post-harvest aging (Grape, Guava, Jujube, Mango, Pomegranate, Strawberry).

### 3.1 Species-Wise Breakdown of Semantic False Acceptances

```
                      PARTITION D1 FALSE ACCEPTANCE RATES BY SPECIES (Dual-Gate tau_95)
                      
   Species / Botanical Taxon       Total   False Acceptances (UFAR)   UFAR-Fresh   Top-1 Proxy Closed-Set Classes
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────
   Grape (Vitis vinifera)          1,783        138 ( 7.74%)          135 ( 7.57%)  fresh_apple, fresh_banana
   Mango (Mangifera indica)        1,393        360 (25.84%)          208 (14.93%)  fresh_apple, rotten_apple
   Strawberry (Fragaria ananassa)    400        102 (25.50%)           98 (24.50%)  fresh_apple, rotten_banana
   Jujube (Ziziphus jujuba)          400        121 (30.25%)           77 (19.25%)  fresh_apple, rotten_orange
   Pomegranate (Punica granatum)     400        191 (47.75%)          133 (33.25%)  fresh_apple, rotten_apple
   Guava (Psidium guajava)           400        232 (58.00%)           93 (23.25%)  rotten_apple, fresh_apple
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────
   Total Partition D1              4,776      1,144 (23.95%)          744 (15.58%)
```

### 3.2 Geometric & Morphological Proxy Mimicry
1. **The Spherical Pome Confounder (Guava & Pomegranate):**
   - Guava (*Psidium guajava*) suffered the highest semantic false acceptance rate (**$58.00\%$**), followed by Pomegranate (*Punica granatum*, **$47.75\%$**).
   - *Root Cause:* Both guavas and pomegranates are spherical to subglobose pomes with distinct calyx crowns. When viewed under 2D RGB projection, their circular silhouettes and greenish-yellow (guava) or reddish-pink (pomegranate) hues align directly with the deep feature distributions of `fresh_apple` and `rotten_apple`.
   - *Network Path:* The global average pooling layer compresses spatial arrangements into a 1,280-dimensional feature vector dominated by radial color transitions and circular boundary contours. Consequently, uncharacterized spherical fruits project directly inside the convex hull of known apple training samples.
2. **Morphological Dissimilarity Rejection (Grape):**
   - Grape (*Vitis vinifera*) achieved the highest rejection rate (**$92.26\%$ successfully rejected**; FA = $7.74\%$).
   - *Mechanism:* Clustered bunches of small, spherical berries on pedicels introduce repetitive high-frequency spatial gradients and nested circular occlusion patterns completely absent in single-specimen training imagery. This triggers high free energy ($S_{\text{Energy}} < 0.918$), enabling decisive open-set abstention.

---

## 4. PARTITION B FAILURE AUDIT: EXTERNAL KNOWN-CLASS DOMAIN SHIFT

Partition B contains 5,350 physical images of known commercial fruit taxa (Apple, Banana, Orange) acquired from independent external repositories (FruitVision and Sultana).

### 4.1 The External Abstention Crisis
In real-world deployment, an OOD detector must reject foreign produce without needlessly abstaining on legitimate commercial produce. Partition B demonstrates that **covariate domain shift causes massive false alarms on valid known produce**:

```
                 PARTITION B FALSE REJECTION / ABSTENTION RATES (Dual-Gate tau_95, N=5,350)
                 
   Botanical Taxon            Condition   Total Samples   False Rejections (KRR)   Abstention Percentage
  ─────────────────────────────────────────────────────────────────────────────────────────────────────
   Apple (Malus domestica)     Fresh            965                 765                    79.27%
   Apple (Malus domestica)     Rotten           830                 566                    68.19%
   Banana (Musa acuminata)     Fresh            948                 395                    41.67%
   Banana (Musa acuminata)     Rotten           831                  98                    11.79%
   Orange (Citrus sinensis)    Fresh            946                 122                    12.90%
   Orange (Citrus sinensis)    Rotten           830                 324                    39.04%
  ─────────────────────────────────────────────────────────────────────────────────────────────────────
   Total Partition B            Both          5,350               2,270                    42.43%
```

### 4.2 Covariate Confounders: Laboratory vs. Field Environments
1. **Background & Illumination Biases:**
   - Training images (Kaggle) were captured under sterile benchtop conditions on pure white sheets with direct flash, producing sharp, high-intensity color saturations.
   - External images (FruitVision/Sultana) were photographed in authentic retail and packinghouse environments: wooden crates, burlap sacks, market cloth, and ambient diffuse daylight.
   - This environmental shift causes clean commercial produce to exhibit muted activations, driving the Free Energy score below the laboratory calibration threshold $\tau_{\text{Energy}} = 0.918451$.
2. **Economic Cost of Abstention:**
   - A False Rejection Rate of **$79.27\%$ on fresh apples** would collapse an automated packing facility by routing 4 out of 5 valid commercial apples to manual human inspection benches.

---

## 5. COMPARATIVE DETECTOR ARCHITECTURE ANALYSIS

```
                                  DETECTOR RADAR COMPARISON
                                  
   Detector          A vs D1 AUROC     A vs C AUROC     B vs C AUROC     ID KRR (Part. B)   Failure Signature
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────
   MSP                   93.70%           90.63%           57.98%             42.77%        Overconfident on OOD
   ENERGY                97.55%           84.09%           52.57%             41.50%        Optimal Semantic OOD
   ODIN                  93.81%           89.11%           55.54%             48.86%        Computationally Heavy
   MAHALANOBIS           93.25%           85.43%           50.10%             19.16%        Catastrophic C FA (80%)
   OPENMAX               96.81%           87.69%           55.18%             43.42%        Weibull Tail Sensitivity
   DUAL-GATE             97.50%           85.35%           53.31%             42.43%        Balanced Risk Coverage
```

### Key Architectural Findings:
1. **Why Mahalanobis Collapses on Chemical Shift (UFAR = 80.70%):**  
   The Ledoit-Wolf precision matrix $\Sigma_{\text{LW}}^{-1}$ models covariance as a unimodal Gaussian ellipsoid in $\mathbb{R}^{1280}$. When external imaging shifts the entire feature cloud outward along background dimensions, the Mahalanobis distance metric loses discriminative power between subtle internal chemical damage and external lighting variance.
2. **Why Energy Outperforms MSP on Semantic Anomalies:**  
   Softmax normalization forces probabilities to sum to 1.0, creating artificial high confidence on out-of-distribution inputs that activate any single arbitrary logit. Free Energy ($-\log \sum e^{z_k}$) avoids this normalization trap, accurately capturing that total unconstrained logit mass is suppressed on exotic species.
3. **The Limits of Dual-Gate:**  
   While Dual-Gate provides the best overall balance between calibration and semantic rejection, it cannot overcome the biological opacity of thick citrus peels, demonstrating the fundamental physical boundaries of standard RGB digital photography.

---

## 6. ACTIONABLE ENGINEERING RECOMMENDATIONS FOR AGRILOGISTICS

Based on this forensic audit, the following engineering revisions are mandated for AgriRoute:
1. **De-couple Chemical Screening from Visual Sorting:**  
   Remove all claims suggesting RGB computer vision can verify food safety against preservative adulteration. Position visual OSR strictly as an *anomaly screening gate* that flags morphological irregularities.
2. **Mandate Multispectral / NIR Sensor Fusion for Chemical Quality:**  
   Integrate short-wave infrared (SWIR) or Raman spectroscopy channels capable of penetrating the citrus flavedo to measure spectral reflectance changes corresponding to formaldehyde C-H and C=O stretching modes.
3. **Implement Domain-Adaptive Normalization:**  
   Deploy test-time batch normalization or background-segmentation masking before feature extraction to decouple fruit peel representation from market backgrounds, mitigating the 42.43% false rejection rate on external known produce.

---
*Signed and sealed on behalf of the AgriRoute Scientific Audit Team,*  
**Lead Independent Scientific Benchmark Auditor & Methodologist**  
*November 10, 2026*

