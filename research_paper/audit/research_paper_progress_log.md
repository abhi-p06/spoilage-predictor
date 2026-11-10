# AgriRoute Research Paper Progress Log

**Target Venue:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026) / *Procedia Computer Science* (Elsevier)  
**Document Type:** Research Engineering & Editorial Milestone Log  
**Author:** Project Research Team  
**Date Initiated:** November 11, 2026  
**Status:** ACTIVE — PHASE 2 (LATEX WORKSPACE, INTRODUCTION AUDIT & COMPILATION) COMPLETE  

---

## 1. Executive Summary & Paper Scope

This project executes the comprehensive manuscript preparation for the empirical research study:
> **"Source-Stratified Evaluation of Out-of-Distribution Detection in Fruit-Quality Classification Under Species and Treatment-Labelled Shifts"**

The research contribution is an exhaustive empirical evaluation, out-of-distribution (OOD) benchmark, and diagnostic failure analysis of a frozen MobileNetV2 vision backbone across $N = 13,465$ image records from three independent repositories. The study investigates closed-set domain collapse, unseen-species semantic shift, and post-harvest treatment-labelled condition shifts. It explicitly disclaims the proposal of novel standalone OOD algorithms or real-world agricultural supply chain deployment.

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
| **Locked Thresholds** | `STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv` | 4,004 B | Frozen validation calibration thresholds ($\tau_{95}$) |
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
│   ├── main.pdf                                 # Compiled Procedia Computer Science PDF (7 pages)
│   ├── ecrc.sty, elsarticle.cls, framed.sty    # Official template style definitions
│   ├── Procs.pdf, SDlogo-3p.pdf, etc.          # Elsevier official vector branding assets
│   ├── sections/                                # Modular LaTeX section files
│   │   ├── 01_introduction.tex                 # Fully audited, de-claimed Section 1
│   │   ├── 02_related_work.tex                 # Section 2 stub
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
    └── page_renders/                            # High-resolution PNG renders of compiled PDF
        ├── page_1.png ... page_7.png            # 150 DPI visual verification renders
```

---

## 4. Scientific Restrictions & Adherence Matrix

| Operational Constraint | Enforced Policy | Compliance Verification |
| :--- | :--- | :---: |
| **Classifier Immutability** | No retraining, fine-tuning, or parameter changes to `MODEL_B_V4_1_CHECKPOINT.keras`. | **STRICTLY ENFORCED** |
| **Inference Immutability** | No re-execution of test inference or modification of `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`. | **STRICTLY ENFORCED** |
| **Threshold Immutability** | All operational gates locked at Stage 4.0.3 validation operating points ($\tau_{\text{Energy}} = 0.918451$, $\tau_{\text{MSP}} = 0.582610$). | **STRICTLY ENFORCED** |
| **Terminology Precision** | Image records designated as "Image Counts" ($N$), never biological specimens. | **STRICTLY ENFORCED** |
| **Treatment Shift Framing** | Formalin-treated fruit characterized as "treatment-labelled condition shift", never claiming chemical detection or optical invisibility. | **STRICTLY ENFORCED** |
| **Novelty Boundaries** | Dual-Gate cascade framed as an operational heuristic / discrete acceptance rule; not claimed as a novel standalone mathematical model. | **STRICTLY ENFORCED** |
| **Open-Set Novelty** | Explicitly acknowledges prior work in open-set recognition and out-of-distribution detection for computer vision and agriculture. | **STRICTLY ENFORCED** |
| **Field Scope Disclaimers** | Zero claims of physical fleet deployment, live cold-chain transit validation, or commercial logistics operations. | **STRICTLY ENFORCED** |

---

## 5. Submission-Policy Check: Format Ambiguity

The supplied conference package contains two distinct authoring tracks:
1. An official Microsoft Word macro-enabled template (`PROCS_ICMLDE_2026_Templates.docm`) with accompanying author guidelines specifying Word format.
2. An official LaTeX template folder (`PROCS_ICMLDE 2026_LATEX Templates/`) containing `PROCS_ICMLDE 2026.tex`, `elsarticle.cls`, and `ecrc.sty` configured with `\documentclass[3p,times,procedia]{elsarticle}`.

**Policy Determination & Risk Mitigation:**
- The LaTeX template has been established as the canonical version-controlled authoring source to ensure mathematical rigor, automated reference management, and exact typestyle reproducibility.
- The compiled output (`main.pdf`) adheres strictly to Elsevier *Procedia Computer Science* geometry ($192 \times 262\text{ mm}$, single column).
- Authors must confirm with the ICMLDE 2026 organizing committee whether the final submission accepts camera-ready LaTeX PDFs or mandates MS Word `.docx`. If Word is mandated, `manuscript_working.docx` serves as the parallel archival fallback.

---

## 6. Milestone History

- **2026-11-11 00:05:** Initialized `research_paper/` workspace. Verified template assets and established `PROCS_ICMLDE_2026_Templates_clean.docx`.
- **2026-11-11 00:06:** Generated initial reference files with 20 citations.
- **2026-11-11 00:10:** Drafted preliminary Section 1 in Markdown and instantiated `manuscript_working.docx`.
- **2026-11-11 00:30:** Commenced LaTeX migration. Discovered missing TeX distribution on host; provisioned `tectonic` 0.17.0 via Homebrew. Executed test compilation in `/tmp/tex_test`.
- **2026-11-11 00:37:** Programmatically verified CrossRef metadata for 9 new and corrected citations. Generated canonical `references.bib` containing 24 fully verified bibliographic entries.
- **2026-11-11 00:38:** Updated `references_audit.csv` and `references_audit.md` with complete taxonomic provenance.
- **2026-11-11 00:39:** Authored `01_introduction.tex` incorporating all scientific de-claiming directives. Created modular section stubs (`02_related_work.tex` through `08_conclusion.tex`) and root `main.tex`.
- **2026-11-11 00:40:** Compiled `main.tex` with `tectonic`. Built complete 7-page `main.pdf`. Generated 150 DPI page renders in `research_paper/audit/page_renders/`.
- **2026-11-11 00:41:** Audited text extracted from `main.pdf`—confirmed 0 undefined citations, 0 broken cross-references, and exact 1-to-24 Vancouver numbering order. Authored `INTRODUCTION_SCIENTIFIC_AUDIT.md` and updated `01_introduction.md`.
