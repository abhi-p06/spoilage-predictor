# STAGE 4.0.3: FINAL RELEASE CONSISTENCY CORRECTION LOG
**AgriRoute Empirical Benchmark Revision: Risk-Aware Open-Set Fruit Quality Classification**  
**Role:** Independent Scientific Benchmark Auditor  
**Date:** November 10, 2026  
**Document ID:** `STAGE4_0_3_CORRECTION_LOG.md`  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** Verification & Repair Complete — Zero External Inference Executed  

---

## 1. PURPOSE AND AUDIT SCOPE

This document provides a forensic correction log for Stage 4.0.3, resolving all remaining numerical, taxonomic, algorithmic, and terminology discrepancies identified between the Stage 4.0.2 audit report, intermediate summary tables, and the underlying source data records.

In strict compliance with audit rules:
- **No external inference was executed.**
- **No external test images were opened, scored, or evaluated.**
- **Frozen Model B V4.1 checkpoint weights remain untouched** (SHA-256: `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`).
- **No original dataset images were deleted or modified.**
- **No missing evidence, licences, or scores were fabricated.**

---

## 2. DEFECT LOG & CORRECTIVE ACTIONS

### DEFECT 1: Threshold Numerical Inconsistency
- **Observation:** `STAGE4_0_2_FINAL_AUDIT_REPORT.md` Section 6.4 displayed obsolete threshold values (e.g., MSP $\tau_{95} = 0.814322$, Energy $\tau_{95} = 1.066491$, Mahalanobis $\tau_{95} = -400.126435$) carried over from earlier draft iterations. These contradicted both the actual score distribution in `experiments/open_set_v1/validation_scores.csv` and the newly generated `STAGE4_0_2_CORRECTED_THRESHOLD_TABLE.csv`.
- **Root Cause:** A draft markdown table containing legacy mock thresholds was inadvertently pasted into the final Stage 4.0.2 report text instead of copying the verified CSV outputs.
- **Corrective Action:**
  1. Recomputed every threshold strictly from `experiments/open_set_v1/validation_scores.csv` ($N=227$) using exact order-statistic indexing under the comparison rule ($S(x) \ge \tau \implies \text{Accept}$; $S(x) < \tau \implies \text{Reject}$).
  2. Single-gate $\tau_{95}$ is locked to the 12th smallest sample $s_{(12)}$ (0-indexed position 11), rejecting exactly 11 samples and accepting 216 ($95.1542\%$).
  3. Single-gate $\tau_{90}$ is locked to the 23rd smallest sample $s_{(23)}$ (0-indexed position 22), rejecting exactly 22 samples and accepting 205 ($90.3084\%$).
  4. Dual-Gate Cascade thresholds are jointly locked using empirical set intersection:
     - $\tau_{\text{cascade}, 95}$ ($s_{(7)}$, index 6 on both gates): $|R_1|=6, |R_2|=6, |R_1 \cap R_2|=1 \implies |R_{\text{union}}|=11$, accepted = 216 ($95.1542\%$).
     - $\tau_{\text{cascade}, 90}$ ($s_{(14)}$, index 13 on both gates): $|R_1|=13, |R_2|=13, |R_1 \cap R_2|=4 \implies |R_{\text{union}}|=22$, accepted = 205 ($90.3084\%$).
  5. Emitted canonical table `STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv` and reconciled every markdown text reference to match this canonical CSV to 6 decimal places.

---

### DEFECT 2: Sultana D1 Taxa Discrepancy & Partition Class Census
- **Observation:** `STAGE4_0_2_FINAL_AUDIT_REPORT.md` repeatedly asserted that Partition D1 contained "11 unseen botanical taxa from Sultana 2022" (2,000 images). However, inspection of `STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv` and the physical filesystem in `data/raw/sultana/extracted/Original Image/` revealed only five unseen species labels.
- **Root Cause:** An unverified assumption conflated external paper discussion (which discussed 15 total fruit categories across agriculture) with the actual 16 extracted folders present in `Sultana_Original.zip`.
- **Forensic Verification of Sultana Repository:**
  The physical directory `data/raw/sultana/extracted/Original Image/` contains exactly 16 subfolders (8 species $\times$ 2 conditions $\times$ 200 images):
  - **3 Known Species (Partition B):** Apple (Fresh, Rotten), Banana (Fresh, Rotten), Orange (Fresh, Rotten) $\implies 6 \times 200 = 1,200$ images (7 duplicate exclusions $\implies 1,193$ net usable).
  - **5 Unseen Species (Partition D1):** Grape, Guava, Jujube, Pomegranate, Strawberry (Fresh, Rotten) $\implies 10 \times 200 = 2,000$ images (0 duplicate exclusions $\implies 2,000$ net usable).
- **Corrective Action:**
  1. Corrected the text from "11 unseen taxa" to **"5 unseen botanical taxa (Grape, Guava, Jujube, Pomegranate, Strawberry)"**.
  2. Regenerated the exact 54-row master census `STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv` directly from `STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv`.
  3. Reconciled the Partition A class breakdown: Partition A in the evaluation manifest is the 227-image primary test set (`FINAL_GROUP_TEST_V4_1.csv`, with class distribution: Apple Fresh 34, Rotten 49; Banana Fresh 33, Rotten 47; Orange Fresh 31, Rotten 33), not the validation set (38, 38, 38, 38, 22, 53).

---

### DEFECT 3: Flawed pHash Interpretation (Multi-Label Intra-Partition Groups)
- **Observation:** `STAGE4_0_2_FINAL_AUDIT_REPORT.md` stated that all 55 intra-partition repeated pHash groups (114 rows) represented "photographic bursts of identical specimens within the same class and partition" and were marked `RETAIN_WITH_CLUSTER_FLAG`.
- **Root Cause:** Incomplete manual review. The previous report assumed that because these groups did not span multiple partition folders, their species and condition labels were identical.
- **Forensic Finding:**
  Inspection of the 55 intra-partition groups revealed that **13 groups spanning 27 rows** contain **conflicting labels**:
  - **7 groups in Partition D1:** Grape Fresh vs Grape Rotten (e.g., pHash `d3cc4c3333cc33cc`).
  - **2 groups in Partition C:** Apple Formalin vs Orange Formalin (e.g., pHash `ca15357a5a656996`).
  - **3 groups in Partition B:** Apple vs Orange, or Orange Fresh vs Rotten (e.g., pHash `e82a97955ada6169`).
  - **1 group in Partition B:** Apple Rotten vs Orange Rotten (pHash `fa2a85a55a9e6169`).
  Only **42 groups spanning 87 rows** are truly single-label intra-partition bursts.
- **Scientific Mechanism:** Low-frequency 64-bit DCT perceptual hashing captures coarse luminance envelopes. A spherical orange on a white cloth and a spherical apple on a white cloth, or grape bunches in similar lighting, can share identical DCT coefficients despite being distinct physical objects or conditions.
- **Corrective Action:**
  1. Authored `STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv` containing all 170 affected rows across 80 pHash groups, categorized into three distinct regimes:
     - `CROSS_PARTITION` (25 groups, 56 rows) $\implies$ `UNRESOLVED`
     - `INTRA_PARTITION_MULTI_LABEL` (13 groups, 27 rows) $\implies$ `UNRESOLVED_MULTI_LABEL`
     - `INTRA_PARTITION_SINGLE_LABEL` (42 groups, 87 rows) $\implies$ `RETAIN_SINGLE_LABEL_BURST`
  2. Prohibited automated deletion based on hash collision alone.
  3. Formulated explicit sensitivity analysis protocol for Stage 4.1: evaluating metrics on the full set ($N=13,465$), excluding cross-partition collisions ($N=13,409$), and excluding all unresolved collisions ($N=13,382$).

---

### DEFECT 4: Image Identifier Formula Documentation Discrepancy
- **Observation:** Section 5.2 of the Stage 4.0.2 report stated that `image_id` was computed as `dataset_prefix || "_" || original_basename || "_" || SHA256(relative_path)[:10]`. However, the Python generation script actually used the file's raw **MD5 hash prefix** (`md5[:10]`), and applied dataset-specific string cleanup.
- **Corrective Action:**
  1. Audited the manifest: all 20,781 rows in `STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv` are 100.0% globally unique (0 collisions).
  2. Amended the documentation in `STAGE4_0_3_FINAL_CONSISTENCY_AUDIT.md` to describe the exact implemented deterministic algorithm:
     - Kaggle (`A`): `kaggle_test_{md5[:10]}_{original_filename}`
     - FruitVision (`B, C, D1, D2`): `fv_{clean_filename}_{md5[:10]}`
     - Sultana (`B, D1`): `sult_{clean_filename}_{md5[:10]}`
     - ToxiFruit (`B, C, D1, D2, M1, M2`): `toxi_{cohort_folder}_{sample_index:04d}`
  3. Explicitly noted that ToxiFruit records represent prospective uningested archive records labeled `PLANNED`, and their paths are expected future archive paths rather than physically verified filesystem paths.

---

### DEFECT 5: Overreaching Chemical/Biochemical Terminology
- **Observation:** Earlier drafts occasionally referred to "detecting chemical adulteration", "detecting formaldehyde contamination", or "hazardous formalin detection" using RGB computer vision.
- **Corrective Action:**
  Strictly eliminated all claims implying that standard RGB cameras perform chemical spectroscopy or detect chemical presence. Replaced with rigorous computer vision and agricultural terminology:
  - *"dataset-labelled formalin-treatment condition"*
  - *"treatment-associated visual distribution shift"*
  - *"open-set visual anomaly rejection"*
  - *"cross-dataset generalization under post-harvest handling shifts"*
  Explicitly acknowledged that RGB imagery observes only superficial visual corrugation, discoloration, and textural artifacts associated with treatment protocols, and cannot substitute for analytical chemical assays.

---

### DEFECT 6: Dataset Licensing Provenance
- **Observation:** FruitVision 2025 was previously described as being under "Kaggle Open Data terms".
- **Corrective Action:**
  Forensic inspection of the upstream source repository established that FruitVision was authored by Hossain et al. (2024/2025) and published on Mendeley Data under **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**.
  - Non-commercial academic research and benchmarking is permitted.
  - Distribution of modified derivative datasets is restricted; local read-only in-memory benchmarking complies with these terms.
  - ToxiFruit 2026 licence remains formally classified as **`UNCONFIRMED`** pending download of the official Zenodo archive.

---

## 3. SUMMARY OF DELIVERABLES GENERATED IN STAGE 4.0.3

| Deliverable File | File Size | Row Count | Description |
| :--- | :---: | :---: | :--- |
| [`STAGE4_0_3_FINAL_CONSISTENCY_AUDIT.md`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_FINAL_CONSISTENCY_AUDIT.md) | ~35 KB | Markdown | Master consistency audit report with 100% reconciled counts, thresholds, and taxonomies |
| [`STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv) | 3,923 B | 12 rows | Canonical operating thresholds with complete inclusion-exclusion set arithmetic and order statistics |
| [`STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv) | 4,749 B | 54 rows | Complete cross-tabulated census directly generated from master image manifest |
| [`STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv) | 75,548 B | 170 rows | Row-level review of all 80 repeated pHash groups with multi-label and cross-partition isolation |
| [`STAGE4_0_3_CORRECTION_LOG.md`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_CORRECTION_LOG.md) | This File | Markdown | Forensic correction log detailing every defect, root cause, and remediation |

---
*Signed and sealed on behalf of the AgriRoute Scientific Audit Team,*  
**Independent Scientific Benchmark Auditor & Lead Methodologist**  
*November 10, 2026*

