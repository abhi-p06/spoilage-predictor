# STAGE 4.1.2 — FINAL SCIENTIFIC CLAIMS AND METHODOLOGY AUDIT

**Document Type:** Formal Scientific Integrity & Claims Ledger Audit  
**Auditor:** Independent Research Methodologist & Scientific Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** COMPLETED — CONDITIONAL GO FOR MANUSCRIPT SUBMISSION  

---

## 1. Audit Scope and Objectives

This audit evaluates the scientific claims, methodological framing, statistical representations, and terminological integrity of the AgriRoute research project (`spoilage-predictor`). 

Following the completion of Stage 4.1.1 metric reconciliation and Stage 4.1.2 source-stratified decomposition, this audit reviews the entire empirical evidence base to ensure complete compliance with the publication standards of Elsevier's *Procedia Computer Science*.

---

## 2. Forensic Review of Methodological and Statistical Frameworks

### 2.1 Terminology Governance: Image Records vs. Biological Specimens
- **Prior Draft Issue:** Several preliminary tables and texts referenced "Specimen Count" when describing image datasets.
- **Audit Mandate:** Because computer vision datasets frequently capture multiple camera angles, lighting conditions, or video frames of the same underlying fruit specimens, image records cannot be assumed to be statistically independent biological units.
- **Enforced Correction:** All occurrences have been standardized to **"Image Count"** ($N$). Confidence intervals are explicitly documented as **conditional on image-level resampling exchangeability** and must not be described as establishing biological specimen-level variance.
- **Partition B Provenance:** Prior text informally cited FruitVision as the sole source of Partition B. The audit establishes that Partition B comprises **4,157 images from FruitVision** and **1,193 images from Sultana** ($N = 5,350$ total).

### 2.2 Reclassification of Unseen Cohorts: "Unseen-Species External Cohort"
- **Prior Draft Issue:** The designation "Pure Semantic Shift" was applied generically to Partition D1 ($N = 4,776$).
- **Audit Mandate:** In comparisons against Partition A (Kaggle studio data), Partition D1 introduces both semantic novelty (unseen species) and covariate/domain shift (different camera sensors, retail backgrounds, regional lighting). Applying the label "pure" is methodologically inaccurate when domain shifts are confounded.
- **Enforced Correction:** Replaced with **"Unseen-Species External Cohort"** in all contexts where dataset-source and semantic shifts are compounded. The label "within-repository semantic shift" is reserved strictly for source-stratified comparisons (e.g., Cohort A: FruitVision B vs. FruitVision D1).

---

## 3. Dual-Gate Cascade: Methodological Deconstruction

The audit examined the relationship between the operational Dual-Gate decision rule and its continuous proxy representation:

### 3.1 The Two Formulations
1. **Operational Discrete AND-Cascade (Deployment Gate):**
   $$\text{Decision}(x) = \begin{cases} \text{Accept (ID)}, & \text{if } S_{\text{Energy}}(x) \ge \tau_{E, 95} \land S_{\text{MSP}}(x) \ge \tau_{M, 95} \\ \text{Reject (OOD)}, & \text{otherwise} \end{cases}$$
   where $\tau_{E, 95} = 0.918451$ and $\tau_{M, 95} = 0.582610$, calibrated on the 227 raw validation images.
2. **Continuous Exploratory Proxy (Curve Tracing):**
   $$S_{\text{proxy}}(x) = \left(S_{\text{Energy}}(x) - \tau_{E, 95}\right) + \left(S_{\text{MSP}}(x) - \tau_{M, 95}\right)$$

### 3.2 Audit Findings on Dual-Gate:
- **Decision Boundary Incompatibility:** The discrete cascade defines a quadrant intersection in $\mathbb{R}^2$ ($\mathcal{A}_{\text{Cascade}} = \{s_E \ge \tau_E\} \cap \{s_M \ge \tau_M\}$), whereas the continuous proxy defines a linear half-space ($\mathcal{A}_{\text{Proxy}} = \{s_E + s_M \ge \tau_E + \tau_M\}$).
- **Scale Imbalance:** $S_{\text{Energy}}$ spans $[-4.8, 8.4]$ ($\sigma \approx 2.15$), while $S_{\text{MSP}}$ spans $[0.17, 1.0]$ ($\sigma \approx 0.18$). Because the Energy margin variance is $\sim 12\times$ larger, the proxy score correlates with Energy at **Spearman $\rho > 0.992$**.
- **Scientific Ruling:** The continuous proxy is **not** a novel standalone algorithm. It is an unweighted boundary-margin proxy used solely to generate continuous ROC and PR curves. The paper must present fixed-threshold operational metrics (UFAR, UFAR-Fresh, KRR) as the primary Dual-Gate results, citing continuous AUROC/OSCR with explicit proxy disclosures.

---

## 4. Coverage-Risk and Selective Classification Integrity

The audit reviewed the selective classification analysis across the 5,350 Partition B images:

### 4.1 Retrospective Diagnostic Nature
- **Audit Mandate:** Selecting the top $K\%$ highest-scoring test samples to construct a coverage-risk curve is a **retrospective diagnostic analysis**, not a prospective deployment calibration. In real-world operation, the system cannot rank test images relative to each other; it must apply pre-calibrated thresholds.
- **Enforced Correction:** The manuscript must clearly distinguish:
  1. **Prospective Operational Performance:** Fixed-threshold rejection calibrated strictly on Partition A validation data ($\tau_{95}^{\text{val}}$).
  2. **Retrospective Coverage-Risk Tradeoff:** Diagnostic demonstration that the model's confidence scores are monotonically well-ordered, reducing risk from $31.64\%$ at $100\%$ coverage down to $<3\%$ at $10\%$ coverage.
- **Dual-Gate Curve Identification:** The Dual-Gate coverage-risk curve must be explicitly described as proxy-margin based, as an AND-gate cascade does not produce a continuous 1D ranking curve without fixing one threshold or applying a scalar proxy.

---

## 5. Scientific Language and Observational Guardrails

To prevent unsupported causal claims, the audit enforces strict observational language across all text:

### Table 1: Permitted vs. Prohibited Phrasing in Manuscript

| Prohibited Unverified Phrasing | Enforced Observational Scientific Phrasing | Scientific Justification |
| :--- | :--- | :--- |
| *"RGB vision detects formaldehyde / chemical adulteration."* | *"Model evaluates dataset-labelled formalin-treatment condition."* | RGB sensors capture broadband visible light ($400\text{--}700\text{ nm}$) and cannot perform chemical spectroscopy. |
| *"UFAR-Fresh measures food-safety verification failure."* | *"UFAR-Fresh measures the proportion of OOD images accepted and assigned a Fresh model class."* | Food safety verification requires chemical/microbiological assays; model outputs are classification decisions. |
| *"Cellular autolysis was inhibited by cross-linking."* | *"Visual decay symptoms were absent in preserved specimens."* | Visual inspection cannot verify biochemical mechanisms without lab assays. |
| *"Russeting caused the 32.12% apple accuracy."* | *"Observed surface striations and specularity consistent with varietal russeting correlate with false-rot predictions."* | Attribution must be framed as an observational hypothesis, not an experimentally isolated causal factor. |
| *"Shared repository proves identical lighting/camera."* | *"Source stratification reduces cross-repository domain shifts, though intra-repository capture variations remain."* | Repositories collect images across multiple sessions, devices, and vendors. |

---

## 6. Comprehensive Claims and Evidence Ledger

Every quantitative claim intended for the manuscript has been cross-referenced against authoritative source files:

| Manuscript Claim | Exact Numerical Value | Primary Source File | Verification Status |
| :--- | :---: | :--- | :---: |
| **Partition A Top-1 Accuracy** | $96.92\%$ (220/227) | `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` | **VERIFIED** |
| **Partition A Macro-F1** | $96.87\%$ [94.11%, 98.81%] | `STAGE4_1_1_RECONCILED_CONFIDENCE_INTERVALS.csv` | **VERIFIED** |
| **Partition B Top-1 Accuracy** | $68.36\%$ (3,657/5,350) | `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` | **VERIFIED** |
| **Partition B Macro-F1** | $67.28\%$ [66.12%, 68.39%] | `STAGE4_1_1_RECONCILED_CONFIDENCE_INTERVALS.csv` | **VERIFIED** |
| **Partition B Fresh Apple Recall** | $32.12\%$ (310/965) | `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` | **VERIFIED** |
| **Partition B Rotten Banana Recall**| $99.40\%$ (826/831) | `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` | **VERIFIED** |
| **Within-FruitVision Semantic AUROC** | $81.57\%$ (Energy) | `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` | **VERIFIED** |
| **Within-FruitVision Formalin AUROC** | $53.13\%$ (Energy) | `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` | **VERIFIED** |
| **Within-FruitVision Formalin UFAR-Fresh**| $42.83\%$ (Dual-Gate) | `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` | **VERIFIED** |
| **Within-Sultana Semantic AUROC** | $67.52\%$ (Energy) | `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` | **VERIFIED** |
| **Maximum Sensitivity Shift** | $0.70$ pp (AUPR-OUT) | `STAGE4_1_1_RECONCILED_SENSITIVITY_ANALYSIS.csv` | **VERIFIED** |
| **Dual-Gate AUROC Sensitivity Shift** | $0.00$ pp (A vs D2) | `STAGE4_1_1_RECONCILED_SENSITIVITY_ANALYSIS.csv` | **VERIFIED** |

---

## 7. Final Manuscript Submission Verdict

### **VERDICT: CONDITIONAL GO**

The AgriRoute manuscript revision is **authorized to proceed to final publication preparation**, subject to incorporating the following mandatory revisions:
1. **Use Reconciled Tables Exclusively:** Embed numbers strictly from `STAGE4_1_1_RECONCILED_PARTITION_METRICS.csv` and `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`.
2. **Transparent Domain Reporting:** Report the drop from $96.92\%$ to $68.36\%$ prominently as an empirical demonstration of why real-world supply chain deployments require open-set abstention.
3. **Dual-Gate Framing:** Maintain the Dual-Gate Cascade as an operational discrete filter; cite continuous AUROC/OSCR with the boundary-margin proxy caveat.
4. **Enforce Observational Language:** Adhere strictly to the phrasing rules in Table 1 (no chemical detection or causal biological assertions).
5. **Traceability:** Maintain the Claims Ledger in all final submission artifacts.

