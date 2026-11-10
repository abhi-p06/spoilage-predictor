# AgriRoute Research Paper Progress Log

**Target Venue:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026) / *Procedia Computer Science* (Elsevier)  
**Document Type:** Research Engineering & Editorial Milestone Log  
**Author:** Project Research Team  
**Date Initiated:** November 11, 2026  
**Status:** ACTIVE — PHASE 3 (REVIEWER RESPONSE MAPPING & AUDIT INTEGRATION) COMPLETE  

---

## 1. Executive Summary & Paper Scope

This project executes the comprehensive manuscript preparation for the empirical research study:
> **"Source-Stratified Evaluation of Out-of-Distribution Detection in Fruit-Quality Classification Under Species and Treatment-Labelled Shifts"**

The research contribution is an empirical evaluation, out-of-distribution (OOD) benchmark, and diagnostic failure analysis of a frozen MobileNetV2 vision backbone across $N = 13,465$ image records from three independent repositories. The study investigates closed-set performance differences under external domain shifts, unseen-species semantic shifts, and post-harvest treatment-labelled condition shifts. It explicitly disclaims the proposal of novel standalone OOD algorithms or real-world agricultural supply chain deployment.

---

## 2. Repository Discovery & Evidence Baseline

A read-only forensic inspection was conducted across the project directory to locate all required templates, canonical results, and historical documentation:

| Component / Artifact | File Location | Status / Hash / Size | Verified Role |
| :--- | :--- | :---: | :--- |
| **ICMLDE 2026 Word Template** | `Template_PROCS_ICMLDE_2026/Template_PROCS_ICMLDE_2026/PROCS_ICMLDE_2026_Templates.docm` | 5,884,240 B | Official Elsevier Procedia Word template with macro styling |
| **ICMLDE 2026 LaTeX Template** | `Template_PROCS_ICMLDE_2026/PROCS_ICMLDE 2026_LATEX Templates/PROCS_ICMLDE 2026.tex` | 21,794 B | Companion LaTeX template & style files (`ecrc.sty`, `elsarticle.cls`) |
| **Final Results Report** | `STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md` | 19,530 B | Canonical textual benchmark report |
| **Final Claims Ledger** | `STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv` | 7,468 B | 15 verified quantitative claims + 1 qualitative hypothesis |
| **Final Correction Log** | `STAGE4_1_2_1_1_FINAL_CORRECTION_LOG.md` | 5,110 B | Cryptographic history & non-circular companion pointer |
| **Canonical Confidence Intervals** | `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv` | 14,930 B | Sole numerical truth for all 95% bootstrap CIs (60 rows) |
| **pHash Sensitivity Table** | `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv` | 19,864 B | 72 evaluations across Primary, Tier 1, and Tier 2 subsets |
| **Source-Stratified Metrics** | `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` | 17,487 B | Point estimates across all 4 cohorts and 6 detectors |
| **Image Predictions** | `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` | 6,344,926 B | 13,465 row-level predictions, scores, and decision flags |
| **Locked Thresholds** | `STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv` | 4,004 B | Frozen validation calibration thresholds ($\tau_{\text{Energy}} = 0.918451$, $\tau_{\text{MSP}} = 0.582610$) |
| **Model Checkpoint** | `MODEL_B_V4_1_CHECKPOINT.keras` | 9,715,984 B | SHA-256: `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` |

---

## 3. Dedicated Research Workspace Structure

To safeguard original files, a dedicated `research_paper/` hierarchy is established and actively maintained:

```
research_paper/
├── template/
│   ├── Template_PROCS_ICMLDE_2026/              # Preserved original Word template (.docm, .pdf)
│   ├── PROCS_ICMLDE 2026_LATEX Templates/       # Preserved original LaTeX assets
│   └── PROCS_ICMLDE_2026_Templates_clean.docx   # Clean .docx working template (192 x 262 mm)
├── manuscript/
│   ├── main.tex                                 # Master LaTeX root document (canonical source)
│   ├── main.pdf                                 # Compiled Procedia Computer Science PDF (14 pages)
│   ├── ecrc.sty, elsarticle.cls, framed.sty    # Official template style definitions
│   ├── Procs.pdf, SDlogo-3p.pdf, etc.          # Elsevier official vector branding assets
│   ├── sections/                                # Modular LaTeX section files
│   │   ├── 01_introduction.tex                 # Audited Section 1; metric terminology and gap framing synchronized
│   │   ├── 02_related_work.tex                 # Section 2 drafted; targeted audit corrections applied
│   │   ├── 03_dataset_and_experimental_design.tex # Section 3 stub
│   │   ├── 04_methodology.tex                  # Section 4 stub
│   │   ├── 05_results.tex                      # Section 5 stub
│   │   ├── 06_discussion.tex                   # Section 6 stub
│   │   ├── 07_limitations.tex                  # Section 7 stub
│   │   └── 08_conclusion.tex                   # Section 8 stub
│   ├── bibliography/
│   │   └── references.bib                      # Canonical BibTeX database (24 verified entries)
│   ├── manuscript_working.docx                  # Working Word manuscript (archival fallback)
│   └── 01_introduction.md                       # Markdown archival source of Section 1
├── references/
│   ├── references_audit.csv                     # Structured ledger of 24 DOIs, venues, and types
│   ├── references_audit.md                      # Human-readable table of verified citations
│   └── references.bib                           # Synchronized BibTeX database
├── figures/                                     # Figure vector and bitmap assets
├── tables/                                      # Standalone tables and summaries
└── audit/
    ├── research_paper_progress_log.md           # Running progress log
    ├── INTRODUCTION_SCIENTIFIC_AUDIT.md         # Comprehensive claims and framing audit
    ├── OLD_VS_CURRENT_PAPER_AUDIT.md            # Detailed comparative analysis of 2025 paper vs V4.1
    ├── REVIEWER_RESPONSE_MATRIX.md              # 12-point reviewer objection traceability matrix
    ├── REVIEWER_FEEDBACK_ANALYSIS.md            # Strategic thematic analysis of reviewer critiques
    ├── REVIEWER_RESPONSE_DRAFT.md               # Point-by-point formal response letter draft
    ├── ICMLDE_RESUBMISSION_REQUIREMENTS_CHECKLIST.md # 12-point resubmission & Procedia compliance checklist
    ├── ICMLDE_SCOPE_CHANGE_QUERY_DRAFT.md       # Administrative inquiry draft for conference secretariat
    └── page_renders/                            # High-resolution PNG renders of compiled PDF
        ├── page_1.png ... page_12.png           # 150 DPI visual verification renders
```

---

## 4. Scientific Restrictions & Adherence Matrix

| Operational Constraint | Enforced Policy | Compliance Verification |
| :--- | :--- | :---: |
| **Classifier Immutability** | No retraining, fine-tuning, or parameter changes to `MODEL_B_V4_1_CHECKPOINT.keras`. | **STRICTLY ENFORCED** |
| **Inference Immutability** | No re-execution of test inference or modification of `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`. | **STRICTLY ENFORCED** |
| **Threshold Immutability** | Operational gates locked at Stage 4.0.3 validation operating points ($\tau_{\text{Energy}} = 0.918451$, $\tau_{\text{MSP}} = 0.582610$). Rule: $\text{ACCEPT only if } S_{\text{Energy}} \ge 0.918451 \land S_{\text{MSP}} \ge 0.582610$. | **STRICTLY ENFORCED** |
| **Terminology Precision** | Image records designated as "Image Counts" ($N$), never biological specimens. | **STRICTLY ENFORCED** |
| **Treatment Shift Framing** | Formalin-treated fruit characterized as "treatment-labelled condition shift" under dataset-reported protocol; no chemical detection claims. | **STRICTLY ENFORCED** |
| **Source Matching Scope** | Formulated as: "Source matching reduces cross-repository confounding while potential within-repository capture variation remains." | **STRICTLY ENFORCED** |
| **Novelty Boundaries** | Dual-Gate cascade framed as an operational heuristic / discrete acceptance rule; not claimed as a novel standalone mathematical model. | **STRICTLY ENFORCED** |
| **Field Scope Disclaimers** | Zero claims of physical fleet deployment, live cold-chain transit validation, or commercial logistics operations. | **STRICTLY ENFORCED** |
| **Quarantined Metrics** | MobileNetV2 97.22%, BiLSTM AUC 1.000, XGBoost >95%, and Guntur–Rajkot demo permanently quarantined from V4.1 evidence. | **STRICTLY ENFORCED** |

---

## 5. Submission-Policy, Historical Status & Provenance Observations

1. **Submission Format Ambiguity:**
   - The official conference package contains both a Word `.docm` template with guidelines mentioning MS Word, and a companion LaTeX template.
   - LaTeX is adopted as the canonical version-controlled authoring source. If Word is mandated upon camera-ready submission, `manuscript_working.docx` serves as the parallel baseline.
2. **Authorship Attribution Policy:**
   - The historical 2025 paper lists six student authors (Eshita Patil, Abhinay Pande, Bijeet Nayek, Vini Pandhare, Keerthana Thirunavukkarasu, Bushra Shaikh) from K. J. Somaiya College of Engineering.
   - Author block in `main.tex` remains anonymized as `"Author Names Redacted for Peer Review"` during draft preparation until contributor roles and author approvals are formally verified.
3. **Historical Document Status Confirmed:**
   - The historical document (`AgriRoute_ICMLDE.pdf`, Paper ID: 1345) was previously submitted to ICMLDE 5.0, received a **revision-and-resubmission** decision, and was unpublished.
   - No assertions regarding whether it was indexed or presented are made without independent documentary confirmation. It is treated as an unfinalized prior submission rather than a published work. No prior publication disclosure or formal self-citation is required.
4. **Response PDF Compilation Policy:**
   - `REVIEWER_RESPONSE_DRAFT.md` is maintained as a working draft. The formal response-to-reviewers PDF will only be compiled after the full manuscript is written, finalized, and compiled, so that exact page numbers and line numbers can be faithfully linked.

---

## 6. Milestone History

- **2026-11-11 00:05:** Initialized `research_paper/` workspace. Verified template assets and established `PROCS_ICMLDE_2026_Templates_clean.docx`.
- **2026-11-11 00:06:** Generated initial reference files with 20 citations.
- **2026-11-11 00:10:** Drafted preliminary Section 1 in Markdown and instantiated `manuscript_working.docx`.
- **2026-11-11 00:30:** Commenced LaTeX migration. Provisioned `tectonic` 0.17.0 via Homebrew; executed test compilation in `/tmp/tex_test`.
- **2026-11-11 00:37:** Programmatically verified CrossRef metadata for 9 new and corrected citations. Generated canonical `references.bib` containing 24 fully verified bibliographic entries.
- **2026-11-11 00:38:** Updated `references_audit.csv` and `references_audit.md` with complete taxonomic provenance.
- **2026-11-11 00:39:** Authored `01_introduction.tex` incorporating all scientific de-claiming directives. Created modular section stubs (`02_related_work.tex` through `08_conclusion.tex`) and root `main.tex`.
- **2026-11-11 00:40:** Compiled `main.tex` with `tectonic`. Built complete 7-page `main.pdf`. Generated 150 DPI page renders in `research_paper/audit/page_renders/`.
- **2026-11-11 01:04:** Analyzed historical document `/Users/abby/Downloads/AgriRoute_ICMLDE.pdf` and generated comprehensive `OLD_VS_CURRENT_PAPER_AUDIT.md`.
- **2026-11-11 01:15:** Executed final audit reconciliation: corrected Dual-Gate acceptance equation sign ($\ge 0.918451$), bounded treatment-condition interpretations, qualified source-matching and accuracy difference language, and updated `01_introduction.tex`, `01_introduction.md`, `INTRODUCTION_SCIENTIFIC_AUDIT.md`, and `OLD_VS_CURRENT_PAPER_AUDIT.md`. Recompiled `main.pdf`.
- **2026-11-11 01:22:** Ingested ICMLDE 5.0 Paper ID 1345 reviewer comments across Reviewers 1, 2, and 3. Generated `REVIEWER_RESPONSE_MATRIX.md`, `REVIEWER_FEEDBACK_ANALYSIS.md`, and `REVIEWER_RESPONSE_DRAFT.md`. Reconciled all 12 reviewer objections against V4.1 empirical evidence, explicitly logging unresolved field data limitations and permanently quarantining historical synthetic metrics.
- **2026-11-11 01:45:** Executed final scientific, numerical, and status reconciliation across all reviewer response and historical comparison documents:
  - Corrected benchmark evaluated record counts: Primary Kaggle: 227; FruitVision: 10,045 (B: 4,157; C: 1,917; D1: 2,776; D2: 1,195); Sultana: 3,193 (B: 1,193; D1: 2,000); Total: 13,465 evaluated records across benchmark partitions.
  - Reconciled Known-Class Rejection Rate (KRR) arithmetic: FruitVision Known KRR = $41.98\%$ ($1,745/4,157$); Sultana Known KRR = $44.01\%$ ($525/1,193$); Pooled Partition B KRR = $42.43\%$ ($2,270/5,350$); Treatment Dual-Gate UFAR-Fresh = $42.83\%$ ($821/1,917$).
  - Inserted exact verbatim quotations for all 12 reviewer comments across Reviewers 1, 2, and 3.
  - Assigned mandated resolution statuses across all 12 reviewer comments, explicitly documenting R1.5 as `Not addressed: actual field data do not exist` and R2.2 as `Pending author approval and final CRediT contributions`.
  - Clarified historical paper provenance: Paper ID 1345 was submitted to ICMLDE 5.0, received revision-and-resubmission, and was never published; eliminated speculation and rejection labeling.
  - Enforced treatment terminology ("FruitVision treatment-labelled images", "dataset-reported formalin-mixed condition", "treatment-associated visual condition shift") and purged overstatements.
  - Created `ICMLDE_RESUBMISSION_REQUIREMENTS_CHECKLIST.md` tracking all 12 decision email and Procedia requirements.
  - Created `ICMLDE_SCOPE_CHANGE_QUERY_DRAFT.md` providing an administrative inquiry for author review.
  - Synchronized companion copies between `research_paper/audit/` and repository root.
- **2026-11-11 01:55:** Applied final editorial patch across the six reviewer response and audit documents:
  - Provenance: Standardized designation to "previously submitted, unpublished manuscript" and removed unverified indexing/presentation claims.
  - Terminology: Replaced formal "retraction" language with "removed from revised manuscript and excluded from empirical claims"; replaced subjective or priority phrasing ("first", "unprecedented", "proves", "universal limitation", "accuracy collapsed", "domain collapse", "significant empirical findings").
  - Reviewer 3.2: Clarified that the single demonstration shipment has been removed as validation evidence, while multi-shipment physical validation remains outside the current study.
  - Dual-Gate & Literature Matrix: Standardized decision rule notation ($\text{ACCEPT}(x) \text{ iff } S_{\text{Energy}}(x) \ge \tau_{\text{Energy}} = 0.918451 \land S_{\text{MSP}}(x) \ge \tau_{\text{MSP}} = 0.582610$) and distinguished structured literature comparison from direct experimental benchmarking.
  - Reviewer Response Conclusion: Replaced conclusive resolution claims with an honest, point-by-point status summary across all 12 reviewer items.
  - Administrative Scope Query: Updated original title to "AgriRoute: A Vision-Based Post-Harvest Risk System", removed ungenerated similarity claims, and clarified the inquiry regarding the revision portal.
  - Resubmission Checklist: Added English proofreading requirement, notification receipt acknowledgement timing, extension request options, and qualified checklist verification statuses.
  - Synchronized all updates across `research_paper/audit/` and repository root copies.
- **2026-11-11 02:10:** Executed final consistency patch across reviewer response and audit package:
  - Replaced "locked a priori on internal validation data" with "calibrated on the primary validation partition using empirical order statistics and held fixed during external cohort evaluation" across all documents ($s_{(7)}$, $\tau_{95} = 95.1542\%$).
  - Delineated Abstract vs. Methodology: verified that compiled Abstract introduces the cascade and reports 42.83% treatment Fresh acceptance; the formal mathematical decision rule ($\text{ACCEPT}(x) \iff S_{\text{Energy}}(x) \ge 0.918451 \land S_{\text{MSP}}(x) \ge 0.582610$) and threshold derivations are formulated for Section 4.3 and Section 5.3; marked modification as pending complete methodology write-up in Section 4.3.
  - Reviewer 2.2: Replaced double-blind compliance assumption with provisional anonymization pending confirmation of conference review policy, recording that author contributor roles remain pending formal author approval.
  - Reviewer 1.4: Explicitly qualified supporting evidence to the 24 verified references cited in Section 1 (documented with CrossRef DOIs, venues, years, and authors in `references_audit.csv`).
  - Section 4 Table Note: Confirmed exact wording: "*(Note: This table reflects a literature-based comparison of reported study characteristics; it is not a direct quantitative head-to-head evaluation across incompatible datasets and evaluation protocols.)*"
  - Administrative Scope Query: Added explicit disclaimer: *"The revised study does not contain physical field shipment measurements or independent chemical assays. It is limited to image-level benchmark evaluation, with a prospective field-validation protocol proposed as future work."*
  - Resubmission Checklist: Updated Phase B title to "LaTeX manuscript compilation and verification", added DOCX preservation as archival fallback only, and removed assumed pagination ranges.
  - Synchronized all companion files between `research_paper/audit/` and repository root.
  - Section 1 LaTeX manuscript and compiled PDF verified. Ready to proceed to Section 2 — Related Work drafting.
- **2026-11-11 02:30:** Authored, verified, and compiled Section 2 (Related Work) in canonical LaTeX manuscript:
  - Authored comprehensive `sections/02_related_work.tex` spanning subsections 2.1 to 2.5.
  - Reconciled authoritative publisher author lists and titles in `references.bib` and references audit ledger (Sultana et al. 2022, Bijoy et al. 2025, Sattar et al. 2024, Wang et al. 2023, Pehlivan & Kara 2026, Jansi & Kavitha 2026, Yan et al. 2026).
  - Embedded publication-quality Table 1 in single-column Procedia layout with zero overfull/underfull hboxes.
  - Compiled `main.tex` via `tectonic` into 14-page PDF with zero unresolved references (`??`), perfectly aligned citation numbers [1]–[24], and rendered Section 2 pages (5–12) to `research_paper/audit/page_renders/`.
  - **2026-11-11 02:45:** Executed comprehensive Section 2 scientific correction and research-gap refinement:
  - Dataset Descriptions: Corrected Sultana et al. (2022) to exact 8 fruit types (grape, guava, jujube, pomegranate, strawberry, apple, banana, orange; 16 classes) per DOI `10.1016/j.dib.2022.108552`, removing vegetable/mango mentions. Formatted FruitQ (Abayomi-Alli et al. 2024) with 11 varieties, 3 freshness stages, 5 deep architectures, and closed-set benchmark scope; added FruitQ row to Table 1.
  - Wang et al. (2023): Corrected method to MobileNetV3 + hybrid attention + LMMD + CORAL evaluated across grape (7 varieties, 4 domains) and general fruit (11 varieties, 2 domains) datasets; clarified UDA adaptation vs. frozen evaluation.
  - Distribution Shift Taxonomy: Formalized mathematical notation ($P_s(X) \ne P_t(X), P_s(Y|X) = P_t(Y|X)$ for covariate shift; $\operatorname{supp}(P_t(Y)) \not\subseteq \operatorname{supp}(P_s(Y))$ for open-set semantic shift); bounded treatment shifts as dataset-reported condition shifts rather than concept shifts or new semantic classes.
  - OOD Scoring Formulations: Corrected MSP as maximum softmax confidence scoring; Mahalanobis as distance under fitted class-conditional Gaussian model; Energy as derived from log-sum-exp as an OOD ranking score avoiding softmax probability saturation.
  - SensorNet & PEOS-Net: Contextualized SensorNet as RGB + chemical sensor array under dataset-reported labels; identified PEOS-Net within-dataset class-holdout design (PlantVillage tomato) as distinct from multi-repository domain shift evaluation.
  - Research Gap Synthesis: Completely restructured Section 2.5 around four specific evaluation dimensions (cross-repository baseline shift, open-set class-holdout, treatment-labelled condition shifts, source-stratified isolation), eliminating universal absence claims and softening language ("reduces cross-repository confounding while potential within-repository capture variations remain").
  - Table 1 Literature Matrix: Formatted 9-study comparison table in single-column Procedia layout with zero overfull hboxes, including explicit literature comparison table note.
  - Section 1 Synchronization: Updated `01_introduction.tex` and `01_introduction.md` to qualify treatment condition context and soften Gap 3 framing.
  - Compilation & Verification: Successfully compiled `main.tex` via `tectonic` into 14-page PDF with 0 errors and zero `??` citations; rendered pages 1–12 at 150 DPI. Sections 3–8 maintained as stubs.
- **2026-11-11 03:20:** Executed targeted scientific correction pass across Introduction and Related Work:
  - Metric Inconsistency Resolution: Mathematically reconciled all reported values across canonical evidence sources (`STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md`, `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv`, `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`, `STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv`). Clarified why Dual-Gate UFAR (16.07%) exceeds standalone Energy UFAR (13.18%) under matched 95.15% validation ID coverage: the Dual-Gate Energy threshold is relaxed to $0.918451$ ($s_{(7)}$) to accommodate the second gate (MSP $\ge 0.582610$), whereas standalone Energy uses $1.054579$ ($s_{(12)}$). Reconciled Sultana Cohort D Energy operational UFAR ($34.15\%$, $683/2,000$ image records) vs. Dual-Gate operational UFAR ($34.90\%$, $698/2,000$ image records) and linked each to its exact detector, threshold, and confidence interval.
  - Terminology Corrections: Standardized "known-class rejection rate (KRR)" with retention explicitly defined as $1 - \text{KRR} \approx 58.02\%$ on FruitVision Known. Delineated AUROC (threshold-independent continuous ranking), retrospective FPR@95 (calculated at post-hoc 95% TPR threshold), and operational UFAR/KRR (fixed validation-calibrated operating points).
  - Unsupported Claims Purged: Removed speculative Asian vs. Western apple cultivar examples and unsupported claims regarding russeted apples and pale citrus cultivars from Section 1; replaced "Fresh Produce" with "a fresh known-fruit class"; qualified broad language ("routinely report" $\to$ "often report on specific datasets"; "routinely violated" $\to$ "rarely holds"); strictly framed all units as image records, disclaiming biological specimen independence, independent chemical assays, and live logistics operations.
  - Research Gap Framing: Accurately described documented evaluation protocols for cited studies in Gap 1 (supervised closed-set classification within curated datasets, not anomaly detection); articulated the methodological risk of cross-repository confounding in Gap 2; clarified operational threshold calibration vs. retrospective ranking in Gap 4.
  - Table 1 Literature Matrix & Census: Removed unverified "baseline CNN verification" from Sultana et al. row; labeled the present study row as "Present study (V4.1 evaluation)"; designated all evaluation units as image records; replaced "free from synthetic replication" with exact cryptographic hash tracking, duplicate auditing, and pHash sensitivity analysis.
  - Synchronization & Compilation: Synchronized `01_introduction.tex` and `01_introduction.md`; updated `02_related_work.tex`; compiled `main.tex` with `tectonic` into a 14-page PDF with 0 errors and 0 unresolved references.
- Ready to proceed to Section 3 — Dataset Census and Experimental Design.
