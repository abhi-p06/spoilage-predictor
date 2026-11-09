# Storage Audit Before Cleanup (Phase 2)

**Timestamp:** 2026-11-09 20:39:16 UTC  
**Repository:** `spoilage-predictor`  
**Total Repository Size:** 32.03 GB (34,394,127,827 bytes)  
**Total File Count:** 27,491 files  

---

## 1. Top-Level Directory Distribution

| Directory | Size | Bytes | Proportion |
| :--- | :--- | :--- | :--- |
| `.git` | 19.42 GB | 20,846,829,689 | 60.61% |
| `data` | 12.36 GB | 13,267,262,257 | 38.57% |
| `(root)` | 126.82 MB | 132,984,488 | 0.39% |
| `AGRIRoute_FINAL_EXPERIMENT_V4_1` | 94.10 MB | 98,667,014 | 0.29% |
| `archive` | 28.23 MB | 29,597,673 | 0.09% |
| `experiments` | 10.47 MB | 10,976,545 | 0.03% |
| `PHASH_COLLISION_CONTACT_SHEET` | 2.12 MB | 2,221,597 | 0.01% |
| `PHASH_REVIEW` | 2.01 MB | 2,107,020 | 0.01% |
| `DATASET_EXCLUSION_MANIFESTS` | 1.21 MB | 1,267,739 | 0.00% |
| `notebooks` | 628.28 KB | 643,358 | 0.00% |
| `scripts` | 620.51 KB | 635,399 | 0.00% |
| `tests` | 195.25 KB | 199,934 | 0.00% |
| `logs` | 132.09 KB | 135,264 | 0.00% |
| `literature_review` | 129.78 KB | 132,892 | 0.00% |
| `.agents` | 129.62 KB | 132,732 | 0.00% |
| `app` | 112.32 KB | 115,014 | 0.00% |
| `research_audit` | 69.20 KB | 70,864 | 0.00% |
| `reports` | 56.34 KB | 57,689 | 0.00% |
| `revision_audit` | 56.21 KB | 57,559 | 0.00% |
| `.playwright-mcp` | 26.10 KB | 26,727 | 0.00% |
| `.github` | 4.04 KB | 4,132 | 0.00% |
| `.pytest_cache` | 2.19 KB | 2,241 | 0.00% |

---

## 2. Redundancy and Duplication Summary

- **Exact Duplicate File Instances:** 337 files across 150 groups.
- **Wasted Storage from Binary Duplicates:** 142.64 MB (149,563,675 bytes).
- **Candidate Disposable / Archival Files:** 100 files totaling 121.24 MB.

### Top 15 Largest Files in Workspace
| Filename | Directory | Size | SHA-256 |
| :--- | :--- | :--- | :--- |
| `fruits-fresh-and-rotten-for-classification.zip` | `data` | 3.58 GB | `5ccfb8624b7a279f...` |
| `Sultana_Original.zip` | `data` | 2.60 GB | `f89d67d4c4b24810...` |
| `FruitVision_Original.zip` | `data` | 857.19 MB | `c72a8d8d9b1f44f8...` |
| `AGRIRoute_FINAL_EXPERIMENT_V4_1.zip` | `(root)` | 61.06 MB | `a18c9ac38cfda028...` |
| `historical_cnn_freshness.keras` | `archive` | 24.61 MB | `49ad201f8d18304e...` |
| `historical_cnn_freshness.keras` | `AGRIRoute_FINAL_EXPERIMENT_V4_1` | 24.61 MB | `49ad201f8d18304e...` |
| `MODEL_B_V4_1_CHECKPOINT.keras` | `(root)` | 9.27 MB | `4a12f354a4157d2b...` |
| `group_aware_mobilenet_v2_v4_1.keras` | `experiments` | 9.27 MB | `4a12f354a4157d2b...` |
| `group_aware_mobilenet_v2_v4_1.keras` | `AGRIRoute_FINAL_EXPERIMENT_V4_1` | 9.27 MB | `4a12f354a4157d2b...` |
| `MODEL_B_V4_1_CHECKPOINT.keras` | `AGRIRoute_FINAL_EXPERIMENT_V4_1` | 9.27 MB | `4a12f354a4157d2b...` |
| `group_aware_mobilenet_v2_v4_1.keras` | `AGRIRoute_FINAL_EXPERIMENT_V4_1` | 9.27 MB | `4a12f354a4157d2b...` |
| `MODEL_B_V4_1_CHECKPOINT.keras` | `AGRIRoute_FINAL_EXPERIMENT_V4_1` | 9.27 MB | `4a12f354a4157d2b...` |
| `FreshPomegranate (183).jpg` | `data` | 6.13 MB | `eecdfd3fbd684966...` |
| `GROUP_SPLIT_MANIFEST_MERGED_V4.csv` | `(root)` | 6.08 MB | `0e7d7d4522c0cfb6...` |
| `GROUP_SPLIT_MANIFEST_MERGED_V4.csv` | `AGRIRoute_FINAL_EXPERIMENT_V4_1` | 6.08 MB | `0e7d7d4522c0cfb6...` |

---

## 3. Storage Optimization Targets

1. **Disposable Caches (`__pycache__`, `.pytest_cache`, `.DS_Store`):** Can be safely pruned.
2. **Identical Root Manifests:** `FINAL_GROUP_TRAIN_V4.csv` and `FINAL_GROUP_TRAIN_V4_1.csv` are 100% bit-for-bit identical (4.47 MB each). `FINAL_GROUP_VAL_V4.csv` and `FINAL_GROUP_VAL_V4_1.csv` (951 KB each), `FINAL_GROUP_TEST_V4.csv` and `FINAL_GROUP_TEST_V4_1.csv` (955 KB each).
3. **Consolidation of Historical Material:** Organize loose `*_V3` and `*_V4` reports into `archive/v3/` and `archive/v4/` to clean the repository root.
4. **Duplicate Packaged Folders:** `AGRIRoute_FINAL_EXPERIMENT_V4_1/` contains uncompressed duplicates of checkpoints and manifests already sealed in `AGRIRoute_FINAL_EXPERIMENT_V4_1.zip`.
