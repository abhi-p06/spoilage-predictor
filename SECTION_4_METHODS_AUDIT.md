# SECTION 4 AUDIT AND EVIDENCE RECONCILIATION REPORT
## AgriRoute V4.1 Research Paper — ICMLDE 2026 / Procedia Computer Science
### Final Scientific Correction Pass & Code Reconciliation Audit

**Document Status:** Fully Reconciled, Formatted, and Code-Verified  
**Audit Date:** November 11, 2026  
**Audited Files:**
- `research_paper/manuscript/sections/04_methodology.tex`
- `research_paper/manuscript/04_methodology.md`
- `research_paper/manuscript/sections/05_results.tex` (Table 8 renamed to Dual-Gate Proxy)
- `research_paper/manuscript/main.tex`
- `research_paper/manuscript/main.pdf`
- `research_paper/figures/figure_02_pipeline.pdf` & `.png`
- `research_paper/manuscript/figures/figure_02_pipeline.pdf` & `.png`
- `scripts/run_stage4_1_benchmark.py`
- `STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv`
- `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`
- `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`
- `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv`
- `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv`
- `STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv`

---

## 1. Executive Summary & Verification of Mandated Corrections

A comprehensive forensic audit and scientific correction pass was executed on Section 4 ("Methodology") of the AgriRoute V4.1 manuscript. All mathematical formulations, scoring algorithms, architectural descriptions, threshold derivations, and evaluation metrics were reconciled against the canonical benchmark execution codebase (`scripts/run_stage4_1_benchmark.py`) and empirical result ledgers.

### Status of the Ten Mandated Correction Areas

| Area | Topic | Issue Identified in Preliminary Draft | Corrective Action Taken & Code Parity | Audit Status |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **OpenMax Formulation** | Equation omitted 1-based index behavior; code implements rank weighting where top-1 class receives zero logit discount. | Formulated as $w_{c_r} = 1.0 - \frac{r-1}{\alpha}(1 - \omega_r(x))$ with $r \in \{1, \dots, \alpha\}$. Transparently documented that $r=1$ receives $w_{c_1} = 1.0$ (no discount) and distance modeling is evaluated on 1280-D global average pooled features. Described as a modified OpenMax-style heuristic. | **VERIFIED** |
| **2** | **ODIN Formulation** | Text described canonical cross-entropy / negative log-likelihood perturbation. | Reconciled against code (L217–231): perturbation is computed along sign gradient of maximum temperature-scaled logit $\max_k z_k/T_{\text{ODIN}}$, clipped to $[-1.0, 1.0]$. Documented as an ODIN-style perturbation variant. | **VERIFIED** |
| **3** | **MobileNetV2 Architecture** | Described as "53 inverted residual bottleneck layers" (inaccurate legacy phrasing). | Reconciled against Keras model inspection: 1 initial $3\times 3$ conv + 17 bottleneck blocks (1 initial inverted bottleneck + 16 inverted residual blocks with expansion 6; 155 layer operations in functional graph), 1280-D global pooling, Dropout(0.3), 6-class dense head. | **VERIFIED** |
| **4** | **Dual-Gate Operational Rule vs. Proxy AUROC** | Ambiguity between discrete Boolean operational rule and continuous score needed for AUROC. | Clarified that operational routing is strictly discrete ($\operatorname{ACCEPT} \iff S_E \ge \tau_E \land S_M \ge \tau_M$). Continuous linear margin proxy $S_{\text{proxy}} = (S_E - \tau_E) + (S_M - \tau_M)$ is documented as an exploratory metric. Explained scale dependence (Energy $[0,10]$ vs MSP $(1/6,1]$). Renamed Table 8 entry in `05_results.tex` to `Dual-Gate (Proxy)`. | **VERIFIED** |
| **5** | **Evaluation Metric Consistency** | Mixing of threshold-free vs. thresholded metrics; over-claiming food safety; pipeline figure mismatch. | Clarified AUROC as threshold-independent; Retrospective FPR@95 as post-hoc operating-point metric ($y_{\text{ood}} = 1$); documented AUPR and OSCR as auxiliary metrics in CSV ledgers; regenerated Figure 1 to match exact labels; reframed UFAR-Fresh as produce routing / non-target acceptance outcome (disclaiming biological food safety). | **VERIFIED** |
| **6** | **Statistical Reporting** | Evaluated domain shift difference with inferential phrasing ("confirming robustness"). | Rephrased to descriptive comparison: non-overlapping 95% bootstrap percentile intervals show substantial descriptive separation without asserting formal inferential hypothesis testing. Verified $B=1,000$, `seed=42`, image-level unit, stratification. | **VERIFIED** |
| **7** | **Threshold Calibration Rigor** | Over-claiming absolute elimination of circularity / data-snooping bias. | Replaced absolute phrasing with evidence-bounded language. Documented $N_{\text{val}} = 227$ raw validation images, order statistics $s_{(12)}$ (single gate) and $s_{(7)}$ (Dual-Gate), inclusion-exclusion union $|R_{\text{union}}| = 11$, and Clopper-Pearson interval $[91.43\%, 97.60\%]$. | **VERIFIED** |
| **8** | **LaTeX & Markdown Synchronization** | Desynchronized citations and figure numbering between `.tex` and `.md`. | Synchronized word-for-word and equation-for-equation. Standardized figure reference to **Figure 1** (matching compiled PDF). Canonical citations verified: MobileNetV2 [7], MSP [9], Sultana [11], FruitVision [12], OpenMax [14], ODIN [16], Mahalanobis [17], Energy [18]. | **VERIFIED** |
| **9** | **Experimental Integrity** | Risk of inadvertent checkpoint modification, re-inference, or threshold retuning. | Checkpoint SHA-256 confirmed unchanged (`4a12f354...b6b4`). Zero weights modified; zero thresholds retuned; zero synthetic runs; zero numbers altered. | **VERIFIED** |
| **10** | **Build & Section 5–8 Status** | Compilation warnings; unverified status of downstream manuscript sections. | Tectonic compiled with Exit code 0, zero overfull hboxes in Section 4, zero unresolved citations. Sections 5–8 explicitly audited and documented as pending completion. | **VERIFIED** |

---

## 2. Forensic Code-to-Manuscript Equation Reconciliation

### 2.1. Modified OpenMax-Style Heuristic
- **Benchmark Code (`scripts/run_stage4_1_benchmark.py`, L267–290):**
  ```python
  # Feature representation:
  # Penultimate feature vector from GlobalAveragePooling2D: h(x) in R^1280
  # Mean Activation Vectors (MAVs): mu_c in R^1280 computed over correctly classified train samples
  # Distances: Euclidean distance ||h(x) - mu_c||_2
  # Weibull fitting: scipy.stats.weibull_min.fit(tail_dists, floc=0) for eta = 20 largest distances

  # Rank-weight calculation at test inference:
  # sorted_classes: classes ranked by descending logit values
  # alpha = 2
  for rank_idx, c in enumerate(sorted_classes[:alpha]):
      # rank_idx = 0 for top class, rank_idx = 1 for second class
      dist = np.linalg.norm(features - mavs[c])
      omega_k = scipy.stats.weibull_min.sf(dist, shape, loc=0, scale=scale)
      alpha_weight = 1.0 - (rank_idx / float(alpha)) * (1.0 - omega_k)
      weights[c] = alpha_weight
  ```
- **Manuscript Formulation (`research_paper/manuscript/sections/04_methodology.tex`, Eq. 146–149):**
  $$w_{c_r} = 1.0 - \frac{r - 1}{\alpha} (1.0 - \omega_r(x))$$
  where $r \in \{1, \dots, \alpha\}$ denotes 1-based class rank.
- **Audit Finding:**
  For the top-predicted class ($r = 1$, corresponding to `rank_idx = 0`), the factor $\frac{r-1}{\alpha} = \frac{0}{2} = 0$, which yields $w_{c_1} \equiv 1.0$ regardless of the Weibull survival probability $\omega_1(x)$. Only the second-ranked class ($r = 2$, `rank_idx = 1`) receives logit discounting: $w_{c_2} = 1.0 - 0.5(1.0 - \omega_2(x))$. Furthermore, distance modeling operates on the 1280-D global pooled embedding rather than spatial activation maps. The manuscript now explicitly describes this implementation as a *modified OpenMax-style heuristic*, accurately reflecting the codebase without modifying any experimental results.

### 2.2. ODIN-Style Perturbation Variant
- **Benchmark Code (`scripts/run_stage4_1_benchmark.py`, L217–231):**
  ```python
  # T_odin = 1000.0, eps_odin = 0.0014
  with tf.GradientTape() as tape:
      tape.watch(batch_x)
      b_feats = base_model(batch_x, training=False)
      b_l = head_model(b_feats, training=False)
      s_l = b_l / T_odin
      max_s_l = tf.reduce_max(s_l, axis=1)  # Target is max temperature-scaled logit!
  grads = tape.gradient(max_s_l, batch_x)
  p_imgs = batch_x - eps_odin * tf.sign(-grads)  # Equals batch_x + eps_odin * tf.sign(grads)
  p_imgs = tf.clip_by_value(p_imgs, -1.0, 1.0)
  ```
- **Manuscript Formulation (`research_paper/manuscript/sections/04_methodology.tex`, Eq. 103–105):**
  $$x_{\text{perturbed}} = \operatorname{clip}\left( x + \varepsilon_{\text{ODIN}} \cdot \operatorname{sign}\left( \nabla_x \max_{k} \frac{z_k(x)}{T_{\text{ODIN}}} \right), \; -1.0, \; 1.0 \right)$$
- **Audit Finding:**
  Canonical ODIN (Liang et al., 2018) perturbs inputs using the cross-entropy gradient with respect to predicted softmax probability $-\log S_{\hat{y}}(x; T)$. The benchmark implementation perturbs along the gradient of the maximum temperature-scaled logit $\max_k z_k/T$. The manuscript now accurately specifies this formulation as an *ODIN-style perturbation variant*, noting the exact gradient target and the $[-1.0, 1.0]$ clipping bounds matching MobileNetV2 preprocessing.

### 2.3. Dual-Gate Operational Cascade vs. Continuous Linear Margin Proxy
- **Benchmark Code (`scripts/run_stage4_1_benchmark.py`, L330–350 & Evaluation Scripts):**
  - Discrete Decision Rule:
    ```python
    accept = (energy_score >= tau_energy) and (msp_score >= tau_msp)
    ```
    where $\tau_E = 0.918451$ and $\tau_M = 0.582610$.
  - Continuous Proxy for ROC Computation:
    ```python
    proxy_score = (energy_score - tau_energy) + (msp_score - tau_msp)
    ```
- **Manuscript Formulation (`research_paper/manuscript/sections/04_methodology.tex`, Eq. 171–177, 187):**
  - Discrete rule:
    $$\operatorname{ACCEPT}(x) \iff S_{\text{Energy}}(x) \ge \tau_E \;\land\; S_{\text{MSP}}(x) \ge \tau_M$$
  - Exploratory continuous linear margin proxy:
    $$S_{\text{proxy}}(x) = (S_{\text{Energy}}(x) - \tau_E) + (S_{\text{MSP}}(x) - \tau_M)$$
- **Audit Finding:**
  The manuscript and results table (`05_results.tex`, Table 8) now maintain complete transparency: Table 8 labels the detector row as `Dual-Gate (Proxy)`. The text explicitly explains that because Energy scores (range $[0, 10]$) and MSP scores (range $(1/6, 1]$) have disparate numerical scales, the linear proxy is unweighted and scale-dependent. All operational metrics (UFAR, UFAR-Fresh, KRR, Retention) are strictly derived from the discrete Boolean conjunction.

### 2.4. Operating Threshold Calibration via Order Statistics
- **Validation Dataset:** $N_{\text{val}} = 227$ raw images (`FINAL_GROUP_VAL_V4_1.csv`, `is_raw == 1`).
- **Single-Gate Calibration:**
  - 12th smallest order statistic $s_{(12)}$ (0-based index 11).
  - Rejection count: $11$ samples ($S < s_{(12)}$).
  - Accepted count: $216$ samples ($S \ge s_{(12)}$).
  - Empirical in-distribution coverage: $216 / 227 = 95.1542\%$.
  - Calibrated values: $\tau_{\text{MSP}} = 0.700580$, $\tau_{\text{Energy}} = 1.054579$, $\tau_{\text{ODIN}} = 0.167164$, $\tau_{\text{Maha}} = -65.133230$, $\tau_{\text{OpenMax}} = 0.778938$.
- **Dual-Gate Joint Calibration via Inclusion--Exclusion:**
  - Individual thresholds relaxed to 7th smallest order statistic $s_{(7)}$ (0-based index 6):
    - Gate 1 (Energy): $\tau_E = 0.918451$, rejecting $|R_1| = 6$ samples.
    - Gate 2 (MSP): $\tau_M = 0.582610$, rejecting $|R_2| = 6$ samples.
  - Overlap: Exactly $|R_1 \cap R_2| = 1$ sample falls below both thresholds simultaneously.
  - Total union: $|R_{\text{union}}| = |R_1| + |R_2| - |R_1 \cap R_2| = 6 + 6 - 1 = 11$.
  - Accepted count: $227 - 11 = 216$, exactly matching the $95.1542\%$ empirical validation coverage.
  - Exact 95% Clopper-Pearson interval for $216/227$: $[91.43\%, 97.60\%]$.

---

## 3. Architecture & Checkpoint Provenance Audit

| Parameter | Audited Specification | Forensic Verification Method | Status |
| :--- | :--- | :--- | :---: |
| **Backbone Architecture** | MobileNetV2 (Sandler et al., 2018 [7]) | Verified via Python/Keras inspection of checkpoint | **VERIFIED** |
| **Convolutional Stages** | 1 initial standard $3 \times 3$ conv + 17 bottleneck blocks (1 initial inverted bottleneck + 16 inverted residual blocks with expansion 6) | Exact layer count: 155 layer operations in functional model graph | **VERIFIED** |
| **Embedding Dimension** | $D = 1280$ (GlobalAveragePooling2D) | Tensor shape `(None, 1280)` verified | **VERIFIED** |
| **Classification Head** | Dropout ($p = 0.3$), Dense($6$, activation='softmax') | Layer inspection of head sub-model | **VERIFIED** |
| **Target Label Space** | $K = 6$: fresh/rotten apple, banana, orange | Label index mapping in `run_stage4_1_benchmark.py` | **VERIFIED** |
| **Checkpoint File** | `MODEL_B_V4_1_CHECKPOINT.keras` | File exists in workspace root | **VERIFIED** |
| **Cryptographic Hash** | `SHA-256: 4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` | Computed via Python hashlib / terminal `sha256sum` | **VERIFIED** |
| **Inference Mode** | Strictly frozen (`training=False`) | `base_model(batch_x, training=False)` in benchmark runner | **VERIFIED** |
| **Input Preprocessing** | Resize $224 \times 224$, normalize to $[-1.0, 1.0]^3$ | `tf.keras.applications.mobilenet_v2.preprocess_input` | **VERIFIED** |

---

## 4. Evaluation Metrics & Wording Bounds Audit

### 4.1. Retrospective FPR@95 vs. AUROC
- **AUROC:** Defined as the threshold-independent area under the receiver operating characteristic curve with out-of-distribution instances designated as the positive class ($y_{\text{ood}} = 1$) and in-distribution knowns as negative ($y_{\text{id}} = 0$). With detector score $S(x)$ oriented towards ID, the anomaly score is $-S(x)$.
- **Retrospective FPR@95:** The false positive rate (proportion of OOD images incorrectly accepted) when threshold $\tau_{95}^{\text{test}}$ is selected retrospectively on the test set to achieve 95.0% true positive rate (known retention) on $\mathcal{D}_{\text{id}}$.
- **Audit Clarification:** The text explicitly notes that FPR@95 is a retrospective operating-point metric tuned to the evaluated partition, distinct from threshold-free AUROC and prospective operational metrics.

### 4.2. Operational UFAR-Fresh Reframing
- **Preliminary Phrasing:** Described as "Catastrophic Food Safety" failure.
- **Corrected Phrasing:** Reframed strictly as an image-level produce routing outcome: the proportion of out-of-distribution image records accepted and assigned to a commercial Fresh class ($\hat{y}(x) \in \{0, 1, 2\}$).
- **Food Safety Disclaimer:** The manuscript explicitly disclaims that this represents verified biological food safety, toxicological certification, or commercial quality assurance compliance.

### 4.3. Auxiliary Metrics
- Exploratory diagnostics computed during benchmarking (AUPR-IN, AUPR-OUT, and OSCR) are documented as preserved in `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`, without cluttering the primary operational analysis.

---

## 5. Statistical Reporting & Non-Independence Bounds Audit

1. **Bootstrap Parameters:**
   - Resamples: $B = 1,000$ with replacement.
   - Seed: `seed=42`.
   - Method: Empirical percentile method ($\text{CI}_{95} = [\hat{\theta}^*_{(25)}, \hat{\theta}^*_{(975)}]$).
2. **Resampling Unit & Stratification:**
   - Resampling unit is strictly an individual image record.
   - Stratification: stratified by class on closed-set knowns; stratified jointly across ID reference and OOD cohort by species and condition labels on open-set cohorts.
3. **Statistical Conditioning:**
   - Confidence intervals are conditional on image-level exchangeability; images from web repositories cannot be assumed to represent independent biological specimens.
   - FruitVision Known (Partition B, $N_{\text{id}} = 4,157$) is shared across Cohorts A, B, and C; confidence intervals across these cohorts share a common reference population and are not statistically independent replications.
4. **Descriptive Comparison of Domain Shift:**
   - The 28.56 percentage-point difference between Partition A ($96.92\%$ [94.71\%, 98.68\%]) and Partition B ($68.36\%$ [67.20\%, 69.40\%]) displays non-overlapping 95% bootstrap percentile intervals, reflecting substantial descriptive separation without asserting formal inferential hypothesis testing.

---

## 6. Figure 1 & Visual Artifacts Audit

- **Figure Reference:** typeset as **Figure 1** in `main.pdf` (first visual figure in document).
- **Vector PDF:** `research_paper/figures/figure_02_pipeline.pdf` (mirrored in `research_paper/manuscript/figures/figure_02_pipeline.pdf`).
- **High-Resolution PNG:** `research_paper/figures/figure_02_pipeline.png` (mirrored in `research_paper/manuscript/figures/figure_02_pipeline.png`).
- **Audit of Pipeline Diagram Contents:**
  - Removed outdated auxiliary metrics (`AUPR-IN / AUPR-OUT`, `OSCR`).
  - Labeled `AUROC (Threshold-Independent)` and `Retrospective FPR@95 (Post-Hoc)`.
  - Backbone box correctly displays `17 Bottleneck Blocks (155 layers)`.
  - Scorer boxes correctly display `OpenMax (Mod.): S_OM = 1 - P_0` and `ODIN-Style: logit perturb`.
  - Operational metrics box displays `UFAR-Fresh (Fresh Class Accept)` (purged "Catastrophic" language).

---

## 7. Status of Manuscript Sections Across Entire Workspace

To maintain absolute research integrity, the current completion status of all manuscript sections in `research_paper/manuscript/` is summarized below:

| Section | Title | File Path | Status | Word Count / Content Notes |
| :---: | :--- | :--- | :---: | :--- |
| **—** | **Frontmatter & Abstract** | `main.tex` | Complete | Procedia template, 24 verified references in `references.bib` |
| **1** | **Introduction** | `sections/01_introduction.tex` | **Audited & Synchronized** | Comprehensive 4-stage failure narrative; matches empirical metrics |
| **2** | **Related Work** | `sections/02_related_work.tex` | **Audited & Synchronized** | SOTA benchmarking matrix; 5 thematic subsections |
| **3** | **Dataset Census & Experimental Design** | `sections/03_dataset_and_experimental_design.tex` | **Audited & Synchronized** | 13,465 evaluation census; pHash duplicate exclusion methodology |
| **4** | **Methodology** | `sections/04_methodology.tex` | **Audited & Synchronized** | Frozen MobileNetV2, 5 detectors, Dual-Gate cascade, order statistics |
| **5** | **Results** | `sections/05_results.tex` | **Partial (In Progress)** | Contains Subsection 5.6 (Table 8: pHash sensitivity table with `Dual-Gate (Proxy)`). Subsections 5.1–5.5 pending drafting. |
| **6** | **Discussion** | `sections/06_discussion.tex` | **Pending / Stub** | Pending drafting after Section 5 completion |
| **7** | **Limitations & Failure Analysis** | `sections/07_limitations.tex` | **Pending / Stub** | Pending drafting after Section 5 completion |
| **8** | **Conclusion** | `sections/08_conclusion.tex` | **Pending / Stub** | Pending drafting after Section 5 completion |

> **Research Integrity Declaration:** While Sections 1 through 4 are fully drafted, verified against code, and audited, the overall manuscript remains an active revision project. Sections 5 through 8 must be drafted and audited in subsequent passes before the manuscript can be submitted.
