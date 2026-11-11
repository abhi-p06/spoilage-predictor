# AgriRoute Final Independent Bibliography Verification

**Document:** Final Independent Verification of Bibliography Synchronization and LaTeX Build Input  
**Target Venue:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026) / *Procedia Computer Science* (Elsevier)  
**Verification Date:** November 11, 2026  
**Auditor:** Senior Research Engineering Agent & Scientific Integrity Auditor  
**Status:** PASS — 100% RECONCILED, BITWISE IDENTICAL MIRRORS, ZERO BUILD DISCREPANCIES  

---

## 1. Inventory of All Bibliography Files in Repository

A comprehensive search of the Git index (`git ls-files | grep -iE '(^|/)references\.bib$'`) and a case-insensitive filesystem search across the entire workspace (excluding `.git` and build caches) identified the following bibliography files:

| # | Exact File Path | Exact Capitalization | Git Tracked? | Project Role & Category | LaTeX Build Role |
| :-: | :--- | :--- | :---: | :--- | :--- |
| **1** | `research_paper/manuscript/bibliography/references.bib` | `references.bib` (lowercase) | **Yes** | **Current Manuscript** (Canonical Master) | **ACTIVE BUILD INPUT** (Resolved by `\bibliography{bibliography/references}`) |
| **2** | `research_paper/references/references.bib` | `references.bib` (lowercase) | **Yes** | **Current Manuscript** (Reference Mirror) | Synchronized companion copy in `references/` |
| **3** | `REFERENCES.bib` (repository root) | `REFERENCES.bib` (uppercase) | **Yes** | **Current Manuscript** (Root Mirror) | Synchronized root mirror; byte-for-byte duplicate of master |
| **4** | `07_LITERATURE/references/REFERENCES.bib` | `REFERENCES.bib` (uppercase) | **Yes** | **Historical Literature Directory** | Symbolic link to `../../REFERENCES.bib` (Inode 29159730) |
| **5** | `literature_review/07_Verified_References.bib` | `07_Verified_References.bib` | **Yes** | **Historical Archive** (Stage 1–3 Logistics Review) | Not used in current build; immutable historical record |

### Status of the Root-Level `references.bib` vs. `REFERENCES.bib`
- On macOS APFS (the host operating system), the filesystem is **case-preserving but case-insensitive**.
- In the repository root, the single directory entry is named `REFERENCES.bib` (uppercase) and tracked by Git under `REFERENCES.bib`.
- File system inode verification confirms:
  ```python
  os.stat('REFERENCES.bib').st_ino == os.stat('references.bib').st_ino  # True (Inode: 29159730)
  ```
- There is **no separate or conflicting lowercase duplicate** file on disk. Any process accessing `references.bib` or `REFERENCES.bib` at root accesses the identical file (Inode 29159730, 9,619 bytes, SHA-256 `2f59991e...`).
- Git index tracks the uppercase filename `REFERENCES.bib`.

---

## 2. Verification of Actual LaTeX Build Input

Inspection of the root manuscript document [research_paper/manuscript/main.tex](file:///Users/abby/Desktop/spoilage-predictor/research_paper/manuscript/main.tex) reveals the following configuration:

```latex
%% References section
\bibliographystyle{elsarticle-num}
\bibliography{bibliography/references}
```

### Path Resolution Mechanics
1. **Document Location:** `research_paper/manuscript/main.tex`.
2. **Build Working Directory:** `research_paper/manuscript/`.
3. **Bibliography Argument:** `bibliography/references`.
4. **Resolved Input File:**
   $$\text{research\_paper/manuscript/} + \text{bibliography/references.bib} = \mathbf{research\_paper/manuscript/bibliography/references.bib}$$
5. **Auxiliary Inspection (`main.aux`):**
   ```latex
   \bibdata{bibliography/references}
   ```
   Under standard TeX / BibTeX search conventions (and internal Tectonic asset resolution), `\bibdata{bibliography/references}` instructs the engine to load the file `bibliography/references.bib` located in the subdirectory relative to `main.tex`.
6. **Confirmation:** Tectonic compiles exclusively from `research_paper/manuscript/bibliography/references.bib`. It does **not** read from the repository root `REFERENCES.bib` during the document build.

---

## 3. Independent Cryptographic Hash Verification

Cryptographic SHA-256 hashes were calculated independently across all bibliography files:

| File Path | Role | File Size | Entry Count | Complete SHA-256 Hash | Byte-for-Byte Comparison |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `research_paper/manuscript/bibliography/references.bib` | **Canonical Build Input** | 9,619 B | 27 | `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` | **REFERENCE TRUTH** |
| `research_paper/references/references.bib` | References Mirror | 9,619 B | 27 | `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` | **BITWISE IDENTICAL (100%)** |
| `REFERENCES.bib` (repository root) | Root Mirror | 9,619 B | 27 | `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` | **BITWISE IDENTICAL (100%)** |
| `07_LITERATURE/references/REFERENCES.bib` | Historical Symlink | 9,619 B | 27 | `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4` | **SYMLINK TO ROOT MIRROR** |
| `literature_review/07_Verified_References.bib` | Stage 1 Archive | 8,054 B | 20 | `ba6d3a8c1d24c5d3ce72fd933f96baf6855693683c0d844b4b1e86d5058836d1` | **HISTORICAL ARCHIVE (Preserved)** |

### Result of Hash Audit
- The three active copies (`manuscript/bibliography/references.bib`, `references/references.bib`, and root `REFERENCES.bib`) are **100% bitwise identical**.
- `07_LITERATURE/references/REFERENCES.bib` is a symlink pointing directly to `../../REFERENCES.bib`.
- `literature_review/07_Verified_References.bib` is an untouched historical file from Stage 1 (Nov 9, 2026) that contains obsolete citations from the discarded logistics system and is intentionally preserved for project auditability.

---

## 4. Citation Key Extraction & Reconciliation

An automated Python audit script extracted all `\cite{...}` commands from the imported LaTeX sections:
- `research_paper/manuscript/sections/01_introduction.tex`
- `research_paper/manuscript/sections/02_related_work.tex`

### Audit Results:
1. **Total BibTeX Entries in Canonical Database:** **27**
2. **Duplicate BibTeX Keys in Database:** **0** (All 27 keys are unique).
3. **Total Unique Citation Keys in Manuscript:** **24**
4. **Missing Citation Keys:** **0** (All 24 cited keys exist in the BibTeX file).
5. **Reserved Citation Keys in Database:** **3**
   - `he2016deep` (ResNet, CVPR 2016; DOI: `10.1109/CVPR.2016.90`) — Reserved for Section 4 (Methodology) & Section 7 (Alternative Vision Backbones).
   - `tan2019efficientnet` (EfficientNet, ICML 2019) — Reserved for Section 4 (Methodology) & Section 7 (Alternative Vision Backbones).
   - `selvaraju2017gradcam` (Grad-CAM, ICCV 2017; DOI: `10.1109/ICCV.2017.74`) — Reserved for Section 5 (Results / Diagnostic Interpretability).

### Active Citation Key Mapping (Numerical Sequence [1] to [24] in PDF):

| PDF Ref # | Citation Key | Author(s) & Year | Title / Publication |
| :---: | :--- | :--- | :--- |
| **[1]** | `fao2019state` | FAO (2019) | *The State of Food and Agriculture 2019* (Monograph) |
| **[2]** | `jha2015assessment` | S. N. Jha et al. (2015) | *Assessment of quantitative harvest and post-harvest losses...* |
| **[3]** | `rizzo2023fruit` | M. Rizzo et al. (2023) | *Fruit ripeness classification: A survey* |
| **[4]** | `zhang2024fruit` | Y. Zhang et al. (2024) | *Fruit freshness detection based on multi-task CNN* |
| **[5]** | `chen2024classification` | H. Chen et al. (2024) | *Classification of agricultural products based on improved MobileNetV2* |
| **[6]** | `gulzar2023fruit` | Y. Gulzar (2023) | *Fruit Image Classification Model Based on MobileNetV2...* |
| **[7]** | `sandler2018mobilenetv2` | M. Sandler et al. (2018) | *MobileNetV2: Inverted Residuals and Linear Bottlenecks* |
| **[8]** | `guo2017calibration` | C. Guo et al. (2017) | *On Calibration of Modern Neural Networks* |
| **[9]** | `hendrycks2017baseline` | D. Hendrycks & K. Gimpel (2017) | *A Baseline for Detecting Misclassified and OOD Examples...* |
| **[10]** | `abayomi2024fruitq` | O. O. Abayomi-Alli et al. (2024) | *FruitQ: A new dataset of multiple fruit images...* |
| **[11]** | `sultana2022extensive` | N. Sultana et al. (2022) | *An extensive dataset for successful recognition of fresh and rotten fruits* |
| **[12]** | `bijoy2025fruitvision` | M. H. I. Bijoy et al. (2025) | *FruitVision: A benchmark dataset for fresh, rotten, and formalin-mixed...* |
| **[13]** | `scheirer2013toward` | W. J. Scheirer et al. (2013) | *Toward Open Set Recognition* |
| **[14]** | `bendale2016towards` | A. Bendale & T. E. Boult (2016) | *Towards Open Set Deep Networks* |
| **[15]** | `yang2024generalized` | J. Yang et al. (2024) | *Generalized Out-of-Distribution Detection: A Survey* |
| **[16]** | `liang2018enhancing` | S. Liang et al. (2018) | *Enhancing The Reliability of Out-of-distribution Image Detection...* |
| **[17]** | `lee2018simple` | K. Lee et al. (2018) | *A Simple Unified Framework for Detecting OOD Samples...* |
| **[18]** | `liu2020energy` | W. Liu et al. (2020) | *Energy-based Out-of-distribution Detection* |
| **[19]** | `vaze2022open` | S. Vaze et al. (2022) | *Open-Set Recognition: A Good Closed-Set Classifier is All You Need* |
| **[20]** | `sattar2024sensornet` | A. Sattar et al. (2024) | *A comprehensive approach to detecting chemical adulteration in fruits...* |
| **[21]** | `wang2023crossdomain` | J. Wang et al. (2023) | *A cross-domain fruit classification method based on lightweight attention...* |
| **[22]** | `pehlivan2026lightweight` | N. Pehlivan & R. Kara (2026) | *A Lightweight One-Shot Open-Set Metric Learning Framework...* |
| **[23]** | `jansi2026peos` | E. Jansi & B. R. Kavitha (2026) | *PEOS-Net: A Prototype-Energy Open-Set Network for Robust Tomato Leaf...* |
| **[24]** | `yan2026pagmsbnet` | S. Yan et al. (2026) | *PAG-MSBNet: Prototype-aware gated multi-scale branch network...* |

### Reference Audit Files Reconciliation
- `research_paper/references/references_audit.csv`: Contains exactly **27 rows**, perfectly matching the 27 entries in the canonical BibTeX database, with columns: `citation_number`, `citation_key`, `authors`, `publication_year`, `exact_title`, `journal_or_conference`, `volume_issue_pages_or_article`, `doi_or_authoritative_url`, `publication_type`, `peer_reviewed_status`, `verification_status`, and `manuscript_section_where_cited`.
- `research_paper/references/references_audit.md`: Contains all **27 entries** with complete author rosters, venues, years, DOIs, and an explicit verification audit trail.

---

## 5. Final Build Verification & PDF Inspection

A clean rebuild of [research_paper/manuscript/main.tex](file:///Users/abby/Desktop/spoilage-predictor/research_paper/manuscript/main.tex) was executed with `tectonic` without cached intermediate files (`.bbl`, `.aux`):

```bash
tectonic research_paper/manuscript/main.tex
```

### Build Diagnostics
- **Compiler:** `tectonic` 0.17.0
- **Exit Status:** `0` (Success)
- **Output Document:** [main.pdf](file:///Users/abby/Desktop/spoilage-predictor/research_paper/manuscript/main.pdf) (181.1 KiB, 14 pages)
- **Unresolved References (`??`):** Exactly **0** across all 14 pages.
- **Overfull `\hbox` in Section 2 / Table 1:** **0 pt** (Single-column Procedia layout perfectly preserved).
- **Bibliography Section Rendering:**
  - Located on **Pages 13 and 14**.
  - Exactly **24 numbered references** (`[1]` to `[24]`) are printed in sequential order.
  - Page 13 prints reference `[1]` (`fao2019state`).
  - Page 14 prints references `[2]` through `[24]` (`jha2015assessment` through `yan2026pagmsbnet`).
- **Visual Inspection Renders:** High-resolution 150 DPI page renders for all 14 pages verified in `research_paper/audit/page_renders/` (`page_1.png` through `page_14.png`).

---

## 6. Verification Summary Checklist

- [x] Every bibliography file across repository discovered, cataloged, and inspected.
- [x] Host OS (macOS APFS case-insensitivity) inode identity confirmed between `REFERENCES.bib` and `references.bib` (Inode 29159730).
- [x] Canonical build input confirmed as `research_paper/manuscript/bibliography/references.bib` via `\bibdata{bibliography/references}`.
- [x] All three active bibliography copies independently verified bitwise identical (SHA-256: `2f59991ef3e90b940d1465285a61de0208d3043e4287dee443d3baa5508a8aa4`).
- [x] All 24 active citations in Sections 1 & 2 resolve with zero missing keys.
- [x] All 3 reserved foundational references preserved for Sections 4–7.
- [x] Zero duplicate BibTeX keys.
- [x] Reference audit CSV (27 rows) and Markdown ledger (27 entries) agree 100% with the canonical bibliography.
- [x] Clean Tectonic recompilation produces 14-page PDF with 0 unresolved `??` citations and 24 cleanly formatted reference entries.
- [x] All historical archives and experimental outputs preserved untouched.

