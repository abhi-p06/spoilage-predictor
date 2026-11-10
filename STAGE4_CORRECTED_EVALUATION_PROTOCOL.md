# Stage 4.0.1 Corrected External Evaluation Protocol

**Document ID:** `STAGE4_CORRECTED_EVALUATION_PROTOCOL.md`  
**Role:** Principal Investigator & Independent Benchmark Methodologist  
**Target Publication:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0) / *Procedia Computer Science* (Elsevier)  
**Execution Timestamp:** November 10, 2026  
**Status:** Pre-Specified & Version-Locked Evaluation Protocol (Read-Only; Prior to External Inference)  
**Authoritative Manifest:** [`STAGE4_CORRECTED_IMAGE_LEVEL_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_CORRECTED_IMAGE_LEVEL_MANIFEST.csv) (20,781 rows)  
**Authoritative Thresholds:** [`STAGE4_CORRECTED_THRESHOLD_TABLE.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_CORRECTED_THRESHOLD_TABLE.csv)  

---

## 1. Executive Summary & Protocol Principles

This corrected protocol locks the scientific, mathematical, and procedural specifications for evaluating open-set recognition (OSR) and out-of-distribution (OOD) screening on the frozen AgriRoute Model B V4.1 checkpoint (`MODEL_B_V4_1_CHECKPOINT.keras`, SHA-256: `4a12f354...`).

### The Four Pillars of the Evaluation:
1. **Model Immutability:** The trained network is 100% frozen. Zero weights, biases, or hyperparameters are modified.
2. **Pre-Specified Thresholds:** Operating thresholds are derived exclusively from the unobserved Kaggle validation knowns ($N=227$). External datasets are never used for parameter selection.
3. **Disentangled Evaluation Cohorts:** Semantic shift is strictly decoupled into *Pure Semantic Shift* (Group D1) and *Combined Semantic & Treatment Shift* (Group D2). Intra-species cultivar transfer (ToxiFruit Malta) is reported in a separate table.
4. **Deterministic Environmental Controls:** A same-canvas foreground/background mask protocol tests whether anomaly rejection stems from fruit tissue degradation or background acquisition leakage.

---

## 2. Model & Baseline Scorers Architecture

### 2.1 The Frozen Primary Network
- **Checkpoint:** `MODEL_B_V4_1_CHECKPOINT.keras` (9,715,984 bytes).
- **Authoritative SHA-256:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`.
- **Penultimate Feature Vector:** $h(x) \in \mathbb{R}^{1280}$ (MobileNetV2 `top_dropout` / pooling output).
- **Canonical In-Distribution Classes ($K=6$):**
  `0: fresh_apple`, `1: fresh_banana`, `2: fresh_orange`, `3: rotten_apple`, `4: rotten_banana`, `5: rotten_orange`.

### 2.2 The Six Evaluated Scoring Methods
Because scalar temperature scaling converged to $T^* = 1.0000$, calibrated confidence is mathematically identical to Maximum Softmax Probability ($0.00\text{e}+00$ deviation). The six distinct methods evaluated are:
1. **MSP (Maximum Softmax Probability):** $S_{\text{MSP}}(x) = \max_k p_k(x)$.
2. **Energy-Based OOD Score:** $S_{\text{Energy}}(x) = T \log \sum_k \exp(z_k / T)$, with $T=1.0$.
3. **Dual-Gate Cascade (Energy AND MSP):** $(S_{\text{Energy}}(x) \ge \tau_1) \land (S_{\text{MSP}}(x) \ge \tau_2)$, jointly calibrated to match single-gate coverage.
4. **OpenMax (EVT Tail Fitting):** $S_{\text{OpenMax}}(x) = 1.0 - p_{\text{openmax}}(0 \mid x)$ ($\eta=20, \alpha=2$).
5. **ODIN (Input Perturbation):** $S_{\text{ODIN}}(x) = \max_k \text{softmax}(z_k(\widetilde{x}) / T_{\text{ODIN}})$ ($T=1000, \epsilon_{\text{norm}}=0.0014$).
6. **Ledoit-Wolf Mahalanobis Distance:** $S_{\text{Maha}}(x) = - \min_k \sqrt{(h(x) - \mu_k)^T \mathbf{\Sigma}_{\text{LW}}^{-1} (h(x) - \mu_k)}$ ($\lambda^* = 0.0978$).

---

## 3. The Mutually Distinguishable Evaluation Distributions

Every image in the benchmark is assigned to exactly one mutually distinguishable partition group:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MASTER EVALUATION PARTITION CENSUS                              │
├──────┬───────────────────────────────┬────────────────────────────┬────────────────────┤
│ Grp  │ Distribution Name             │ Sources & Composition      │ Usable Sample Count│
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ A    │ Primary In-Distribution Known │ Kaggle Fresh/Rotten Test   │ Exactly 227        │
│      │ Test Partition                │ (is_raw == 1, 6 classes)   │ (Primary Baseline) │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ B    │ External Known-Class Domain   │ FruitVision Clean Knowns   │ Exactly 5,350      │
│      │ Shift (Apple, Banana, Orange) │ (4,157) + Sultana (1,193)  │ (35 Dups Excluded) │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ C    │ Condition-Shift Unknown       │ FruitVision Formalin-mixed │ Exactly 1,950      │
│      │ (Treatment on Known Fruits)   │ (Apple 643, Ban 660, Or 647) (Local Available) │
│      │                               │ + ToxiFruit (Apple/Ban)    │ + 1,800 (Zenodo)   │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ D1   │ Pure Semantic Shift           │ FruitVision Mango/Grape    │ Exactly 4,793      │
│      │ (Natural Untreated Decay)     │ (2,793) + Sultana (2,000)  │ (Local Available)  │
│      │                               │ + ToxiFruit Fresh Mango    │ + 900 (Zenodo)     │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ D2   │ Combined Semantic &           │ FruitVision Formalin-mixed │ Exactly 1,226      │
│      │ Treatment Shift               │ (Mango 616, Grape 610)     │ (Local Available)  │
│      │                               │ + ToxiFruit Formalin Mango │ + 900 (Zenodo)     │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ M1   │ Cultivar Transfer (Known)     │ ToxiFruit Fresh Malta      │ 900 (Zenodo)       │
│      │ (Citrus sinensis cv. Malta)   │ (Reported Separately)      │                    │
├──────┼───────────────────────────────┼────────────────────────────┼────────────────────┤
│ M2   │ Cultivar Condition Shift      │ ToxiFruit Formalin Malta   │ 900 (Zenodo)       │
│      │ (Adulterated Citrus sinensis) │ (Reported Separately)      │                    │
├──────┴───────────────────────────────┴────────────────────────────┼────────────────────┤
│ TOTAL LOCAL PHYSICAL SAMPLES (Groups A, B, C-local, D1-local, D2) │ Exactly 13,546     │
│ TOTAL INCLUDING REMOTE TOXIFRUIT ARCHIVE                          │ Exactly 20,746     │
└───────────────────────────────────────────────────────────────────┴────────────────────┘
```

*Note on Duplicate Exclusion:* Out of 13,581 local image files, exactly 35 duplicate file copies (28 FruitVision + 7 Sultana) were excluded, leaving exactly **13,546 net usable local images**.

---

## 4. Pre-Locked Threshold & Joint Cascade Specification

Thresholds were calibrated strictly using the unobserved validation partition ($N=227$) and locked in [`STAGE4_CORRECTED_THRESHOLD_TABLE.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_CORRECTED_THRESHOLD_TABLE.csv):

### 4.1 Order-Statistic Discrete Thresholding
For a sorted validation vector $s_{(1)} \le \dots \le s_{(227)}$:
- **$\tau_{95} = s_{(12)}$ (Sample rank 12):** Rejects 11 samples ($s_{(1)} \dots s_{(11)}$), accepts 216 samples ($s_{(12)} \dots s_{(227)}$). Exact empirical coverage: **$216 / 227 = 95.1542\%$**.
- **$\tau_{90} = s_{(23)}$ (Sample rank 23):** Rejects 22 samples, accepts 205 samples. Exact empirical coverage: **$205 / 227 = 90.3084\%$**.

### 4.2 Locked Threshold Values
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        AUTHORITATIVE LOCKED THRESHOLDS TABLE                           │
├────┬────────────────────────┬──────────────────┬───────────────────┬───────────────────┤
│ ID │ Scorer                 │ Score Column     │ tau_95 (Coverage) │ tau_90 (Coverage) │
├────┼────────────────────────┼──────────────────┼───────────────────┼───────────────────┤
│ 1  │ MSP                    │ score_msp        │ 0.700580 (95.15%) │ 0.792790 (90.31%) │
│ 2  │ Free Energy            │ score_energy_id  │ 1.054579 (95.15%) │ 1.309243 (90.31%) │
│ 3  │ ODIN                   │ score_odin       │ 0.167164 (95.15%) │ 0.167207 (90.31%) │
│ 4  │ Ledoit-Wolf Mahalanobis│ score_mahalanobis│ -65.133230 (95.15%) -58.251335 (90.31%) │
│ 5  │ OpenMax                │ score_openmax_id │ 0.778938 (95.15%) │ 0.837232 (90.31%) │
├────┼────────────────────────┼──────────────────┼───────────────────┼───────────────────┤
│ 6  │ Dual-Gate Joint Cascade│ Energy AND MSP   │ tau_1 = 0.918497  │ tau_1 = 1.133139  │
│    │ (Coverage-Calibrated)  │                  │ tau_2 = 0.582613  │ tau_2 = 0.722049  │
│    │                        │                  │ Acc: 216 (95.15%) │ Acc: 205 (90.31%) │
└────┴────────────────────────┴──────────────────┴───────────────────┴───────────────────┘
```

*Joint Calibration Rule:* Marginal rejection ranks $k_1 = k_2 = 6$ were selected jointly on validation data, guaranteeing that the cascade accepts **exactly 216 samples (95.15%)**, resolving the coverage collapse observed with independent marginal thresholds.

---

## 5. Metric Standards & Disentangled Evaluation Protocol

### 5.1 ID Reference Cohorts
1. **Intra-Domain Reference:** Group A (Kaggle Test Raw, $N=227$). Establishes baseline in-distribution discrimination without geographic or sensor shift.
2. **Cross-Domain Reference (Covariate Shift):** Group B (FruitVision & Sultana Knowns, $N=5,350$). Evaluates known-class classification retention and threshold calibration under real-world multi-camera domain shift.

### 5.2 Reporting Separation
Results must be reported across two distinct evaluation perspectives:
1. **Validation-Locked Operating-Point Results:**
   Evaluates performance at the fixed thresholds locked in Section 4. Reports actual ID coverage on Group B, known-class rejection rate, and false acceptance rates across Groups C, D1, and D2.
2. **Retrospective Diagnostic Curves:**
   Reports AUROC, AUPR-IN, AUPR-OUT, OSCR, and retrospective FPR@95 across threshold sweeps to characterize intrinsic feature separability independent of calibration error.

### 5.3 Open-World Selective Risk Formulation
In an intake screening facility, accepting any uncharacterized or toxic produce is an operational error. Selective risk on accepted samples is formally defined as:
$$\text{Selective Risk}(c) = \frac{\sum_{x \in \mathcal{D}_{\text{accepted}}^{\text{known}}} \mathbf{1}\{\hat{y}(x) \ne y(x)\} + |\mathcal{D}_{\text{accepted}}^{\text{unknown}}|}{|\mathcal{D}_{\text{accepted}}^{\text{known}}| + |\mathcal{D}_{\text{accepted}}^{\text{unknown}}|}$$
The four false acceptance rates must be reported independently:
- **Condition-OOD False Acceptance Rate (Group C)**
- **Condition-OOD-to-Fresh False Acceptance Rate (Group C $\to$ Fresh)**
- **Pure Semantic-OOD False Acceptance Rate (Group D1)**
- **Combined Semantic-and-Condition False Acceptance Rate (Group D2)**

---

## 6. Deterministic Background & Acquisition Control Protocol

### 6.1 Segmentation Protocol
To isolate fruit tissue signals from background illumination shortcuts:
- **Algorithm:** Otsu multi-thresholding on saturation/value color contrast in HSV space, followed by a $5 \times 5$ elliptical morphological closing (2 iterations).
- **Same-Canvas Foreground (Fruit-Only):**
  $$I_{\text{fg}}(u, v) = I(u, v) \cdot M(u, v) + [128, 128, 128] \cdot (1 - M(u, v))$$
- **Same-Canvas Background-Only Control:**
  $$I_{\text{bg}}(u, v) = I(u, v) \cdot (1 - M(u, v)) + [128, 128, 128] \cdot M(u, v)$$
  The fruit is replaced with neutral middle gray while preserving peripheral tablecloths, lighting gradients, and camera boundaries on the exact original $224 \times 224$ canvas.
- **Validation Calibration:** Kaggle validation images are passed through the identical segmentation pipeline to establish control-specific calibration baselines.
- **Scientific Claim Restriction:** Termed **"foreground-associated visual separability"**. Causal biochemical claims regarding formaldehyde molecules are strictly prohibited.

---

## 7. Legal Rights & Verification Status

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATASET RIGHTS & LICENCE AUDIT                            │
├───────────────────┬─────────────────────────┬──────────────────────┬───────────────────┤
│ Dataset           │ Official Repository     │ Licence Specification│ Permitted Usage   │
├───────────────────┼─────────────────────────┼──────────────────────┼───────────────────┤
│ FruitVision 2025  │ Mendeley Data           │ CC BY-NC-ND 4.0      │ Academic research;│
│                   │ 10.17632/xkbjx8959c.2   │                      │ IN-MEMORY TRANS-  │
│                   │                         │                      │ FORMS ONLY.       │
├───────────────────┼─────────────────────────┼──────────────────────┼───────────────────┤
│ Sultana 2022      │ Mendeley Data           │ CC BY 4.0            │ Academic research │
│                   │ 10.17632/bdd69gyhv8.1   │                      │ and derivatives.  │
├───────────────────┼─────────────────────────┼──────────────────────┼───────────────────┤
│ ToxiFruit 2026    │ Zenodo                  │ CC BY 4.0            │ Academic research │
│                   │ 10.5281/zenodo.21480141 │                      │ and derivatives.  │
├───────────────────┼─────────────────────────┼──────────────────────┼───────────────────┤
│ Kaggle Fresh/Rott.│ Kaggle Public Benchmark │ UNCONFIRMED          │ Non-commercial    │
│                   │ sriramr/fruits-...      │ (Web-scraped)        │ fair-use research │
└───────────────────┴─────────────────────────┴──────────────────────┴───────────────────┘
```

---

## 8. Final Audit Verdict & Stage 4.1 Authorization

### **VERDICT:**
1. **GO FOR LOCAL BENCHMARK (FruitVision & Sultana):**
   Exactly **13,546 net usable local physical images** (spanning Groups A, B, C-local, D1-local, and D2) are cryptographically hashed, indexed, and fully prepared for sealed execution.
2. **CONDITIONAL GO FOR FULL BENCHMARK (Including ToxiFruit):**
   Full evaluation across all 20,746 images is contingent upon downloading and extracting the 14.2 GB `Original Dataset.zip` from Zenodo.
3. **Execution Directive:**
   Stage 4.1 may immediately execute the sealed evaluation on the local physical cohorts (Groups A, B, C-local, D1-local, and D2) using the pre-locked thresholds and in-memory controls.

---
*Protocol Certified by Principal Investigator and Independent Benchmark Auditor.*

