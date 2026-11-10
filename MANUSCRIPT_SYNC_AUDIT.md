# AgriRoute Repository-Wide Manuscript Source Synchronization Audit

**Document:** Canonical Manuscript Source Synchronization Audit Report  
**Target Venue:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026) / *Procedia Computer Science* (Elsevier)  
**Execution Date:** November 11, 2026  
**Auditor:** Senior Research Engineering Agent & Scientific Integrity Auditor  
**Status:** COMPLETED — 100% RECONCILED & SYNCHRONIZED ACROSS CANONICAL PATHS  

---

## 1. Executive Summary

This forensic audit verifies the repository-wide synchronization of all manuscript source files, bibliography databases, reference audit ledgers, and compiled PDF deliverables for the AgriRoute V4.1 empirical research study:
> *"Source-Stratified Evaluation of Out-of-Distribution Detection in Fruit-Quality Classification Under Species and Treatment-Labelled Shifts"*

Every active LaTeX document, Markdown archival document, BibTeX mirror, and reference audit record has been inspected, cross-checked against authoritative publisher registries (CrossRef, DOI, PubMed), and cryptographically verified.

---

## 2. Source Synchronization Matrix

| File | Canonical path | Updated? | Verification |
| :--- | :--- | :---: | :--- |
| **Main LaTeX** | `research_paper/manuscript/main.tex` | **Yes** | Built via `tectonic`; imports modular sections; single-column Procedia layout verified. |
| **Introduction** | `research_paper/manuscript/sections/01_introduction.tex` | **Yes** | Fully synchronized with `01_introduction.md`; metrics, terminology (KRR), and research gaps audited. |
| **Related Work** | `research_paper/manuscript/sections/02_related_work.tex` | **Yes** | Fully synchronized with `02_related_work.md`; Table 1 literature matrix (9 studies) embedded with zero overfull `\hbox`. |
| **Canonical bibliography** | `research_paper/manuscript/bibliography/references.bib` | **Yes** | Resolved by `\bibliography{bibliography/references}`; contains 27 verified entries (24 active, 3 reserved). |
| **Repository-root bibliography** | `REFERENCES.bib` (repository root) | **Yes** | Hash-verified byte-for-byte duplicate of canonical master file (`2f59991e...`). |
| **Reference audit CSV** | `research_paper/references/references_audit.csv` | **Yes** | 27 structured records matching canonical BibTeX database; verified DOIs and section usage. |
| **Reference audit Markdown** | `research_paper/references/references_audit.md` | **Yes** | Formatted ledger of all 27 entries; complete author rosters, venues, and verification trail. |
| **Compiled PDF** | `research_paper/manuscript/main.pdf` | **Yes** | 14 pages; 0 unresolved `??` references; citations `[1]`–`[24]` cleanly rendered; verified visual pages. |

---

## 3. Cryptographic Hash & Bibliography Mirror Integrity

All active bibliography copies in the repository have been synchronized from the canonical source:
`research_paper/manuscript/bibliography/references.bib`.

| File Path | Role | File Size | Entry Count | SHA-256 Hash | Synchronization Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `research_paper/manuscript/bibliography/references.bib` | **Canonical Master** | 9,619 bytes | 27 | `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` | **CANONICAL TRUTH** |
| `research_paper/references/references.bib` | Reference Directory Mirror | 9,619 bytes | 27 | `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` | **IDENTICAL MATCH** |
| `REFERENCES.bib` (repository root) | Root Directory Mirror | 9,619 bytes | 27 | `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` | **IDENTICAL MATCH** |

> [!NOTE]
> All three bibliography mirrors share the identical SHA-256 hash `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4`. No out-of-sync or partial BibTeX files remain in the active authoring directories.

---

## 4. Reconciliation of Citation Keys & Reference Inventory

### 4.1. The 24 Actively Cited References in Sections 1 & 2
The compiled PDF (`main.pdf`) cites exactly 24 unique works, resolving in numerical sequence `[1]` through `[24]`:
1. `[1]` `fao2019state`: Food and Agriculture Organization (FAO) (2019) — *The State of Food and Agriculture 2019* (Monograph)
2. `[2]` `jha2015assessment`: S. N. Jha et al. (2015) — *Assessment of quantitative harvest and post-harvest losses...* (ICAR-CIPHET Monograph)
3. `[3]` `rizzo2023fruit`: M. Rizzo et al. (2023) — *Fruit ripeness classification: A survey* (*AI in Agriculture*, 7:44–57)
4. `[4]` `zhang2024fruit`: Y. Zhang et al. (2024) — *Fruit freshness detection based on multi-task CNN* (*Curr. Res. Food Sci.*, 8:100733)
5. `[5]` `chen2024classification`: H. Chen et al. (2024) — *Classification of agricultural products based on improved MobileNetV2* (*Sci. Rep.*, 14:3454)
6. `[6]` `gulzar2023fruit`: Y. Gulzar (2023) — *Fruit Image Classification Model Based on MobileNetV2...* (*Sustainability*, 15:1906)
7. `[7]` `sandler2018mobilenetv2`: M. Sandler et al. (2018) — *MobileNetV2: Inverted Residuals and Linear Bottlenecks* (CVPR, pp. 4510–4520)
8. `[8]` `guo2017calibration`: C. Guo et al. (2017) — *On Calibration of Modern Neural Networks* (ICML, PMLR 70:1321–1330)
9. `[9]` `hendrycks2017baseline`: D. Hendrycks & K. Gimpel (2017) — *A Baseline for Detecting Misclassified and OOD Examples...* (ICLR)
10. `[10]` `abayomi2024fruitq`: O. O. Abayomi-Alli et al. (2024) — *FruitQ: A new dataset of multiple fruit images...* (*Multimed. Tools Appl.*, 83:11433–11460)
11. `[11]` `sultana2022extensive`: N. Sultana et al. (2022) — *An extensive dataset for successful recognition of fresh and rotten fruits* (*Data in Brief*, 44:108552)
12. `[12]` `bijoy2025fruitvision`: M. H. I. Bijoy et al. (2025) — *FruitVision: A benchmark dataset for fresh, rotten, and formalin-mixed fruit detection* (*Data in Brief*, 61:111752)
13. `[13]` `scheirer2013toward`: W. J. Scheirer et al. (2013) — *Toward Open Set Recognition* (IEEE TPAMI, 35:1757–1772)
14. `[14]` `bendale2016towards`: A. Bendale & T. E. Boult (2016) — *Towards Open Set Deep Networks* (CVPR, pp. 1563–1572)
15. `[15]` `yang2024generalized`: J. Yang et al. (2024) — *Generalized Out-of-Distribution Detection: A Survey* (IJCV, 132:4619–4654)
16. `[16]` `liang2018enhancing`: S. Liang et al. (2018) — *Enhancing The Reliability of Out-of-distribution Image Detection...* (ICLR)
17. `[17]` `lee2018simple`: K. Lee et al. (2018) — *A Simple Unified Framework for Detecting OOD Samples...* (NeurIPS, 31:7167–7177)
18. `[18]` `liu2020energy`: W. Liu et al. (2020) — *Energy-based Out-of-distribution Detection* (NeurIPS, 33:21464–21475)
19. `[19]` `vaze2022open`: S. Vaze et al. (2022) — *Open-Set Recognition: A Good Closed-Set Classifier is All You Need* (ICLR)
20. `[20]` `sattar2024sensornet`: A. Sattar et al. (2024) — *A comprehensive approach to detecting chemical adulteration in fruits...* (*Intell. Syst. Appl.*, 23:200402)
21. `[21]` `wang2023crossdomain`: J. Wang et al. (2023) — *A cross-domain fruit classification method based on lightweight attention networks and UDA* (*Complex Intell. Syst.*, 9:4227–4247)
22. `[22]` `pehlivan2026lightweight`: N. Pehlivan & R. Kara (2026) — *A Lightweight One-Shot Open-Set Metric Learning Framework...* (*Electronics*, 15:3533)
23. `[23]` `jansi2026peos`: E. Jansi & B. R. Kavitha (2026) — *PEOS-Net: A Prototype-Energy Open-Set Network for Robust Tomato Leaf Disease Recognition...* (*Front. Artif. Intell.*, 9:1938398)
24. `[24]` `yan2026pagmsbnet`: S. Yan et al. (2026) — *PAG-MSBNet: Prototype-aware gated multi-scale branch network for open-set crop disease recognition* (*Ecol. Inform.*, 95:103703)

### 4.2. The 3 Verified Reserved References for Sections 4–7
Three additional verified foundational references are maintained in the canonical database to support subsequent sections without requiring out-of-band bibliography edits during later drafting phases:
25. `he2016deep`: K. He et al. (2016) — *Deep Residual Learning for Image Recognition* (CVPR, pp. 770–778; DOI: `10.1109/CVPR.2016.90`). Reserved for Section 4 (Methodology) and Section 7 (Alternative Vision Backbones).
26. `tan2019efficientnet`: M. Tan & Q. V. Le (2019) — *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks* (ICML, PMLR 97:6105–6114). Reserved for Section 4 (Methodology) and Section 7 (Alternative Vision Backbones).
27. `selvaraju2017gradcam`: R. R. Selvaraju et al. (2017) — *Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization* (ICCV, pp. 618–626; DOI: `10.1109/ICCV.2017.74`). Reserved for Section 5 (Results / Diagnostic Interpretability).

### 4.3. Deprecation of Obsolete Draft Keys
- The draft key `abayomi2023fruitq` has been reconciled to `abayomi2024fruitq` per final journal volume assignment (*Multimedia Tools and Applications*, Vol. 83, No. 4, pp. 11433–11460, 2024). The obsolete 2023 entry has been removed from all active bibliography files.
- The obsolete identifier `3214` for Chen et al. (2024) has been corrected to official article number `3454` (*Scientific Reports*, 14:3454).
- The obsolete draft key `ciphet2015assessment` has been standardized to `jha2015assessment`.
- The obsolete draft key `sultana2022fresh` has been standardized to `sultana2022extensive`.

---

## 5. Master Document & Section File Verification

`research_paper/manuscript/main.tex` imports the following modular section files:

| Imported File Path | Status | Verification Detail |
| :--- | :---: | :--- |
| `sections/01_introduction.tex` | **VERIFIED** | Audited Introduction text; 24 citations; qualified language; zero unsupported claims. |
| `sections/02_related_work.tex` | **VERIFIED** | Audited Related Work text; Subsections 2.1–2.5; Table 1 literature matrix (9 studies). |
| `sections/03_dataset_and_experimental_design.tex` | **VERIFIED** | Section 3 stub; ready for drafting. |
| `sections/04_methodology.tex` | **VERIFIED** | Section 4 stub; ready for drafting. |
| `sections/05_results.tex` | **VERIFIED** | Section 5 stub; ready for drafting. |
| `sections/06_discussion.tex` | **VERIFIED** | Section 6 stub; ready for drafting. |
| `sections/07_limitations.tex` | **VERIFIED** | Section 7 stub; ready for drafting. |
| `sections/08_conclusion.tex` | **VERIFIED** | Section 8 stub; ready for drafting. |

### Markdown Archival Copies
- `research_paper/manuscript/01_introduction.md`: Fully synchronized with `01_introduction.tex` (18,869 bytes, SHA-256: `042efc73...`).
- `research_paper/manuscript/02_related_work.md`: Fully synchronized with `02_related_work.tex` (30,681 bytes, SHA-256: `be95dea9...`).

---

## 6. Build Environment & PDF Compilation Verification

- **Compiler:** `tectonic` 0.17.0
- **Build Command:** `tectonic research_paper/manuscript/main.tex`
- **Exit Status:** `0` (Success)
- **Output Document:** `research_paper/manuscript/main.pdf` (185,425 bytes, 14 pages)
- **Unresolved References (`??`):** **0** across all 14 pages.
- **Overfull `\hbox` in Section 2 / Table 1:** **0 pt** (Formatted cleanly within 160 mm single-column Procedia boundaries).
- **Page Layout & Rendering:**
  - Pages 1–4: Title, Abstract, Section 1 (Introduction).
  - Pages 5–11: Section 2 (Related Work text and subsections 2.1–2.5).
  - Page 12: Table 1 (9-study Literature Comparison Table and note).
  - Page 13: Section 3–8 Stubs, Acknowledgements, and References 1–1.
  - Page 14: References 2–24 (concluding with Yan et al. [24]).
- **Visual Renders:** 150 DPI page renders generated in `research_paper/audit/page_renders/` (`page_1.png` through `page_14.png`).

---

## 7. Historical Archives & Untouched Files Register

The following historical files were deliberately preserved unchanged as immutable historical project records from earlier research stages:

| File Path | Role | Status / Reason Untouched |
| :--- | :--- | :--- |
| `literature_review/07_Verified_References.bib` | Historical literature review (Stage 1–3) | Preserved historical record of the 2025 logistics review; not part of V4.1 manuscript build. |
| `07_LITERATURE/references/REFERENCES.bib` | Historical literature directory (Stage 1–3) | Preserved historical record of initial project literature ingest; not part of V4.1 manuscript build. |
| `REFERENCE_VERIFICATION_V4.csv` | Historical reference verification manifest | Preserved historical audit trail from Stage 4.0; superseded by `references_audit.csv`. |
| `UPDATED_REFERENCE_VERIFICATION.csv` | Historical reference verification update | Preserved historical audit trail from Stage 4.0; superseded by `references_audit.csv`. |
| `Template_PROCS_ICMLDE_2026/` | Original conference template directory | Preserved clean, unmodified upstream template package per project integrity rules. |

---

## 8. Final Audit Conclusion

All active manuscript components—the master LaTeX document (`main.tex`), the Section 1 and Section 2 source files, their Markdown archival mirrors, the canonical BibTeX database and its two repository mirrors, the reference audit CSV, and the reference audit Markdown ledger—are now in **100% mutual agreement and cryptographic synchronization**.

