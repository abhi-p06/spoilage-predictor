# Stage 4.0 Final External Evaluation Protocol Design

**Document ID:** `STAGE4_EXTERNAL_EVALUATION_PROTOCOL.md`  
**Role:** Principal Investigator & Independent Benchmark Methodologist  
**Target Publication:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0) / *Procedia Computer Science* (Elsevier)  
**Execution Timestamp:** November 10, 2026  
**Status:** Pre-Registered Protocol Specification (Sealed Prior to External Inference)  
**Governing Rule:** Read-Only Benchmark Protocol Design — Zero External Test Predictions Inspected  

---

## 1. Executive Summary & Protocol Architecture

This document establishes the pre-registered, sealed external evaluation protocol for benchmarking open-set recognition (OSR) and out-of-distribution (OOD) screening in post-harvest fruit quality inspection.

Over previous iterations, AgriRoute has resolved historical target leakage, audited upstream dataset duplicates, discarded synthetic BiLSTM models, and validated the mathematical infrastructure for OSR scoring on the frozen Model B V4.1 checkpoint (`MODEL_B_V4_1_CHECKPOINT.keras`, SHA-256: `4a12f354...`).

To guarantee absolute scientific integrity and prevent test-set snooping or post-hoc threshold selection:
1. **The Model and Baselines Are Frozen:** Zero retraining, zero weight tuning, and zero architectural modifications.
2. **Thresholds Are Pre-Locked on Validation Knowns:** Operating points ($\tau_{95}$ and $\tau_{90}$) are derived exclusively from the unobserved Kaggle validation partition ($N=227$).
3. **Evaluation Populations Are Strictly Disentangled:** Four distinct evaluation distributions are formalized, keeping *Condition Shift* (withheld chemical preservation) separate from *Semantic Shift* (unseen botanical species).
4. **Mandatory Environmental Controls Are Enforced:** Full-image, fruit-only masked, and background-only patch experiments are specified to prevent "Clever Hans" shortcut learning.

---

## 2. Part 1: Frozen Model & Baseline Scorer Architecture

### 2.1 The Primary Frozen Backbone
- **Model Checkpoint:** `MODEL_B_V4_1_CHECKPOINT.keras`
- **File Size:** Exactly **9,715,984 bytes**
- **Authoritative SHA-256:**
  `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Architecture:** Pre-trained MobileNetV2 backbone $\to$ Dropout(rate=0.30) $\to$ Dense(6, softmax).
- **Penultimate Feature Space:** Exactly **1,280 dimensions** ($h(x) \in \mathbb{R}^{1280}$).
- **Canonical Known Classes ($K=6$):**
  `0: fresh_apple`, `1: fresh_banana`, `2: fresh_orange`, `3: rotten_apple`, `4: rotten_banana`, `5: rotten_orange`.

### 2.2 The Eight Evaluated Scoring Baselines
In accordance with open-set standards, all baselines are post-hoc score functions applied directly to the frozen network without retraining:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE EIGHT EVALUATED SCORERS                               │
├────┬─────────────────────────────┬─────────────────────────────────────────────────────┤
│ ID │ Scorer Name                 │ Primary Scoring Formulation                         │
├────┼─────────────────────────────┼─────────────────────────────────────────────────────┤
│ 1  │ Maximum Softmax Prob (MSP)  │ S_MSP(x) = max_k p_k(x)                             │
│ 2  │ Energy-Based OOD Score      │ S_Energy(x) = T * log sum_k exp(z_k / T), with T=1.0│
│ 3  │ ODIN Score                  │ S_ODIN(x) = max_k softmax(z_k(x_pert) / T_odin)     │
│ 4  │ Ledoit-Wolf Mahalanobis     │ S_Maha(x) = - min_k sqrt((h - mu_k)^T Sigma_LW^-1)  │
│ 5  │ OpenMax                     │ S_OpenMax(x) = 1.0 - p_openmax(Unknown | x)         │
│ 6  │ Energy-Only Selective Gate  │ S_Energy(x) >= tau_Energy                           │
│ 7  │ Calibrated Selective Gate   │ S_Calib(x) >= tau_Calib                             │
│ 8  │ Cascaded Dual-Gate Filter   │ (S_Energy(x) >= tau_1) AND (S_Calib(x) >= tau_2)    │
└────┴─────────────────────────────┴─────────────────────────────────────────────────────┘
```

*Note on Dual-Gate Framing:* The Dual-Gate architecture is strictly positioned as a *post-hoc cascaded screening filter* that decouples coarse OOD rejection from risk-sensitive selective abstention. It is **not** claimed as an algorithmic invention or custom neural network architecture.

---

## 3. Part 2 & 3: Definition of the Four Evaluation Distributions

The incoming evaluation stream is partitioned into four mutually distinguishable distributions plus a dedicated cultivar-transfer group:

```
                                  INCOMING EVALUATION STREAM
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         │                                    │                                    │
   [DISTRIBUTION A]                     [DISTRIBUTION B]                     [DISTRIBUTION C & D]
PRIMARY IN-DISTRIBUTION               EXTERNAL KNOWN SHIFT                    EXTERNAL UNKNOWNS
Kaggle V4.1 Test Partition            FruitVision & Sultana Knowns                         │
(227 Raw Base Images)                 (5,350 Raw Images)                                   │
                                                                       ┌───────────────────┴───────────────────┐
                                                                       │                                       │
                                                              [DISTRIBUTION C]                        [DISTRIBUTION D]
                                                              CONDITION SHIFT                         SEMANTIC SHIFT
                                                              Formalin-Treated Apples,                Mango, Grape, Guava,
                                                              Bananas, and Oranges                    Jujube, Strawberry
                                                              (3,750 Raw Images)                      (6,019 Raw Images)
```

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MASTER EVALUATION PARTITION CENSUS                              │
├──────┬───────────────────────────────┬────────────────────────────┬────────────────────┤
│ Grp  │ Distribution Name             │ Sources & Composition      │ Net Usable Images  │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ A    │ Primary In-Distribution Known │ Kaggle Fresh/Rotten Test   │ Exactly 227        │
│      │ Test Partition                │ (is_raw == 1, 6 classes)   │ (Primary Baseline) │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ B    │ External Known-Class Domain   │ FruitVision Clean Knowns   │ Exactly 5,350      │
│      │ Shift (Apple, Banana, Orange) │ (4,157) + Sultana (1,193)  │ (Covariate Shift)  │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ C    │ Condition-Shift Unknown       │ FruitVision Formalin       │ Exactly 3,750      │
│      │ (Treatment on Known Fruits)   │ (1,950) + ToxiFruit (1,800)│ (Safety Hazards)   │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ D    │ Semantic-Shift Unknown        │ FruitVision (Mango, Grape) │ Exactly 6,019      │
│      │ (Unseen Fruit Species)        │ + Sultana (5 exotic crops) │ (Species Outliers) │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ M1   │ Cultivar Transfer (Known)     │ ToxiFruit Fresh Malta      │ Exactly 900        │
│      │ (Intra-species sweet orange)  │ (Citrus sinensis cv Malta) │ (Reported Sep.)    │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ M2   │ Cultivar Condition Shift      │ ToxiFruit Formalin Malta   │ Exactly 900        │
│      │ (Adulterated sweet orange)    │ (Treated Citrus sinensis)  │ (Reported Sep.)    │
├──────┴───────────────────────────────┴────────────────────────────┼────────────────────┤
│ TOTAL EVALUATION SAMPLES ACROSS ALL PARTITIONS                    │ Exactly 17,146     │
└───────────────────────────────────────────────────────────────────┴────────────────────┘
```

### 3.1 Strict Separation of ToxiFruit Malta
As established in `STAGE1_CORRECTION_LOG.md` (§CORR-07), Malta is taxonomically *Citrus sinensis* (sweet orange cultivar), but possesses distinct visual traits (persistent greenish-yellow mottling, thin peel, oblate shape).
*Protocol Rule:* Malta images (Fresh: 900; Formalin: 900) must **never be silently pooled** into the primary orange class. They must be evaluated and reported in a separate table as an *intra-species phenotypic cultivar transfer* study.

### 3.2 Scientific Nomenclature for Treatment Samples
Treated fruits in Distribution C must be rigorously designated as **"Dataset-labelled treatment-associated fruit specimens"** (prepared via 30-min 10% formalin immersion in FruitVision, and chamber vapor exposure in ToxiFruit). Under no circumstances shall they be referred to as "optically verified formaldehyde molecules".

---

## 4. Part 4: Background and Acquisition Bias Controls

### 4.1 Confounding Threat Assessment
Because formalin-treated specimens in FruitVision were prepared in laboratory environments, while portions of untreated fresh controls were collected in retail markets, models risk learning lighting or backdrop shortcuts.

### 4.2 The Three Mandatory Controls
To isolate genuine fruit-surface decomposition from environmental background leakage, three parallel passes must be executed:
1. **Control 1 (Full-Image Evaluation):** Evaluates unmodified camera images resized to $224 \times 224$.
2. **Control 2 (Fruit-Only Masked Evaluation):** Foreground fruit segmented in memory; background pixels replaced with uniform neutral gray ($[128, 128, 128]$).
3. **Control 3 (Background-Only Evaluation):** Central $224 \times 224$ patches cropped exclusively from background areas containing zero fruit pixels.

### 4.3 Diagnostic Decision Rules
- If Background-Only AUROC $\ge 0.75$, the OOD detector is responding to camera/backdrop context leakage.
- If Fruit-Only Masked AUROC drops by $> 15$ percentage points compared to Full-Image, the paper must report context leakage as an empirical limitation.
- The paper is **strictly barred** from claiming that rejection is based on fruit peel degradation unless the Fruit-Only Masked experiment confirms separation.

### 4.4 Legal & Licence Mandate
In strict compliance with FruitVision's **CC BY-NC-ND 4.0** licence, all fruit-masking and patch-cropping transformations must be executed **in-memory during evaluation batch streaming**. No modified image files, cropped archives, or derivative image datasets shall be serialized or redistributed.

---

## 5. Part 5: Pre-Locked Threshold & Calibration Specification

All baseline thresholds are pre-locked strictly on the Kaggle validation partition ($N=227$ raw images) prior to external testing:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PRE-LOCKED OPERATING THRESHOLDS TABLE                           │
├────┬────────────────────────┬──────────────────┬───────────────────┬───────────────────┤
│ ID │ Scorer / Baseline      │ Score Symbol     │ Primary Operating │ Secondary Oper.   │
│    │                        │                  │ Point (tau_95)    │ Point (tau_90)    │
├────┼────────────────────────┼──────────────────┼───────────────────┼───────────────────┤
│ 1  │ Maximum Softmax Prob.  │ S_MSP(x)         │ 0.702499          │ 0.794850          │
│ 2  │ Free Energy (ID Score) │ S_Energy(x)      │ 1.063041          │ 1.338210          │
│ 3  │ ODIN (T=1000, eps=0.0014) S_ODIN(x)       │ 0.167167          │ 0.167209          │
│ 4  │ Ledoit-Wolf Mahalanobis│ S_Maha(x)        │ -64.977946        │ -58.126742        │
│ 5  │ OpenMax (eta=20, alpha=2) S_OpenMax(x)    │ 0.779116          │ 0.840834          │
│ 6  │ Calibrated Confidence  │ S_Calib(x)       │ 0.702499          │ 0.794850          │
└────┴────────────────────────┴──────────────────┴───────────────────┴───────────────────┘
```

- **Fair Coverage Benchmarking:** Baselines are compared at standardized ID acceptance levels (95% and 90% validation coverage).
- **Dual-Gate Combinations:** Evaluated at $(\tau_{95}^{\text{Energy}}, \tau_{95}^{\text{Calib}})$ and $(\tau_{90}^{\text{Energy}}, \tau_{90}^{\text{Calib}})$.
- **No Risk Guarantees:** Clopper-Pearson binomial confidence intervals must accompany all selective risk estimates; theoretical risk certification claims are prohibited.

---

## 6. Part 6 & 7: Metric Definitions & Statistical Standards

### 6.1 The Twelve Authoritative Metrics
1. **Known-Class Macro-F1:** Arithmetic mean of F1 across 6 known classes on accepted samples.
2. **Balanced Accuracy:** Macro-averaged recall across 6 known classes.
3. **OOD AUROC:** Area under the ROC curve with OOD/Unknown designated as positive ($y=1$).
4. **AUPR-OUT:** Precision-Recall area treating OOD as positive.
5. **AUPR-IN:** Precision-Recall area treating In-Distribution as positive.
6. **FPR@95% ID Acceptance:** False Positive Rate on unknowns when ID acceptance is fixed at 95.0%.
7. **OSCR:** Open-Set Classification Rate plotting Correct Classification Rate on knowns vs. False Positive Rate on unknowns.
8. **Unknown False Acceptance Rate (UFAR):** Proportion of unknown samples accepted as known.
9. **Unknown-to-Fresh False Acceptance Rate (UFAR-Fresh):** Proportion of unknown samples accepted and specifically misclassified as "Fresh".
10. **Known-Class Rejection Rate (KRR):** Proportion of true known samples unnecessarily abstained.
11. **Coverage-Risk Trade-off Curve:** Selective risk as a function of coverage $c \in [0.10, 1.00]$.
12. **In-Sample Calibration:** 10-bin Expected Calibration Error (ECE) and Multiclass Brier Score.

### 6.2 Statistical Uncertainty Standards
- Report **95% non-parametric bootstrap confidence intervals** (1,000 resamples) across all continuous metrics.
- Report **exact Clopper-Pearson binomial confidence intervals** for rare catastrophic misclassifications (UFAR-Fresh).
- Clearly document the sample exchangeability limitation when batch-level cluster metadata is unavailable.

---

## 7. Part 8: Contextualization Against PEOS-Net, PAG-MSBNet & SensorNet

The benchmark rationale directly incorporates and positions against the latest literature:
1. **PEOS-Net (Frontiers in AI, 2026; `10.3389/frai.2026.1938398`):** PEOS-Net evaluates pre-harvest foliar tomato leaf diseases using custom retrained prototype-memory and energy branches under intra-dataset semantic withholding. AgriRoute benchmarks post-harvest edible fruits under multi-source cross-dataset shifts, decoupling fine-grained condition shift from semantic shift using a post-hoc screening filter.
2. **PAG-MSBNet (Ecological Informatics, 2026; `10.1016/j.ecoinf.2026.103703`):** Evaluates open-set crop leaf pathology using multi-scale branches. It does not address post-harvest decay, chemical adulteration, or asymmetric food-safety loss matrices.
3. **SensorNet (Intelligent Systems with Applications, 2024; `10.1016/j.iswa.2024.200402`):** Authored by the creators of ToxiFruit, SensorNet evaluates *closed-set supervised classification* of formalin fruit using hardware gas sensors (MQ-138) alongside images. AgriRoute evaluates *withheld-condition open-set screening*: testing whether an optical model trained strictly on natural decomposition can detect unobserved chemical preservation as an OOD anomaly without multimodal sensors.

---

## 8. Part 9: Final Protocol Decision

### **PROTOCOL DECISION: GO (READY FOR SEALED EXECUTION)**

All dataset partitions, sample counts, baseline score formulations, operating thresholds, negative controls, and statistical metrics are fully designed, documented, and locked.

- **Local Datasets (FruitVision & Sultana):** 100% verified and extracted on local disk (`data/raw/`). Execution on these datasets can proceed immediately.
- **Remote Dataset (ToxiFruit):** 100% specified; execution will proceed upon completion of the Zenodo archive ingestion.

*The external test data may now be unsealed in Stage 4.1 in strict accordance with this locked protocol.*

---
*Protocol Designed, Audited, and Certified by Principal Investigator and Lead Methodologist.*

