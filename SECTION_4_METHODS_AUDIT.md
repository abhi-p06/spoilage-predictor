# SECTION 4 AUDIT AND EVIDENCE RECONCILIATION REPORT
## Source-Stratified Evaluation of Out-of-Distribution Detection in Fruit-Quality Classification Under Species and Treatment-Labelled Shifts
### V4.2 Final Scientific Claim-Boundary and Audit Reconciliation Report

**Document Status:** Fully Reconciled, Formatted, and Code-Verified  
**Audit Date:** November 11, 2026 (V4.2 Final Claim-Boundary Pass)  
**Audited Files:**
- `research_paper/manuscript/sections/04_methodology.tex`
- `research_paper/manuscript/04_methodology.md`
- `research_paper/manuscript/sections/05_results.tex` (Subsections 5.1–5.5 fully drafted and audited)
- `research_paper/manuscript/05_results.md`
- `research_paper/manuscript/sections/06_discussion.tex` & `06_discussion.md`
- `research_paper/manuscript/sections/07_limitations.tex` & `07_limitations.md`
- `research_paper/manuscript/sections/08_conclusion.tex` & `08_conclusion.md`
- `research_paper/manuscript/main.tex` (Abstract qualified, double-blind anonymity enforced)
- `research_paper/manuscript/sections/01_introduction.tex` & `01_introduction.md`
- `research_paper/manuscript/sections/02_related_work.tex` & `02_related_work.md`
- `research_paper/manuscript/sections/03_dataset_and_experimental_design.tex` & `03_dataset_and_experimental_design.md`
- `research_paper/manuscript/main.pdf` (44 pages, compiled via Tectonic)
- `research_paper/figures/figure_02_pipeline.pdf` & `.png` (Figure 1 in compiled PDF)
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

A targeted scientific consistency pass was conducted across the AgriRoute V4.1 manuscript and audit infrastructure. Ten specific scientific, statistical, and architectural consistency requirements were audited, independently calculated, and verified against canonical project assets.

### Status of the Ten Consistency Directives

| Area | Topic | Prior Formulation / Discrepancy | Corrective Action Taken & Code Parity | Audit Status |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **FPR@95 Class Orientation** | Section 4.6.2 erroneously stated OOD was positive ($y_{\text{ood}} = 1$) in FPR@95; Section 4.1 grouped FPR@95 as threshold-free. | Reconciled: In FPR@95, ID is the positive class ($\text{TPR}_{\text{id}} \ge 0.95$), OOD is the negative class, and FPR is the proportion of negative (OOD) records accepted as ID. In AUROC, OOD is positive ($y_{\text{ood}} = 1$), ID is negative, and anomaly score is $-S(x)$. Section 4.1 correctly distinguishes threshold-independent AUROC from retrospective operating-point FPR@95. | **VERIFIED** |
| **2** | **Clopper-Pearson Interval Recalculation** | Previously reported interval was $[91.43\%, 97.60\%]$. | Independently recalculated exact two-sided 95% Clopper-Pearson binomial interval for $k=216$ successes in $n=227$ trials using `scipy.stats.beta`: $[91.50\%, 97.56\%]$ (exact: $[91.4951\%, 97.5565\%]$). Synchronized across `.tex`, `.md`, and audit ledgers. Preserved $N_{\text{val}}=227$, rejected=11, accepted=216, coverage=95.1542%, $\tau_E=0.918451$, $\tau_M=0.582610$. | **VERIFIED** |
| **3** | **pHash Sensitivity Cohort Sizes** | Table 8 listed only static $N_{\text{id}} = 4,157$ and omitted intermediate Tier 1 counts. | Reconciled against canonical `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv`: Cohort A ($N_{\text{id}}: 4,157 \to 4,146 \to 4,140$; $N_{\text{ood}}: 2,776 \to 2,762 \to 2,746$); Cohort B ($N_{\text{id}}: 4,157 \to 4,146 \to 4,140$; $N_{\text{ood}}: 1,917 \to 1,906 \to 1,901$); Cohort C ($N_{\text{id}}: 4,157 \to 4,146 \to 4,140$; $N_{\text{ood}}: 1,195 \to 1,175 \to 1,175$); Cohort D ($N_{\text{id}}: 1,193$; $N_{\text{ood}}: 2,000$ invariant). Table 8 formatted to show full progression. | **VERIFIED** |
| **4** | **Standardized Method Naming** | Inconsistent method naming across abstract, introduction, and results tables. | Standardized nomenclature: MSP, Energy, ODIN-style perturbation variant (or `ODIN (Variant)`), Ledoit-Wolf Mahalanobis (or `LW-Mahalanobis`), and modified OpenMax-style heuristic (or `OpenMax (Mod.)`). Synchronized in Abstract, RQ2 (§1.2), §4.1, Figure 1 caption, Table 5, Table 8, and Section 5 results narrative. | **VERIFIED** |
| **5** | **Energy–MSP Proxy Scale Statement** | Described Energy score as having a "typical range $[0, 10]$" (theoretically unsupported). | Clarified that theoretical Energy score $S_{\text{Energy}}(x) = \operatorname{logsumexp}(z(x))$ is mathematically unbounded on $(-\infty, +\infty)$, with an observed empirical range of $[-1.753, 5.264]$ across 13,465 evaluation images, whereas MSP lies strictly in $[1/K, 1]$ (for $K=6$, $[1/6, 1]$; empirically $[0.231, 1.000]$). Additive proxy remains scale-dependent and exploratory. | **VERIFIED** |
| **6** | **Abstract Metric Qualification** | Abstract stated "with an operational false acceptance rate of 13.18\%" without specifying detector. | Qualified in Abstract: explicitly stated as the "standalone Energy operational false acceptance rate of 13.18\% under its locked validation threshold", distinguishing it from the Dual-Gate UFAR (16.07\%). Verified values retained. | **VERIFIED** |
| **7** | **Section 5 Full Results Drafting** | Subsections 5.2–5.5 were previously in progress. | Fully drafted and audited: Subsection 5.1 (Sensitivity Table 8), Subsection 5.2 (Closed-set domain degradation Table 9, confusion modes Table 10), Subsection 5.3 (Source-stratified OOD Table 11 across Cohorts A–D), Subsection 5.4 (Operational decision performance Table 12), Subsection 5.5 (Uncertainty and RQ consolidation). | **VERIFIED** |
| **8** | **Progress Log Synchronization** | Progress log stated earlier page counts and partial statuses. | Updated progress log with comprehensive milestones: 44 compiled pages, Figure 1 (Methodology Pipeline), complete drafting of Sections 1–8, resolved cross-references, and zero unresolved markers. | **VERIFIED** |
| **9** | **Experimental Integrity** | Constraint on retraining, inference reruns, threshold retuning, or synthetic data. | Checkpoint SHA-256 confirmed unchanged (`4a12f354...b6b4`). Zero weights altered; zero thresholds modified; zero synthetic runs; zero numbers altered. | **VERIFIED** |
| **10** | **Build & Visual Verification** | Verification of compilation without overfull hboxes or broken citations. | Tectonic compiled canonical `main.tex` with Exit code 0, 44 pages, zero overfull hboxes in Sections 4 & 5, zero unresolved citations, zero literal `??` references, and zero `TODO`/`TBD` tokens. All 44 pages rendered to PNG for visual inspection. | **VERIFIED** |

---

## 2. Forensic Code-to-Manuscript Verification

### 2.1. Exact Clopper-Pearson Calculation
- **Script Verification:** Executed Python script using `scipy.stats.beta`:
  - $n = 227$, $k = 216$, $\alpha = 0.05$.
  - Lower bound: $I_{\alpha/2}^{-1}(k, n - k + 1) = \text{beta.ppf}(0.025, 216, 12) = 0.914951478\dots \to 91.50\%$
  - Upper bound: $I_{1 - \alpha/2}^{-1}(k + 1, n - k) = \text{beta.ppf}(0.975, 217, 11) = 0.975564993\dots \to 97.56\%$
- **Manuscript Parity:** Both `04_methodology.tex` (L231) and `04_methodology.md` (L157) state: `[91.50%, 97.56%] (exact: [91.4951%, 97.5565%])`.

### 2.2. pHash Sensitivity Sample Counts Parity
- **Provenance Verification:** Audited `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv`:
  - FruitVision Knowns reference exclusions: $4,157 - 11 = 4,146$ in Tier 1; $4,146 - 6 = 4,140$ in Tier 2.
  - Cohort A OOD exclusions: $2,776 - 14 = 2,762$ in Tier 1; $2,762 - 16 = 2,746$ in Tier 2.
  - Cohort B OOD exclusions: $1,917 - 11 = 1,906$ in Tier 1; $1,906 - 5 = 1,901$ in Tier 2.
  - Cohort C OOD exclusions: $1,195 - 20 = 1,175$ in Tier 1; $1,175 - 0 = 1,175$ in Tier 2.
  - Cohort D (Sultana): Zero pHash collisions at $r \le 8$; sample counts remain completely invariant.
- **Table 8 Parity:** Table 8 in `05_results.tex` and `05_results.md` explicitly reports the exact $N_{\text{id}}$ and $N_{\text{ood}}$ sample counts across all three tiers.

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

## 4. Status of Manuscript Sections Across Entire Workspace

To maintain absolute research integrity, the current completion status of all manuscript sections in `research_paper/manuscript/` is summarized below:

| Section | Title | File Path | Status | Content Notes |
| :---: | :--- | :--- | :---: | :--- |
| **—** | **Frontmatter & Abstract** | `main.tex` | Complete & Synchronized | Procedia template; double-blind author blocks; qualified standalone Energy UFAR (13.18\%); standardized method naming |
| **1** | **Introduction** | `sections/01_introduction.tex` | **Audited & Synchronized** | 4-stage failure narrative; RQ2 standardized with implementation variant names |
| **2** | **Related Work** | `sections/02_related_work.tex` | **Audited & Synchronized** | SOTA benchmarking matrix; 5 thematic subsections |
| **3** | **Dataset Census & Experimental Design** | `sections/03_dataset_and_experimental_design.tex` | **Audited & Synchronized** | 13,465 evaluation census; pHash duplicate exclusion methodology |
| **4** | **Methodology** | `sections/04_methodology.tex` | **Audited & Synchronized** | Frozen MobileNetV2, 5 detectors + implementation variants, Dual-Gate cascade, order statistics, theoretical MSP range $[1/K, 1]$, FPR@95 positive class |
| **5** | **Results** | `sections/05_results.tex` | **Audited & Synchronized** | Full empirical results (§5.1--§5.5): Table 8 (pHash sensitivity), Table 9 (closed-set across domains), Table 10 (Partition B class-wise confusion), Table 11 (OOD discrimination across 4 cohorts), Table 12 (operational decision performance) |
| **6** | **Discussion** | `sections/06_discussion.tex` | **Audited & Synchronized** | 5 subsections: domain collapse, visual limits on chemical fixatives, economic abstention cost (42.43\% KRR), architectural comparisons, multi-modal recommendations |
| **7** | **Limitations & Threats to Validity** | `sections/07_limitations.tex` | **Audited & Synchronized** | 8 mandated areas: specimen independence, unverified treatment labels, within-repository variation, external acquisition, bootstrap conditioning and independent cohort resampling, lack of physical sorting, implementation variants, proxy scale dependence |
| **8** | **Conclusion** | `sections/08_conclusion.tex` | **Audited & Synchronized** | Explicit, evidence-bounded resolutions to RQ1, RQ2, and RQ3; disclaimers of algorithmic novelty and deployment claims; prospective multi-sensor directions |

---

## 5. Current Manuscript Summary & Remaining Work

- **Compiled PDF Artifact:** 44 pages (`main.pdf`, Procedia Computer Science format, $192\text{ mm} \times 262\text{ mm}$).
- **Sections Completed:** Sections 1–8 fully drafted, verified, and synchronized across LaTeX source and Markdown mirrors.
- **Results Subsections:** Subsections 5.1–5.5 fully drafted and audited.
- **Pipeline Diagram:** Figure 1 (Methodology Pipeline) fully synchronized and numbered.
- **Theoretical MSP Range:** $[1/K, 1]$ (empirically $[0.231, 1.000]$).
- **Cross-Reference Scan:** Zero unresolved literal references (`Section ??` = 0; `??` = 0; `TODO` = 0; `TBD` = 0).
- **Remaining Work:** Author review, final source verification, and venue compliance checks. The paper is **not marked submission-ready** until final author sign-off.
