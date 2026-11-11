# Section 3: Dataset Census and Experimental Design

This section details the source-stratified evaluation benchmark, comprising $N = 13,465$ audited photographic image records assembled from three independent repositories. We present the study design rationale, repository provenance, label-mapping protocol, five-partition census, four source-matched evaluation cohorts, duplicate and perceptual-hash sensitivity analysis, experimental separation safeguards, and reproducibility artifacts.

## 3.1. Study Design Overview

Evaluating automated fruit-quality classification models under practical deployment conditions presents a complex experimental challenge. When vision models trained on curated image datasets are evaluated on external imagery, observed performance degradation typically reflects multiple confounding factors acting simultaneously: variations in camera sensor optics, ambient illumination, photographic backgrounds, biological cultivars, and post-harvest handling marks [10]–[12]. If images from diverse sources are simply pooled into an aggregated test set, it becomes impossible to determine whether detection failures stem from semantic novelty (encountering an unseen fruit species), physiological or surface anomalies (encountering damaged or chemically treated produce), or mere covariate shift in image acquisition conditions.

To resolve these compounding factors, this study implements a *source-stratified empirical evaluation*. We freeze a pre-trained six-class MobileNetV2 classifier [7] and evaluate it across structured image cohorts drawn from three independent repositories: the Primary Kaggle dataset, FruitVision [12], and Sultana et al. [11]. Crucially, the experimental architecture maintains a strict distinction between:

1. **Closed-Set Generalization (Partitions A and B):** Evaluating accuracy, balanced accuracy, and class-wise confusion on known classes across laboratory baseline conditions (Partition A, $N = 227$) versus external retail and field environments (Partition B, $N = 5,350$), holding the label space $\mathcal{Y} = \{0, 1, \dots, 5\}$ constant.
2. **Out-of-Distribution Detection (Partitions C, D1, and D2):** Evaluating the capacity of post-hoc scoring functions to detect and reject non-target inputs, including treatment-labelled condition shifts (Partition C, $N = 1,917$), unseen fruit species (Partition D1, $N = 4,776$), and compound shifts (Partition D2, $N = 1,195$).

Furthermore, to separate the specific mechanism of out-of-distribution (OOD) shift from cross-repository acquisition bias, we structure the OOD evaluation into four *source-matched cohorts* (Cohorts A, B, C, and D). By comparing in-distribution known images and out-of-distribution anomalous images collected within the same parent repository, source matching reduces repository-level provenance differences, while within-repository acquisition variation remains possible. Throughout this study, the evaluation unit is designated strictly as an *image record*; photographic records cannot be assumed to represent statistically independent biological specimens.

---

## 3.2. Dataset Sources and Provenance

The benchmark image census is compiled from three independent photographic archives, each characterized by distinct acquisition settings, camera modalities, and environmental conditions. Table 2 summarizes the provenance, published composition, evaluated subsets, and key characteristics of each repository.

### Table 2: Dataset Source and Provenance Summary
*Evaluated record counts represent audited, unique image records included in the present study after hash-identified duplicate removal, distinguishing local benchmark subsets from published repository totals.*

| Source Repository | Citation / Venue | Published Composition | Evaluated $N$ | Evaluated Species & Conditions | Capture Environment & Key Provenance |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Primary Kaggle Archive** | Curated public benchmark | 2,043 test images (227 raw, 1,816 aug.) | 227 | Apple, banana, orange (Fresh, Rotten) | Controlled laboratory-style conditions with uniform backgrounds; neutral illumination; baseline ID test set (Partition A). |
| **FruitVision** | Bijoy et al. (2025) [12] <br> *Data in Brief* | 10,154 raw images (81,232 aug. archive) | 10,045 | Apple, banana, orange, grape, mango (Fresh, Rotten, Formalin-mixed) | 3 mobile smartphone cameras (Samsung A50, Redmi Note 7, iPhone 11); indoor/outdoor retail lighting; 109 hash-identified duplicates excluded. |
| **Sultana et al.** | Sultana et al. (2022) [11] <br> *Data in Brief* | 16 classes, 8 fruits ($\sim$3,200 raw images) | 3,193 | Apple, banana, orange, grape, guava, jujube, pomegranate, strawberry (Fresh, Rotten) | Retail fruit shops and open agricultural fields; natural ambient illumination; agricultural specialist annotation; 7 hash-identified duplicates excluded. |
| **Total Benchmark** | **Three Repositories** | **Multiple Archives** | **13,465** | **8 Fruit Species, 3 Conditions** | **Audited multi-source evaluation census (Partitions A–D2).** |

### 3.2.1. Primary Kaggle Dataset
The primary training and baseline evaluation partition originates from a widely utilized curated benchmark repository for fruit freshness classification. The repository covers three commercial fruit types—apple (*Malus domestica*), banana (*Musa acuminata*), and orange (*Citrus sinensis*)—each categorized into fresh and rotten states. Photography was conducted under controlled laboratory-style conditions with relatively uniform, neutral backgrounds and stable illumination. The published test partition contains 2,043 files consisting of 227 raw photographic images and 1,816 synthetic geometric and photometric augmentations. In this study, we strictly isolate the 227 raw, unaugmented photographic images (`is_raw == 1`) to construct Partition A (Primary In-Distribution Test). The 1,816 synthetically augmented images were set aside to restrict evaluation strictly to authentic photographic captures; these represent upstream synthetic transformations and are not classified as duplicate removals. An independent validation partition of 227 raw images was maintained strictly for operating-threshold calibration (see Section 3.7).

### 3.2.2. FruitVision Repository
The FruitVision dataset was introduced by Bijoy et al. [12] as a benchmark for produce freshness, rot, and adulteration recognition. The repository encompasses five fruit species: three known species (apple, banana, orange) and two non-target species (grape *Vitis vinifera* and mango *Mangifera indica*). Photography was conducted across diverse wholesale markets, retail stalls, and laboratory benches using three commercial smartphone devices: Samsung Galaxy A50 (25 MP primary sensor), Xiaomi Redmi Note 7 (48 MP primary sensor), and Apple iPhone 11 (12 MP primary sensor). Image capture spanned varied ambient indoor lighting, direct outdoor sunlight, and fluorescent retail illumination.

A distinctive feature of FruitVision is its inclusion of a dataset-reported treatment protocol: fruits were immersed in a solution of 10% formalin and 90% water for 30 minutes, allowed to air-dry, and photographed 48 hours post-immersion under natural ambient conditions alongside untreated fresh and naturally decaying specimens. While Bijoy et al. published 10,154 raw photographs (expanded via photometric and geometric transformations to an 81,232-image augmented archive), the present study extracts exclusively the raw photographic collection. Cryptographic hash auditing identified and removed 109 hash-identified duplicate files, yielding exactly 10,045 audited image records evaluated across Partitions B, C, D1, and D2. We emphasize that treatment-labelled images are evaluated strictly under their dataset-reported labels; no independent chemical assays or residue validations were conducted.

### 3.2.3. Sultana et al. Repository
The dataset introduced by Sultana et al. [11] was curated to recognize produce quality across authentic retail and farm environments. The dataset contains 16 fresh and rotten categories representing eight distinct fruit species: apple, banana, orange, grape, guava (*Psidium guajava*), jujube (*Ziziphus jujuba*), pomegranate (*Punica granatum*), and strawberry (*Fragaria $\times$ ananassa*). Images were captured in local retail shops and active agricultural orchards under ambient natural lighting, with fruit specimen selection and freshness categorization verified with assistance from an agricultural domain specialist. We harvested 3,200 raw photographic records (200 records per class across all 16 classes). MD5 cryptographic hashing identified 7 hash-identified duplicate files within the orange fresh class, leaving exactly 3,193 audited image records evaluated across Partitions B and D1.

---

## 3.3. Known-Class Definition and Label Mapping

The classification space of the frozen MobileNetV2 backbone is defined over $K = 6$ discrete semantic classes:
$$\mathcal{Y} = \{0: \text{fresh\_apple}, \; 1: \text{fresh\_banana}, \; 2: \text{fresh\_orange}, \; 3: \text{rotten\_apple}, \; 4: \text{rotten\_banana}, \; 5: \text{rotten\_orange}\}.$$

To integrate external imagery into this framework, we apply unambiguous label-mapping rules governed by the underlying biological species and physical freshness condition:

1. **External Known-Class Mapping (Partition B):** External images from FruitVision and Sultana et al. depicting apple, banana, or orange in natural fresh or rotten states are mapped directly to their corresponding index in $\mathcal{Y}$. For example, FruitVision `Fresh_Apple` maps to class 0, and Sultana `rotten_orange` maps to class 5. No class collapsing across fresh/rotten boundaries or cross-species reassignments are permitted.
2. **Unseen-Species OOD Mapping (Partition D1):** Images depicting botanical species outside the set $\{\text{apple}, \text{banana}, \text{orange}\}$ in natural fresh or rotten conditions are designated as out-of-distribution unseen species. This includes grape and mango from FruitVision, and grape, guava, jujube, pomegranate, and strawberry from Sultana et al.
3. **Treatment-Labelled Condition Shift Mapping (Partition C):** Images from FruitVision depicting known species (apple, banana, orange) photographed under the dataset-reported formalin-immersion condition are designated as treatment-labelled condition shifts. Because the classifier was trained exclusively on untreated produce, these images evaluate whether post-hoc OOD scoring functions discriminate images bearing the dataset-reported treatment label from untreated knowns. This evaluation tests model behavior on produce labelled under altered post-harvest handling; it does not claim independent chemical detection, residue verification, or the establishment of treatment-caused visual anomalies.
4. **Combined Shift Mapping (Partition D2):** Images from FruitVision depicting unseen species (grape and mango) subjected to the dataset-reported formalin-immersion condition are designated as combined shifts, presenting simultaneous semantic and treatment condition divergence.

No subjective manual pruning or post-hoc relabeling was performed; all annotations adhere strictly to the verified manifests of the respective source publications.

---

## 3.4. Image-Level Census and Partition Construction

The complete evaluation benchmark comprises $N = 13,465$ audited photographic image records structured into five mutually exclusive partitions, designated Partitions A through D2. Table 3 presents the detailed census, detailing the evaluation role, source repositories, target classification status, species composition, and exact record counts.

### Table 3: Evaluation Partition Census ($N = 13,465$)
*Partitions are mutually exclusive based on unique SHA-256 and MD5 hashes. Counts represent individual photographic image records rather than independent biological specimens.*

| Partition | Evaluation Role | Source Repository | Target Status | Species, Conditions, and Sub-counts | Partition $N$ |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Partition A** | Primary In-Distribution (ID Test) | Primary Kaggle | Known ($\mathcal{Y}$) | Apple (F 34, R 49), Banana (F 33, R 47), Orange (F 31, R 33) | 227 |
| **Partition B** | External Known-Class Shift | FruitVision <br> Sultana et al. | Known ($\mathcal{Y}$) | *FruitVision ($N = 4,157$):* Apple (F 765, R 630), Banana (F 748, R 631), Orange (F 753, R 630) <br> *Sultana ($N = 1,193$):* Apple (F 200, R 200), Banana (F 200, R 200), Orange (F 193, R 200) | 5,350 |
| **Partition C** | Treatment-Labelled Condition Shift | FruitVision | Unknown (OOD Condition) | *Formalin-mixed Knowns ($N = 1,917$):* <br> Apple (641), Banana (660), Orange (616) | 1,917 |
| **Partition D1** | Unseen-Species Pure Semantic Shift | FruitVision <br> Sultana et al. | Unknown (OOD Species) | *FruitVision ($N = 2,776$):* Grape (F 753, R 630), Mango (F 763, R 630) <br> *Sultana ($N = 2,000$):* Grape (F 200, R 200), Guava (F 200, R 200), Jujube (F 200, R 200), Pomegranate (F 200, R 200), Strawberry (F 200, R 200) | 4,776 |
| **Partition D2** | Combined Semantic & Treatment Shift | FruitVision | Unknown (OOD Compound) | *Formalin-mixed Unseen ($N = 1,195$):* <br> Grape (587), Mango (608) | 1,195 |
| **Total** | **Complete Evaluation Benchmark** | **Three Repositories** | **Audited Census** | **5 Mutually Exclusive Partitions ($A + B + C + D1 + D2$)** | **13,465** |

The census reconciles precisely across source repositories:
- **Primary Kaggle:** Contributes 227 image records, all within Partition A.
- **FruitVision:** Contributes 10,045 image records, spanning Partition B ($N = 4,157$), Partition C ($N = 1,917$), Partition D1 ($N = 2,776$), and Partition D2 ($N = 1,195$).
- **Sultana et al.:** Contributes 3,193 image records, spanning Partition B ($N = 1,193$) and Partition D1 ($N = 2,000$).

Summing across sources gives $227 + 10,045 + 3,193 = 13,465$ records. Similarly, summing across partitions yields $227 + 5,350 + 1,917 + 4,776 + 1,195 = 13,465$ records. Cryptographic hash analysis confirms that all 13,465 images possess unique SHA-256 and MD5 checksums, verifying complete mutual exclusivity.

---

## 3.5. Source-Stratified Evaluation Cohorts

To evaluate out-of-distribution detection without conflating produce anomalies with cross-dataset domain shifts, we establish four source-matched evaluation cohorts, summarized in Table 4. In standard unstratified evaluations, pairing in-distribution images from one repository (e.g., Kaggle) against out-of-distribution images from another (e.g., FruitVision) introduces severe macro-confounders: differences in background chromaticity, ambient illumination, and sensor colour calibration enable detectors to distinguish sources rather than semantic or condition anomalies.

### Table 4: Source-Matched Out-of-Distribution Evaluation Cohorts (Cohorts A–D)
*Source matching reduces repository-level provenance differences, while within-repository acquisition variation remains possible.*

| Cohort | Known Reference ($N_{\text{id}}$) | Shifted / OOD ($N_{\text{ood}}$) | Source Repository | Shift Dimension | Primary Research Question |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cohort A** | FruitVision Known <br> (Partition B, $N = 4,157$) | FruitVision Unseen <br> (Partition D1, $N = 2,776$) | FruitVision | Within-Repository Semantic Shift | Can post-hoc detectors identify unseen fruit species (grape, mango) within the same repository collection? |
| **Cohort B** | FruitVision Known <br> (Partition B, $N = 4,157$) | FruitVision Formalin-mixed <br> (Partition C, $N = 1,917$) | FruitVision | Within-Repository Treatment Shift | Can post-hoc detectors or frozen classifiers discriminate dataset-reported treatment-labelled condition shifts on familiar fruit species? |
| **Cohort C** | FruitVision Known <br> (Partition B, $N = 4,157$) | FruitVision Preserved Unseen <br> (Partition D2, $N = 1,195$) | FruitVision | Within-Repository Combined Shift | How does compound shift (unseen species bearing dataset-reported treatment labels) affect detector discrimination? |
| **Cohort D** | Sultana Known <br> (Partition B, $N = 1,193$) | Sultana Unseen <br> (Partition D1, $N = 2,000$) | Sultana et al. | Within-Repository Semantic Shift | How does unseen-species detection generalize across field and retail market imagery containing diverse unseen agricultural species? |

The four source-matched cohorts isolate specific distributional dimensions:

1. **Cohort A (Within-FruitVision Semantic Shift):** Compares $N_{\text{id}} = 4,157$ natural known images (apple, banana, orange from Partition B) against $N_{\text{ood}} = 2,776$ natural unseen-species images (grape, mango from Partition D1). As both subsets originate from the FruitVision repository, this comparison reduces cross-repository acquisition bias, though within-repository capture variations remain possible.
2. **Cohort B (Within-FruitVision Treatment Condition Shift):** Compares the same $N_{\text{id}} = 4,157$ natural known images against $N_{\text{ood}} = 1,917$ images of the identical three fruit species bearing the dataset-reported treatment-labelled condition (Partition C). This cohort assesses detector behavior on images labelled under post-harvest chemical immersion protocols, without asserting independent chemical verification or treatment-induced visual artifacts.
3. **Cohort C (Within-FruitVision Combined Shift):** Compares $N_{\text{id}} = 4,157$ natural known images against $N_{\text{ood}} = 1,195$ images of unseen species bearing the dataset-reported treatment-labelled condition (grape and mango from Partition D2), evaluating the empirical interaction between semantic and treatment condition labelling.
4. **Cohort D (Within-Sultana Semantic Shift):** Compares $N_{\text{id}} = 1,193$ natural known images from Sultana et al. against $N_{\text{ood}} = 2,000$ natural unseen-species images (grape, guava, jujube, pomegranate, strawberry from Partition D1). This cohort evaluates semantic shift under outdoor farm and retail market conditions across diverse unseen agricultural species.

Importantly, Cohorts A, B, and C all utilize FruitVision Known (Partition B, $N_{\text{id}} = 4,157$) as their common in-distribution reference subset, evaluating distinct shifted cohorts (unseen species in Partition D1, treatment condition in Partition C, and combined shift in Partition D2, respectively) against this shared baseline. Because these source-matched cohorts reuse the same underlying reference records, they do not constitute statistically independent datasets. Rather, they provide comparative diagnostic probes of different distribution shift mechanisms against a unified, fixed reference distribution within the FruitVision repository.

We note an important methodological qualification: source matching substantially reduces repository-level provenance differences, but cannot eliminate potential micro-variations in capture angle, background clutter, or fruit specimen batching within a given repository.

---

## 3.6. Image Curation, Duplicate Handling, and Sensitivity Analysis

Photographic archives in agricultural computer vision frequently contain near-duplicate captures resulting from camera burst shooting, minor viewpoint adjustments, or synthetic data augmentation [10], [11]. To guarantee experimental integrity, we implemented a two-stage deduplication and sensitivity auditing protocol:

### 3.6.1. Hash-Identified Duplicate Auditing
Every candidate image file was audited via MD5 and SHA-256 cryptographic hashing. Duplicate files identified through matching cryptographic digests were purged prior to partition assignment. This forensic audit identified and removed 109 hash-identified duplicate files from FruitVision:
- **Partition B:** 28 duplicates excluded (1 fresh banana, 1 rotten banana, 26 rotten orange).
- **Partition C:** 33 duplicates excluded (2 apple formalin-mixed, 31 orange formalin-mixed).
- **Partition D1:** 17 duplicates excluded (17 grape fresh).
- **Partition D2:** 31 duplicates excluded (23 grape formalin-mixed, 8 mango formalin-mixed).

From Sultana et al., 7 hash-identified duplicate files were detected and purged from Partition B (7 orange fresh). In total, 116 hash-identified duplicate files were excluded across evaluated external repositories, ensuring that all 13,465 evaluated records represent unique files.

We strictly distinguish these 116 hash-identified duplicate exclusions from the primary dataset curation protocol: in the primary Kaggle test split, 1,816 synthetically augmented images were set aside to isolate the 227 unaugmented raw photographic records (`is_raw == 1`) for Partition A. These 1,816 exclusions represent the intentional omission of upstream synthetic augmentations, and are never classified as duplicate removals.

### 3.6.2. Perceptual Hash (pHash) Sensitivity Analysis
Beyond exact duplicate files, photographic archives may contain visually near-identical frames captured seconds apart during burst photography or camera repositions. To quantify whether near-duplicate frames artificially distort OOD detection metrics, we computed 64-bit discrete cosine transform (DCT) perceptual hashes (pHash) for all 13,465 images. Pairwise collision scans were conducted across Hamming distance radii $r \in \{0, 4, 8\}$, corresponding to:
- $r = 0$: exact perceptual hash match;
- $r \le 4$: strict near-duplicate match;
- $r \le 8$: permissive visual collision.

Crucially, these pairwise Hamming radii $r$ are scanning thresholds, which are distinguished from the resulting filtered evaluation tiers. Based on detected collisions at $r \le 8$, we constructed three nested evaluation tiers:

1. **Primary Cohort ($N = 13,465$):** The canonical evaluation benchmark, containing all unique image records following exact MD5 deduplication.
2. **Tier 1 Sensitivity ($N = 13,409$):** Excludes image records exhibiting cross-partition pHash collisions at $r \le 8$ (instances where an image in an in-distribution partition closely resembles an image in an out-of-distribution partition). Because FruitVision Known (Partition B, $N_{\text{id}} = 4,157$) serves as the shared reference subset across Cohorts A, B, and C, cohort-level pHash exclusions are not additive; naively summing exclusions across individual cohorts repeatedly counts the same reference images. In Tier 1, exactly 11 unique reference records from Partition B are excluded across all three FruitVision cohorts, alongside 14 shifted records from Partition D1 (Cohort A), 11 shifted records from Partition C (Cohort B), and 20 shifted records from Partition D2 (Cohort C), with zero cross-partition collisions in Sultana et al. This yields a global benchmark total of exactly 56 unique excluded image records ($13,465 - 56 = 13,409$).
3. **Tier 2 Sensitivity ($N = 13,382$):** Further excludes image records exhibiting intra-partition multi-label collisions (near-identical images within the same partition bearing conflicting condition or sub-class labels). Tier 2 removes an additional 6 unique records from Partition B, 5 from Partition C, and 16 from Partition D1 (with 0 in Partition D2 and Sultana et al.), yielding 27 additional multi-label exclusions and an overall global benchmark total of exactly 83 unique excluded image records ($13,465 - 83 = 13,382$).

The empirical evaluation of detector performance across these three sensitivity tiers is presented in Section 5 (Sensitivity and Near-Duplicate Robustness Analysis), where metric stability is examined across scoring functions and cohorts.

*Methodological Limitations of Perceptual Hashing:* While this sensitivity framework provides a structured probe of metric stability under detected near-duplicate collisions, perceptual hashing has inherent limitations. Operating on low-frequency DCT coefficients, pHash cannot guarantee the detection of heavily cropped, rotated, or lighting-altered captures of the same physical fruit specimen, nor can it prevent collisions between distinct produce specimens with uniform surface colouration. Consequently, pHash sensitivity analysis provides a bounded robustness check against detectable visual collisions; it does not claim the complete elimination of all near-duplicates, burst-shooting captures, or specimen-level correlations in the underlying archives.

---

## 3.7. Evaluation Integrity and Experimental Separation

To maintain rigorous scientific standards and prevent methodological leakage, the experimental protocol enforces four strict integrity safeguards:

1. **Separation of Validation Calibration and Evaluation Census:** Prospective operating thresholds ($\tau_{95}$, targeting approximately 95% in-distribution acceptance) were calibrated strictly on an independent primary validation partition ($N = 227$ raw Kaggle validation images, `is_raw == 1`). Partition A comprises $N = 227$ raw Kaggle test images (`is_raw == 1`). Cryptographic auditing confirms that MD5 hash overlap between the reported validation calibration partition and Partition A is strictly zero, establishing that there is no exact-file overlap between the two sets. Furthermore, the 227 validation images are used exclusively for threshold estimation and are not included in the $N = 13,465$ evaluation census. While this cryptographic separation demonstrates the absence of exact duplicate files between calibration and test data, we emphasize that exact-hash verification is evidence-bounded: it establishes no file overlap, but does not prove the absence of every conceivable upstream correlation (such as potential near-duplicate specimens or sequential camera bursts in the underlying Kaggle collection).
2. **A Priori Threshold Locking:** All decision thresholds (e.g., $\tau_{\text{Energy}} = 1.054579$, $\tau_{\text{MSP}} = 0.700580$, and the Dual-Gate pair $\tau_E = 0.918451, \tau_M = 0.582610$) were locked on the validation partition using empirical order statistics and held fixed throughout all external evaluations. No threshold tuning, post-hoc threshold selection, or parameter optimization was performed on external partitions or test cohorts.
3. **Model Checkpoint Immutability:** The evaluated MobileNetV2 architecture (checkpoint `MODEL_B_V4_1_CHECKPOINT.keras`, with SHA-256 hash `4a12f354...b6b4`) remained strictly frozen throughout all experiments. No transfer learning, fine-tuning, domain adaptation, or parameter updates were applied to any external cohort.
4. **Physical and Chemical Non-Claim Boundary:** This study evaluates digital RGB images under their published labels. It does not conduct chemical residue assays, does not verify biological specimen independence, and does not evaluate physical sorting machinery or live post-harvest conveyor operations.

---

## 3.8. Experimental Traceability and Data Availability

Experimental traceability is supported by structured digital artifacts maintained within the project research repository. We distinguish preserved internal artifacts from external runtime and source-access dependencies:

- **Preserved Research Artifacts:** The frozen model checkpoint weights (`MODEL_B_V4_1_CHECKPOINT.keras`), image-level prediction logs (`STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`), partition manifests, threshold configurations, bootstrap confidence interval tables, and claims ledgers are preserved in the repository for audit and inspection:
  - Image-level predictions and scores: `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`
  - Partition manifest and exclusion audit: `STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv`
  - Empirical metric point estimates: `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`
  - Non-parametric bootstrap confidence intervals ($B = 1,000$, seed 42): `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv`
  - Perceptual hash sensitivity evaluation tiers: `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv`
  - Verified claims ledger: `STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv`
- **External Dependencies:** Full end-to-end execution of evaluation scripts depends on specific Python virtual environments, scientific machine-learning libraries (TensorFlow/Keras, scikit-learn, NumPy), underlying hardware drivers, and external network access to the original photographic archives hosted by third-party publisher repositories.

External photographic datasets utilized in this study were released by their respective authors under academic open-access licenses (e.g., Creative Commons Attribution 4.0 International for FruitVision [12] and Sultana et al. [11] via *Data in Brief*). In compliance with third-party licensing terms, raw photographic files must be accessed through their primary publisher archives, while all derived metadata, prediction matrices, and evaluation scripts are preserved for academic verification.
