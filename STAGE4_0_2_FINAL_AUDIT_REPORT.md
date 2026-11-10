# STAGE 4.0.2 — FINAL FORENSIC AUDIT OF CORRECTED EVALUATION MANIFEST
**AgriRoute Empirical Benchmark Revision: Risk-Aware Open-Set Fruit Quality Classification**  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Role:** Independent Scientific Data Auditor and Benchmark Methodologist  
**Audit Completion Date:** November 10, 2026  
**Active Repository Branch:** `remediation/v4-evidence-consistency`  
**Frozen Model Checkpoint:** `MODEL_B_V4_1_CHECKPOINT.keras`  
**Checkpoint SHA-256:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` (Verified Byte-Identical)  

---

## EXECUTIVE SUMMARY

This forensic audit report documents the formal verification, mathematical correction, and locking of all data structures, thresholds, and taxonomies required for the AgriRoute open-set benchmark prior to external model evaluation.

In accordance with strict read-only audit protocols:
1. **Zero External Inference Executed:** No model predictions were computed on primary test partitions, FruitVision, Sultana, or ToxiFruit datasets.
2. **Zero Checkpoint Alteration:** Frozen Model B V4.1 weights and architectures remain completely untouched and verified via SHA-256.
3. **Zero Dataset Destruction:** No original image files or metadata directories were deleted, moved, or altered.
4. **Independent Reproduction of Duplicate Finding:** The auditor independently confirmed the existence of **81 additional exact SHA-256 duplicate pairs** across partitions C, D1, and D2 in the previous manifest. Applying a deterministic tie-breaking rule (retaining the lexicographically first relative path and excluding duplicate copies), total duplicate exclusions now stand at exactly **116 images** (35 prior exclusions in Partition B + 81 new exclusions in Partitions C, D1, and D2).
5. **Net Usable Local Evaluation Set:** Exactly **13,465 local images** across five distinct experimental partitions (A: 227; B: 5,350; C: 1,917; D1: 4,776; D2: 1,195).
6. **Perceptual Hash Audit:** Audited all 80 repeated pHash values (covering 170 rows). Exactly **25 cross-partition groups spanning 56 rows** have been flagged as `UNRESOLVED` in `STAGE4_PHASH_MANUAL_REVIEW.csv` and locked for mandatory sensitivity testing. The remaining 55 intra-partition groups (114 rows) represent photographic burst captures of identical specimens within the same class and partition and are marked `RETAIN_WITH_CLUSTER_FLAG`.
7. **ToxiFruit Taxonomic Correction:** Properly categorized ToxiFruit classes into botanical and treatment partitions: Fresh Apple/Banana $\to$ Partition B (1,800); Formalin Apple/Banana $\to$ Partition C (1,800); Fresh Mango $\to$ Partition D1 (900); Formalin Mango $\to$ Partition D2 (900); Fresh Malta $\to$ Partition M1 (900); Formalin Malta $\to$ Partition M2 (900). All 7,200 rows are strictly designated `PLANNED` under `UNCONFIRMED` licence until physical acquisition from Zenodo.
8. **Mathematical Resolution of Dual-Gate Contradiction:** Resolved the empirical coverage deficit where independent 95% single-gate thresholds yielded only 91.63% joint coverage. Formulated exact inclusion-exclusion order-statistic arithmetic ($|R_1 \cup R_2| = |R_1| + |R_2| - |R_1 \cap R_2|$) and derived joint thresholds yielding exactly **95.1542%** coverage (216 accepted, 11 rejected) and **90.3084%** coverage (205 accepted, 22 rejected).
9. **Final Audit Verdict:** 
   - **GO** for Local Cross-Dataset Evaluation (Partitions A, B, C, D1, D2; $N=13,465$).
   - **CONDITIONAL GO** for Full Benchmark including ToxiFruit ($N=20,665$), conditioned upon physical download and SHA-256 verification of the Zenodo repository.

---

## PART 1 — EXACT DUPLICATE FORENSIC AUDIT

### 1.1 Independent Reproduction of 81 Additional Duplicate Pairs
The auditor independently scanned all 13,581 local candidate evaluation images across FruitVision, Sultana, and Kaggle validation splits using full 256-bit SHA-256 hashing. 

In the Stage 4.0 manifest, 35 exact binary duplicates had been excluded exclusively from Partition B (28 in FruitVision, 7 in Sultana). However, forensic analysis of the remaining rows marked `INCLUDED` revealed exactly **81 additional duplicate groups** (162 total rows, representing 81 duplicate pairs) where identical byte streams were duplicated across filesystem locations.

The 81 duplicate pairs are distributed across partitions as follows:
- **Partition C (Condition Shift Unknown - Formalin-mixed Known Species):** 33 duplicate pairs (66 rows). Redundant copies excluded: **33 images**.
- **Partition D1 (Pure Semantic Shift - Unseen Species Fresh/Rotten):** 17 duplicate pairs (34 rows). Redundant copies excluded: **17 images**.
- **Partition D2 (Combined Semantic & Treatment Shift - Unseen Species Formalin-mixed):** 31 duplicate pairs (62 rows). Redundant copies excluded: **31 images**.

### 1.2 Deterministic Resolution Rule
To eliminate evaluation bias without manual cherry-picking, a strict deterministic rule was applied:
$$\text{Retain: } \min_{\text{lexicographic}}(\text{relative\_path}) \implies \text{status} = \text{INCLUDED}$$
$$\text{All other identical SHA-256 copies} \implies \text{status} = \text{EXCLUDED}, \quad \text{reason} = \text{EXACT\_BINARY\_DUPLICATE\_SHA256}$$

No image files were modified, moved, or deleted from disk. The master manifest `STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv` explicitly records the `duplicate_group_id`, preserving complete forensic lineage.

### 1.3 Complete Census of Duplicate Exclusions (116 Total Excluded Rows)

| Dataset | Partition Group | Fruit Species | Condition | Excluded Count | Forensic Lineage / Root Cause |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **FruitVision 2025** | `B_EXTERNAL_KNOWN_SHIFT` | Orange (*C. sinensis*) | Rotten | 26 | Duplicate captures stored across multiple batch directories |
| **FruitVision 2025** | `B_EXTERNAL_KNOWN_SHIFT` | Banana (*M. acuminata*) | Rotten | 1 | Identical upload duplicate in source repository |
| **FruitVision 2025** | `B_EXTERNAL_KNOWN_SHIFT` | Orange (*C. sinensis*) | Fresh | 1 | Identical upload duplicate in source repository |
| **Sultana 2022** | `B_EXTERNAL_KNOWN_SHIFT` | Orange (*C. sinensis*) | Fresh | 6 | Duplicate image frames extracted from capture burst |
| **Sultana 2022** | `B_EXTERNAL_KNOWN_SHIFT` | Banana (*M. acuminata*) | Fresh | 1 | Duplicate frame extracted from capture burst |
| **FruitVision 2025** | `C_CONDITION_SHIFT_UNKNOWN` | Orange (*C. sinensis*) | Formalin-mixed | 31 | Duplicate web/field camera uploads in source folder |
| **FruitVision 2025** | `C_CONDITION_SHIFT_UNKNOWN` | Apple (*M. domestica*) | Formalin-mixed | 2 | Duplicate upload in source folder |
| **FruitVision 2025** | `D1_PURE_SEMANTIC_SHIFT` | Grape (*V. vinifera*) | Fresh | 17 | Near-burst or redundant uploads in source folder |
| **FruitVision 2025** | `D2_COMBINED_SEMANTIC_TREATMENT_SHIFT` | Grape (*V. vinifera*) | Formalin-mixed | 23 | Identical files duplicated across subfolders |
| **FruitVision 2025** | `D2_COMBINED_SEMANTIC_TREATMENT_SHIFT` | Mango (*M. indica*) | Formalin-mixed | 8 | Identical files duplicated across subfolders |
| **Total Excluded** | — | — | — | **116** | **35 (Stage 4.0) + 81 (Stage 4.0.2)** |

### 1.4 Net Local Usable Cohort
$$\text{Gross Local Candidate Images:} \quad 13,581$$
$$\text{Total Deduplication Exclusions:} \quad -116$$
$$\mathbf{\text{Net Usable Local Evaluation Set:}} \quad \mathbf{13,465}$$

---

## PART 2 — PERCEPTUAL HASH (pHash) AUDIT AND SENSITIVITY DESIGN

### 2.1 Perceptual Hashing Methodology
To detect near-duplicate images that escape exact SHA-256 byte matching (e.g., identical photographs subjected to re-compression, metadata stripping, minor resizing, or photographic burst captures), 64-bit Discrete Cosine Transform (DCT) perceptual hashes (`pHash`) were computed for all 13,465 usable images.

The audit revealed **80 repeated pHash values** spanning **170 rows**:
- **Intra-Partition Groups:** 55 groups spanning **114 rows**.
- **Cross-Partition Groups:** 25 groups spanning **56 rows**.

### 2.2 Forensic Inspection of 25 Cross-Partition Groups (56 Rows)
Every cross-partition collision was isolated and inspected. All 56 rows originate from `FruitVision_2025`.

Representative cross-partition collision patterns:
1. **D1 Fresh vs D2 Formalin Grape (e.g., pHash `c41b1967679a9a65`, 3 rows):**
   - Files: `msg5170347760-67835.jpg`, `msg5170347760-68023.jpg` (Formalin-mixed) vs `msg5170347760-63459.jpg` (Fresh).
   - Analysis: Grape bunches photographed against plain white cardboard share nearly identical low-frequency DCT energy distributions. While slight color differences exist, automated pHash cannot definitively rule out that the same physical bunch was photographed before and after treatment, or re-used across folders.
2. **D1 Rotten vs D2 Formalin Grape (e.g., pHash `c619196666999b67`, 5 rows):**
   - Files: Formalin-mixed grape images colliding with Rotten grape images.
3. **B Fresh vs C Formalin Orange (e.g., pHash `ca2a35a55a9e6969`, 2 rows):**
   - Files: `msg5170347760-68267.jpg` (Formalin) vs `msg5170347760-69314.jpg` (Fresh). Single centered citrus sphere on uniform dark cloth.

### 2.3 Status in `STAGE4_PHASH_MANUAL_REVIEW.csv` and Sensitivity Protocol
Because the original FruitVision collection logs lack hardware serial numbers and timestamps to definitively confirm specimen identity, an auditor must avoid subjective deletion while preventing data contamination.

Protocol locked in `STAGE4_PHASH_MANUAL_REVIEW.csv`:
- All **25 cross-partition groups (56 rows)** are designated `UNRESOLVED`.
- All **55 intra-partition groups (114 rows)** are designated `RETAIN_WITH_CLUSTER_FLAG` (since intra-partition bursts cannot cause false cross-partition leakage).
- **Mandatory Sensitivity Evaluation:** During Stage 4.1, the evaluation script must report all OOD metrics under two parallel regimes:
  1. **Primary Protocol ($N=13,465$):** All 13,465 usable images included.
  2. **Leakage-Free Sensitivity Protocol ($N=13,409$):** Exactly 56 `UNRESOLVED` cross-partition rows removed.
  3. **Verification Criterion:** If AUROC or FPR@95 varies by more than $\pm 0.5\%$ between regimes, both numbers must be explicitly reported in the final *Procedia Computer Science* manuscript.

---

## PART 3 — TOXIFRUIT TAXONOMY AND PARTITION ASSIGNMENT

### 3.1 Forensic Correction of Earlier Categorization Flaws
Earlier draft iterations exhibited severe taxonomic confusions, including mapping chemical formalin adulteration to semantic shift ($D$) or treating distinct citrus cultivars as known test classes ($B$).

The taxonomic assignments for the 7,200 planned ToxiFruit samples are formally corrected and locked below:

```
                                  TOXIFRUIT TAXONOMIC MAPPING
                                  
     Botanical Species            Chemical State               Correct Partition
 ───────────────────────────────────────────────────────────────────────────────────────
  Apple (Malus domestica)       Fresh (Lab baseline)    ──>  B_EXTERNAL_KNOWN_SHIFT (900)
  Banana (Musa acuminata)       Fresh (Lab baseline)    ──>  B_EXTERNAL_KNOWN_SHIFT (900)
  
  Apple (Malus domestica)       Formalin-treated        ──>  C_CONDITION_SHIFT_UNKNOWN (900)
  Banana (Musa acuminata)       Formalin-treated        ──>  C_CONDITION_SHIFT_UNKNOWN (900)
  
  Mango (Mangifera indica)      Fresh (Unseen species)  ──>  D1_PURE_SEMANTIC_SHIFT (900)
  Mango (Mangifera indica)      Formalin-treated        ──>  D2_COMBINED_SEMANTIC_TREATMENT_SHIFT (900)
  
  Malta (C. sinensis cv. Malta) Fresh (Cultivar shift)  ──>  M1_CULTIVAR_TRANSFER (900)
  Malta (C. sinensis cv. Malta) Formalin-treated        ──>  M2_CULTIVAR_CONDITION_SHIFT (900)
```

### 3.2 Methodological Justification
1. **Partitions B and C (Apple & Banana):** Apple and Banana are known ID training taxa for Model B V4.1. Fresh specimens under ToxiFruit imaging represent pure external sensor/lighting domain shift ($B$). Formalin-treated specimens represent the primary open-set condition shift: a known biological species subjected to an unseen, hazardous chemical condition ($C$).
2. **Partitions D1 and D2 (Mango):** Mango (*Mangifera indica*) is completely absent from Model B V4.1 training. Fresh mango represents pure semantic OOD ($D1$). Formalin-treated mango represents compounded semantic and treatment OOD ($D2$).
3. **Partitions M1 and M2 (Malta Cultivar Shift):** While Model B V4.1 was trained on sweet orange (*Citrus sinensis*), Malta orange (*Citrus sinensis cv. Malta*) is an agro-ecological cultivar exhibiting distinct rind thickness, anthocyanin pigmentation, and morphology. To preserve strict scientific rigor, Malta is segregated into exploratory partitions `M1_CULTIVAR_TRANSFER` and `M2_CULTIVAR_CONDITION_SHIFT`, preventing uncalibrated mixing with primary sweet orange test sets.

---

## PART 4 — REBUILT EVALUATION CENSUS (20,781 MASTER RECORDS)

The complete evaluation census across all datasets, partitions, taxa, and inclusion statuses is tabulated below:

### 4.1 Master Partition Summary

| Partition Group | Partition Description | Local Included | Local Excluded | Remote Planned | Total Manifest Records |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `A_PRIMARY_IN_DISTRIBUTION` | Kaggle V4.1 Raw Validation ID Knowns | 227 | 0 | 0 | 227 |
| `B_EXTERNAL_KNOWN_SHIFT` | External Known Species (Apple, Banana, Orange Fresh/Rotten) | 5,350 | 35 | 1,800 | 7,185 |
| `C_CONDITION_SHIFT_UNKNOWN` | Known Species + Hazardous Formalin Adulteration | 1,917 | 33 | 1,800 | 3,750 |
| `D1_PURE_SEMANTIC_SHIFT` | Unseen Species (Mango, Grape, 11 Sultana Taxa Fresh/Rotten) | 4,776 | 17 | 900 | 5,693 |
| `D2_COMBINED_SEMANTIC_TREATMENT_SHIFT` | Unseen Species + Hazardous Formalin Adulteration | 1,195 | 31 | 900 | 2,126 |
| `M1_CULTIVAR_TRANSFER` | Exploratory Cultivar Transfer (Fresh Malta Orange) | 0 | 0 | 900 | 900 |
| `M2_CULTIVAR_CONDITION_SHIFT` | Exploratory Cultivar Transfer + Formalin Adulteration | 0 | 0 | 900 | 900 |
| **Total Census** | — | **13,465** | **116** | **7,200** | **20,781** |

### 4.2 Detailed Breakdown of Usable Local Benchmark ($N=13,465$)

| Partition Group | Dataset | Botanical Species | Condition | Usable Count |
| :--- | :--- | :--- | :--- | :---: |
| `A_PRIMARY_IN_DISTRIBUTION` | `Kaggle_Fresh_Rotten_V4_1` | Apple (*Malus domestica*) | Fresh | 38 |
| `A_PRIMARY_IN_DISTRIBUTION` | `Kaggle_Fresh_Rotten_V4_1` | Apple (*Malus domestica*) | Rotten | 38 |
| `A_PRIMARY_IN_DISTRIBUTION` | `Kaggle_Fresh_Rotten_V4_1` | Banana (*Musa acuminata*) | Fresh | 38 |
| `A_PRIMARY_IN_DISTRIBUTION` | `Kaggle_Fresh_Rotten_V4_1` | Banana (*Musa acuminata*) | Rotten | 38 |
| `A_PRIMARY_IN_DISTRIBUTION` | `Kaggle_Fresh_Rotten_V4_1` | Orange (*Citrus sinensis*) | Fresh | 22 |
| `A_PRIMARY_IN_DISTRIBUTION` | `Kaggle_Fresh_Rotten_V4_1` | Orange (*Citrus sinensis*) | Rotten | 53 |
| *Subtotal Partition A* | — | — | — | **227** |
| `B_EXTERNAL_KNOWN_SHIFT` | `FruitVision_2025` | Apple (*Malus domestica*) | Fresh | 794 |
| `B_EXTERNAL_KNOWN_SHIFT` | `FruitVision_2025` | Apple (*Malus domestica*) | Rotten | 652 |
| `B_EXTERNAL_KNOWN_SHIFT` | `FruitVision_2025` | Banana (*Musa acuminata*) | Fresh | 741 |
| `B_EXTERNAL_KNOWN_SHIFT` | `FruitVision_2025` | Banana (*Musa acuminata*) | Rotten | 625 |
| `B_EXTERNAL_KNOWN_SHIFT` | `FruitVision_2025` | Orange (*Citrus sinensis*) | Fresh | 731 |
| `B_EXTERNAL_KNOWN_SHIFT` | `FruitVision_2025` | Orange (*Citrus sinensis*) | Rotten | 614 |
| `B_EXTERNAL_KNOWN_SHIFT` | `Sultana_2022` | Apple (*Malus domestica*) | Fresh | 200 |
| `B_EXTERNAL_KNOWN_SHIFT` | `Sultana_2022` | Apple (*Malus domestica*) | Rotten | 200 |
| `B_EXTERNAL_KNOWN_SHIFT` | `Sultana_2022` | Banana (*Musa acuminata*) | Fresh | 199 |
| `B_EXTERNAL_KNOWN_SHIFT` | `Sultana_2022` | Banana (*Musa acuminata*) | Rotten | 200 |
| `B_EXTERNAL_KNOWN_SHIFT` | `Sultana_2022` | Orange (*Citrus sinensis*) | Fresh | 194 |
| `B_EXTERNAL_KNOWN_SHIFT` | `Sultana_2022` | Orange (*Citrus sinensis*) | Rotten | 200 |
| *Subtotal Partition B* | — | — | — | **5,350** |
| `C_CONDITION_SHIFT_UNKNOWN` | `FruitVision_2025` | Apple (*Malus domestica*) | Formalin-mixed | 641 |
| `C_CONDITION_SHIFT_UNKNOWN` | `FruitVision_2025` | Banana (*Musa acuminata*) | Formalin-mixed | 627 |
| `C_CONDITION_SHIFT_UNKNOWN` | `FruitVision_2025` | Orange (*Citrus sinensis*) | Formalin-mixed | 649 |
| *Subtotal Partition C* | — | — | — | **1,917** |
| `D1_PURE_SEMANTIC_SHIFT` | `FruitVision_2025` | Mango (*Mangifera indica*) | Fresh | 763 |
| `D1_PURE_SEMANTIC_SHIFT` | `FruitVision_2025` | Mango (*Mangifera indica*) | Rotten | 630 |
| `D1_PURE_SEMANTIC_SHIFT` | `FruitVision_2025` | Grape (*Vitis vinifera*) | Fresh | 753 |
| `D1_PURE_SEMANTIC_SHIFT` | `FruitVision_2025` | Grape (*Vitis vinifera*) | Rotten | 630 |
| `D1_PURE_SEMANTIC_SHIFT` | `Sultana_2022` | 11 Unseen Botanical Taxa | Fresh | 1,000 |
| `D1_PURE_SEMANTIC_SHIFT` | `Sultana_2022` | 11 Unseen Botanical Taxa | Rotten | 1,000 |
| *Subtotal Partition D1* | — | — | — | **4,776** |
| `D2_COMBINED_SEMANTIC_TREATMENT_SHIFT` | `FruitVision_2025` | Mango (*Mangifera indica*) | Formalin-mixed | 608 |
| `D2_COMBINED_SEMANTIC_TREATMENT_SHIFT` | `FruitVision_2025` | Grape (*Vitis vinifera*) | Formalin-mixed | 587 |
| *Subtotal Partition D2* | — | — | — | **1,195** |
| **Total Usable Local** | — | — | — | **13,465** |

---

## PART 5 — GLOBALLY UNIQUE STABLE IMAGE IDENTIFIERS

### 5.1 Elimination of Index Collisions
Prior draft manifests utilized either arbitrary row index integers or bare image basenames. This introduced critical vulnerabilities:
- In `FruitVision_2025`, generic filenames like `msg5170347760-63431.jpg` occurred repeatedly across different category subfolders.
- In `Sultana_2022`, filenames like `fresh_apple_1.jpg` collided with identical filenames in other directories.
- In `ToxiFruit_2026`, filenames like `apple_fresh_001.jpg` directly overlapped with standard naming conventions.

### 5.2 Deterministic Identifier Specification
To guarantee 100% collision-free traceability across all current and future pipelines, every image record is assigned a canonical `image_id` generated according to the following deterministic formula:
$$\text{image\_id} = \text{dataset\_prefix} \mathbin{\Vert} \text{"\_"} \mathbin{\Vert} \text{original\_basename} \mathbin{\Vert} \text{"\_"} \mathbin{\Vert} \text{SHA256}(\text{relative\_path})[:10]$$

Examples:
- `fv_msg5170347760-63431.jpg_89cc7ff28d`
- `sultana_fresh_apple_1.jpg_33cfb9aa45`
- `toxi_fresh_apple_001.jpg_c5ec20bb33`

Verification in `STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv`:
$$\text{Total Records: } 20,781, \quad \text{Unique } \text{image\_id} \text{ Count: } 20,781, \quad \mathbf{\text{Collision Rate: } 0.00\%}$$
The original file basename is preserved unmodified in column `original_filename`, and the relative path from repository root is preserved in `relative_path`.

---

## PART 6 — MATHEMATICAL RESOLUTION OF DUAL-GATE CONTRADICTION

### 6.1 Audit of the Flaw in Stage 4.0
In Stage 4.0, the Dual-Gate Cascade was proposed to reject samples if Gate 1 (Free Energy) fell below $\tau_1$ **OR** Gate 2 (Calibrated Confidence) fell below $\tau_2$. Both $\tau_1$ and $\tau_2$ were independently calibrated on the 227 known validation images ($N=227$) to achieve a nominal $95\%$ acceptance rate ($s_{(12)}$).

The Stage 4.0 report asserted that combining both gates with an `AND` rule maintained 95% validation coverage. **This is mathematically impossible.**

Let:
- $R_1 = \{i : S_{\text{Energy}}(x_i) < \tau_1\}$ be the set of samples rejected by Gate 1 ($|R_1| = 11$).
- $R_2 = \{i : S_{\text{Conf}}(x_i) < \tau_2\}$ be the set of samples rejected by Gate 2 ($|R_2| = 11$).

Under a cascading rejection rule, a sample is rejected if it fails *either* gate:
$$R_{\text{union}} = R_1 \cup R_2$$
By the principle of inclusion-exclusion:
$$|R_{\text{union}}| = |R_1| + |R_2| - |R_1 \cap R_2|$$
Unless $R_1 \equiv R_2$ identically:
$$|R_1 \cup R_2| > 11 \implies \text{Joint Coverage} = \frac{N - |R_{\text{union}}|}{N} < 95.15\%$$

Empirical audit of the validation set ($N=227$) revealed that the overlap between Energy rejections and MSP rejections at rank 12 was only $|R_1 \cap R_2| = 3$. Consequently:
$$|R_{\text{union}}| = 11 + 11 - 3 = 19 \implies \text{Joint Coverage} = \frac{227 - 19}{227} = 91.6299\%$$
This represented a severe 3.37% coverage collapse below the pre-specified 95% operating target.

### 6.2 Temperature Scaling Convergence Note
Optimization of the validation temperature scalar via negative log-likelihood on raw Model B V4.1 logits yielded:
$$T^* = 1.0000 \pm 0.0000$$
Because $T^* = 1.0000$, the Platt calibrated confidence $\sigma(z_i / T^*)$ is **mathematically identical to Maximum Softmax Probability (MSP)** ($\Delta = 0.00\text{e}+00$). In all threshold specifications, Gate 2 is formally documented as MSP confidence.

### 6.3 Corrected Joint Threshold Calibration
To guarantee exact, mathematically defensible operating points matching the single-gate baselines, the Dual-Gate cascade thresholds were calibrated jointly using empirical order statistics on validation knowns ($N=227$).

```
                    DUAL-GATE CASCADE INCLUSION-EXCLUSION
                    
            Gate 1: Energy Rejections (R1)     Gate 2: MSP Rejections (R2)
            ┌───────────────────────────┐     ┌───────────────────────────┐
            │                           │     │                           │
            │           R1 \ R2         │ R1∩R2│          R2 \ R1         │
            │          (5 samples)      │ (1) │         (5 samples)       │
            │                           │     │                           │
            └───────────────────────────┴─────┴───────────────────────────┘
                                   Total Rejected = 11
                               Total Accepted = 216 (95.1542%)
```

#### A. Operating Point $\tau_{95}$ (Target: $\ge 95\%$ ID Coverage)
- **Selection Criterion:** Set threshold to the 7th smallest order statistic $s_{(7)}$ (0-indexed position 6) for both Energy and MSP:
  $$\tau_{\text{Energy}} = 0.918451, \quad \tau_{\text{MSP}} = 0.582610$$
- **Rejection Counts:** $|R_1| = 6$, $|R_2| = 6$.
- **Empirical Set Intersection:** $|R_1 \cap R_2| = 1$.
- **Joint Rejection Union:** $|R_{\text{union}}| = 6 + 6 - 1 = 11$.
- **Empirical Validation Coverage:** $\frac{227 - 11}{227} = \mathbf{95.1542\%}$ (Exactly 216 accepted, 11 rejected, identical to single-gate baselines).

#### B. Operating Point $\tau_{90}$ (Target: $\ge 90\%$ ID Coverage)
- **Selection Criterion:** Set threshold to the 14th smallest order statistic $s_{(14)}$ (0-indexed position 13) for both Energy and MSP:
  $$\tau_{\text{Energy}} = 1.133109, \quad \tau_{\text{MSP}} = 0.722009$$
- **Rejection Counts:** $|R_1| = 13$, $|R_2| = 13$.
- **Empirical Set Intersection:** $|R_1 \cap R_2| = 4$.
- **Joint Rejection Union:** $|R_{\text{union}}| = 13 + 13 - 4 = 22$.
- **Empirical Validation Coverage:** $\frac{227 - 22}{227} = \mathbf{90.3084\%}$ (Exactly 205 accepted, 22 rejected, identical to single-gate baselines).

### 6.4 Locked Threshold Calibration Table (`STAGE4_0_2_CORRECTED_THRESHOLD_TABLE.csv`)

| Method Name | Target Coverage | Order Statistic | Primary Threshold Value | Comparison Rule | Rej Union | Acc Count | Coverage |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| **MSP Baseline** | $\tau_{95}$ | $s_{(12)}$ (index 11) | $0.814322$ | $S_{\text{MSP}} \ge 0.814322$ | 11 | 216 | 95.1542% |
| **MSP Baseline** | $\tau_{90}$ | $s_{(23)}$ (index 22) | $0.932970$ | $S_{\text{MSP}} \ge 0.932970$ | 22 | 205 | 90.3084% |
| **Energy Baseline** | $\tau_{95}$ | $s_{(12)}$ (index 11) | $1.066491$ | $S_{\text{Energy}} \ge 1.066491$ | 11 | 216 | 95.1542% |
| **Energy Baseline** | $\tau_{90}$ | $s_{(23)}$ (index 22) | $1.416801$ | $S_{\text{Energy}} \ge 1.416801$ | 22 | 205 | 90.3084% |
| **ODIN Baseline** | $\tau_{95}$ | $s_{(12)}$ (index 11) | $0.166827$ | $S_{\text{ODIN}} \ge 0.166827$ | 11 | 216 | 95.1542% |
| **ODIN Baseline** | $\tau_{90}$ | $s_{(23)}$ (index 22) | $0.166948$ | $S_{\text{ODIN}} \ge 0.166948$ | 22 | 205 | 90.3084% |
| **Mahalanobis** | $\tau_{95}$ | $s_{(12)}$ (index 11) | $-400.126435$ | $S_{\text{Maha}} \ge -400.126435$ | 11 | 216 | 95.1542% |
| **Mahalanobis** | $\tau_{90}$ | $s_{(23)}$ (index 22) | $-364.551694$ | $S_{\text{Maha}} \ge -364.551694$ | 22 | 205 | 90.3084% |
| **OpenMax** | $\tau_{95}$ | $s_{(12)}$ (index 11) | $0.814322$ | $S_{\text{OpenMax}} \ge 0.814322$ | 11 | 216 | 95.1542% |
| **OpenMax** | $\tau_{90}$ | $s_{(23)}$ (index 22) | $0.932970$ | $S_{\text{OpenMax}} \ge 0.932970$ | 22 | 205 | 90.3084% |
| **Dual-Gate Cascade** | $\tau_{\text{cascade}, 95}$ | $s_{(7)}$ on both | $\tau_E=0.918451; \tau_M=0.582610$ | $(S_E \ge 0.918451) \land (S_M \ge 0.582610)$ | 11 | 216 | **95.1542%** |
| **Dual-Gate Cascade** | $\tau_{\text{cascade}, 90}$ | $s_{(14)}$ on both | $\tau_E=1.133109; \tau_M=0.722009$ | $(S_E \ge 1.133109) \land (S_M \ge 0.722009)$ | 22 | 205 | **90.3084%** |

---

## PART 7 — TRANSFORMED CONTROL STATISTICS PROTOCOL

To establish whether open-set detectors are genuinely sensitive to biological and chemical anomalies rather than superficial covariate image corruptions, four synthetic image transforms are specified in the benchmark protocol:
1. **Salt & Pepper Noise** ($p=0.02$)
2. **Gaussian Blur** ($\sigma=1.5$)
3. **Mild JPEG Compression** ($Q=50$)
4. **Mild Illumination Shift** ($\gamma=1.3$)

The scientific protocol for computing baseline statistics and thresholds under these controls is locked as follows:

### 7.1 Representation Extraction
All transformed images are passed through the frozen Model B V4.1 backbone without weight updates, extracting the 1,280-dimensional penultimate feature representation $f(x)$ and raw logit vector $z(x)$.

### 7.2 Training-Side Baseline Statistics: FROZEN CLEAN TRAINING DATA
- **Class Centroids $\mu_c$ and Ledoit-Wolf Precision Matrix $\Sigma^{-1}$:**
  Must be computed strictly on the **clean, frozen training features** ($N=1,057$ raw images).
  *Rationale:* In real-world agricultural deployments, models are trained on standard uncorrupted imagery. Re-fitting training centroids to corrupted imagery would represent test-time adaptation or retraining, violating the frozen-model protocol.
- **OpenMax Weibull Tail Fitting:**
  Must be fit strictly on extreme distances derived from the **clean, frozen training features**.
  *Rationale:* The class boundary and extreme value distribution represent the model's known internal representation.

### 7.3 Validation-Side Thresholds: DUAL EVALUATION PROTOCOL
To avoid methodological circularity while evaluating domain robustness, transformed controls must be tested under two distinct operational paradigms:
1. **Zero-Adaptation Clean Thresholds (Primary):** Apply clean thresholds ($\tau_{95}^{\text{clean}}, \tau_{90}^{\text{clean}}$) directly to transformed validation images. This measures whether synthetic noise causes erroneous false-alarm rejections on known fruit.
2. **Transform-Matched Calibration (Secondary Ablation):** Recalibrate thresholds on the transformed validation set. This measures whether recalibration can restore nominal 95% coverage under known sensor noise regimes.

Both evaluations must be reported side-by-side in the revision results.

---

## PART 8 — RIGHTS, LICENSING, AND SCHOLARLY TERMINOLOGY

### 8.1 Dataset Licensing Verification
- **FruitVision 2025:** Hosted on Kaggle under Kaggle Community Open Data terms. Non-commercial scholarly benchmarking and evaluation permitted.
- **Sultana 2022:** Published under Creative Commons Attribution 4.0 International (CC BY 4.0). Full scholarly research, citation, and evaluation permitted with attribution.
- **ToxiFruit 2026 (Zenodo):** Physical archive not yet downloaded locally. Licence status is formally classified as **`UNCONFIRMED`**. All 7,200 ToxiFruit records remain tagged with status `PLANNED` and cannot enter active benchmark inference until the Zenodo archive is retrieved, inspected, and hashed.

### 8.2 Scholarly Terminology Standardization
In accordance with Elsevier publication standards and peer-reviewer guidelines:
- The term **"pre-registered"** has been eradicated across all documents, as formal clinical/social-science trial registries (e.g., OSF, ClinicalTrials.gov) were not utilized.
- All references have been replaced with the scientifically accurate phrase: **"pre-specified and version-locked"**.
- This accurately reflects that all hypotheses, exclusion rules, feature extraction pipelines, mathematical thresholds, and evaluation partitions were locked in version-controlled git manifests prior to unsealing external test predictions.

---

## PART 9 — FINAL SCIENTIFIC AUDIT VERDICT

### 9.1 Evaluation Readiness Determination

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                             FINAL AUDIT VERDICT                                   ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║   1. LOCAL CROSS-DATASET BENCHMARK (N = 13,465 Images):                           ║
║      VERDICT: >>> GO <<<                                                          ║
║      All image checksums, relative paths, deduplications (116 excluded),           ║
║      unique identifiers, and joint mathematical thresholds are verified,          ║
║      consistent, and locked.                                                      ║
║                                                                                   ║
║   2. FULL BENCHMARK INCLUDING TOXIFRUIT (N = 20,665 Images):                      ║
║      VERDICT: >>> CONDITIONAL GO <<<                                              ║
║      All ToxiFruit rows (7,200) remain strictly marked PLANNED. Execution is      ║
║      conditioned upon physical download, extraction, SHA-256 verification,        ║
║      and licence confirmation from the Zenodo repository.                         ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

### 9.2 Mandatory Pre-Conditions for Stage 4.1 Inference
Before running inference on any external partition:
1. Confirm that `pytest tests/test_reproducibility_v4_1.py` executes with 100% pass rate.
2. Confirm that `MODEL_B_V4_1_CHECKPOINT.keras` matches SHA-256 `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`.
3. Ensure the evaluation script reads images strictly using `image_id` and `relative_path` from `STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv` filtered by `inclusion_status == 'INCLUDED'`.
4. Ensure the evaluation script applies the joint cascade thresholds from `STAGE4_0_2_CORRECTED_THRESHOLD_TABLE.csv`.
5. Execute the secondary sensitivity benchmark removing the 56 `UNRESOLVED` cross-partition pHash images to verify metric invariance.

---

## PART 10 — DELIVERABLES REGISTER

The following four locked deliverables constitute the definitive forensic record of Stage 4.0.2:

1. **`STAGE4_0_2_FINAL_AUDIT_REPORT.md`** (This document)
   - Comprehensive forensic audit report detailing duplicate reproduction, pHash review, taxonomic assignments, census tabulation, mathematical threshold resolution, control protocols, and final verdict.
2. **`STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv`** (7,688,573 bytes, 20,781 rows)
   - Full master manifest with stable `image_id`, `original_filename`, `relative_path`, physical file size, MD5, SHA-256, pHash, and inclusion statuses (13,465 `INCLUDED`, 116 `EXCLUDED`, 7,200 `PLANNED`).
3. **`STAGE4_0_2_CORRECTED_THRESHOLD_TABLE.csv`** (3,744 bytes, 12 rows)
   - Order-statistic calibration table resolving the Dual-Gate contradiction, specifying exact set sizes, intersections, unions, and coverage rates for both $\tau_{95}$ and $\tau_{90}$ operating points.
4. **`STAGE4_PHASH_MANUAL_REVIEW.csv`** (26,303 bytes, 80 rows across 10 canonical columns)
   - Forensic review of all 80 repeated pHash values, categorizing 55 intra-partition groups (114 images) as `RETAIN_WITH_CLUSTER_FLAG` and 25 cross-partition groups (56 images) as `UNRESOLVED` for sensitivity analysis.

---
*Signed and sealed on behalf of the AgriRoute Scientific Audit Team,*  
**Independent Scientific Data Auditor & Lead Benchmark Methodologist**  
*November 10, 2026*

