# Conference Submission Summary & Scientific Integrity Report
**Target Venue:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026)  
**Publication:** Elsevier *Procedia Computer Science* (`elsarticle`, 3p, single-column)  
**Document Title:** *Source-Stratified Evaluation of Out-of-Distribution Detection in Fruit-Quality Classification Under Species and Treatment-Labelled Shifts*  
**Date:** November 11, 2026  
**Status:** **NOT MARKED SUBMISSION-READY** (Requires human author review and venue compliance sign-off)

---

## 1. Executive Summary & Page Count Audit

| Metric | Target / Constraint | Realized Output | Compliance Status |
| :--- | :--- | :--- | :--- |
| **Page Count** | Strict Minimum: 3 pages<br>Strict Maximum: 10 pages | **Exactly 10 pages** | **FULLY COMPLIANT** (0 overlength fee) |
| **Page 10 Headroom** | Must terminate on or before Page 10 | Content terminates at $y = 561.0\text{ pt}$ / $742.7\text{ pt}$ | **181.7 pt safe margin** (~24.5% remaining blank space) |
| **Template & Typography** | `\documentclass[3p,times,procedia]{elsarticle}` with `ecrc` | Standard Elsevier Procedia 3p single-column geometry | **COMPLIANT** |
| **Citation Style** | Vancouver numbered format (`elsarticle-num.bst`) | Numbered `[1]--[23]`, sorted and compressed | **COMPLIANT** |
| **Double-Blind Redaction** | Peer review anonymity required | Author names, affiliations, correspondence redacted | **COMPLIANT** |
| **Unresolved Cross-Refs** | Zero `??`, zero `TODO`/`TBD`, zero `[?]` | 0 occurrences across all 10 pages | **COMPLIANT** |

---

## 2. Exact List of Files Modified

All edits were strictly confined to the conference submission workspace [`research_paper/submission_10_pages/`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/); the 44-page thesis-style manuscript in [`research_paper/manuscript/`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/manuscript/) was **100% untouched**:

1. [`research_paper/submission_10_pages/main.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/main.tex): Replaced prescriptive multimodal sensing claim with prospective wording in the Abstract.
2. [`research_paper/submission_10_pages/sections/01_introduction.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/sections/01_introduction.tex): Corrected Cohort B OOD discrimination ceiling to AUROC $\le 58.77\%$.
3. [`research_paper/submission_10_pages/sections/02_related_work.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/sections/02_related_work.tex): Corrected MobileNetV2 parameter count to approximately $2.26\times 10^6$ trainable parameters; replaced input marginal density claim with approved Energy score formulation.
4. [`research_paper/submission_10_pages/sections/03_dataset_and_experimental_design.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/sections/03_dataset_and_experimental_design.tex): Reconciled upstream published archives vs evaluated partition census for FruitVision and Sultana; corrected pHash scan radii vs exclusion tiers; updated Cohort D descriptor in Table 1.
5. [`research_paper/submission_10_pages/sections/04_methodology.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/sections/04_methodology.tex): Corrected classification head dropout to $p = 0.3$ (verified from checkpoint config); updated Table 2 Energy note and Section 4.3 text to remove unconstrained density estimation claims.
6. [`research_paper/submission_10_pages/sections/05_results.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/sections/05_results.tex): Reconciled all AUROC and FPR@95 values in Table 4 against `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`; corrected Fresh Apple russeting text to untested observational hypothesis; updated Cohort D header and narrative; reconciled pHash sensitivity text to 0.22 pp shift in Cohort C Mahalanobis (80.08% $\to$ 79.86%).
7. [`research_paper/submission_10_pages/sections/06_discussion_limitations.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/sections/06_discussion_limitations.tex): Corrected russeting text, treatment-cohort boundary language, prospective multimodal sensing phrasing, and Limitation 1 pHash tier exclusion details.
8. [`research_paper/submission_10_pages/sections/07_conclusion.tex`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/sections/07_conclusion.tex): Bound RQ1 to untested observational hypothesis; updated RQ2 comparative wording ("achieve higher AUROC point estimates than") and Cohort B bounds; adjusted final multimodal sentence to prospective evaluation.
9. [`research_paper/submission_10_pages/CONFERENCE_SUBMISSION_SUMMARY.md`](file:///Users/abby/Desktop/spoilage-predictor/research_paper/submission_10_pages/CONFERENCE_SUBMISSION_SUMMARY.md): Reconciled full evidence report.

---

## 3. Dataset Source-Total and Partition Census Reconciliation

Reconciled against `STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv` and `STAGE4_DATASET_PARTITION_MANIFEST.csv`:

| Repository | Published Raw Archive | Excluded Duplicates | Evaluated Records | Partition Allocation |
| :--- | :---: | :---: | :---: | :--- |
| **FruitVision** \cite{bijoy2025fruitvision} | 10,154 | 109 (hash collisions) | **10,045** | Part.\ B: 4,157; Part.\ C: 1,917; Part.\ D1: 2,776; Part.\ D2: 1,195 |
| **Sultana et al.** \cite{sultana2022extensive} | $\approx 3,200$ | 7 (Orange Fresh duplicates) | **3,193** | Part.\ B: 1,193; Part.\ D1: 2,000 |
| **Kaggle Primary** | 2,043 total (1,816 syn.) | 0 (raw test partition) | **227** | Part.\ A: 227 (`is_raw == 1`) |
| **Total Benchmark** | --- | --- | **13,465** | Partition sum: $227 + 5,350 + 1,917 + 4,776 + 1,195 = 13,465$ |

**Source Sum:** $10,045\text{ (FruitVision)} + 3,193\text{ (Sultana)} + 227\text{ (Kaggle)} = \mathbf{13,465}$.  
**Partition Sum:** $227\text{ (A)} + 5,350\text{ (B)} + 1,917\text{ (C)} + 4,776\text{ (D1)} + 1,195\text{ (D2)} = \mathbf{13,465}$.

---

## 4. Full Table 4 Metric Reconciliation Status

All values in Table 4 were audited against canonical register `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` and Table 11 of the approved 44-page manuscript:

| Cohort | Detection Algorithm | Previous Incorrect Value | Canonical Register Value | Reconciliation Status |
| :--- | :--- | :---: | :---: | :---: |
| **Cohort A** | MSP AUROC / FPR@95 | 72.42 / 82.53 | **72.42 / 82.74** | Reconciled to canonical |
| | Energy AUROC / FPR@95 | 81.57 / 68.84 | **81.57 [80.81, 82.38] / 68.84** | Verified |
| | ODIN Variant AUROC / FPR@95 | 72.30 / 83.18 | **72.30 / 87.43** | Reconciled to canonical |
| | LW-Mahalanobis AUROC / FPR@95 | 81.41 / 79.00 | **81.41 / 79.00** | Verified |
| | Modified OpenMax AUROC / FPR@95 | 72.46 / 82.53 | **72.46 / 91.28** | Reconciled to canonical |
| | Dual-Gate Proxy AUROC / FPR@95 | 80.93 / 69.27 | **80.93 [80.13, 81.72] / 69.27** | Verified |
| **Cohort B** | MSP AUROC / FPR@95 | 58.77 / 91.08 | **58.77 / 92.85** | Reconciled to canonical |
| | Energy AUROC / FPR@95 | 53.13 / 93.95 | **53.13 [52.16, 54.09] / 94.42** | Reconciled to canonical |
| | ODIN Variant AUROC / FPR@95 | 56.73 / 91.81 | **56.73 / 91.13** | Reconciled to canonical |
| | LW-Mahalanobis AUROC / FPR@95 | 47.91 / 98.07 | **47.91 / 98.07** | Verified |
| | Modified OpenMax AUROC / FPR@95 | 55.35 / 95.20 | **55.35 / 95.20** | Verified |
| | Dual-Gate Proxy AUROC / FPR@95 | 53.96 / 93.53 | **53.96 [52.96, 54.91] / 94.16** | Reconciled to canonical |
| **Cohort C** | MSP AUROC / FPR@95 | 76.54 / 76.82 | **76.47 / 76.40** | Reconciled to canonical |
| | Energy AUROC / FPR@95 | 84.72 / 60.08 | **84.72 [83.85, 85.58] / 64.94** | Reconciled to canonical |
| | ODIN Variant AUROC / FPR@95 | 76.43 / 77.24 | **78.11 / 83.85** | Reconciled to canonical |
| | LW-Mahalanobis AUROC / FPR@95 | 84.85 / 69.87 | **80.08 / 78.49** | Reconciled to canonical |
| | Modified OpenMax AUROC / FPR@95 | 76.44 / 77.07 | **77.22 / 88.12** | Reconciled to canonical |
| | Dual-Gate Proxy AUROC / FPR@95 | 84.14 / 61.00 | **84.16 [83.28, 85.05] / 63.18** | Reconciled to canonical |
| **Cohort D** | MSP AUROC / FPR@95 | 59.77 / 94.75 | **59.77 / 94.30** | Reconciled to canonical |
| | Energy AUROC / FPR@95 | 67.52 / 86.85 | **67.52 [65.67, 69.25] / 83.50** | Reconciled to canonical |
| | ODIN Variant AUROC / FPR@95 | 59.85 / 94.70 | **60.02 / 94.25** | Reconciled to canonical |
| | LW-Mahalanobis AUROC / FPR@95 | 68.15 / 81.20 | **68.15 / 81.20** | Verified |
| | Modified OpenMax AUROC / FPR@95 | 60.10 / 94.50 | **64.38 / 94.75** | Reconciled to canonical |
| | Dual-Gate Proxy AUROC / FPR@95 | 66.86 / 87.75 | **66.68 [64.98, 68.38] / 84.60** | Reconciled to canonical |

---

## 5. pHash Methodology, Tiers, and Exclusion Reconciliation

Reconciled against `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv` and `research_audit/`:
- **Scan Radii:** Discrete cosine transform 64-bit pHash scanned across Hamming radii $r \in \{0, 4, 8\}$.
- **Evaluation Tiers (Exclusion Procedures):**
  - **Primary Cohort:** $N = 13,465$ records.
  - **Tier 1 (Cross-Partition Collision Exclusions):** $N = 13,409$ records, excluding **56 unique records** detected at $r \le 8$:
    - 11 shared FruitVision Known reference records.
    - 14 FruitVision D1 records.
    - 11 FruitVision C records.
    - 20 FruitVision D2 records.
    - 0 Sultana exclusions.
  - **Tier 2 (Intra-Partition Multi-Label Exclusions):** $N = 13,382$ records, excluding an **additional 27 records**:
    - 6 Partition B records.
    - 5 Partition C records.
    - 16 Partition D1 records.
- **Sensitivity Results & Ranking Invariance:**
  - Maximum observed AUROC change across all 24 configurations between Primary and Tier 2: **$0.22\text{ percentage points}$** (Ledoit--Wolf Mahalanobis in Cohort C: $80.08\% \to 79.86\%$).
  - Cohort A Energy: $81.57\% \to 81.55\% \to 81.46\%$.
  - Cohort B Energy: $53.13\% \to 53.16\% \to 53.19\%$.
  - Cohort D (Sultana): $0.00\text{ pp}$ change (0 collisions detected at $r \le 8$; completely invariant).
  - Relative detector rankings remain **strictly invariant** across all tiers in all cohorts.

---

## 6. Model Architecture & Checkpoint Verification

- **Checkpoint File:** `MODEL_B_V4_1_CHECKPOINT.keras`
- **SHA-256 Checksum:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Classification Head Dropout:** Verified directly from checkpoint JSON configuration:
  ```json
  {"class_name": "Dropout", "config": {"name": "top_dropout", "rate": 0.3}}
  ```
  Manuscript corrected from erroneous $p = 0.2$ to canonical **$p = 0.3$**.
- **Model Parameter Count:**
  - Base MobileNetV2 feature extractor: 2,257,984 parameters.
  - 6-class Dense classification head: $1,280 \times 6 + 6 = 7,686$ parameters.
  - Total model parameters: **2,265,670** (approximately **$2.26 \times 10^6$ trainable parameters**).
  - Manuscript corrected from ImageNet 1,000-class count ($3.4 \times 10^6$) to **$2.26 \times 10^6$**.

---

## 7. Scientific Claim-Boundary Corrections

1. **Energy Score Formulation:** Language claiming Energy aligns with the exact input marginal density $p(x)$ or calling it an unconstrained density estimator was replaced with:  
   *“The Energy score is a post-hoc logit-based OOD scoring function motivated by an energy-based formulation; it is not treated here as a calibrated estimate of the true input marginal density.”*
2. **Fresh Apple Russeting Texture:** Causal claims that surface irregularities are systematically confused with fungal decay lesions were replaced with an explicit untested visual hypothesis:  
   *“we present the correlation between natural surface striations, lenticel spots, and decay misclassifications strictly as an untested observational hypothesis, distinguishing qualitative visual inspection from causal evidence.”*
3. **Treatment-Labelled Produce (Cohort B):** Claims that formalin preserves turgor or pigmentation, that treated produce is visually indistinguishable from fresh fruit, or that RGB cannot detect treatments in general were removed. Replaced with cohort-specific wording:  
   *“highlights the challenge of identifying chemical treatment status from standard RGB imagery without independent biochemical assays... we report strictly that the evaluated post-hoc RGB detectors fail on this repository-assigned treatment cohort.”*
4. **Multimodal Sensing Claims:** Prescriptive conclusions (“Future post-harvest automation must transition toward multimodal architectures”) were replaced with prospective wording:  
   *“Future work could evaluate whether complementary sensing modalities improve screening under these dataset-reported condition shifts...”*
5. **Detector Comparisons:** Subjective terms like “superior separation” and “outperforms” were replaced with:  
   *“achieves a higher AUROC point estimate than”*.
6. **Cohort D Framing:** Renamed from “Cross-Source Semantic Degradation” and “Cross-source validation” to:  
   *“Sultana source-matched semantic-shift evaluation”*.

---

## 8. Preservation of Operational Screening Metrics & Thresholds

All operational thresholds and screening metrics were audited and preserved exactly:
- **Prospective Validation Calibration:**
  - Standalone Energy threshold: $\tau_E = 1.054579$
  - Dual-Gate thresholds: $\tau_E = 0.918451 \land \tau_M = 0.582610$
- **Operational Metrics (Table 5):**
  - Pooled Known-Class Rejection Rate (KRR): $42.43\%$ $[41.10, 43.76]$ ($2,270/5,350$ valid knowns rejected).
  - Retained Automated Sorting Decisions: $57.57\%$ $[56.24, 58.90]$ ($3,080/5,350$).
  - Cohort B Dual-Gate UFAR: $52.63\%$ $[50.81, 54.25]$ ($1,009/1,917$).
  - Cohort B Dual-Gate UFAR-Fresh: $42.83\%$ $[41.26, 44.34]$ ($821/1,917$ treatment-labelled produce routed into classifier Fresh-class output labels).
  - Standalone Energy UFAR-Fresh: $44.03\%$ $[42.41, 45.59]$ ($844/1,917$).
  - Cohort A Dual-Gate UFAR: $16.07\%$ ($446/2,776$); UFAR-Fresh: $10.48\%$ ($291/2,776$).
  - Cohort D Dual-Gate UFAR: $34.90\%$ ($698/2,000$); UFAR-Fresh: $22.65\%$ ($453/2,000$).

---

## 9. Submission-Readiness Status & Verification

> [!WARNING]
> **SUBMISSION READINESS STATUS: NOT MARKED SUBMISSION-READY**  
> Under research integrity guidelines, this manuscript cannot be certified as "submission-ready" until final human author validations are completed:

1. **Double-Blind Identity Verification:** Confirm that institutional policies and conference rules require full anonymization of author names and affiliations for initial submission.
2. **Procedia Copyright / Licence Block:** Elsevier Procedia Computer Science will assign final volume numbers, page numbers, and copyright dates upon acceptance.
3. **Conference Portal Profile:** Verify that the primary corresponding author has registered on the ICMLDE 2026 CMT/EasyChair portal and matches the submission metadata.
