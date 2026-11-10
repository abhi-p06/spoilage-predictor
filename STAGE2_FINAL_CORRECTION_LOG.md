# Stage 2.1 Final Scientific Correction & Validation Audit

**Document ID:** `STAGE2_FINAL_CORRECTION_LOG.md`  
**Role:** Independent Scientific Research Auditor  
**Target Publication:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0) / *Procedia Computer Science* (Elsevier)  
**Audit Timestamp:** November 10, 2026  
**Audited Documents:**
- [`STAGE1_CORRECTION_LOG.md`](file:///Users/abby/Desktop/spoilage-predictor/STAGE1_CORRECTION_LOG.md)
- [`REPOSITORY_FEASIBILITY_ADDENDUM.md`](file:///Users/abby/Desktop/spoilage-predictor/REPOSITORY_FEASIBILITY_ADDENDUM.md)
**Status:** Definitive Read-Only Validation (Non-destructive; no code, dataset, checkpoint, or manuscript modifications)

---

## 1. Executive Auditor Statement

This Stage 2.1 audit provides the definitive forensic correction and validation of the prior Stage 1 and Stage 2 research audit documents. It resolves literature misattributions, validates physical repository checksums, audits Zenodo data files directly, recomputes exact partition distributions from raw manifests, and establishes the strict scientific boundaries of AgriRoute's open-set contribution.

All claims in this document are derived directly from verified publisher records, physical repository manifests, Zenodo API metadata, and compiled Python inspection scripts.

---

## 2. Mandatory Prior-Art Corrections & Literature Synthesis

### 2.1 PEOS-Net (Frontiers in Artificial Intelligence, 2026)
- **DOI:** [`10.3389/frai.2026.1938398`](https://doi.org/10.3389/frai.2026.1938398)
- **Full Article Title:** *PEOS-Net: a Prototype-Energy Open-Set Network for robust tomato leaf disease recognition beyond the closed-world assumption*
- **Journal & Date:** *Frontiers in Artificial Intelligence*, Vol. 9, 2026.

#### Architectural Mechanics:
1. **Backbone:** EfficientNet-B0 combined with a Convolutional Block Attention Module (CBAM) that adaptively emphasizes spatial lesion areas and suppresses background leaf noise.
2. **Dual-Head Formulation:** The shared backbone feature representation $h(x)$ is fed concurrently to two distinct branches:
   - **Prototype-Memory Branch:** Maintains an Exponential Moving Average (EMA) of class-conditional feature representations $p_k \in \mathbb{R}^D$ ($k=1, \dots, K$). For an input $x$, it computes the minimum Euclidean distance to known class prototypes:
     $$D_{\text{proto}}(x) = \min_{k \in \{1,\dots,K\}} \|h(x) - p_k\|_2$$
   - **Independent Energy-Based OOD Branch:** A classifier head outputs unnormalized class logits $z_k(x)$, from which an independent Helmholtz free-energy score is calculated:
     $$E(x; T) = -T \cdot \log \sum_{k=1}^K \exp\left(\frac{z_k(x)}{T}\right)$$
3. **Fused Hybrid Scoring:** PEOS-Net fuses the prototype metric distance and the energy score into a single hybrid score function:
   $$S_{\text{PEOS}}(x) = \alpha \cdot \widetilde{D}_{\text{proto}}(x) + (1 - \alpha) \cdot \widetilde{E}(x)$$
   where $\widetilde{D}$ and $\widetilde{E}$ are min-max normalized scores, and $\alpha \in [0, 1]$ is a balancing hyperparameter. Rejection occurs if $S_{\text{PEOS}}(x) > \tau_{\text{open}}$.
4. **Component Ablations in the Published Paper:** The authors empirically proved that:
   - *Prototype branch alone* suffers from high-dimensional feature compression and fails when open-set classes project near known prototypes.
   - *Energy branch alone* lacks metric compactness in penultimate space and can produce overconfident low-energy scores on far-OOD anomalies.
   - *Fused branch* significantly outperforms both isolated branches, achieving 93.87% closed-set accuracy and superior AUROC/OSCR on withheld tomato leaf disease classes.

#### Overlap and Differences with AgriRoute:
- **Conceptual Overlap:** Both frameworks reject closed-world assumptions in agriculture, use energy-based formulation as an OOD score, and evaluate class-withholding protocols.
- **Critical Differences:**
  1. *Task & Commodity Domain:* PEOS-Net is an agronomic, pre-harvest *foliar disease* classifier (PlantVillage tomato leaves). AgriRoute is a post-harvest, packhouse *edible fruit quality* screening framework (Apple, Banana, Orange).
  2. *Nature of Open-Set Shift:* PEOS-Net evaluates *semantic disease shift* (withholding specific pathological categories like early blight or leaf mold under identical laboratory capture setups). AgriRoute evaluates *fine-grained condition shift* on known fruit species (naturally decayed fresh/rotten fruit vs. chemically adulterated/formalin-dipped fruit) across multi-source *covariate domain shifts* (differing geographic, lighting, and camera sensors).
  3. *Inference Architecture:* PEOS-Net requires end-to-end retraining of custom EMA memory heads and CBAM blocks. AgriRoute's Dual-Gate architecture is a *post-hoc screening cascade* (Gate 1 OOD filter + Gate 2 calibrated selective prediction with asymmetric risk abstention) applicable to pre-trained backbones without architectural modification or prototype storage.

---

### 2.2 PAG-MSBNet (Ecological Informatics, 2026)
- **DOI:** [`10.1016/j.ecoinf.2026.103703`](https://doi.org/10.1016/j.ecoinf.2026.103703)
- **Full Article Title:** *PAG-MSBNet: Prototype-aware gated multi-scale branch network for open-set crop disease recognition*
- **Authors:** Shuang Yan, Lunhong Lou, Jianwu Lin, et al.
- **Journal & Volume:** *Ecological Informatics*, Volume 92, May 2026, Article 103703.

#### Correction of Prior Auditor Mischaracterization:
In `REPOSITORY_FEASIBILITY_ADDENDUM.md` §2.1, PAG-MSBNet was erroneously characterized as *"broad biodiversity and macro-ecological patterns across vast biodiversity taxonomies"*. 

**Authoritative Correction:** PAG-MSBNet is explicitly designed for **open-set crop disease recognition** in agricultural monitoring. It targets the open-set identification of crop leaf diseases by utilizing multi-scale feature branches to capture subtle symptom variations, gated feature fusion to filter irrelevant background foliage, and prototype-aware margin losses to enforce compact intra-class representations while rejecting unseen crop pathologies. It does not address macro-ecological biodiversity.

#### Distinction from AgriRoute:
PAG-MSBNet evaluates foliar disease lesions across pre-harvest crops. It does not study post-harvest produce degradation, physiological decomposition, chemical preservation adulteration, or asymmetric food-safety loss matrices.

---

### 2.3 SensorNet (Intelligent Systems with Applications, 2024)
- **DOI:** [`10.1016/j.iswa.2024.200402`](https://doi.org/10.1016/j.iswa.2024.200402)
- **Full Article Title:** *A comprehensive approach to detecting chemical adulteration in fruits using computer vision, deep learning, and chemical sensors*
- **Authors:** Abdus Sattar, Md. Asif Mahmud Ridoy, Aloke Kumar Saha, Hafiz Md. Hasan Babu, Mohammad Nurul Huda.
- **Journal & Volume:** *Intelligent Systems with Applications*, Volume 23, September 2024, Article 200402.

#### Correction of Prior Auditor Mischaracterization:
In `REPOSITORY_FEASIBILITY_ADDENDUM.md` §2.1, SensorNet was erroneously described as a *"telemetry hardware system requiring physical gas sensors; no optical computer vision or open-set visual anomaly rejection"*.

**Authoritative Correction:** SensorNet is an explicit multimodal computer vision and chemical sensing study. It integrates:
1. **Computer Vision & Deep Learning:** CNN feature extraction from RGB fruit images (Apple, Banana, Malta, Mango) using fine-tuned transfer learning backbones (MobileNet, ResNet).
2. **Chemical Sensors:** An array of metal oxide semiconductor (MOS) gas sensors, notably the **MQ-138** (sensitive to formaldehyde, benzene, and toluene vapor) and **MQ-3** (alcohol/decomposition vapor), housed in an airtight test chamber.
3. **Multimodal Fusion:** Concatenation of image feature embeddings with sensor voltage/ppm readings to classify fruit into Fresh vs. Chemically Adulterated categories.

#### Why SensorNet is Highly Relevant Prior Art:
SensorNet is authored by the exact research group that created ToxiFruit. It directly tackles the same chemical adulterant (formalin dipping in fruits) and uses the same fruit commodities (Apple, Banana, Malta, Mango).

#### Why SensorNet's Task Differs from AgriRoute's Proposed Evaluation:
SensorNet evaluates a **closed-set supervised classification task**. Both fresh and formalin-adulterated fruit samples were provided to the model during training. SensorNet's models learn explicit supervised boundaries between fresh and formalin classes, assuming that test samples will only belong to the known trained adulteration conditions.

In stark contrast, AgriRoute's proposed evaluation tests **withheld-condition Open-Set Recognition (OSR) / Out-of-Distribution (OOD) rejection**:
- The model is trained **strictly on natural organic decay** (fresh vs. rotten fruit).
- Formalin-treated fruits are **completely withheld during training and validation**.
- At test time, the model must detect formalin-adulterated commodities as an **unseen condition anomaly / out-of-distribution state** and safely abstain, rather than falsely categorizing them as "Fresh".

---

### 2.4 GPR NIR Spectroscopy (Food Quality and Safety, 2023)
- **DOI:** [`10.1093/fqsafe/fyac068`](https://doi.org/10.1093/fqsafe/fyac068)
- **Correct Article Title:** *Gaussian process regression for prediction and confidence analysis of fruit traits by near-infrared spectroscopy*
- **Correct Authors:** Xiaojing Chen, Jianxia Xue, Xiao Chen, Xinyu Zhao, Shujat Ali, and Guangzao Huang.
- **Journal & Volume:** *Food Quality and Safety*, Volume 7, 2023 (Published online November 2022), Article ID `fyac068`.

#### Correction of Prior Auditor Errors:
In `REPOSITORY_FEASIBILITY_ADDENDUM.md` §2.1, this study was incorrectly attributed to *"Li et al."* with a fabricated title (*"Uncertainty-aware prediction of internal fruit quality attributes using Gaussian process regression and diffuse reflectance NIR spectroscopy"*). 

The publisher record confirms the authors are **Xiaojing Chen et al.**, and the title is *Gaussian process regression for prediction and confidence analysis of fruit traits by near-infrared spectroscopy*.

#### Core Scientific Content:
Chen et al. demonstrate that standard partial least squares regression (PLSR) on near-infrared (NIR) spectra fails when encountering out-of-distribution fruit specimens. By employing Gaussian Process Regression (GPR), the predictive variance $\sigma^2(x)$ serves as an analytical metric of prediction confidence, allowing the system to abstain from certifying internal dry matter content in mangoes when spectral features diverge from the training distribution.

---

## 3. Direct Census of Validation Partition (`FINAL_GROUP_VAL_V4_1.csv`)

A direct programmatic audit of [`FINAL_GROUP_VAL_V4_1.csv`](file:///Users/abby/Desktop/spoilage-predictor/FINAL_GROUP_VAL_V4_1.csv) resolves the conflict between Stage 1 and Stage 2:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               EXACT DISTRIBUTION OF FINAL_GROUP_VAL_V4_1.csv (N = 2,043)               │
├─────────────────┬──────────────────────┬──────────────────────┬────────────────────────┤
│ Class Name      │ Total Rows (All)     │ Raw Base Images      │ Offline Augmented      │
│                 │                      │ (is_raw == 1)        │ Variants (is_raw == 0) │
├─────────────────┼──────────────────────┼──────────────────────┼────────────────────────┤
│ rotten_apple    │ 441                  │ 49                   │ 392                    │
│ rotten_banana   │ 414                  │ 46                   │ 368                    │
│ fresh_apple     │ 315                  │ 35                   │ 280                    │
│ fresh_banana    │ 297                  │ 33                   │ 264                    │
│ rotten_orange   │ 297                  │ 33                   │ 264                    │
│ fresh_orange    │ 279                  │ 31                   │ 248                    │
├─────────────────┼──────────────────────┼──────────────────────┼────────────────────────┤
│ TOTAL           │ 2,043                │ 227                  │ 1,816                  │
└─────────────────┴──────────────────────┴──────────────────────┴────────────────────────┘
```

### Key Manifest Properties:
- **Total Manifest Rows:** Exactly 2,043.
- **Original Unaugmented Base Images (`is_raw == 1`):** Exactly **227**.
- **Offline Augmented Variants (`is_raw == 0`):** Exactly **1,816** (8 variants per base image: rotation, zoom, shear, crop).
- **Unique Base Filenames (`base_filename`):** Exactly **227** (1:1 correspondence with `is_raw == 1`).
- **Unique Group IDs (`group_id`):** Exactly **227**.
- **Unique Supergroups (`super_group_id`):** Exactly **226** (two base image groups were merged into a single supergroup due to confirmed perceptual hash collision).

### Resolution of Prior Stage Discrepancies:
- Stage 2 (`REPOSITORY_FEASIBILITY_ADDENDUM.md` §5.3) erroneously assumed an artificial balanced split of 37–39 samples per class ($38, 39, 38, 38, 37, 37$).
- The actual distribution reflects natural Kaggle dataset imbalance, where `rotten_apple` has 49 raw specimens and `fresh_orange` has 31 raw specimens.
- All subsequent calibration calculations must use the ground-truth distribution ($49, 46, 35, 33, 33, 31$).

---

## 4. Forensic Investigation of ToxiFruit Zenodo Repository

### 4.1 Verification of Deposited Files
An inspection of the official Zenodo repository ([DOI: 10.5281/zenodo.21480141](https://doi.org/10.5281/zenodo.21480141)) via the Zenodo REST API reveals that the deposit contains **only three files**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ZENODO 10.5281/ZENODO.21480141 CONTENTS                         │
├───────────────────────────────┬─────────────────┬──────────────────────────────────────┤
│ File Key                      │ Size (Bytes)    │ MD5 Checksum                         │
├───────────────────────────────┼─────────────────┼──────────────────────────────────────┤
│ ToxiFruit_class_metadata.csv  │ 7,889           │ 08a9a379047fdc21172b0751606ee616     │
│ Original Dataset.zip          │ 14,226,606,226  │ f491266ad5903e37edd1d135e832e0ac     │
│ Augmented_Dataset.zip         │ 10,464,597,957  │ 5859a08981764eb3ce08a25d6a2fbc84     │
└───────────────────────────────┴─────────────────┴──────────────────────────────────────┘
```

### 4.2 Schema and Granularity of `ToxiFruit_class_metadata.csv`
The metadata CSV contains exactly 8 rows corresponding to the 8 evaluated classes. Its schema consists of:
`class_id`, `class_name`, `repository_folder`, `original_manuscript_label`, `fruit_type`, `scientific_name`, `condition`, `condition_display`, `original_image_count`, `augmented_image_count`, `total_files_in_class`, `image_format`, `raw_resolution_range_px`, `standardized_resolution_px`, `capture_devices`, `camera_type`, `camera_specifications`, `weather`, `temperature_c`, `reported_class_locations`, `dataset_collection_sites`, `augmentation_methods`, `class_description`, `license`, `metadata_scope_note`.

Crucially, the authors appended the following explicit scope note to every class entry:
> *"Class-level summary compiled from the manuscript. Device, location, weather, temperature, and resolution values are not verified as image-level assignments for every deposited file."*

### 4.3 Sensor Data Availability Finding:
1. **Sensor Readings Are NOT Downloadable:** There are **zero** MQ-138 sensor log files, zero voltage traces, zero ppm time-series, and zero tabular sensor arrays deposited in the Zenodo repository.
2. **Neither Image-Level Nor Specimen-Level Join Is Possible:** The sensor data reported in Sattar et al. (2024) exists only in private author archives or as aggregated summary figures in their journal text.
3. **Scientific Directive:** Any suggestion that AgriRoute can evaluate multimodal sensor fusion on ToxiFruit is scientifically unfeasible. ToxiFruit can only be utilized as an external optical image benchmark for cross-dataset condition-shift evaluation.

---

## 5. Checkpoint & Manifest Consistency Verification

### 5.1 Authoritative Checkpoint Verification
- **Primary Checkpoint Path:** `MODEL_B_V4_1_CHECKPOINT.keras`
- **Mirror Checkpoint Path:** `04_MODELS/checkpoints/MODEL_B_V4_1_CHECKPOINT.keras`
- **Training Artifact Path:** `experiments/group_leakage_study/CHECKPOINTS/group_aware_mobilenet_v2_v4_1.keras`
- **Exact File Size:** **9,715,984 bytes**
- **Authoritative SHA-256:**
  `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
  (Identical across all three paths).

### 5.2 Training Manifest Relationship
A forensic audit of `scripts/train_model_b_v4_1_raw_primary.py` and [`FINAL_GROUP_TRAIN_V4_1.csv`](file:///Users/abby/Desktop/spoilage-predictor/FINAL_GROUP_TRAIN_V4_1.csv) confirms:
- **Total Rows in Manifest:** 9,513 rows.
- **Original Raw Base Images (`is_raw == 1`):** Exactly **1,057** images across 1,052 supergroups.
- **Offline Augmented Variants (`is_raw == 0`):** Exactly **8,456** images.
- **Did Augmentation Derivatives Enter Training?** **NO.** The training script explicitly loaded data via:
  ```python
  df_raw = df[df["is_raw"] == 1].copy().reset_index(drop=True)
  assert len(df_raw) == 1057
  ```
  All 8,456 offline augmented variants were completely excluded from the training generator.
- **Online Augmentation:** Data augmentation during training was performed strictly on the fly using dynamic Keras layers (`RandomFlip("horizontal")`, `RandomRotation(0.15)`, `RandomZoom((-0.10, 0.10))`, `RandomContrast(0.10)`).
- **Validation and Test Isolation:** Validation ($N=227$) and Test ($N=227$) raw partitions remained strictly unaugmented and unobserved during training.

---

## 6. Rigorous Novelty Bounds & Literature Positioning

AgriRoute must **not** claim to be the "first-ever open-set food safety recognition system". Such a claim is demonstrably false and would be immediately rejected by reviewers citing PEOS-Net, PAG-MSBNet, or SensorNet.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        COMPARATIVE NOVELTY DECONSTRUCTION                              │
├─────────────────────┬──────────────┬──────────────────┬──────────────┬─────────────────┤
│ Dimension           │ PEOS-Net     │ PAG-MSBNet       │ SensorNet    │ AgriRoute       │
│                     │ (2026)       │ (2026)           │ (2024)       │ (Proposal)      │
├─────────────────────┼──────────────┼──────────────────┼──────────────┼─────────────────┤
│ Domain              │ Pre-harvest  │ Pre-harvest      │ Post-harvest │ Post-harvest    │
│                     │ foliar crops │ field crops      │ fruits       │ fruits          │
├─────────────────────┼──────────────┼──────────────────┼──────────────┼─────────────────┤
│ Evaluation Task     │ Open-Set leaf│ Open-Set crop    │ Closed-Set   │ Open-Set        │
│                     │ disease class│ disease class    │ supervised   │ condition &     │
│                     │ withholding  │ withholding      │ adulteration │ semantic shift  │
├─────────────────────┼──────────────┼──────────────────┼──────────────┼─────────────────┤
│ Adulterant Testing  │ None         │ None             │ Formalin     │ Formalin        │
│                     │              │                  │ (Supervised) │ (Withheld OOD)  │
├─────────────────────┼──────────────┼──────────────────┼──────────────┼─────────────────┤
│ Domain Shift Scope  │ Intra-dataset│ Intra-dataset    │ Single lab   │ Cross-dataset   │
│                     │ (PlantVillage│ (Curated crops)  │ setup        │ (Kaggle ->      │
│                     │ only)        │                  │              │ Multi-source)   │
├─────────────────────┼──────────────┼──────────────────┼──────────────┼─────────────────┤
│ Cost Formulation    │ Symmetric    │ Symmetric        │ Symmetric    │ Asymmetric Food-│
│                     │ OSR metric   │ OSR metric       │ Accuracy/F1  │ Safety Loss     │
├─────────────────────┼──────────────┼──────────────────┼──────────────┼─────────────────┤
│ Inference Mechanism │ Retrained EMA│ Retrained gated  │ Multi-modal  │ Post-hoc Dual-  │
│                     │ memory heads │ multi-scale net  │ sensor fusion│ Gate screening  │
└─────────────────────┴──────────────┴──────────────────┴──────────────┴─────────────────┘
```

### What Precisely Remains Distinct in AgriRoute:
AgriRoute's defensible, peer-reviewable contribution is:
1. **The First Investigation of Post-Harvest Condition Shift vs. Semantic Shift:** Decoupling unseen chemical preservation states (formalin on familiar fruits) from unseen botanical species (mango, grape) under severe cross-dataset domain shift.
2. **Evaluation of Closed-Set Failure on Withheld Chemical Adulterants:** Proving that standard models trained only on natural decay exhibit catastrophic overconfidence on adulterated fruit, falsely labeling toxic commodities as "Fresh".
3. **Asymmetric Risk-Aware Selective Screening:** Formulating intake packhouse screening with an asymmetric loss matrix that strictly penalizes false acceptance of spoiled/toxic commodities while permitting low-cost abstention to manual inspection.
4. **Post-Hoc Applicability Without Custom Re-training:** Demonstrating that a cascaded dual-gate filter can be applied directly to pre-trained standard backbones (MobileNetV2, EfficientNetB0) without complex prototype memories or multi-branch re-architecting.

---

## 7. Updated Final Recommendation & Unresolved Blockers

### Updated Recommendation: **CONDITIONAL GO**

The scientific pivot remains viable and significantly stronger than the original dynamic routing narrative. However, **six unresolved blockers** must be formally addressed:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              SIX UNRESOLVED BLOCKERS                                   │
├────┬───────────────────────────────────────────────────────────────────────────────────┤
│ 1  │ FLEET LOGISTICS WITHDRAWAL: Formally excise dynamic truck routing from primary    │
│    │ empirical claims. Reframe AgriRoute strictly as packhouse intake quality          │
│    │ screening and risk-sensitive abstention.                                          │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 2  │ PERMANENT PURGE OF SENSOR FUSION CLAIMS: ToxiFruit Zenodo archive contains zero   │
│    │ sensor data. Restrict all ToxiFruit experiments strictly to optical vision.       │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 3  │ FRUITVISION CC BY-NC-ND 4.0 COMPLIANCE: Perform all fruit-cropping or background- │
│    │ masking controls strictly as in-memory transformations during evaluation; do not  │
│    │ re-distribute modified derivative image archives.                                 │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 4  │ MAHALANOBIS SINGULARITY REMEDIATION: Feature dimension D=1280 exceeds training    │
│    │ N_train=1057 (rank 1051). Direct matrix inversion is singular. Gate 1 must use   │
│    │ Ledoit-Wolf shrinkage, PCA reduction, or adopt Energy scoring as default.         │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 5  │ MANDATORY BACKGROUND CONTROLS: Execute background-patch and fruit-only mask tests │
│    │ to verify that OOD rejection responds to fruit rind changes, not laboratory vs.   │
│    │ retail market lighting shortcuts.                                                 │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 6  │ STATISTICAL POWER REPORTING: Validation set N_val=227 cannot certify a strict 2%  │
│    │ risk bound. Report empirical selective risk-coverage curves alongside exact       │
│    │ Clopper-Pearson binomial confidence intervals and cluster-aware bootstrap.        │
└────┴───────────────────────────────────────────────────────────────────────────────────┘
```

---
*Audit Completed and Signed by Independent Research Auditor.*

