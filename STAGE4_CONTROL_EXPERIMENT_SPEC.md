# Stage 4.0 Background & Acquisition Control Experiment Specification

**Document ID:** `STAGE4_CONTROL_EXPERIMENT_SPEC.md`  
**Role:** Principal Investigator & Lead Methodologist  
**Execution Timestamp:** November 10, 2026  
**Status:** Mandatory Experimental Control Protocol  
**Compliance Mandate:** FruitVision CC BY-NC-ND 4.0 Strict Compliance (In-Memory Transforms Only; No Derivative File Distribution)  

---

## 1. Scientific Motivation & Confounding Risk Analysis

In post-harvest computer vision benchmarks—specifically FruitVision (Bijoy et al., 2025) and ToxiFruit (Sattar et al., 2026)—chemically treated fruits (e.g. formalin immersion) were prepared under controlled laboratory protocols, whereas portions of the fresh and untreated control fruits were collected from wholesale produce markets or commercial stalls.

This introduces severe physical and environmental confounding:
1. **Illumination & Glare Discrepancies:** Laboratory environments utilize overhead fluorescent or fixed LED arrays that produce distinct high-frequency specular glazes on fruit wax rinds. Market stalls rely on diffused sunlight or open-air incandescent bulbs.
2. **Backdrop Context Discrepancies:** Laboratory images frequently feature white laminate tables, stainless steel trays, or neutral cloth backdrops. Commercial market captures contain wooden crates, corrugated cardboard, or burlap sacking.
3. **Hardware Sensor Profiles:** Differences in camera sensors (e.g., Samsung Galaxy A50 vs. Redmi Note 8 in FruitVision) introduce varying chromatic aberration, Bayer demosaicing artifacts, and dynamic range profiles.

> [!CAUTION]
> **The "Clever Hans" Effect:** If a deep neural network learns to reject formalin-treated fruits purely by recognizing the white laboratory table or fluorescent specular glare, the model has learned a spurious environmental shortcut rather than true post-harvest degradation or surface tissue anomalies.

---

## 2. The Three Experimental Control Conditions

To isolate genuine fruit-surface degradation signals from environmental background leakage, the benchmark must execute three parallel evaluation passes:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THREE CONTROL PROTOCOLS                                   │
├────┬─────────────────────────────┬─────────────────────────────────────────────────────┤
│ ID │ Protocol Name               │ Visual Processing Mechanics                         │
├────┼─────────────────────────────┼─────────────────────────────────────────────────────┤
│ 1  │ Full-Image Baseline         │ Standard unmodified RGB images resized to 224x224.   │
├────┼─────────────────────────────┼─────────────────────────────────────────────────────┤
│ 2  │ Fruit-Only Masked           │ In-memory foreground segmentation; background pixels│
│    │ (Tissue Isolation)          │ replaced with neutral mean gray (128, 128, 128).     │
├────┼─────────────────────────────┼─────────────────────────────────────────────────────┤
│ 3  │ Background-Only Control     │ Central 224x224 crop taken exclusively from the      │
│    │ (Shortcut Verification)     │ non-fruit background region.                         │
└────┴─────────────────────────────┴─────────────────────────────────────────────────────┘
```

### 2.1 Protocol 1: Full-Image Baseline
Evaluates the standard end-to-end model performance as deployed on natural camera captures without segmentation preprocessing.

### 2.2 Protocol 2: Fruit-Only Masked (Foreground Isolation)
- **Objective:** Determine whether the model retains OOD anomaly separation when all background, table, crate, and wall textures are entirely eliminated.
- **In-Memory Transformation:**
  1. Detect the fruit contour using an automated Otsu color threshold or bounding-box crop centered on the primary fruit mass.
  2. Generate a binary foreground mask $M \in \{0, 1\}^{H \times W}$.
  3. Replace background pixels $(1 - M)$ with neutral mean gray ($[128, 128, 128]$) or uniform black ($[0, 0, 0]$).
  4. Resize the masked foreground fruit to $224 \times 224$ and apply MobileNetV2 preprocessing.

### 2.3 Protocol 3: Background-Only Control (Shortcut Verification)
- **Objective:** Quantify the predictive power of the background context alone.
- **In-Memory Transformation:**
  1. Extract a $224 \times 224$ patch from the image periphery that contains zero fruit pixels ($M = 0$).
  2. Pass this background patch into the frozen Model B V4.1 checkpoint.
  3. Compute OOD anomaly scores ($S_{\text{Energy}}, S_{\text{Maha}}, S_{\text{MSP}}$).

---

## 3. Decision Rules & Interpretive Criteria

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DIAGNOSTIC MATRIX FOR CONTROL EXPERIMENT                        │
├───────────────────────────────┬───────────────────────────────┬────────────────────────┤
│ Background Control AUROC      │ Fruit-Only Masked AUROC       │ Scientific Conclusion  │
├───────────────────────────────┼───────────────────────────────┼────────────────────────┤
│ AUROC < 0.60 (Near Random)    │ AUROC >= 0.80 (High Sep.)     │ VALID FRUIT BIOMARKER: │
│                               │                               │ Model responds to peel │
│                               │                               │ surface degradation.   │
├───────────────────────────────┼───────────────────────────────┼────────────────────────┤
│ AUROC >= 0.75 (High Context)  │ AUROC Drops by > 15 pp        │ CONTEXT LEAKAGE: Model │
│                               │                               │ exploits studio/market │
│                               │                               │ background shortcuts.  │
├───────────────────────────────┼───────────────────────────────┼────────────────────────┤
│ AUROC >= 0.75 (High Context)  │ AUROC Remains High (>= 0.80)  │ PARTIAL DUAL SIGNAL:   │
│                               │                               │ Both background and    │
│                               │                               │ fruit rinds differ.    │
└───────────────────────────────┴───────────────────────────────┴────────────────────────┘
```

*Scientific Integrity Constraint:* If the Background-Only AUROC exceeds $0.75$, the manuscript is **strictly forbidden** from claiming that open-set rejection is driven by biochemical fruit-surface characteristics alone. The paper must report the background leakage as a documented limitation of public post-harvest benchmarks.

---

## 4. Bias Analysis of Object Segmentation Algorithms

Automated segmentation algorithms (e.g., GrabCut, U-Net, or Segment Anything Model [SAM]) can introduce secondary biases:
1. **Edge Halo Artifacts:** Segmentation masks often leave a 1-to-3 pixel border of background color around fruit silhouettes, potentially leaking background illumination through boundary contrast.
2. **Rind Boundary Distortion:** Morphological opening or smoothing operations can eliminate fine rind dehydration ridges or fungal hyphae present along the fruit contour.
3. **Standardization:** To prevent segmentation artifacts from biasing comparisons, the exact same automated segmentation pipeline must be applied across all classes (fresh, rotten, and formalin-treated) without class-specific parameter tuning.

---

## 5. FruitVision CC BY-NC-ND 4.0 Strict Legal Compliance

Under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International licence:
> *"If you remix, transform, or build upon the material, you may not distribute the modified material."*

To maintain 100% legal compliance:
1. **Zero Derivative File Persistence:** Cropped or masked fruit patches must be generated dynamically **in volatile memory** during evaluation batch iteration.
2. **Prohibition of Derivative Dataset Distribution:** No masked image archives, cropped datasets, or derived image files shall be uploaded, saved to public repositories, or distributed.
3. **Permissibility of Tabular Predictions:** Numerical score tables, logits, and metric summaries generated from in-memory arrays do not constitute image derivatives and are fully compliant.

---
*Specification Locked and Certified by Lead Methodologist.*

