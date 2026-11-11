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
│   ├── main.pdf                                 # Compiled Procedia Computer Science PDF (34 pages)
│   ├── ecrc.sty, elsarticle.cls, framed.sty    # Official template style definitions
│   ├── Procs.pdf, SDlogo-3p.pdf, etc.          # Elsevier official vector branding assets
│   ├── sections/                                # Modular LaTeX section files
│   │   ├── 01_introduction.tex                 # Section 1: Drafted and audited, subject to final source review
│   │   ├── 02_related_work.tex                 # Section 2: Drafted and audited, subject to final source review
│   │   ├── 03_dataset_and_experimental_design.tex # Section 3: Drafted and audited, subject to final source review
│   │   ├── 04_methodology.tex                  # Section 4: Drafted, audited, and compiled (Subsections 4.1--4.8, Fig 2, Tabs 5--7)
│   │   ├── 05_results.tex                      # Section 5: Sensitivity analysis table & evaluation integrated
│   │   ├── 06_discussion.tex                   # Section 6: Pending
│   │   ├── 07_limitations.tex                  # Section 7: Pending
│   │   └── 08_conclusion.tex                   # Section 8: Pending
│   ├── bibliography/
│   │   └── references.bib                      # Canonical BibTeX database (27 verified entries: 24 active, 3 reserved)
│   ├── manuscript_working.docx                  # Working Word manuscript (archival fallback)
│   ├── 01_introduction.md                       # Markdown archival source of Section 1
│   ├── 02_related_work.md                       # Markdown archival source of Section 2
│   ├── 03_dataset_and_experimental_design.md    # Markdown archival source of Section 3
│   └── 04_methodology.md                        # Markdown archival source of Section 4
├── references/
│   ├── references_audit.csv                     # Structured ledger of 27 DOIs, venues, and types
│   ├── references_audit.md                      # Human-readable table of 27 verified citations
│   └── references.bib                           # Synchronized BibTeX database (27 entries)
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
    ├── SECTION_3_AUDIT.md                       # Comprehensive Section 3 evidence reconciliation report
    ├── SECTION_4_METHODS_AUDIT.md               # Comprehensive Section 4 methods evidence reconciliation report
    └── page_renders/                            # High-resolution PNG renders of compiled PDF
        ├── page_01.png ... page_34.png          # 150 DPI visual verification renders of all 34 compiled pages
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
- **2026-11-11 03:30:** Executed comprehensive repository-wide manuscript source synchronization audit:
  - Canonical Bibliography Established: Identified `research_paper/manuscript/bibliography/references.bib` as canonical truth (resolved via `\bibliography{bibliography/references}`). Contains 27 fully verified entries: 24 actively cited in compiled Sections 1 & 2 (`[1]`–`[24]`) plus 3 verified entries (`he2016deep`, `tan2019efficientnet`, `selvaraju2017gradcam`) reserved for Sections 4–7.
  - Byte-for-Byte Mirror Synchronization: Propagated canonical file to `research_paper/references/references.bib` and repository-root `REFERENCES.bib`; all three files verified identical with SHA-256 hash `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` (9,619 bytes).
  - Reference Audit Ledger Reconciled: Updated both `references_audit.csv` and `references_audit.md` to reflect all 27 entries with complete fields (citation key, author list, year, exact title, journal/conference with volume/issue/pages, DOI/URL, publication type, peer-reviewed status, verification status, and section cited). Reconciled obsolete `abayomi2023fruitq` key to `abayomi2024fruitq`.
  - Archival Markdown Mirrors: Created `research_paper/manuscript/02_related_work.md` synchronized with `02_related_work.tex`.
  - Verification & Rendering: Recompiled with `tectonic` (exit code 0, 14 pages, 0 unresolved `??` citations); generated high-resolution page renders covering all 14 pages in `research_paper/audit/page_renders/`. Created `MANUSCRIPT_SYNC_AUDIT.md`.
- **2026-11-11 13:30:** Authored, verified, audited, and compiled Section 3 (Dataset Census and Experimental Design) in canonical LaTeX manuscript:
  - Canonical LaTeX File: Authored `research_paper/manuscript/sections/03_dataset_and_experimental_design.tex` spanning 8 complete subsections (3.1 Study Design Overview, 3.2 Dataset Sources and Provenance, 3.3 Known-Class Definition and Label Mapping, 3.4 Image-Level Census and Partition Construction, 3.5 Source-Stratified Evaluation Cohorts, 3.6 Image Curation, Duplicate Handling, and Sensitivity Analysis, 3.7 Evaluation Integrity and Experimental Separation, 3.8 Reproducibility and Data Availability).
  - Archival Markdown Copy: Authored `research_paper/manuscript/03_dataset_and_experimental_design.md` fully synchronized word-for-word, equation-for-equation, and table-for-table.
  - Three Publication-Quality Tables:
    - Table 2: Dataset Source and Provenance Summary (Primary Kaggle, FruitVision, Sultana et al. with published vs. evaluated subsets and capture environments).
    - Table 3: Evaluation Partition Census ($N = 13,465$ images across Partitions A, B, C, D1, D2 with full species, conditions, sub-counts, and source reconciliation: $B = 4,157 + 1,193 = 5,350$; $D1 = 2,776 + 2,000 = 4,776$).
    - Table 4: Source-Matched OOD Cohort Construction (Cohorts A, B, C, D detailing reference ID subsets, shifted OOD subsets, source repositories, shift dimensions, and specific research questions).
  - Experimental Separation Safeguards: Formally verified that the primary validation calibration population ($N = 227$ raw Kaggle validation images, `is_raw == 1` in `FINAL_GROUP_VAL_V4_1.csv`) is strictly distinct from Partition A ($N = 227$ raw Kaggle test images, `is_raw == 1` in `FINAL_GROUP_TEST_V4_1.csv`) with exactly zero MD5 overlap, and is strictly excluded from the $N = 13,465$ evaluation census.
  - Deduplication & pHash Audit: Documented 116 upstream exact duplicate exclusions (109 FruitVision, 7 Sultana); verified pHash sensitivity across Hamming radii $r \in \{0, 4, 8\}$ across Primary ($N = 13,465$), Tier 1 ($N = 13,409$), and Tier 2 ($N = 13,382$) with AUROC shifts $\le 0.22$ percentage points.
  - Compilation & Verification: Successfully compiled `main.tex` via `tectonic` into a 21-page PDF with 0 errors, 0 warnings in Section 3, 0 unresolved `??` citations/references, and zero table margin overflows. Rendered high-resolution pages 13–19 to `research_paper/audit/page_renders/`.
  - Comprehensive Audit Deliverable: Authored `SECTION_3_AUDIT.md` (and mirrored to `research_paper/audit/SECTION_3_AUDIT.md`).
- **2026-11-11 13:45:** Executed targeted correction pass across Section 3 audit package:
  - Shared Reference Subset & Non-Independence: Clarified in Section 3.5 and Section 3.6.2 that FruitVision Known (Partition B, $N_{\text{id}} = 4,157$) is a shared reference subset evaluated across Cohorts A, B, and C; explicitly documented that these cohorts reuse common reference records and do not constitute independent datasets.
  - Non-Additivity of Cohort pHash Exclusions: Stated explicitly that cohort-level pHash exclusions are not additive; distinguished the global count of unique excluded image records across the benchmark (56 in Tier 1, 83 in Tier 2) from repeated cohort-specific counts.
  - Deduplication vs. Augmentation Distinctions: Strictly distinguished the 116 exact binary duplicate exclusions (109 FruitVision, 7 Sultana et al.) from the 1,816 Kaggle synthetic augmentations excluded during test set curation to isolate the 227 raw photographic captures (`is_raw == 1`), enforcing that augmentations are never classified as duplicate removals.
  - Evidence-Bounded Validation Separation: Replaced absolute language with evidence-bounded phrasing in Section 3.7 Item 1 and audit ledgers, noting that cryptographic MD5 separation establishes no exact-file overlap between the reported validation calibration and test sets, but does not prove the absence of every conceivable upstream correlation.
  - Perceptual Hash Sensitivity Levels & Limitations: Formally defined Tier 1 (cross-partition collisions at $r \le 8$) and Tier 2 (cross-partition plus intra-partition multi-label collisions); articulated the low-frequency DCT limitations of pHash and explicitly disclaimed that all near-duplicates have been eliminated.
  - Workspace Inventory Updated: Formally updated repository inventory to record Section 3 as drafted and integrated, canonical bibliography at 27 entries (24 active, 3 reserved), compiled PDF at 22 pages, and visual page-render archive containing all 22 pages (`page_01.png` through `page_22.png`).
  - Synchronization & PDF Compilation: Recompiled canonical `main.tex` via `tectonic` into a 22-page PDF (0 errors, 0 warnings in Section 3, 0 unresolved `??` citations); synchronized all updates to `research_paper/manuscript/03_dataset_and_experimental_design.md` and `SECTION_3_AUDIT.md` (and its mirror); re-rendered all 22 pages to `research_paper/audit/page_renders/page_01.png` through `page_22.png`.
- **2026-11-11 13:55:** Final narrowly scoped audit of Section 3 completed:
  - Numerical Sensitivity Results Relocated: Inspected Section 3.6.2 and identified empirical AUROC sensitivity results; cleanly moved all numerical findings into Section 5.1 (`sec:results_sensitivity` in `05_results.tex`), preserving every single reported numerical metric (Cohort A Energy: $81.57\% \to 81.53\% \to 81.46\%$; Cohort B Energy: $53.13\% \to 53.18\% \to 53.19\%$; Cohort C Energy: $84.72\% \to 84.64\% \to 84.65\%$; Cohort D Energy: $67.52\%$ invariant; max shift $\le 0.22$ pp).
  - Experimental Design Scope Restored: Section 3 is now strictly focused on study design, pHash hashing methodology, definitions of Primary ($N=13,465$), Tier 1 ($N=13,409$), and Tier 2 ($N=13,382$) tiers, and pHash methodological limitations.
  - Terminology Standardized: The 116 duplicate exclusions across external repositories (109 FruitVision, 7 Sultana et al.) are consistently characterized as "hash-identified duplicate files" based on cryptographic hash collision detection, avoiding over-assertion of byte-for-byte comparison. Exclusion counts remain unchanged.
  - Section 3 Audit Checklist Updated: Reflected exact manuscript state in `SECTION_3_AUDIT.md` (and mirrored copy).
- **2026-11-11 14:35:** Executed final scientific wording correction and sensitivity-table enhancement across Section 3 and Section 5:
  - Source-Matching Framing: Replaced claims that source matching "controls" or "isolates" confounders with evidence-bounded phrasing: "source matching reduces repository-level provenance differences, while within-repository acquisition variation remains possible" across §3.1, §3.5, and Table 4 caption/body.
  - FruitVision Cohort Framing: Removed unsupported claims that FruitVision known and unseen subsets were photographed across the same market locations with the same smartphone cameras; described strictly as same-repository comparisons.
  - Dataset-Reported Treatment Framing: Reframed Cohorts B and C descriptions in §3.3 and §3.5 strictly as "dataset-reported treatment-labelled condition", eliminating claims of independent chemical detection or treatment-caused visual anomalies.
  - Speculative Mimicry Purged: Removed speculative assertion that green guava and jujube visually mimic green apples and citrus from Cohort D; described strictly as diverse unseen agricultural species.
  - Deduplication Terminology: Standardized terminology to "duplicate files identified through matching cryptographic digests" (MD5/SHA-256), purging "hash collision" terminology when referring to duplicate files and avoiding byte-for-byte comparison claims.
  - Reproducibility Terminology: Renamed Section 3.8 to "Experimental Traceability and Data Availability", replacing "Complete experimental reproducibility" with "Experimental traceability", and explicitly distinguishing preserved research artifacts (checkpoints, prediction records, manifests, ledgers) from external runtime and publisher dependencies.
  - Perceptual Hash Design: Clarified pairwise scanning radii $r \in \{0, 4, 8\}$ as scanning thresholds ($r=0$ exact perceptual match, $r \le 4$ strict near-duplicate, $r \le 8$ permissive visual collision), cleanly distinguishing these radii from the resulting evaluation tiers (Primary, Tier 1, Tier 2), while strictly preserving 56 and 83 unique global exclusions.
  - Section 5 Sensitivity Table & Ranking Invariance: Embedded compact Table 5 in `05_results.tex` reporting all 5 post-hoc detectors + Dual-Gate across all 4 cohorts and 3 sensitivity tiers (24 evaluated configurations) derived from canonical `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv`. Formally verified and documented that relative detector rankings remain strictly invariant across all three tiers in every single cohort. Qualified conclusions as applying to tested pHash exclusions and evaluated image records.
  - File Synchronization: Word-for-word synchronization applied to `03_dataset_and_experimental_design.md` and audit ledgers.
  - Compilation & Layout Verification: Compiled canonical `main.tex` via `tectonic` into a 23-page PDF with 0 errors, 0 overfull hboxes in Section 3 and Section 5, 0 underfull hboxes, and 0 unresolved `??` citations. All 23 pages rendered at 150 DPI to `research_paper/audit/page_renders/page_01.png` through `page_23.png`.
  - Status Reconfirmed:
    - Sections 1–4: Drafted, audited, and compiled.
    - Section 5: Sensitivity analysis table & evaluation integrated.
    - Sections 6–8: Pending.
- **2026-11-11 15:00:** Authored, verified, audited, and compiled Section 4 (Methodology) in canonical LaTeX manuscript:
  - Canonical LaTeX File: Authored `research_paper/manuscript/sections/04_methodology.tex` covering 8 complete subsections:
    - 4.1 Methodological Overview (with Figure 2 vector pipeline graphic).
    - 4.2 Frozen MobileNetV2 Classifier (architecture, label space $\mathcal{Y}$, input preprocessing, immutability safeguards, checkpoint SHA-256: `4a12f354...b6b4`).
    - 4.3 Post-Hoc OOD Detection Scoring Functions (MSP, Energy as log-sum-exp, ODIN with perturbation $T=1000, \varepsilon=0.0014$, Ledoit-Wolf regularized Mahalanobis distance, OpenMax with Weibull tail fitting $\eta=20, \alpha=2$).
    - 4.4 Operational Energy--MSP Dual-Gate Cascade (discrete acceptance rule $\operatorname{ACCEPT}(x) \iff S_{\text{Energy}}(x) \ge 0.918451 \land S_{\text{MSP}}(x) \ge 0.582610$, and continuous linear margin proxy for exploratory AUROC).
    - 4.5 Validation-Based Operating-Threshold Calibration ($N_{\text{val}} = 227$ raw Kaggle validation images, order-statistic derivations, inclusion--exclusion joint calibration for Dual-Gate matching $95.1542\%$ empirical ID coverage, 95% Clopper--Pearson exact interval $[91.43\%, 97.60\%]$).
    - 4.6 Evaluation Metrics (closed-set Acc/BalAcc/Macro-F1, continuous OOD AUROC/FPR@95/OSCR, operational UFAR/UFAR-Fresh/KRR/Retention).
    - 4.7 Uncertainty Quantification and Statistical Reporting ($B = 1,000$ non-parametric bootstrap, `seed=42`, percentile CIs, image record resampling unit, class/cohort stratification, statistical conditioning on exchangeability, shared reference population disclaimers).
    - 4.8 Software and Implementation Reproducibility (controlled Python/TensorFlow/SciPy/scikit-learn environment, canonical CSV ledgers).
  - Three Publication-Quality Tables:
    - Table 5: Post-Hoc Out-of-Distribution Detector Formulations and Verified Configurations.
    - Table 6: Calibrated Operating Thresholds ($\tau_{95}$) Determined on Validation Data ($N_{\text{val}} = 227$).
    - Table 7: Authoritative Evaluation Metrics Across Closed-Set Classification, Continuous OOD Ranking, and Operational Gating.
  - Figure 2 Pipeline Graphic: Generated vector and raster assets (`research_paper/figures/figure_02_pipeline.pdf` & `.png`, mirrored in `research_paper/manuscript/figures/`).
  - Archival Markdown Copy: Authored `research_paper/manuscript/04_methodology.md` fully synchronized word-for-word, equation-for-equation, and table-for-table.
  - Comprehensive Audit Deliverable: Authored `SECTION_4_METHODS_AUDIT.md` (and mirrored to `research_paper/manuscript/audit/SECTION_4_METHODS_AUDIT.md`).
  - Compilation & Formatting Verification: Successfully compiled `main.tex` via `tectonic` into a 34-page PDF with 0 errors, ZERO overfull hboxes in Section 4, ZERO unresolved `??` citations, and all 27 references resolved. All 34 pages rendered at 150 DPI to `research_paper/audit/page_renders/page_01.png` through `page_34.png`.
  - Status Reconfirmed:
    - Sections 1–4: Drafted, audited, and compiled.
    - Section 5: Drafted sensitivity subsection; full results write-up pending.
    - Sections 6–8: Pending.
- **2026-11-11 16:15:** Completed Final Scientific Correction Pass on Section 4 (Methodology):
  - Verified OpenMax Code Parity: `scripts/run_stage4_1_benchmark.py` (L267–290) calculates rank-adjusted weights as `alpha_weight = 1.0 - (rank_idx / float(alpha)) * (1.0 - omega_k)`. For top rank `rank_idx = 0` ($r = 1$), `rank_idx / alpha = 0 / 2 = 0`, giving $w_{c_1} \equiv 1.0$ (no Weibull logit discount). Reconciled manuscript equation to $w_{c_r} = 1.0 - \frac{r-1}{\alpha}(1 - \omega_r(x))$ with $r \in \{1, \dots, \alpha\}$. Formally documented this as a modified OpenMax-style heuristic evaluated on 1280-D global average pooled features.
  - Verified ODIN Code Parity: Benchmark code (L217–231) perturbs inputs along the sign gradient of the maximum temperature-scaled logit $\max_k z_k/T_{\text{ODIN}}$, clipped to $[-1.0, 1.0]$. Documented as an ODIN-style perturbation variant.
  - Reconciled MobileNetV2 Architecture: Verified against `MODEL_B_V4_1_CHECKPOINT.keras`: 1 initial $3\times 3$ conv + 17 bottleneck blocks (1 initial inverted bottleneck + 16 inverted residual blocks with expansion factor 6; 155 layer operations in functional graph), 1280-D global average pooling, Dropout(0.3), 6-class dense head. Replaced legacy "53 inverted residual bottleneck layers" phrasing.
  - Clarified Dual-Gate Decision Rule vs. Exploratory Proxy: Operational decision rule is strictly a discrete Boolean conjunction ($\operatorname{ACCEPT} \iff S_{\text{Energy}} \ge 0.918451 \land S_{\text{MSP}} \ge 0.582610$). Continuous linear margin proxy $S_{\text{proxy}} = (S_E - \tau_E) + (S_M - \tau_M)$ documented as an exploratory metric with scale-dependence notes ($[0,10]$ vs $(1/6,1]$). Renamed Table 8 entry in `05_results.tex` to `Dual-Gate (Proxy)`.
  - Reconciled Evaluation Metrics: Clarified AUROC as threshold-independent; Retrospective FPR@95 as post-hoc operating-point metric with OOD as positive class ($y_{\text{ood}} = 1$); documented AUPR and OSCR as auxiliary metrics in CSV ledgers; regenerated Figure 1 to match exact labels; reframed UFAR-Fresh as produce routing / non-target acceptance outcome (disclaiming biological food safety).
  - Rephrased Statistical Reporting: Descriptive comparison for closed-set domain shift (non-overlapping bootstrap percentile intervals show substantial descriptive separation without asserting formal inferential hypothesis testing). Verified $B=1,000$, `seed=42`, image-level unit, stratified resampling.
  - Validation Threshold Calibration: Documented $N_{\text{val}} = 227$ raw validation images, order statistics $s_{(12)}$ (single gate) and $s_{(7)}$ (Dual-Gate), inclusion-exclusion union $|R_{\text{union}}| = 11$, and Clopper-Pearson interval $[91.43\%, 97.60\%]$. Softened absolute claims of "zero circularity" to evidence-bounded terms.
  - Synchronized Markdown Mirror: Updated `04_methodology.md` to match `04_methodology.tex` word-for-word, equation-for-equation, and table-for-table. Standardized figure label to **Figure 1** (matching compiled PDF numbering). Canonical citations verified: MobileNetV2 [7], MSP [9], Sultana [11], FruitVision [12], OpenMax [14], ODIN [16], Mahalanobis [17], Energy [18].
  - Checkpoint Integrity: Checkpoint SHA-256 `4a12f354...b6b4` strictly unmodified; zero weights altered; zero thresholds modified; zero synthetic runs; zero numbers altered.
  - LaTeX Compilation: Recompiled canonical `main.tex` via `tectonic` into 34-page PDF with 0 errors, ZERO overfull hboxes in Section 4, ZERO unresolved `??` citations, and all references resolved.
  - Comprehensive Audit Deliverable: Updated `SECTION_4_METHODS_AUDIT.md` (and mirrored to `research_paper/manuscript/audit/SECTION_4_METHODS_AUDIT.md`).
  - Repository Completion Status:
    - Sections 1–4: Drafted, audited, and compiled.
    - Section 5: Drafted sensitivity subsection (Table 8 with Dual-Gate Proxy); full results write-up pending.
    - Sections 6–8: Pending.
- **2026-11-11 16:45:** Executed Final Section 4 Consistency Pass addressing remaining scientific, statistical, and architectural consistency requirements:
  - Corrected FPR@95 Class Orientation: Explicitly defined in-distribution (ID) produce as positive class ($\text{TPR}_{\text{id}} \ge 0.95$) and out-of-distribution (OOD) produce as negative class in the retrospective FPR@95 operating-point formulation. FPR@95 measures the proportion of negative (OOD) images incorrectly accepted as positive (ID). Separated this operating-point metric from threshold-independent AUROC (where OOD is positive class $y_{\text{ood}} = 1$ and anomaly score is $-S(x)$). Updated §4.1, Table 7, and §4.6.2.
  - Recalculated Clopper-Pearson Exact Interval: Independently recalculated the standard two-sided 95% Clopper-Pearson exact binomial confidence interval for $k = 216$ successes out of $n = 227$ trials using `scipy.stats.beta`: $[91.50\%, 97.56\%]$ (exact: $[91.4951\%, 97.5565\%]$). Replaced legacy $[91.43\%, 97.60\%]$ across `.tex`, `.md`, and audit ledgers while strictly preserving $N_{\text{val}} = 227$, rejected = 11, accepted = 216, coverage = 95.1542%, $\tau_E = 0.918451$, and $\tau_M = 0.582610$.
  - Reconciled Sensitivity Cohort Counts in Table 8: Verified against canonical `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv` and updated Table 8 to clearly display sample count progression across all three tiers (Primary $\to$ Tier 1 $\to$ Tier 2): Cohort A ($N_{\text{id}}: 4,157 \to 4,146 \to 4,140$; $N_{\text{ood}}: 2,776 \to 2,762 \to 2,746$); Cohort B ($N_{\text{id}}: 4,157 \to 4,146 \to 4,140$; $N_{\text{ood}}: 1,917 \to 1,906 \to 1,901$); Cohort C ($N_{\text{id}}: 4,157 \to 4,146 \to 4,140$; $N_{\text{ood}}: 1,195 \to 1,175 \to 1,175$); Cohort D ($N_{\text{id}}: 1,193 \to 1,193 \to 1,193$; $N_{\text{ood}}: 2,000 \to 2,000 \to 2,000$).
  - Standardized Method Nomenclature: Standardized names to MSP, Energy, ODIN-style perturbation variant (or `ODIN (Variant)`), Ledoit-Wolf Mahalanobis (or `LW-Mahalanobis`), and modified OpenMax-style heuristic (or `OpenMax (Mod.)`). Synchronized across Abstract, RQ2 (§1.2), §4.1, Figure 1 caption, Table 5, Table 8, and Section 5 results narrative.
  - Corrected Energy Scale Statement: Clarified that raw Energy score $S_{\text{Energy}}(x) = \operatorname{logsumexp}(z(x))$ is mathematically unbounded on $(-\infty, +\infty)$ with an observed empirical range of $[-1.753, 5.264]$ across 13,465 evaluation images, whereas MSP is strictly bounded in $(1/6, 1]$ (empirically $[0.231, 1.000]$), explaining the scale-dependence of the exploratory linear proxy.
  - Qualified Abstract Metric: Explicitly qualified 13.18% as the standalone Energy operational false acceptance rate under its locked validation threshold ($\tau_E = 1.054579$), distinguishing it from Dual-Gate UFAR (16.07%).
  - Synchronized Results Subsections: Clarified in audit ledgers that sensitivity analysis is currently typeset as Subsection 5.1 (Table 8) in the compiled manuscript, with other primary Results subsections (5.2–5.5) pending drafting.
  - Recompiled and Verified: Recompiled `main.tex` via `tectonic` into 35-page PDF with 0 errors, ZERO overfull hboxes in Sections 4 & 5, and ZERO unresolved citations. All 35 pages re-rendered to `research_paper/audit/page_renders/page_01.png` through `page_35.png`.
  - Repository Completion Status Reconfirmed:
    - Sections 1–4: Complete and audited.
    - Section 5: Partial (Subsection 5.1 drafted; Subsections 5.2–5.5 pending).
    - Sections 6–8: Pending stubs.
- **2026-11-11 17:30:** Completed Final Section 4 Micro-Corrections, Complete Results Drafting (Subsections 5.2--5.5), and Full Drafting of Discussion (Section 6), Limitations (Section 7), and Conclusion (Section 8):
  - **Part A Section 4 Micro-Corrections:**
    - Acknowledged in §4.1 (L59) that ODIN-style perturbation variant and modified OpenMax-style heuristic represent specific implementation variants.
    - Standardized Table 6 rows: `MSP (Single Gate)`, `Energy (Single Gate)`, `ODIN-style Variant (Single Gate)`, `Ledoit--Wolf Mahalanobis (Single Gate)`, and `Modified OpenMax-style (Single Gate)`. Standardized Table 5 rows accordingly.
    - Corrected theoretical MSP range from $(1/K, 1]$ to $[1/K, 1]$ (L89) and bounded MSP proxy scale to $[1/6, 1]$ (L189) across `.tex` and `.md`.
    - Corrected FPR@95 wording (L307 & L311): retrospective threshold $\tau_{95}^{\text{test}}$ enforces an in-distribution True Positive Rate of *at least 95.0\%* ($\text{TPR}_{\text{id}} \ge 0.95$), not exactly 95.0\%.
    - Reframed opening sentence of §4.7 (L337) to confidence intervals and empirical uncertainty summaries without claiming formal hypothesis testing.
    - Reframed `seed=42` statement (L339) to support repeatability of the bootstrap resampling procedure across runs.
    - Synchronized all changes word-for-word into `research_paper/manuscript/04_methodology.md`.
  - **Part B Section 5.1 Corrections:**
    - Explicitly designated Dual-Gate AUROC as the "exploratory Energy--MSP linear-margin proxy" ($S_{\text{proxy}} = (S_E - \tau_E) + (S_M - \tau_M)$) with clear scale-dependence qualification ($\sigma \approx 2.15$ vs. $\sigma \approx 0.18$), distinguishing it from the operational Boolean AND rule.
  - **Part C Complete Results Write-Up (§5.2--§5.5):**
    - Subsection 5.2 (Closed-Set Performance): Table 9 reports Partition A (96.92\% [94.71\%, 98.68\%]) vs. Partition B Pooled (68.36\% [67.20\%, 69.40\%]), FruitVision B (69.14\%), and Sultana B (65.63\%) with 95\% bootstrap CIs. Table 10 documents class-wise confusions, catastrophic Fresh Apple collapse to 32.12\% (393 Rotten Apple, 255 Rotten Orange confusions), source-specific diagnostics (FruitVision B fresh apple 174/765; Sultana B fresh orange 98/193), and the varietal russeting observational hypothesis.
    - Subsection 5.3 (Source-Stratified OOD Discrimination): Table 11 reports all 4 cohorts (A--D) across 6 detectors for AUROC, retrospective FPR@95, AUPR-IN, AUPR-OUT, and OSCR, with exact 95\% bootstrap CIs. Highlights Energy superiority on semantic shifts (81.57\% in A, 84.72\% in C, 67.52\% in D) and total collapse on chemical treatment shift in Cohort B (Energy AUROC = 53.13\%, Mahalanobis = 47.91\%, MSP = 58.77\%, FPR@95 > 91\%).
    - Subsection 5.4 (Operational Decision Performance): Table 12 reports operational screening under locked prospective thresholds ($\tau_{95}$). Analyzes severe in-distribution abstention penalty (KRR = 41.98\% on FruitVision B, 44.01\% on Sultana B, pooling at 42.43\% abstention across Partition B). Documents critical safety failure on Cohort B: 821 out of 1,917 treated fruits (42.83\% [41.26\%, 44.34\%]) penetrate the gate into commercial Fresh grades. Reasserts food-safety scope disclaimer.
    - Subsection 5.5 (Uncertainty & Consolidated Findings): Provides evidence-bounded resolutions to RQ1, RQ2, and RQ3, synthesizes pHash sensitivity findings, and formalizes statistical non-independence of Cohorts A--C due to shared reference population.
  - **Part D Complete Sections 6, 7, and 8:**
    - Section 6 (Discussion): Authored 5 substantive subsections analyzing domain collapse, the physical visual invariance of chemical fixatives to RGB imaging, the severe economic cost of in-distribution abstention (42.43\% KRR), architectural comparisons across detectors, and multi-modal engineering recommendations (hyperspectral/SWIR, VOC e-noses, dynamic cold-chain telemetry).
    - Section 7 (Limitations and Threats to Validity): Authored 8 comprehensive subsections addressing image records vs. biological independence, dataset-reported treatment labels without independent assays, within-repository variation under source matching, external acquisition variability, bootstrap conditioning and shared baseline non-independence, lack of physical sorting/conveyance validation, algorithmic implementation variants (modified OpenMax and ODIN), and proxy score scale dependence.
    - Section 8 (Conclusion): Authored definitive, evidence-bounded answers to RQ1, RQ2, and RQ3 using exact verified metrics, prospective research pathways, and an explicit disclaimer of algorithmic novelty or deployment claims.
  - **Synchronization & Verification:**
    - Synchronized all sections into companion Markdown files (`04_methodology.md`, `05_results.md`, `06_discussion.md`, `07_limitations.md`, `08_conclusion.md`).
    - Successfully compiled `main.tex` via `tectonic` into a 44-page PDF with 0 errors, ZERO overfull hboxes in Sections 4--8, ZERO unresolved citations, and all references resolved.
    - Rendered all 44 compiled pages at 150 DPI to `research_paper/audit/page_renders/page_01.png` through `page_44.png`.
    - Checkpoint SHA-256 confirmed unchanged (`4a12f354...b6b4`).
  - **Manuscript Status:** Sections 1 through 8 are fully drafted, mathematically reconciled, and verified against canonical project ledgers. Ready for author review.
- **2026-11-11 18:30:** Executed Final Full-Manuscript Scientific Audit and Forensic Verification Pass across 44-Page V4.1 Manuscript (`main.tex` and Sections 1--8):
  - **Resolution of Unresolved LaTeX Cross-References:** Fixed all four unresolved cross-reference targets in LaTeX source:
    - §5.3 source-matched cohort definition resolved to `\ref{sec:source_stratified_cohorts}` (§3.4).
    - §5.3 linear-margin proxy description resolved to `\ref{sec:continuous_proxy}` (§4.4.2).
    - §7.1 dataset record tracking discussion resolved to `\ref{sec:dataset_sources_provenance}` (§3.2).
    - §7.3 source-stratified design resolved to `\ref{sec:source_stratified_cohorts}` (§3.4).
    - Forensic PDF extraction via PyMuPDF confirmed ZERO literal `??`, ZERO `TODO`, and ZERO `TBD` across all 44 compiled pages.
  - **Bounded Treatment-Related Claims:** Replaced unsupported chemical claims with precise, evidence-bounded phrasing: "dataset-reported treatment-labelled images" / "dataset-reported formalin-mixed condition". Removed assertions that the study verified chemical immersion, tested tissue toxicity, or proved chemical fixatives preserve surface optical properties in these images. Reframed Cohort B results to weak or near-chance discrimination on the evaluated dataset-reported cohort (Energy AUROC = 53.13%, MSP = 58.77%, Mahalanobis = 47.91%, Proxy = 53.96%, UFAR-Fresh = 42.83%).
  - **Tempered Morphological Explanations:** Replaced speculative causal claims regarding guava/jujube resemblance and apple russeting with explicitly labeled observational hypotheses, distinguishing qualitative visual inspection from causally tested mechanisms. Kept pooled Partition B misclassification counts separate from FruitVision-only counts.
  - **Standardized Known-Class Terminology:** Replaced "valid commercial produce/images" with "known-class image records" or "known-class images". Described UFAR-Fresh strictly as an image-level classifier routing outcome, disclaiming biological food safety certification. Preserved verified counts: Pooled KRR = 2,270/5,350 (42.43%), Dual-Gate UFAR-Fresh on Cohort B = 821/1,917 (42.83%).
  - **Standardized Source-Matching Language:** Standardized phrasing across Sections 3, 5, 6, 7, and Abstract to: *"Source matching reduces repository-level provenance differences, while within-repository acquisition variation remains possible."*
  - **Non-Causal Framing of Cohort C:** Clarified that higher observed AUROC on Cohort C (84.72%) compared to Cohort A (81.57%) reflects empirical cohort definitions and cannot isolate a causal treatment effect.
  - **Standardized Dual-Gate Proxy Nomenclature:** Designated continuous ROC ranking metric as the "Energy--MSP linear-margin proxy (exploratory)", strictly distinguishing it from the discrete Boolean operational Dual-Gate rule (UFAR, UFAR-Fresh, KRR) and noting scale dependence.
  - **Statistical Independence of Bootstrap CIs:** Documented that FruitVision Known KRR point estimates are identical across Cohorts A, B, and C ($41.98\%$), and clarified that differing bootstrap CI bounds arise from independent bootstrap resampling draws ($B = 1,000$, seed 42) of the shared reference partition across cohort runs.
  - **Corrected Discussion & Limitations Overclaims:** Reframed packhouse throughput impacts as potential economic consequences; removed uncomputed convex-hull claims; cited Sattar et al. [32] (`\cite{sattar2024sensornet}`) for chemical/VOC sensing; removed uncited 1.5–3.0 m/s conveyor speed; clarified that $\rho > 0.992$ represents the Spearman rank correlation; qualified operational metrics as offline screening evaluations.
  - **Reconciled Audit Files:** Synchronized `SECTION_4_METHODS_AUDIT.md` (and mirrored to `research_paper/manuscript/audit/SECTION_4_METHODS_AUDIT.md`), documenting 44 pages, complete drafting of Sections 1--8, theoretical MSP range $[1/K, 1]$, and zero unresolved references.
  - **Front Matter & Acknowledgements:** Enforced strict double-blind anonymity (`\runauth{Anonymous Author(s)}`, redacted affiliation and contact details). Updated Acknowledgements to thank creators of Kaggle Fruit Quality, FruitVision, and Sultana datasets, purging historical references to FruitQ.
  - **Full Artifact & Code Synchronization:** Synchronized companion Markdown mirrors (`04_methodology.md`, `05_results.md`, `06_discussion.md`, `07_limitations.md`, `08_conclusion.md`). Verified frozen checkpoint SHA-256 (`4a12f354...b6b4`). Recompiled via `tectonic` into a 44-page PDF and re-rendered all 44 pages at 150 DPI to `research_paper/audit/page_renders/page_01.png` through `page_44.png`. Successfully passed 8/8 test suite cases in `pytest tests/test_reproducibility_v4_1.py`.
- **2026-11-11 18:50:** Executed V4.1 Final Claim-Boundary and Document Synchronization Pass:
  - **Conclusion Refinement (§8):** Replaced "chemical condition shifts" with "dataset-reported treatment-labelled condition shifts"; presented russeting correlation strictly as an untested observational hypothesis rather than a causally verified visual mechanism; preserved exact class-wise counts (Fresh Apple accuracy: 32.12% [310/965], 393 Rotten Apple, 255 Rotten Orange); replaced "commercial Fresh class" with "model-predicted Fresh class"; replaced "known-class produce" with "known-class image records"; reframed economic implications as potential operational consequences; rephrased future work as prospective exploration of complementary sensing modalities.
  - **Results Refinement (§5.4):** Qualified Table 12 as reporting offline operational metrics rather than a physical sorting deployment; clarified UFAR-Fresh in caption and text as false acceptance into a Fresh known-class model output ($\hat{y} \in \{0, 1, 2\}$) rather than commercial grade certification; updated list header from "safety-critical failure modes" to "notable operational trade-offs and rejection/acceptance outcomes"; replaced "commercial Fresh class" with "model-predicted Fresh class"; reframed Sultana D rejection degradation as association rather than direct morphological causation; preserved all canonical numbers (42.43% pooled KRR, 42.83% Cohort B UFAR-Fresh).
  - **Consolidated Findings Refinement (§5.5):** Retained Fresh Apple counts; explicitly qualified russeting explanation as an untested observational hypothesis; retained source-matched cohort findings; clarified that Cohorts A, B, and C are not independent experimental replications due to shared underlying reference records.
  - **Discussion Refinement (§6):** In §6.2, bounded optical claims strictly to the evaluated dataset-reported treatment cohort; stated explicitly that the study cannot determine whether biochemical differences were visible in the evaluated photographs; removed universal claims regarding RGB imaging capabilities; retained explicit disclaimers of chemical/toxicological assays; in §6.3, retained guava/jujube resemblance strictly as an untested observational hypothesis; removed claims of demonstrated "intrinsic feature overlap"; reframed operational throughput and inspection-staffing implications as potential consequences.
  - **Limitations Refinement (§7.5):** Clarified distinction between shared FruitVision Known reference records and independent bootstrap resampling draws per cohort, stating: "Although Cohorts A--C share the same underlying FruitVision known-class reference records ($N_{\text{id}} = 4,157$), bootstrap resampling was performed independently for each cohort evaluation. Therefore, the marginal confidence intervals should not be interpreted as paired intervals for differences between cohorts. These cohorts are not independent experimental replications."
  - **Terminology Standardization:** Verified complete purge of "commercial Fresh class", "commercial fresh grades", "valid commercial produce", "safety-critical failure", "chemical treatment shift", "direct morphological causation", and "intrinsic feature overlap" across all LaTeX and Markdown files.
  - **Audit Synchronization:** Reconciled `SECTION_4_METHODS_AUDIT.md` (and mirrored to `research_paper/manuscript/audit/SECTION_4_METHODS_AUDIT.md`) and progress log to report current 44-page PDF, complete drafting of Sections 1–8 and Subsections 5.1–5.5, Figure 1 (Pipeline), MSP range $[1/K, 1]$, zero unresolved references, and remaining author review work.
  - **LaTeX & PDF Verification:** Recompiled `main.tex` via `tectonic` into 44-page PDF with 0 errors. Verified 0 literal `??`, 0 `TODO`, 0 `TBD`. Re-rendered all 44 pages to `research_paper/audit/page_renders/`. Verified 8/8 test suite cases passed. Checkpoint SHA-256 confirmed unchanged (`4a12f354...b6b4`).

- **2026-11-11 19:45:** Executed V4.2 Final Scientific Claim-Boundary and Audit Cleanup:
  - **Results §5.4 Refinement (Cohort D Observational Hypothesis):** Replaced assertion that rejection rates confirmed closer visual commonalities with an explicitly bounded observational statement. Documented weaker empirical discrimination and higher operational false acceptance on Cohort D (UFAR = 34.90%) than Cohort A (16.07%), while stating explicitly that morphological and chromatic similarities were not formally quantified via feature distance or perceptual metrics, presenting class overlap strictly as an untested observational hypothesis.
  - **Discussion §6.4 Refinement (Mahalanobis Feature Representation):** Replaced claim that 47.91% AUROC in Cohort B proves extracted penultimate features overlap closely with natural clusters. Stated this outcome is consistent with weak separation under the evaluated regularized Mahalanobis scoring function, and explicitly highlighted that latent feature-space geometry and cluster overlap were not independently quantified via embedding distances or density estimation.
  - **Operational Abstention Burden (§5.4, §5.5, §6.3, §8):** Replaced "unsustainable operational abstention cost" with "substantial operational abstention burden"; retained exact 42.43% pooled KRR and explicitly noted that physical sorting implications, line throughput, and financial costs were not directly measured in this offline study.
  - **UFAR-Fresh Terminology Standardization:** Standardized definition throughout Abstract (`main.tex`), §5.4, §5.5, §6.2, §6.3, and §8 as: *the proportion of OOD image records accepted by the evaluated gate and assigned one of the classifier's Fresh-class output labels ($\hat{y} \in \{0, 1, 2\}$)*. Replaced language implying verified freshness, grade certification, or toxicological clearance.
  - **Validation Produce Terminology:** Replaced "clean laboratory validation data" and "clean validation produce" with "primary in-distribution validation images" ($N = 227$), recognizing that validation data contains all six known classes (fresh and rotten).
  - **External Source Terminology:** Standardized references to pooled Partition B ($N = 5,350$) as "external photographic repository images", "external repository conditions", or "external repository environments", avoiding "retail" generalizations since Sultana et al. comprises both retail and field imagery.
  - **Prospective Multi-Modal Engineering Framing (§6.5):** Bounded discussions of hyperspectral/NIR spectroscopy, VOC headspace sensing, and cold-chain telemetry strictly as prospective research directions rather than demonstrated project capabilities. Cited `\cite{sattar2024sensornet}` appropriately.
  - **Mahalanobis Mathematical Notation Consistency (§2.3 vs §4.3.4):** Explicitly documented that canonical literature quadratic form $- (f(x) - \mu_k)^	op \Sigma^{-1} (f(x) - \mu_k)$ in Section 2.3 and benchmark codebase implementation $- \sqrt{\max(d_M^2(x), 0)}$ in Section 4.3.4 are strictly monotonic transformations on $[0, +\infty)$, ensuring complete mathematical consistency and preserving AUROC, ranking, and score orientation.
  - **Audit Documents & Companion Markdown Synchronization:** Synchronized `SECTION_4_METHODS_AUDIT.md` (and manuscript audit mirror), updating document identity to the current fruit-quality OOD title. Synchronized all companion Markdown files (`01_introduction.md` through `08_conclusion.md`).
  - **Frozen Experimental Integrity:** Confirmed zero retraining, zero inference reruns, frozen checkpoint SHA-256 (`4a12f354...b6b4`), frozen thresholds ($	au_E = 0.918451$, $	au_M = 0.582610$, standalone $	au_E = 1.054579$), and unchanged metric tables.
  - **Recompilation & Verification:** Recompiled `main.tex` via `tectonic` into an exact 44-page PDF with 0 errors, 0 unresolved literal `??`, 0 `TODO`/`TBD`. Re-rendered all 44 pages at 150 DPI to `research_paper/audit/page_renders/page_01.png` through `page_44.png`. Verified 8/8 test suite cases passed in `pytest tests/test_reproducibility_v4_1.py`.

- **2026-11-11 21:15:** Executed V4.3 Final Manuscript Micro-Corrections and Source Synchronization:
  - **Results §5.4 Unsupported Confidence Comparison Removed:** Replaced the claim that post-hoc gates perceive treatment-labelled images with confidence levels comparable to natural fresh produce with: *"Under the evaluated operating thresholds, a substantial fraction of treatment-labelled image records were accepted and assigned one of the classifier's Fresh-class output labels. This outcome does not establish that their confidence-score distributions match those of untreated fresh fruit."* Preserved all point estimates and sample counts. Synchronized across `05_results.tex` and `05_results.md`.
  - **Discussion §6.3 Unquantified Score-Distribution Overlap Claim Removed:** Replaced the unproven claim that conservative rejection thresholds cannot fully resolve cases where post-hoc score distributions of unseen botanical classes substantially overlap with those of known classes with: *"These results show that, under the locked thresholds, the evaluated score-based gate did not reliably reject all unseen-species records in Cohort D. The underlying score-distribution and feature-space overlap were not independently quantified."* Preserved the visual resemblance discussion strictly as an explicitly untested observational hypothesis. Synchronized across `06_discussion.tex` and `06_discussion.md`.
  - **Table 9 Source Descriptions Corrected and Synchronized:** Aligned descriptions in both LaTeX (`05_results.tex`) and Markdown (`05_results.md`): FruitVision B described as *"FruitVision Known subset (mixed capture settings)"* and Sultana B described as *"Sultana Known subset (retail and field)"*, accurately reflecting dataset provenance without over-attributing images strictly to retail stalls.
  - **Confidence Interval Register Verification:** Verified Dual-Gate KRR bounds for the reused FruitVision Known reference population against canonical register `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv`: Cohort A [40.75%, 43.06%], Cohort B [40.80%, 43.23%], Cohort C [40.89%, 43.20%]. Verified that differing bounds arise from independent stratified bootstrap resampling draws ($B = 1,000$, seed 42) across cohort runs, confirming identical point estimate (41.98%, 1,745/4,157). Also verified Sultana B Standalone Energy KRR CI [39.31%, 44.26%] and synchronized across Markdown and LaTeX.
  - **Minor Editorial Refinements:**
    - Table 10 caption: Replaced *"Catastrophic failure occurs specifically on Fresh Apples"* with *"The lowest class-wise accuracy is observed for Fresh Apple (32.12%)."*
    - Results §5.3: Replaced *"Superiority of Energy and Feature Scoring on Semantic Shifts"* with *"Comparative Performance of Energy and Feature Scoring on Semantic Shifts."*
    - Conclusion opening: Replaced *"directly resolve the three core research questions"* with *"provide empirical answers to the three core research questions."*
    - Renamed §5.4: *"Operational Rejection and Packaging Decision Performance"* to *"Operational Rejection and Image-Level Decision Performance."*
  - **Statistical and Methodological Synchronization (§4.7):** Explicitly expanded Section 4.7 item 3 in `04_methodology.tex` and `04_methodology.md` to articulate that: (1) Cohorts A--C share the same underlying FruitVision Known reference population ($N_{\text{id}} = 4,157$); (2) bootstrap resampling was performed independently for each cohort evaluation ($B = 1,000$, seed 42); (3) the resulting marginal intervals are not paired confidence intervals for differences between cohorts; and (4) these cohorts should not be treated as independent experimental replications. Perfectly aligned with Results §5.5 and Limitations §7.5.
  - **Frozen Research Integrity Preserved:** Model checkpoint SHA-256 (`4a12f354...b6b4`), Dual-Gate thresholds ($\tau_E = 0.918451$, $\tau_M = 0.582610$), standalone Energy threshold (1.054579), sample counts, and all metric registers strictly preserved. No retraining, inference reruns, or synthetic data generation.
  - **Recompilation & Verification:** Recompiled `main.tex` via `tectonic` into an exact 44-page PDF with 0 errors, 0 unresolved `??`, 0 `TODO`/`TBD`. Re-rendered all 44 pages at 150 DPI to `research_paper/audit/page_renders/`. Verified 8/8 test suite cases passed in `pytest tests/test_reproducibility_v4_1.py`.
