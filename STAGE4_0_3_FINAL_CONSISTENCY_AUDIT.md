# STAGE 4.0.3: FINAL RELEASE CONSISTENCY AUDIT REPORT
**AgriRoute Empirical Benchmark Revision: Risk-Aware Open-Set Fruit Quality Classification**  
**Role:** Independent Scientific Benchmark Auditor & Lead Methodologist  
**Document ID:** `STAGE4_0_3_FINAL_CONSISTENCY_AUDIT.md`  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Date:** November 10, 2026  
**Repository Branch:** `remediation/v4-evidence-consistency`  
**Model Checkpoint:** `MODEL_B_V4_1_CHECKPOINT.keras`  
**Checkpoint SHA-256:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` (Byte-Identical, Untouched)  

---

## EXECUTIVE SUMMARY & AUDIT VERDICT

This consistency audit formally verifies, reconciles, and locks all data structures, mathematical thresholds, partition censuses, perceptual hash classifications, and scientific documentation for the AgriRoute open-set fruit quality benchmark.

### Core Audit Outcomes
1. **Zero External Inference Executed:** No primary test images, FruitVision, Sultana, or ToxiFruit images were unsealed or evaluated during this stage. Model B V4.1 remains completely frozen.
2. **Reconciled Operating Thresholds:** Derived and verified every single-method and dual-gate threshold strictly from [`experiments/open_set_v1/validation_scores.csv`](file:///Users/abby/Desktop/spoilage-predictor/experiments/open_set_v1/validation_scores.csv) ($N=227$). All values in this report match [`STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv) to six decimal places.
3. **Partition Census Reconciled:** Generated [`STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv) directly from [`STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv). Resolved the Sultana D1 discrepancy: the dataset contains exactly **5 unseen botanical taxa** (2,000 images), not 11 as previously claimed in narrative drafts. Reconciled Partition A class counts to the primary test set in the manifest ($N=227$).
4. **Forensic pHash Reclassification:** Corrected the erroneous assumption that all 55 intra-partition repeated pHash groups were same-class bursts. Identified **13 multi-label intra-partition groups (27 rows)** exhibiting conflicting species or freshness labels due to DCT low-frequency luminance similarities. All 25 cross-partition groups (56 rows) and 13 multi-label groups (27 rows) are locked as `UNRESOLVED` in [`STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv) for mandatory three-tier sensitivity analysis.
5. **Image-ID Implementation Truth:** Documented the actual deterministic string-construction algorithm used in the manifest (`md5[:10]` prefix and clean basenames), verifying 100.0% uniqueness (20,781 unique IDs, 0 collisions).
6. **Scientific Terminology Alignment:** Eradicated all overreaching claims suggesting RGB cameras detect chemical contamination or residual formaldehyde; enforced precise terminology (*"dataset-labelled formalin-treatment condition"*, *"treatment-associated visual distribution shift"*, *"open-set visual rejection"*).
7. **Licensing Integrity:** Clarified that FruitVision is distributed via Mendeley Data under **CC BY-NC-ND 4.0** (not generic Kaggle terms), and maintained ToxiFruit licence as **`UNCONFIRMED`** with rows tagged **`PLANNED`**.

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                             FINAL AUDIT VERDICT                                   ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║   1. LOCAL CROSS-DATASET BENCHMARK (N = 13,465 Usable Local Images):              ║
║      VERDICT: >>> GO <<<                                                          ║
║      All image checksums, relative paths, deduplications (116 excluded),           ║
║      unique identifiers, and joint mathematical thresholds are verified,          ║
║      consistent, and locked.                                                      ║
║                                                                                   ║
║   2. FULL BENCHMARK INCLUDING TOXIFRUIT (N = 20,665 Total Usable Images):         ║
║      VERDICT: >>> CONDITIONAL GO <<<                                              ║
║      All ToxiFruit rows (7,200) remain strictly marked PLANNED. Execution is      ║
║      conditioned upon physical retrieval, extraction, SHA-256 verification,        ║
║      and licence confirmation from the official Zenodo repository.                ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. CANONICAL OPERATING THRESHOLDS & ORDER-STATISTIC VERIFICATION

### 1.1 Source of Truth & Decision Rules
All baseline detectors and the Dual-Gate Cascade are calibrated strictly using [`experiments/open_set_v1/validation_scores.csv`](file:///Users/abby/Desktop/spoilage-predictor/experiments/open_set_v1/validation_scores.csv), which contains the raw logits, features, and detector scores for all $N=227$ raw validation images extracted from frozen Model B V4.1.

The standardized decision rule applied across all methods is:
$$\text{Decision}(x) = \begin{cases} \text{Accept as In-Distribution Known}, & \text{if } S(x) \ge \tau \\ \text{Reject as Out-of-Distribution / Unknown}, & \text{if } S(x) < \tau \end{cases}$$

### 1.2 Order-Statistic Indexing & Operating Points
Because the validation cohort consists of $N=227$ discrete samples, thresholds are derived using sample order statistics $s_{(1)} \le s_{(2)} \le \dots \le s_{(227)}$:
- **Primary Operating Target ($\tau_{95}$, $\sim 95\%$ ID Coverage):**  
  Threshold is set to the 12th smallest order statistic $s_{(12)}$ (0-indexed position 11).  
  Samples with $S(x) < s_{(12)}$ are rejected (ranks 1 through 11, exactly 11 samples).  
  Samples with $S(x) \ge s_{(12)}$ are accepted (ranks 12 through 227, exactly 216 samples).  
  $$\text{Empirical In-Distribution Coverage} = \frac{216}{227} = \mathbf{95.1542\%}$$
- **Secondary Operating Target ($\tau_{90}$, $\sim 90\%$ ID Coverage):**  
  Threshold is set to the 23rd smallest order statistic $s_{(23)}$ (0-indexed position 22).  
  Samples with $S(x) < s_{(23)}$ are rejected (ranks 1 through 22, exactly 22 samples).  
  Samples with $S(x) \ge s_{(23)}$ are accepted (ranks 23 through 227, exactly 205 samples).  
  $$\text{Empirical In-Distribution Coverage} = \frac{205}{227} = \mathbf{90.3084\%}$$

### 1.3 Tie Analysis
Audit of all 227 validation scores confirmed:
- `score_msp`, `score_energy_id`, `score_mahalanobis_id`, `score_openmax_id`, and `score_calibrated_conf` exhibit **zero tied scores** across the entire validation distribution (227 unique values out of 227).
- `score_odin` contains 3 duplicate pairs far above the operating thresholds (at scores 0.167319, 0.167396, and 0.167532). At the operating points $s_{(12)}$ and $s_{(23)}$, ODIN values are strictly unique ($s_{(12)} = 0.167164$, $s_{(23)} = 0.167207$).
- Therefore, the strict inequality $S(x) < \tau$ rejects exactly 11 and 22 samples respectively, with zero threshold-boundary tie ambiguity.

### 1.4 Dual-Gate Cascade Joint Set Formulation
Under a cascade rejecting if $S_{\text{Energy}}(x) < \tau_{\text{Energy}}$ **OR** $S_{\text{MSP}}(x) < \tau_{\text{MSP}}$, the joint rejection set is $R_{\text{union}} = R_1 \cup R_2$.
By inclusion-exclusion: $|R_{\text{union}}| = |R_1| + |R_2| - |R_1 \cap R_2|$.

To achieve exact coverage matching single-gate baselines:
1. **$\tau_{\text{cascade}, 95}$ ($95.1542\%$ Coverage):**  
   Set thresholds to the 7th smallest order statistic $s_{(7)}$ (0-indexed position 6) on both gates:
   $$\tau_{\text{Energy}} = 0.918451, \quad \tau_{\text{MSP}} = 0.582610$$
   $|R_1| = 6$, $|R_2| = 6$, with empirical intersection $R_1 \cap R_2 = \{14\}$ (sample index 14, $|R_1 \cap R_2| = 1$).  
   $$|R_{\text{union}}| = 6 + 6 - 1 = 11 \implies \text{Accepted} = 227 - 11 = 216 \quad (\mathbf{95.1542\%})$$
2. **$\tau_{\text{cascade}, 90}$ ($90.3084\%$ Coverage):**  
   Set thresholds to the 14th smallest order statistic $s_{(14)}$ (0-indexed position 13) on both gates:
   $$\tau_{\text{Energy}} = 1.133109, \quad \tau_{\text{MSP}} = 0.722009$$
   $|R_1| = 13$, $|R_2| = 13$, with empirical intersection $R_1 \cap R_2 = \{14, 68, 73, 96\}$ ($|R_1 \cap R_2| = 4$).  
   $$|R_{\text{union}}| = 13 + 13 - 4 = 22 \implies \text{Accepted} = 227 - 22 = 205 \quad (\mathbf{90.3084\%})$$

### 1.5 Temperature Scaling Equivalence Note
Validation temperature scalar optimization converged to $T^* = 1.0000 \pm 0.0000$. Consequently, Platt calibrated confidence is **mathematically identical to Maximum Softmax Probability (MSP)** ($\max |S_{\text{Calib}} - S_{\text{MSP}}| = 0.00\text{e}+00$). Gate 2 is therefore functionally identical to MSP confidence.

### 1.6 Canonical Operating Threshold Table
The values below match [`STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv) exactly:

| Configuration ID | Scorer / Baseline Name | Target | Order Statistic | Primary Threshold Value | Decision Rule | Rej Count | Acc Count | Empirical Coverage |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| `score_msp_tau95` | MSP (Maximum Softmax Probability) | $\tau_{95}$ | $s_{(12)}$ (index 11) | $0.700580$ | $S_{\text{MSP}} \ge 0.700580$ | 11 | 216 | 95.1542% |
| `score_msp_tau90` | MSP (Maximum Softmax Probability) | $\tau_{90}$ | $s_{(23)}$ (index 22) | $0.792790$ | $S_{\text{MSP}} \ge 0.792790$ | 22 | 205 | 90.3084% |
| `score_energy_id_tau95` | Energy (ID Free Energy T=1.0) | $\tau_{95}$ | $s_{(12)}$ (index 11) | $1.054579$ | $S_{\text{Energy}} \ge 1.054579$ | 11 | 216 | 95.1542% |
| `score_energy_id_tau90` | Energy (ID Free Energy T=1.0) | $\tau_{90}$ | $s_{(23)}$ (index 22) | $1.309243$ | $S_{\text{Energy}} \ge 1.309243$ | 22 | 205 | 90.3084% |
| `score_odin_tau95` | ODIN (T=1000.0, eps=0.0014) | $\tau_{95}$ | $s_{(12)}$ (index 11) | $0.167164$ | $S_{\text{ODIN}} \ge 0.167164$ | 11 | 216 | 95.1542% |
| `score_odin_tau90` | ODIN (T=1000.0, eps=0.0014) | $\tau_{90}$ | $s_{(23)}$ (index 22) | $0.167207$ | $S_{\text{ODIN}} \ge 0.167207$ | 22 | 205 | 90.3084% |
| `score_mahalanobis_id_tau95` | Ledoit-Wolf Mahalanobis | $\tau_{95}$ | $s_{(12)}$ (index 11) | $-65.133230$ | $S_{\text{Maha}} \ge -65.133230$ | 11 | 216 | 95.1542% |
| `score_mahalanobis_id_tau90` | Ledoit-Wolf Mahalanobis | $\tau_{90}$ | $s_{(23)}$ (index 22) | $-58.251335$ | $S_{\text{Maha}} \ge -58.251335$ | 22 | 205 | 90.3084% |
| `score_openmax_id_tau95` | OpenMax (eta=20, alpha=2) | $\tau_{95}$ | $s_{(12)}$ (index 11) | $0.778938$ | $S_{\text{OpenMax}} \ge 0.778938$ | 11 | 216 | 95.1542% |
| `score_openmax_id_tau90` | OpenMax (eta=20, alpha=2) | $\tau_{90}$ | $s_{(23)}$ (index 22) | $0.837232$ | $S_{\text{OpenMax}} \ge 0.837232$ | 22 | 205 | 90.3084% |
| `dual_gate_cascade_tau95` | Dual-Gate Cascade (Energy AND MSP) | $\tau_{\text{cascade}, 95}$ | $s_{(7)}$ on both | $\tau_E=0.918451; \tau_M=0.582610$ | $(S_E \ge 0.918451) \land (S_M \ge 0.582610)$ | 11 | 216 | **95.1542%** |
| `dual_gate_cascade_tau90` | Dual-Gate Cascade (Energy AND MSP) | $\tau_{\text{cascade}, 90}$ | $s_{(14)}$ on both | $\tau_E=1.133109; \tau_M=0.722009$ | $(S_E \ge 1.133109) \land (S_M \ge 0.722009)$ | 22 | 205 | **90.3084%** |

---

## 2. RECONCILED PARTITION CENSUS & CLASS-BY-CLASS BREAKDOWN

### 2.1 Reconciled Master Summary

| Partition Group | Partition Description | Local Included | Local Excluded | Remote Planned | Total Manifest Rows |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `A_PRIMARY_IN_DISTRIBUTION` | Kaggle Fresh/Rotten V4.1 Primary Test (is_raw == 1) | 227 | 0 | 0 | 227 |
| `B_EXTERNAL_KNOWN_SHIFT` | External Known Species (Apple, Banana, Orange Fresh/Rotten) | 5,350 | 35 | 1,800 | 7,185 |
| `C_CONDITION_SHIFT_UNKNOWN` | Known Species + Labelled Formalin Treatment | 1,917 | 33 | 1,800 | 3,750 |
| `D1_PURE_SEMANTIC_SHIFT` | Unseen Botanical Species (Fresh & Rotten) | 4,776 | 17 | 900 | 5,693 |
| `D2_COMBINED_SEMANTIC_TREATMENT_SHIFT` | Unseen Botanical Species + Labelled Formalin Treatment | 1,195 | 31 | 900 | 2,126 |
| `M1_CULTIVAR_TRANSFER` | Exploratory Cultivar Transfer (Fresh Malta Orange) | 0 | 0 | 900 | 900 |
| `M2_CULTIVAR_CONDITION_SHIFT` | Exploratory Cultivar Transfer + Labelled Formalin Treatment | 0 | 0 | 900 | 900 |
| **Total Evaluation Manifest Records** | — | **13,465** | **116** | **7,200** | **20,781** |

### 2.2 Resolution of the Sultana D1 Discrepancy
Forensic inspection of the Sultana dataset archive (`data/raw/sultana/extracted/Original Image/`) confirmed exactly 16 subdirectories corresponding to 8 botanical species:
- **Known Species (Partition B):** Apple (Fresh: 200, Rotten: 200), Banana (Fresh: 200, Rotten: 200), Orange (Fresh: 200, Rotten: 200) $\implies$ 1,200 raw images (7 duplicate exclusions in Fresh Orange $\implies$ 1,193 usable).
- **Unseen Species (Partition D1):** Exactly **5 unseen botanical taxa** (not 11):
  1. *Vitis vinifera* (Grape): 200 Fresh, 200 Rotten (400 images)
  2. *Psidium guajava* (Guava): 200 Fresh, 200 Rotten (400 images)
  3. *Ziziphus jujuba* (Jujube): 200 Fresh, 200 Rotten (400 images)
  4. *Punica granatum* (Pomegranate): 200 Fresh, 200 Rotten (400 images)
  5. *Fragaria $\times$ ananassa* (Strawberry): 200 Fresh, 200 Rotten (400 images)  
  $$\text{Total Sultana D1 Usable Images} = 5 \text{ species} \times 2 \text{ conditions} \times 200 = \mathbf{2,000 \text{ images}}$$

The prior claim of "11 unseen taxa" was an unverified narrative assumption from general food-waste literature. The actual local filesystem contains 5 unseen species, fully accounted for in the manifest.

### 2.3 Detailed Class-by-Class Census (`STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv`)

```
========================================================================================================
PARTITION A: PRIMARY IN-DISTRIBUTION TEST SET (Kaggle Fresh/Rotten V4.1, is_raw == 1)
--------------------------------------------------------------------------------------------------------
  Apple (Malus domestica)     Fresh:   34 INCLUDED | Rotten:   49 INCLUDED   --> Subtotal:  83
  Banana (Musa acuminata)     Fresh:   33 INCLUDED | Rotten:   47 INCLUDED   --> Subtotal:  80
  Orange (Citrus sinensis)    Fresh:   31 INCLUDED | Rotten:   33 INCLUDED   --> Subtotal:  64
                                                                                 Partition A Total: 227
========================================================================================================
PARTITION B: EXTERNAL KNOWN SHIFT (FruitVision 2025 + Sultana 2022 + ToxiFruit 2026 Planned)
--------------------------------------------------------------------------------------------------------
  FruitVision 2025:
    Apple (Malus domestica)   Fresh:  765 INCLUDED | Rotten:  630 INCLUDED   --> Subtotal: 1395
    Banana (Musa acuminata)   Fresh:  748 INCLUDED (1 Excluded) | Rotten: 631 INCLUDED (1 Excluded) -> 1379
    Orange (Citrus sinensis)  Fresh:  753 INCLUDED | Rotten:  630 INCLUDED (26 Excluded)           -> 1383
  Sultana 2022:
    Apple (Malus domestica)   Fresh:  200 INCLUDED | Rotten:  200 INCLUDED   --> Subtotal:  400
    Banana (Musa acuminata)   Fresh:  200 INCLUDED | Rotten:  200 INCLUDED   --> Subtotal:  400
    Orange (Citrus sinensis)  Fresh:  193 INCLUDED (7 Excluded) | Rotten: 200 INCLUDED             ->  393
  ToxiFruit 2026 (Planned):
    Apple (Malus domestica)   Fresh:  900 PLANNED                            --> Subtotal:  900
    Banana (Musa acuminata)   Fresh:  900 PLANNED                            --> Subtotal:  900
                                                Local Usable: 5,350 | Local Excluded: 35 | Planned: 1,800
========================================================================================================
PARTITION C: CONDITION SHIFT UNKNOWN (Known Species + Labelled Formalin Treatment)
--------------------------------------------------------------------------------------------------------
  FruitVision 2025:
    Apple (Malus domestica)   Formalin-mixed:  641 INCLUDED (2 Excluded)     --> Subtotal:  641
    Banana (Musa acuminata)   Formalin-mixed:  660 INCLUDED                  --> Subtotal:  660
    Orange (Citrus sinensis)  Formalin-mixed:  616 INCLUDED (31 Excluded)    --> Subtotal:  616
  ToxiFruit 2026 (Planned):
    Apple (Malus domestica)   Formalin-treated: 900 PLANNED                  --> Subtotal:  900
    Banana (Musa acuminata)   Formalin-treated: 900 PLANNED                  --> Subtotal:  900
                                                Local Usable: 1,917 | Local Excluded: 33 | Planned: 1,800
========================================================================================================
PARTITION D1: PURE SEMANTIC SHIFT (Unseen Species Fresh & Rotten)
--------------------------------------------------------------------------------------------------------
  FruitVision 2025:
    Grape (Vitis vinifera)    Fresh:  753 INCLUDED (17 Excluded) | Rotten: 630 INCLUDED    -> 1383
    Mango (Mangifera indica)  Fresh:  763 INCLUDED | Rotten: 630 INCLUDED                  -> 1393
  Sultana 2022 (5 Unseen Species):
    Grape (Vitis vinifera)    Fresh:  200 INCLUDED | Rotten:  200 INCLUDED   --> Subtotal:  400
    Guava (Psidium guajava)   Fresh:  200 INCLUDED | Rotten:  200 INCLUDED   --> Subtotal:  400
    Jujube (Ziziphus jujuba)  Fresh:  200 INCLUDED | Rotten:  200 INCLUDED   --> Subtotal:  400
    Pomegranate (P. granatum) Fresh:  200 INCLUDED | Rotten:  200 INCLUDED   --> Subtotal:  400
    Strawberry (Fragaria)     Fresh:  200 INCLUDED | Rotten:  200 INCLUDED   --> Subtotal:  400
  ToxiFruit 2026 (Planned):
    Mango (Mangifera indica)  Fresh:  900 PLANNED                            --> Subtotal:  900
                                                Local Usable: 4,776 | Local Excluded: 17 | Planned: 900
========================================================================================================
PARTITION D2: COMBINED SEMANTIC & TREATMENT SHIFT (Unseen Species + Labelled Formalin)
--------------------------------------------------------------------------------------------------------
  FruitVision 2025:
    Grape (Vitis vinifera)    Formalin-mixed:  587 INCLUDED (23 Excluded)    --> Subtotal:  587
    Mango (Mangifera indica)  Formalin-mixed:  608 INCLUDED (8 Excluded)     --> Subtotal:  608
  ToxiFruit 2026 (Planned):
    Mango (Mangifera indica)  Formalin-treated: 900 PLANNED                  --> Subtotal:  900
                                                Local Usable: 1,195 | Local Excluded: 31 | Planned: 900
========================================================================================================
PARTITIONS M1 & M2: EXPLORATORY CULTIVAR TRANSFER (ToxiFruit 2026 Planned)
--------------------------------------------------------------------------------------------------------
  M1 (Fresh Malta Orange):    Fresh:             900 PLANNED                 --> Subtotal:  900
  M2 (Formalin Malta Orange): Formalin-treated:  900 PLANNED                 --> Subtotal:  900
========================================================================================================
```

---

## 3. PERCEPTUAL HASH (pHash) FORENSIC REVIEW & SENSITIVITY DESIGN

### 3.1 Taxonomy of Repeated pHash Groups
All 80 repeated pHash values covering 170 rows among the 13,465 usable images were forensically reviewed and catalogued in [`STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv).

The 80 groups divide into three distinct operational regimes:
1. **`CROSS_PARTITION` (25 groups, 56 rows):** Images sharing identical 64-bit pHashes across distinct evaluation partitions (e.g., Partition D1 Grape vs Partition D2 Formalin Grape; Partition B Orange vs Partition C Formalin Orange). Status: **`UNRESOLVED`**.
2. **`INTRA_PARTITION_MULTI_LABEL` (13 groups, 27 rows):** Images residing within the same partition folder that share identical pHashes despite carrying **conflicting botanical species or freshness labels**. Status: **`UNRESOLVED_MULTI_LABEL`**.
3. **`INTRA_PARTITION_SINGLE_LABEL` (42 groups, 87 rows):** Images within the same partition sharing identical pHashes and **identical species and condition labels** (e.g., burst captures of the same orange). Status: **`RETAIN_SINGLE_LABEL_BURST`**.

### 3.2 Detailed Audit of Multi-Label Intra-Partition Groups (13 Groups, 27 Rows)
The table below documents all 13 multi-label collisions occurring inside individual partitions:

| Group ID | Perceptual Hash | Partition Group | Rows | Species Involved | Conditions Involved | Root Cause / Mechanism |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| `PHASH_GRP_03` | `ca15357a5a656996` | `C_CONDITION_SHIFT_UNKNOWN` | 3 | Apple & Orange | Formalin-mixed | Centered spherical fruit on plain background yielding identical low-frequency DCT luminance profile. |
| `PHASH_GRP_10` | `d3cc4c3333cc33cc` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Dark grape bunch on white paper; textural rot details reside in high-frequency DCT bands discarded by pHash. |
| `PHASH_GRP_14` | `c59a1a65659a7761` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Similar bunch silhouette and lighting geometry across fresh and rotting lots. |
| `PHASH_GRP_18` | `c619196666995b67` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Low-frequency DCT collision across grape bunches. |
| `PHASH_GRP_19` | `c51e1a65659e3365` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Low-frequency DCT collision across grape bunches. |
| `PHASH_GRP_22` | `e16786d6989a5999` | `B_EXTERNAL_KNOWN_SHIFT` | 2 | Orange | Fresh & Rotten | WhatsApp mobile upload vs field camera upload of single centered citrus. |
| `PHASH_GRP_35` | `c59e1e61699e1669` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Low-frequency DCT collision across grape bunches. |
| `PHASH_GRP_38` | `e82a97955ada6169` | `B_EXTERNAL_KNOWN_SHIFT` | 2 | Apple & Orange | Rotten & Fresh | Spherical fruit boundary collision on uniform background. |
| `PHASH_GRP_51` | `c51a1e65619e9e69` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Low-frequency DCT collision across grape bunches. |
| `PHASH_GRP_53` | `fa2a85a55a9e6169` | `B_EXTERNAL_KNOWN_SHIFT` | 2 | Apple & Orange | Rotten | Severe rot discoloration creating similar global dark circle envelope. |
| `PHASH_GRP_57` | `ca15355ada656996` | `C_CONDITION_SHIFT_UNKNOWN` | 2 | Apple & Orange | Formalin-mixed | Spherical fruit boundary collision on uniform background. |
| `PHASH_GRP_65` | `c59a1a65619e9e69` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Low-frequency DCT collision across grape bunches. |
| `PHASH_GRP_75` | `c51e1e65619e9669` | `D1_PURE_SEMANTIC_SHIFT` | 2 | Grape | Fresh & Rotten | Low-frequency DCT collision across grape bunches. |

### 3.3 Prohibition of Automated Deletion & Sensitivity Protocol
Because standard perceptual hashing discards high-frequency DCT components (where surface fungal mycelium, peel pitting, and fine color variegation reside), two images with identical 64-bit pHashes are **not necessarily identical physical specimens**. Automatically deleting images based on pHash alone introduces severe selection bias.

Stage 4.1 evaluation must execute a **Three-Tier Sensitivity Analysis**:
1. **Primary Evaluation ($N=13,465$ images):** Complete set of usable local images.
2. **Sensitivity Tier 1 ($N=13,409$ images):** Excludes the 56 cross-partition collision rows (`CROSS_PARTITION`), verifying that potential cross-partition leakage does not inflate OOD detection metrics.
3. **Sensitivity Tier 2 ($N=13,382$ images):** Excludes both cross-partition (56 rows) and multi-label intra-partition collisions (27 rows, total 83 rows excluded), verifying that ambiguous label clusters do not distort within-partition AUROC or false alarm rates.
4. **Tolerance Criterion:** If AUROC or FPR@95 varies by more than $\pm 0.5\%$ across tiers, all three numbers must be documented in the manuscript.

---

## 4. IMAGE IDENTIFIER ARCHITECTURE & VERIFICATION

### 4.1 Implemented Algorithm
Every image record in [`STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv) is identified by a deterministic, collision-free `image_id` generated via:
- **Kaggle Primary Test (`A`):** `kaggle_test_{md5[:10]}_{original_filename}`
- **FruitVision (`B, C, D1, D2`):** `fv_{clean_filename}_{md5[:10]}` (spaces and parentheses stripped from filename)
- **Sultana (`B, D1`):** `sult_{clean_filename}_{md5[:10]}` (spaces and parentheses stripped from filename)
- **ToxiFruit (`B, C, D1, D2, M1, M2`):** `toxi_{cohort_folder}_{sample_index:04d}` (prospective cohort ID)

### 4.2 Verification Metrics
- Total Manifest Records: **20,781**
- Unique `image_id` Count: **20,781**
- Collision Rate: **0.00%**
- Original filesystem basenames are preserved in column `original_filename`.
- Local relative paths are preserved in `relative_path`.
- All ToxiFruit records (7,200) carry status `PLANNED` with hashes designated `PENDING_ARCHIVE_DOWNLOAD`, distinguishing prospective archive paths from verified local files.

---

## 5. SCIENTIFIC TERMINOLOGY STANDARDIZATION

In compliance with publication ethics and scientific accuracy:
1. **No Chemical Sensing Claims:** Conventional 3-channel RGB digital photography cannot measure chemical concentration, ppm of formaldehyde, or molecular adulteration. Claims that AgriRoute "detects chemical adulteration" or "identifies formalin contamination" are unscientific.
2. **Standardized Empirical Vocabulary:** All text, figures, and reviewer rebuttals must strictly employ:
   - *"dataset-labelled formalin-treatment condition"*
   - *"treatment-associated visual distribution shift"*
   - *"open-set visual anomaly rejection"*
   - *"cross-dataset generalization under post-harvest handling shifts"*
3. **Physical Scope:** RGB-based OSR detects only the morphological, textural, and chromatic degradation artifacts associated with post-harvest immersion protocols, functioning as a non-destructive visual screening gate rather than a biochemical assay.

---

## 6. DATASET LICENSING & PROVENANCE REGISTER

| Dataset | Primary Repository / DOI | Author / Year | Verified Licence | Commercial Use | Derivative Redistribution | Benchmark Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **Kaggle Fresh/Rotten** | Kaggle (`sriramr/fruits-fresh-and-rotten-for-classification`) | R., Sriram (2018) | Kaggle Open Data Terms | Non-Commercial Research | Research Use | **INCLUDED (Partition A, N=227)** |
| **FruitVision 2025** | Mendeley Data (DOI: 10.17632/vcm6437y88.1) | Hossain et al. (2025) | **CC BY-NC-ND 4.0** | Prohibited | Prohibited (Read-Only In-Memory Use) | **INCLUDED (Partitions B, C, D1, D2, N=10,045 usable)** |
| **Sultana 2022** | Kaggle / Mendeley Data | Sultana et al. (2022) | **CC BY 4.0** | Permitted with Attribution | Permitted with Attribution | **INCLUDED (Partitions B, D1, N=3,193 usable)** |
| **ToxiFruit 2026** | Zenodo (Prospective Archive) | ToxiFruit Authors (2026) | **`UNCONFIRMED`** | Pending Archive Inspection | Pending Archive Inspection | **`PLANNED` (Partitions B, C, D1, D2, M1, M2, N=7,200)** |

---

## 7. FINAL AUDIT VERDICT & STAGE 4.1 PRE-REQUISITES

### 7.1 Verdict
- **LOCAL BENCHMARK (Partitions A, B, C, D1, D2; $N=13,465$ Usable Images):** **`>>> GO <<<`**  
  All pre-conditions, data manifests, deduplications, and joint thresholds are fully verified, consistent, and reproducible.
- **REMOTE TOXIFRUIT COHORT ($N=7,200$ Planned Images):** **`>>> CONDITIONAL GO <<<`**  
  Execution is conditioned upon physical acquisition, extraction, byte-level hashing, and licence confirmation from Zenodo.

### 7.2 Mandatory Stage 4.1 Execution Rules
When executing Stage 4.1 external inference:
1. `MODEL_B_V4_1_CHECKPOINT.keras` must be loaded in read-only inference mode (`training=False`).
2. Images must be loaded strictly by joining `image_id` from [`STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv) where `inclusion_status == 'INCLUDED'`.
3. Operating thresholds must be loaded strictly from [`STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv).
4. Three-tier sensitivity analysis must be computed and logged using [`STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv).
5. All 8 tests in `tests/test_reproducibility_v4_1.py` must pass with zero failures.

---
*Signed and sealed on behalf of the AgriRoute Scientific Audit Team,*  
**Independent Scientific Benchmark Auditor & Lead Methodologist**  
*November 10, 2026*

