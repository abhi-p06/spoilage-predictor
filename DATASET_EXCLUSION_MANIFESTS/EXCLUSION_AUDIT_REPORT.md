# External Dataset Exclusion & Integrity Audit Report

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Reproducibility Auditor:** Lead Scientific Reproducibility Engineer  
**Document ID:** `DATASET_EXCLUSION_MANIFESTS/EXCLUSION_AUDIT_REPORT.md`  
**Execution Timestamp:** 2026-11-09  

---

## 1. Executive Summary

An independent external audit requested an exact accounting of sample discrepancies in external datasets:
1. **FruitVision:** An earlier manifest contained 4,185 rows, whereas the evaluated benchmark contains 4,157 rows (a 28-image discrepancy).
2. **Sultana et al. (2022):** The six-class evaluation contains 1,193 images rather than the expected 1,200 class-balanced samples (a 7-image discrepancy).

Our forensic cryptographic analysis proves conclusively that **zero physical images were dropped due to arbitrary filtering or cherry-picking**. In both cases, the discrepancy is caused entirely by **exact binary duplicate files (identical MD5 hashes) present under multiple filenames in the original authors' upstream repository uploads**.

---

## 2. FruitVision Mendeley V2 Deduplication ($4,185 \to 4,157$)

- **Upstream Scanned Target Rows:** 4,185 images across the 6 target classes.
- **Unique Cryptographic MD5 Hashes:** Exactly 4,157 unique hashes.
- **Exact Binary Duplicates Identified:** Exactly 28 files ($56$ rows total; $28$ duplicate pairs).
- **Deduplication Rule:** The first instance of each unique MD5 was retained; the 28 duplicate file copies were excluded to avoid corrupting test metrics with duplicate samples.
- Full sample-by-sample listing: [`FRUITVISION_EXCLUSION_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_EXCLUSION_MANIFESTS/FRUITVISION_EXCLUSION_MANIFEST.csv).

### Representative Duplicate Pairs in FruitVision
- `msg5170347760-66762.jpg` $\leftrightarrow$ `msg5170347760-66774.jpg` (`MD5: fcd7c613960fca396f04a2cd5509cf6b`)
- `msg5170347760-65591.jpg` $\leftrightarrow$ `msg5170347760-65587.jpg` (`MD5: 5c5a8be1cdf6650c832bdd20132cc455`)
- `add (1).jpg` $\leftrightarrow$ `6150065028531862755.jpg` (`MD5: 5e43bd08714cd415160f534a06ce6de7`)

---

## 3. Sultana et al. Data in Brief 2022 Deduplication ($1,200 \to 1,193$)

- **Upstream Raw Images:** Exactly 200 images per class across 6 classes ($1,200$ images).
- **Unique Cryptographic MD5 Hashes:** Exactly 1,193 unique hashes.
- **Exact Binary Duplicates Identified:** Exactly 7 duplicate files, all residing within the `FreshOrange` class.
- **Deduplication Rule:** The primary instance was retained; the 7 duplicate files were excluded.
- Full sample-by-sample listing: [`SULTANA_EXCLUSION_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_EXCLUSION_MANIFESTS/SULTANA_EXCLUSION_MANIFEST.csv).

### Exact Duplicate Pairs in Sultana FreshOrange
1. `FreshOrange (63).jpg` $\leftrightarrow$ `FreshOrange (168).jpg` (`MD5: fd2ade13917c1b5981d999cb2b8bb37e`)
2. `FreshOrange (79).jpg` $\leftrightarrow$ `FreshOrange (66).jpg` (`MD5: c6089862f60a1d6b52611b31ac1185cc`)
3. `FreshOrange (78).jpg` $\leftrightarrow$ `FreshOrange (65).jpg` (`MD5: 10a4651896ca2bcc5b6075ec603dda03`)
4. `FreshOrange (62).jpg` $\leftrightarrow$ `FreshOrange (167).jpg` (`MD5: 0997a7ad7e4a6303ba560944c7774406`)
5. `FreshOrange (87).jpg` $\leftrightarrow$ `FreshOrange (74).jpg` (`MD5: e615bcb52711aaeab54e12c59b3eab47`)
6. `FreshOrange (88).jpg` $\leftrightarrow$ `FreshOrange (75).jpg` (`MD5: 0bbaa7e6891938911c69f9480af13143`)
7. `FreshOrange (77).jpg` $\leftrightarrow$ `FreshOrange (27).jpg` (`MD5: c3ba6f74967a8253af0d6b2ee1c80d4f`)

---

## 4. Verification Checksum Standard

Every retained sample in [`FRUITVISION_INCLUSION_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_EXCLUSION_MANIFESTS/FRUITVISION_INCLUSION_MANIFEST.csv) and [`SULTANA_INCLUSION_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_EXCLUSION_MANIFESTS/SULTANA_INCLUSION_MANIFEST.csv) contains an authoritative MD5 hash verified against physical disk bytes.
