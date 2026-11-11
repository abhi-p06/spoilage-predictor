# SECTION 3 AUDIT AND EVIDENCE RECONCILIATION REPORT
## AgriRoute V4.1 Research Paper — ICMLDE 2026 / Procedia Computer Science

**Document Status:** Fully Reconciled and Audited (Final Scientific Wording and Sensitivity Table Applied)  
**Date:** November 11, 2026  
**Audited Files:**
- `research_paper/manuscript/sections/03_dataset_and_experimental_design.tex`
- `research_paper/manuscript/03_dataset_and_experimental_design.md`
- `research_paper/manuscript/sections/05_results.tex`
- `research_paper/manuscript/main.tex`
- `research_paper/manuscript/main.pdf`

---

## 1. Executive Summary

Section 3 ("Dataset Census and Experimental Design") and the Section 5 sensitivity-results subsection have undergone a final scientific wording correction pass and tabular upgrade to guarantee absolute precision, evidence-bounding, and alignment with canonical empirical findings:

1. **Source Matching Framing:** Replaced over-reaching claims that source matching "controls" or "isolates" acquisition confounders with the accurate, evidence-bounded statement that source matching *reduces repository-level provenance differences, while within-repository acquisition variation remains possible*.
2. **FruitVision Cohort Framing:** Removed unsupported claims that FruitVision known and unseen subsets were photographed across the same market locations and under controlled identical camera conditions. Described strictly as same-repository comparisons.
3. **Dataset-Reported Treatment Framing:** Reframed all Cohort B and Cohort C descriptions using "dataset-reported treatment-labelled condition", explicitly disclaiming independent chemical detection, chemical immersion verification, or treatment-caused visual anomalies.
4. **Removal of Speculative Mimicry Claims:** Eliminated the speculative assertion that green guava and jujube visually mimic green apples and citrus, describing them strictly as unseen agricultural species.
5. **Deduplication Terminology:** Replaced cryptographic "hash collision" terminology when referring to duplicate files with *duplicate files identified through matching cryptographic digests* (MD5/SHA-256), preserving all 116 exclusions without asserting unverified byte-for-byte comparisons.
6. **Traceability Terminology:** Replaced "Complete experimental reproducibility" with *Experimental traceability*, explicitly distinguishing preserved internal research artifacts (predictions, checkpoints, manifests, ledgers) from external runtime, environment, and third-party publisher dependencies.
7. **pHash Scanning Radii vs. Evaluation Tiers:** Clarified pairwise Hamming radii $r \in \{0, 4, 8\}$ as scanning thresholds ($r = 0$ exact perceptual match, $r \le 4$ strict near-duplicate, $r \le 8$ permissive visual collision), cleanly distinguishing these radii from the resulting filtered evaluation tiers (Primary $N = 13,465$, Tier 1 $N = 13,409$, Tier 2 $N = 13,382$) and preserving the 56 and 83 unique global exclusions.
8. **Section 5 Sensitivity Table & Ranking Invariance:** Added a compact, overflow-free LaTeX table in `05_results.tex` presenting all five post-hoc scoring functions and the Dual-Gate operational rule across all four cohorts and three sensitivity tiers. Verified and reported that relative detector rankings remain *strictly invariant* across all tiers in every cohort, and qualified conclusions as applying to tested pHash exclusions and evaluated image records.
9. **Full Format Synchronization:** Word-for-word synchronization maintained between `03_dataset_and_experimental_design.tex` and `03_dataset_and_experimental_design.md`.

---

## 2. Partition Census Reconciliation ($N = 13,465$)

Every evaluated image record maps to an audited row in `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`. The five evaluation partitions reconcile exactly:

| Partition Code | Evaluation Role | Source Repositories | Target Status | Detailed Sub-counts | Partition $N$ |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Partition A** | Primary In-Distribution (ID Test) | Primary Kaggle Archive | Known ($\mathcal{Y}$) | Apple (F 34, R 49), Banana (F 33, R 47), Orange (F 31, R 33) | **227** |
| **Partition B** | External Known-Class Shift | FruitVision ($N=4,157$) + Sultana ($N=1,193$) | Known ($\mathcal{Y}$) | **FruitVision:** Apple (F 765, R 630), Banana (F 748, R 631), Orange (F 753, R 630)<br>**Sultana:** Apple (F 200, R 200), Banana (F 200, R 200), Orange (F 193, R 200) | **5,350** |
| **Partition C** | Treatment-Labelled Condition Shift | FruitVision | Unknown (OOD Condition) | Apple Formalin-mixed (641), Banana Formalin-mixed (660), Orange Formalin-mixed (616) | **1,917** |
| **Partition D1** | Unseen-Species Pure Semantic Shift | FruitVision ($N=2,776$) + Sultana ($N=2,000$) | Unknown (OOD Species) | **FruitVision:** Grape (F 753, R 630), Mango (F 763, R 630)<br>**Sultana:** Grape (F 200, R 200), Guava (F 200, R 200), Jujube (F 200, R 200), Pomegranate (F 200, R 200), Strawberry (F 200, R 200) | **4,776** |
| **Partition D2** | Combined Semantic \& Treatment Shift | FruitVision | Unknown (OOD Compound) | Grape Formalin-mixed (587), Mango Formalin-mixed (608) | **1,195** |
| **Total Benchmark** | **Complete Evaluation Census** | **Three Repositories** | **Audited Test Suite** | **$A (227) + B (5,350) + C (1,917) + D1 (4,776) + D2 (1,195)$** | **13,465** |

### Mathematical Reconciliations:
- **Sum by Partition:** $227 + 5,350 + 1,917 + 4,776 + 1,195 = 13,465$.
- **Sum by Source Repository:**
  - Primary Kaggle: $227$ (Partition A)
  - FruitVision: $4,157\text{ (B)} + 1,917\text{ (C)} + 2,776\text{ (D1)} + 1,195\text{ (D2)} = 10,045$.
  - Sultana et al.: $1,193\text{ (B)} + 2,000\text{ (D1)} = 3,193$.
  - Total across sources: $227 + 10,045 + 3,193 = 13,465$.
- **Partition B Reconciliation:** $4,157\text{ (FruitVision)} + 1,193\text{ (Sultana)} = 5,350$.
- **Partition D1 Reconciliation:** $2,776\text{ (FruitVision)} + 2,000\text{ (Sultana)} = 4,776$.

---

## 3. Mutual Exclusivity and Cryptographic Integrity

Cryptographic analysis of all 13,465 records in `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` confirms:
- Total rows: $13,465$
- Unique `image_id` values: $13,465$
- Unique `md5` hashes: $13,465$
- Unique `sha256` hashes: $13,465$
- Overlap between evaluation partitions: **Strictly 0**.
- Every evaluated image record is unique, mutually exclusive, and cryptographically verified.

---

## 4. Hash-Identified Duplicate Auditing vs. Upstream Augmentation Exclusions

We maintain a strict distinction between cryptographic hash duplicate removal and evaluation subset curation:
1. **Hash-Identified Deduplication ($N = 116$):**
   - Forensically identified and removed from external datasets based on matching MD5 and SHA-256 cryptographic digests, as recorded in `STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv`:
     - **FruitVision Exclusions ($N = 109$):**
       - Partition B ($N = 28$): 1 Banana Fresh, 1 Banana Rotten, 26 Orange Rotten.
       - Partition C ($N = 33$): 2 Apple Formalin-mixed, 31 Orange Formalin-mixed.
       - Partition D1 ($N = 17$): 17 Grape Fresh.
       - Partition D2 ($N = 31$): 23 Grape Formalin-mixed, 8 Mango Formalin-mixed.
       - Subtotal FruitVision: $28 + 33 + 17 + 31 = 109$.
     - **Sultana et al. Exclusions ($N = 7$):**
       - Partition B ($N = 7$): 7 Orange Fresh.
     - Total duplicate files identified through matching digests: $109 + 7 = 116$.
2. **Upstream Augmentation Exclusions ($N = 1,816$):**
   - In the primary Kaggle test archive (2,043 total files), 1,816 synthetically augmented images were excluded during dataset assembly to isolate the 227 unaugmented raw photographic records (`is_raw == 1`) for Partition A.
   - **Crucial Classification Rule:** These 1,816 exclusions represent the intentional curation of raw photographic imagery from synthetic transforms; they are **never** classified as duplicate removals.

---

## 5. Source-Matched Cohorts: Shared Baseline and Bounded Framing

Verified against `STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md` and `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`:

| Cohort | Known Reference Subset ($N_{\text{id}}$) | Shifted / OOD Subset ($N_{\text{ood}}$) | Source Repository | Shift Type | Primary Diagnostic Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cohort A** | FruitVision Known (Partition B, $N = 4,157$) | FruitVision Unseen (Partition D1, $N = 2,776$) | FruitVision | Within-Repository Semantic Shift | Same-repository evaluation of unseen fruit species (grape, mango) |
| **Cohort B** | FruitVision Known (Partition B, $N = 4,157$) | FruitVision Formalin-mixed (Partition C, $N = 1,917$) | FruitVision | Within-Repository Treatment Shift | Detector behavior on dataset-reported treatment-labelled condition |
| **Cohort C** | FruitVision Known (Partition B, $N = 4,157$) | FruitVision Preserved Unseen (Partition D2, $N = 1,195$) | FruitVision | Within-Repository Combined Shift | Interaction between unseen species and dataset-reported treatment label |
| **Cohort D** | Sultana Known (Partition B, $N = 1,193$) | Sultana Unseen (Partition D1, $N = 2,000$) | Sultana et al. | Within-Repository Semantic Shift | Semantic shift across farm and retail imagery with diverse unseen species |

### Key Methodological Clarifications:
- **Evidence-Bounded Framing:** Source matching *reduces repository-level provenance differences, while within-repository acquisition variation remains possible*. We avoid claiming complete isolation or experimental control of hardware/lighting confounders.
- **Shared Reference Population:** FruitVision Known (Partition B, $N_{\text{id}} = 4,157$) is a **shared reference subset** evaluated across Cohorts A, B, and C.
- **Dataset Non-Independence:** Because Cohorts A, B, and C reuse the identical known reference records, they do not represent statistically independent datasets.
- **Physical Non-Claim Boundary:** Formalin-treated images are evaluated strictly under their published, dataset-reported condition labels; this study does not verify chemical immersion, perform residue assays, or assert treatment-caused visual anomalies.

---

## 6. Perceptual Hash (pHash) Sensitivity Analysis: Radii, Tiers, and Tabular Results

Verified against canonical register `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv`:

### 6.1. Scanning Radii vs. Evaluation Tiers
- **Pairwise Scanning Radii:** 64-bit DCT perceptual hashes were scanned across Hamming radii $r \in \{0, 4, 8\}$:
  - $r = 0$: exact perceptual hash match;
  - $r \le 4$: strict near-duplicate match;
  - $r \le 8$: permissive visual collision.
- **Evaluation Tiers (Filtered Subsets):**
  1. **Primary Benchmark Cohort ($N = 13,465$):** Canonical baseline following cryptographic deduplication.
  2. **Tier 1 Sensitivity ($N = 13,409$):** Excludes image records exhibiting **cross-partition collisions** at Hamming radius $r \le 8$.
     - *Non-Additivity Rule:* In Tier 1, exactly 11 unique reference records from Partition B are excluded across all three FruitVision cohorts, alongside 14 shifted records from Partition D1 (Cohort A), 11 from Partition C (Cohort B), and 20 from Partition D2 (Cohort C), with 0 in Sultana et al. Global unique exclusions = $11 + 11 + 14 + 20 = 56$ records ($13,465 - 56 = 13,409$).
  3. **Tier 2 Sensitivity ($N = 13,382$):** Excludes cross-partition collisions **plus intra-partition multi-label collisions** (conflicting condition/species labels within the same partition at $r \le 8$).
     - Removes an additional 6 unique records from Partition B, 5 from Partition C, and 16 from Partition D1 (0 in D2 and Sultana). Additional multi-label exclusions = $6 + 5 + 16 = 27$.
     - Global unique exclusions across Tier 2 = $56 + 27 = 83$ records ($13,465 - 83 = 13,382$).

### 6.2. Section 5 Compact Table and Ranking Invariance

In `research_paper/manuscript/sections/05_results.tex`, Table `tab:phash_sensitivity` presents all 24 evaluated configurations:

| Evaluation Cohort | Scoring Function | Primary ($N=13,465$) | Tier 1 ($N=13,409$) | Tier 2 ($N=13,382$) | Max $|\Delta|$ (pp) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Cohort A: Semantic Shift** | MSP | 72.42% | 72.38% | 72.33% | 0.09 |
| *FruitVision B vs D1* | Energy | 81.57% | 81.53% | 81.46% | 0.11 |
| ($N_{\text{id}} = 4,157$, | ODIN | 72.30% | 72.27% | 72.20% | 0.10 |
| $N_{\text{ood}} = 2,776 \to 2,746$) | Mahalanobis | 81.41% | 81.34% | 81.27% | 0.14 |
| | OpenMax | 72.46% | 72.44% | 72.38% | 0.08 |
| | Dual-Gate | 80.93% | 80.89% | 80.82% | 0.11 |
| **Cohort B: Treatment Shift** | MSP | 58.77% | 58.80% | 58.81% | 0.04 |
| *FruitVision B vs C* | Energy | 53.13% | 53.18% | 53.19% | 0.06 |
| ($N_{\text{id}} = 4,157$, | ODIN | 56.73% | 56.78% | 56.78% | 0.05 |
| $N_{\text{ood}} = 1,917 \to 1,901$) | Mahalanobis | 47.91% | 47.96% | 48.01% | 0.10 |
| | OpenMax | 55.35% | 55.38% | 55.40% | 0.05 |
| | Dual-Gate | 53.96% | 54.01% | 54.02% | 0.06 |
| **Cohort C: Combined Shift** | MSP | 76.47% | 76.48% | 76.50% | 0.03 |
| *FruitVision B vs D2* | Energy | 84.72% | 84.64% | 84.65% | 0.08 |
| ($N_{\text{id}} = 4,157$, | ODIN | 78.11% | 78.11% | 78.13% | 0.02 |
| $N_{\text{ood}} = 1,195 \to 1,175$) | Mahalanobis | 80.08% | 79.88% | 79.86% | 0.22 |
| | OpenMax | 77.22% | 77.22% | 77.22% | 0.00 |
| | Dual-Gate | 84.16% | 84.09% | 84.10% | 0.07 |
| **Cohort D: Semantic Shift** | MSP | 59.77% | 59.77% | 59.77% | 0.00 |
| *Sultana B vs D1* | Energy | 67.52% | 67.52% | 67.52% | 0.00 |
| ($N_{\text{id}} = 1,193$, | ODIN | 60.02% | 60.02% | 60.02% | 0.00 |
| $N_{\text{ood}} = 2,000 \to 2,000$) | Mahalanobis | 68.15% | 68.15% | 68.15% | 0.00 |
| | OpenMax | 64.38% | 64.38% | 64.38% | 0.00 |
| | Dual-Gate | 66.68% | 66.68% | 66.68% | 0.00 |

### 6.3. Key Findings & Invariance Audit:
- **Detector Ranking Invariance:** Relative detector rankings are **strictly invariant** across all three tiers in all four cohorts:
  - Cohort A: Energy $>$ Mahalanobis $>$ Dual-Gate $>$ OpenMax $>$ MSP $>$ ODIN
  - Cohort B: MSP $>$ ODIN $>$ OpenMax $>$ Dual-Gate $>$ Energy $>$ Mahalanobis
  - Cohort C: Energy $>$ Dual-Gate $>$ Mahalanobis $>$ ODIN $>$ OpenMax $>$ MSP
  - Cohort D: Mahalanobis $>$ Energy $>$ Dual-Gate $>$ OpenMax $>$ ODIN $>$ MSP
- **Maximum Shift:** Bounded at $0.22$ percentage points (Mahalanobis in Cohort C).
- **Evidence-Bounded Scope:** Sensitivity conclusions apply to tested pHash collision exclusions and evaluated image records; they do not imply that all potential unmodelled capture correlations or subtle specimen re-photographing have been eliminated.

---

## 7. Validation Calibration vs. Partition A: Evidence-Bounded Separation

- **Validation Calibration Set:** $N = 227$ raw images (`is_raw == 1` in `FINAL_GROUP_VAL_V4_1.csv`).
- **Partition A (Primary ID Test):** $N = 227$ raw images (`is_raw == 1` in `FINAL_GROUP_TEST_V4_1.csv`).
- **MD5 Overlap:** Exactly **0** overlapping files between the validation raw images and test raw images.
- **Census Separation:** The validation calibration images are used strictly for prospective threshold derivation ($\tau_{95}$) and are **not** counted in the $N = 13,465$ evaluation census.
- **Evidence-Bounded Scope:** Cryptographic MD5 separation establishes that there is no exact-file overlap between the reported validation and test sets. However, this check is evidence-bounded: it demonstrates the absence of duplicate files, but cannot prove the absence of every possible upstream correlation in the underlying Kaggle collection.

---

## 8. Typography, Tables, and Compilation Audit

- **Compilation Tool:** `tectonic research_paper/manuscript/main.tex`
- **Exit Code:** `0` (Success).
- **Page Count:** 23 pages (incorporating all clarified explanations, Section 5 sensitivity table, and complete bibliography).
- **Compiler Warnings for Section 3 & Section 5:** **ZERO** overfull `\hbox`, **ZERO** underfull `\hbox`.
- **Unresolved Cross-References / Citations (`??`):** **0** across all 23 pages.
- **Table Dimensions in Procedia Single-Column Layout ($\le 16.0\text{ cm}$):**
  - Table 2 (Provenance Summary): 6 columns, width $\approx 15.85\text{ cm} \le 16.0\text{ cm}$. Zero overflow.
  - Table 3 (Partition Census): 6 columns, width $\approx 15.85\text{ cm} \le 16.0\text{ cm}$. Zero overflow.
  - Table 4 (Source-Matched Cohorts): 6 columns, width $\approx 15.85\text{ cm} \le 16.0\text{ cm}$. Zero overflow.
  - Table 5 (pHash Sensitivity Results): 6 columns, width $\approx 15.28\text{ cm} \le 16.0\text{ cm}$. Zero overflow.
- **Visual Page Renders:** All 23 pages rendered at 150 DPI into `research_paper/audit/page_renders/` (`page_01.png` through `page_23.png`).

---

## 9. Scientific Restriction Compliance Checklist

- [x] Source matching framed as *reducing repository-level provenance differences, while within-repository acquisition variation remains possible*.
- [x] Removed unsupported claim that FruitVision known/unseen subsets were photographed across same market locations with same smartphone cameras.
- [x] Cohort B and Cohort C descriptions reframed strictly as *dataset-reported treatment-labelled condition*; zero claims of chemical detection or residue verification.
- [x] Speculative claim of guava/jujube visual mimicry removed; described simply as diverse unseen agricultural species.
- [x] Deduplication terminology standardized to *duplicate files identified through matching cryptographic digests* (MD5/SHA-256); no byte-for-byte claims asserted.
- [x] Reproducibility terminology reframed as *Experimental traceability*, explicitly distinguishing preserved internal research artifacts from external dependencies.
- [x] Pairwise pHash scanning radii $r \in \{0, 4, 8\}$ clearly explained and distinguished from evaluation tiers (Primary, Tier 1, Tier 2); 56 and 83 unique global exclusions preserved.
- [x] Compact Table 5 in `05_results.tex` presents all 5 OOD detectors + Dual-Gate across all 4 cohorts and 3 tiers with zero layout overflow.
- [x] Relative detector rankings verified and reported as strictly invariant across all tiers in every cohort.
- [x] Sensitivity conclusions explicitly qualified as applying to tested pHash exclusions and evaluated image records.
- [x] Word-for-word synchronization maintained between `03_dataset_and_experimental_design.tex` and `03_dataset_and_experimental_design.md`.
- [x] Model checkpoint strictly frozen (`MODEL_B_V4_1_CHECKPOINT.keras`, SHA-256: `4a12f354...b6b4`).
- [x] Canonical prediction records unchanged (`STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`).
- [x] Operating thresholds strictly locked a priori on validation data; no post-hoc tuning on test sets.
- [x] Progress log updated accurately.
