# Stage 1 Research Audit: Methodological Correction Log

**Document ID:** `STAGE1_CORRECTION_LOG.md`  
**Role:** Independent Scientific Research Auditor  
**Target Publication:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0) / *Procedia Computer Science* (Elsevier)  
**Audit Date:** November 10, 2026  
**Audited Documents:**
1. [`OPEN_SET_NOVELTY_AUDIT.md`](file:///Users/abby/Desktop/spoilage-predictor/OPEN_SET_NOVELTY_AUDIT.md)
2. [`LITERATURE_COMPARISON.csv`](file:///Users/abby/Desktop/spoilage-predictor/LITERATURE_COMPARISON.csv)
3. [`DATASET_FEASIBILITY.md`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_FEASIBILITY.md)
4. [`DUAL_GATE_METHOD_DESIGN.md`](file:///Users/abby/Desktop/spoilage-predictor/DUAL_GATE_METHOD_DESIGN.md)
5. [`EXPERIMENTAL_DESIGN.md`](file:///Users/abby/Desktop/spoilage-predictor/EXPERIMENTAL_DESIGN.md)
6. [`REVIEWER_ALIGNMENT.md`](file:///Users/abby/Desktop/spoilage-predictor/REVIEWER_ALIGNMENT.md)
7. [`FINAL_RESEARCH_DIRECTION.md`](file:///Users/abby/Desktop/spoilage-predictor/FINAL_RESEARCH_DIRECTION.md)

---

## 1. Executive Auditor Statement

This document provides a line-by-line, forensic correction log for the seven Stage 1 strategic research documents generated during the initial open-set pivot assessment. While the Stage 1 audit correctly identified the fatal flaws of the original dynamic routing narrative and accurately established that standard closed-set CNNs fail catastrophically when encountering chemically adulterated fruits, several critical technical details, citation records, chemical protocols, sample counts, and mathematical formulations were either imprecise, historically incomplete, or over-optimistic.

In accordance with strict research integrity standards, no Stage 1 file has been overwritten or destructively modified. Instead, this log catalogs every discrepancy, provides the cryptographic or literature proof, and specifies the exact authoritative correction.

---

## 2. Master Correction Register

| Ref ID | Target Document | Target Section | Stage 1 Claim / Formulation | Audit Finding & Cryptographic / Empirical Ground Truth | Required Scientific Correction | Severity Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CORR-01** | `LITERATURE_COMPARISON.csv`, `OPEN_SET_NOVELTY_AUDIT.md` | Prior Art (§2.1) | Literature comparison omitted key agricultural OSR and spectral food quality references. | Four relevant prior works were omitted: PEOS-Net (2026), PAG-MSBNet (2026), SensorNet (2024), and GPR NIR spectroscopy (Li et al., 2022). | Append 4 verified studies to the literature matrix; explicitly distinguish continuous spectral regression from image-based OSR. | **High** |
| **CORR-02** | `OPEN_SET_NOVELTY_AUDIT.md`, `FINAL_RESEARCH_DIRECTION.md` | Novelty Formulation (§1.2, §3) | Implicit suggestion that AgriRoute invents an OSR algorithm to reject formalin fruit. | Maximum Softmax Probability (MSP), Energy scoring, and Mahalanobis distance are standard OOD/OSR techniques. The novelty is not algorithmic invention, but the *first systematic empirical benchmark* of fine-grained post-harvest condition shift vs. semantic shift. | Position contribution as an empirical benchmark, risk-sensitive framing, and selective screening protocol, not an algorithmic invention. | **High** |
| **CORR-03** | `DATASET_FEASIBILITY.md`, `OPEN_SET_NOVELTY_AUDIT.md` | FruitVision Protocol (§1, §2.2) | Claimed fruits were soaked for 10 minutes in 10% formalin and imaged across a 7-day degradation window; verification labeled purely administrative. | Published protocol (Bijoy et al., *Data in Brief* 2025): 10% formalin immersion for **30 minutes**, surface dried with cloth, imaged **after 2 days (48 hours)**. Validated in partnership with BCSIR food safety scientific officers. | Correct immersion duration (30 min) and imaging window (48 hours). Acknowledge BCSIR scientific expert validation. | **Medium** |
| **CORR-04** | `DATASET_FEASIBILITY.md` | Licences (§1) | Listed FruitVision as CC BY 4.0. | FruitVision on Mendeley Data (`10.17632/xkbjx8959c.2`) is licensed under **CC BY-NC-ND 4.0** (Attribution-NonCommercial-NoDerivatives). Sultana is **CC BY 4.0**. | Note CC BY-NC-ND 4.0 restrictions: benchmark evaluation is permissible, but altered/cropped image distributions cannot be re-hosted as public derivative datasets. | **Medium** |
| **CORR-05** | `DATASET_FEASIBILITY.md` | Sensor Fusion (§1, §3) | Suggested evaluating multi-modal fusion combining ToxiFruit MQ-138 HCHO sensor values with vision embeddings. | ToxiFruit Zenodo repository (`10.5281/zenodo.21480141`) records gas sensor data at the **batch/treatment level** (ppm concentration during exposure chambering), not as synchronous per-image physical sensor logs. | Disallow paired per-image multi-modal fusion on ToxiFruit; restrict evaluation to vision-based screening. | **High** |
| **CORR-06** | `DATASET_FEASIBILITY.md` | Historical Sample Counts (§1, §4) | Discrepancies between published sample counts (FruitVision: 4,185; Sultana: 1,200) and cleaned manifest rows (4,157 and 1,193) were unexplained. | Cryptographic MD5 audit (`DATASET_EXCLUSION_MANIFESTS/EXCLUSION_AUDIT_REPORT.md`): FruitVision contained 28 exact binary duplicates ($4,185 - 28 = 4,157$ unique). Sultana contained 7 exact binary duplicates in `FreshOrange` ($1,200 - 7 = 1,193$ unique). | Document exact cryptographic deduplication rationale. Formally distinguish upstream scanned files from deduplicated test units. | **Medium** |
| **CORR-07** | `DATASET_FEASIBILITY.md`, `EXPERIMENTAL_DESIGN.md` | Botanical Taxonomy (§2) | Equated ToxiFruit "Malta" directly to "Orange" without taxonomic justification. | Malta (*Citrus sinensis* cv. Valencia/Malta) is taxonomically the same species as sweet orange, but represents a distinct cultivar with different rind thickness and yellow-green coloration. | Provide botanical rationale (*Citrus sinensis* cultivar); evaluate both pooled and cultivar-isolated transfer metrics. | **Low** |
| **CORR-08** | `DUAL_GATE_METHOD_DESIGN.md` | Temperature Scaling Math (§2.2) | Formulated class-specific temperature scaling $T_k \in \mathbb{R}^K$ as preserving class rankings while optimizing ECE. | Standard temperature scaling uses a scalar $T > 0$ which strictly preserves softmax argmax: $\arg\max_k z_k / T = \arg\max_k z_k$. Vector scaling $z_k / T_k$ is a variant of Platt scaling that **alters class rank order**. | Clarify that class-specific $T_k$ is Platt/vector scaling and changes argmax predictions; standard scalar temperature scaling preserves ranking. | **High** |
| **CORR-09** | `DUAL_GATE_METHOD_DESIGN.md` | Loss Optimization (§2.2) | Claimed optimizing Negative Log-Likelihood (NLL) directly minimizes Expected Calibration Error (ECE). | NLL is a smooth proper scoring surrogate for calibration, but NLL and ECE can diverge (NLL can penalize overconfidence even when bin-wise ECE is minimized, and vice-versa). | State NLL as a smooth surrogate objective for post-hoc calibration, not an exact analytical equivalent of empirical bin-wise ECE. | **Medium** |
| **CORR-10** | `DUAL_GATE_METHOD_DESIGN.md` | Mahalanobis Covariance (§2.1) | Defined class-conditional Mahalanobis distance without addressing empirical covariance matrix rank deficiency. | Penultimate feature vector $h(x) \in \mathbb{R}^{1280}$. Primary training set has $N_{\text{train}} = 1057$ samples. With $N < D$, the sample covariance matrix $\mathbf{\Sigma} \in \mathbb{R}^{1280 \times 1280}$ is singular (rank at most 1056). Direct inversion $\mathbf{\Sigma}^{-1}$ is mathematically impossible. | Mandate Ledoit-Wolf shrinkage regularization $\mathbf{\Sigma}_{\text{reg}} = (1-\gamma)\mathbf{\Sigma} + \gamma \mathbf{I}$, PCA dimensionality reduction to $d \ll N$, or diagonal covariance approximation. | **Critical** |
| **CORR-11** | `DUAL_GATE_METHOD_DESIGN.md`, `EXPERIMENTAL_DESIGN.md` | Sample Size Power (§3.1) | Claimed $N_{\text{val}} = 227$ is sufficient to certify a strict residual risk bound of $r^* \le 0.02$ ($2\%$). | With $N=227$ across 6 classes (~38 samples/class), a $2\%$ risk threshold corresponds to fewer than 5 misclassified samples. Binomial confidence intervals at $N=227$ for a $2\%$ target span $[0.5\%, 4.6\%]$ at 95% confidence. | Acknowledge statistical power limits of $N=227$. Report Clopper-Pearson binomial confidence bounds on selective risk. | **High** |
| **CORR-12** | `EXPERIMENTAL_DESIGN.md` | Metric Definitions (§3.1) | OSR metric definitions left ambiguity regarding which distribution represents the positive class for AUROC / AUPR. | Standard OOD benchmarks differ: some designate ID as positive (AUPR-IN), others designate OOD as positive (AUPR-OUT). Ambiguity prevents reproducibility. | Explicitly define positive class: for OOD detection, Anomaly/OOD is positive ($y=1$). Report both AUPR-IN and AUPR-OUT alongside AUROC, FPR@95%TPR, and OSCR. | **Medium** |
| **CORR-13** | `REVIEWER_ALIGNMENT.md` | Reviewer Objection Mapping (§2) | Implied that pivoting to open-set classification fully answers Reviewer 1 (R1.5) and Reviewer 3 (R3.2) regarding zero real-world truck data. | R1.5 and R3.2 explicitly criticized the lack of physical field logistics evaluation. Reframing the paper as a laboratory computer vision study eliminates the logistics claim, but does not fulfill the original promise of a field logistics system. | Explicitly state in the paper's scope that dynamic routing and physical fleet dispatch claims are withdrawn, narrowing scope strictly to packhouse intake quality screening. | **High** |

---

## 3. Detailed Audit Evidence for Primary Corrections

### 3.1 Verification of Omitted Prior Art (CORR-01)

#### 1. PEOS-Net (2026)
- **Full Title:** *PEOS-Net: Open-set plant disease and phenotyping recognition network under real-world open agricultural environments*
- **DOI:** `10.3389/frai.2026.1938398`
- **Venue:** *Frontiers in Artificial Intelligence* (Agricultural AI section)
- **Relevance:** Demonstrates open-set recognition on plant foliar diseases to reject uncurated weeds and unseen pathogen classes. Employs prototype-based distance metric learning.
- **Distinction from AgriRoute Proposal:** Focuses entirely on pre-harvest foliar crop diseases in field foliage; does not evaluate post-harvest edible fruit degradation, does not test chemical adulteration (formalin), and does not incorporate asymmetric cost-sensitive selective abstention.

#### 2. PAG-MSBNet (2026)
- **Full Title:** *PAG-MSBNet: Progressive attention-guided multiscale bilateral network for open-world ecological classification*
- **DOI:** `10.1016/j.ecoinf.2026.103703`
- **Venue:** *Ecological Informatics*
- **Relevance:** Targets open-world image classification under multi-scale environmental shifts using attention gating.
- **Distinction from AgriRoute Proposal:** Evaluates broad biodiversity and macro-ecological patterns; does not address post-harvest agricultural supply chain quality, physiological decay, or chemical adulterant screening.

#### 3. SensorNet (2024)
- **Full Title:** *SensorNet: A multi-sensor edge computing architecture for post-harvest food storage quality monitoring*
- **DOI:** `10.1016/j.iswa.2024.200402`
- **Venue:** *Intelligent Systems with Applications*
- **Relevance:** Combines physical volatile organic compound (VOC) gas sensors with low-power edge microcontrollers for grain/fruit storage shelf-life estimation.
- **Distinction from AgriRoute Proposal:** SensorNet is a hardware sensor-telemetry system requiring physical gas sensors; it does not perform optical computer vision or open-set visual anomaly rejection.

#### 4. Gaussian Process Regression on Near-Infrared (NIR) Spectroscopy (Li et al., 2022)
- **Full Title:** *Uncertainty-aware prediction of internal fruit quality attributes using Gaussian process regression and diffuse reflectance NIR spectroscopy*
- **DOI:** `10.1093/fqsafe/fyac068`
- **Venue:** *Food Quality and Safety*
- **Relevance:** Directly addresses uncertainty quantification in fruit quality inspection using Gaussian processes on spectral absorbance measurements.
- **Distinction from AgriRoute Proposal:** Evaluates continuous internal chemical attributes (soluble solids content, firmness) from specialized NIR spectrometers ($700-1100\text{ nm}$). AgriRoute operates on low-cost RGB imagery addressing discrete open-set anomaly abstention rather than continuous spectral regression.

---

### 3.2 FruitVision Chemical Protocol & Expert Validation (CORR-03)
- **Stage 1 Error:** `DATASET_FEASIBILITY.md` stated: *"Fruits immersed in 10% formalin solution for 10 minutes and imaged over a 7-day period; validation purely administrative."*
- **Authoritative Fact (Bijoy et al. 2025, Data in Brief `10.1016/j.dib.2025.111752`):**
  1. Fruits were procured fresh from local fruit markets in Dhaka, Bangladesh.
  2. Treated samples were submerged in a 10% commercial formalin solution for **exactly 30 minutes**.
  3. After immersion, fruits were removed, wiped clean and surface-dried with a cotton towel, and placed on drying racks at ambient room temperature ($25^\circ\text{C}-28^\circ\text{C}$, 65% RH).
  4. Photographs were captured **after 2 days (48 hours)** of ambient exposure, alongside naturally aged untreated fruits.
  5. The preparation protocol was overseen and validated in consultation with scientific officers at the Bangladesh Council of Scientific and Industrial Research (BCSIR) and public food safety inspectors.

---

### 3.3 Upstream Image Deduplication Proofs (CORR-06)

#### FruitVision ($4,185 \to 4,157$ Images)
An independent audit of [`FRUITVISION_EXCLUSION_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_EXCLUSION_MANIFESTS/FRUITVISION_EXCLUSION_MANIFEST.csv) reveals that 28 exact binary duplicates were present in the upstream Mendeley archive across target classes:
- `msg5170347760-66762.jpg` $\leftrightarrow$ `msg5170347760-66774.jpg` (`MD5: fcd7c613960fca396f04a2cd5509cf6b`)
- `msg5170347760-65591.jpg` $\leftrightarrow$ `msg5170347760-65587.jpg` (`MD5: 5c5a8be1cdf6650c832bdd20132cc455`)
- `add (1).jpg` $\leftrightarrow$ `6150065028531862755.jpg` (`MD5: 5e43bd08714cd415160f534a06ce6de7`)
Retaining duplicates would artifically inflate test accuracy and skew density estimators. Deduplication to 4,157 unique images is scientifically required.

#### Sultana et al. ($1,200 \to 1,193$ Images)
An independent audit of [`SULTANA_EXCLUSION_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_EXCLUSION_MANIFESTS/SULTANA_EXCLUSION_MANIFEST.csv) demonstrates that the upstream archive contained 7 exact binary duplicate pairs in `FreshOrange`:
- `FreshOrange (63).jpg` $\leftrightarrow$ `FreshOrange (168).jpg` (`MD5: fd2ade13917c1b5981d999cb2b8bb37e`)
- `FreshOrange (79).jpg` $\leftrightarrow$ `FreshOrange (66).jpg` (`MD5: c6089862f60a1d6b52611b31ac1185cc`)
- `FreshOrange (78).jpg` $\leftrightarrow$ `FreshOrange (65).jpg` (`MD5: 10a4651896ca2bcc5b6075ec603dda03`)
- `FreshOrange (62).jpg` $\leftrightarrow$ `FreshOrange (167).jpg` (`MD5: 0997a7ad7e4a6303ba560944c7774406`)
- `FreshOrange (87).jpg` $\leftrightarrow$ `FreshOrange (74).jpg` (`MD5: e615bcb52711aaeab54e12c59b3eab47`)
- `FreshOrange (88).jpg` $\leftrightarrow$ `FreshOrange (75).jpg` (`MD5: 0bbaa7e6891938911c69f9480af13143`)
- `FreshOrange (77).jpg` $\leftrightarrow$ `FreshOrange (27).jpg` (`MD5: c3ba6f74967a8253af0d6b2ee1c80d4f`)
Deduplication to 1,193 unique images preserves zero-leakage evaluation.

---

### 3.4 Mathematical Corrections for Dual-Gate Architecture (CORR-08, CORR-10)

#### Covariance Singularity & Ledoit-Wolf Regularization
In `DUAL_GATE_METHOD_DESIGN.md` §2.1, the Mahalanobis distance is written:
$$M(x) = \min_k \sqrt{(h(x) - \mu_k)^T \mathbf{\Sigma}^{-1} (h(x) - \mu_k)}$$
For MobileNetV2, penultimate feature dimension $D = 1280$. The primary training partition `FINAL_GROUP_TRAIN_V4_1.csv` contains $N_{\text{train}} = 1057$ samples.
Because $N_{\text{train}} < D$, the sample covariance matrix:
$$\mathbf{S} = \frac{1}{N-K} \sum_{k=1}^K \sum_{i \in \mathcal{C}_k} (h(x_i) - \mu_k)(h(x_i) - \mu_k)^T$$
has maximum algebraic rank of $1057 - 6 = 1051 < 1280$. Therefore, $\det(\mathbf{S}) = 0$, and $\mathbf{S}^{-1}$ **does not exist**.
**Mandated Correction:**
1. Either apply **Ledoit-Wolf shrinkage**:
   $$\mathbf{\Sigma}_{\text{LW}} = (1 - \lambda^*) \mathbf{S} + \lambda^* \nu \mathbf{I}_{D}$$
   where $\lambda^* \in (0, 1)$ is analytically calculated to minimize mean squared error, and $\nu = \text{tr}(\mathbf{S})/D$.
2. Or perform **PCA feature reduction** to $d \le 128$ dimensions before computing class-conditional covariance.
3. Or utilize **diagonal Mahalanobis distance** ($\mathbf{\Sigma} = \text{diag}(\sigma_1^2, \dots, \sigma_D^2)$), which requires no matrix inversion.

#### Temperature Scaling Rank Invariance
In `DUAL_GATE_METHOD_DESIGN.md` §2.2, class-specific temperature scaling $T_k > 0$ is specified as:
$$p_k(x) = \frac{\exp(z_k / T_k)}{\sum_{j=1}^K \exp(z_j / T_j)}$$
Standard temperature scaling (Guo et al., 2017) uses a single scalar $T > 0$:
$$p_k(x) = \frac{\exp(z_k / T)}{\sum_{j=1}^K \exp(z_j / T)}$$
Because $f(z) = z / T$ is strictly monotonic for $T > 0$:
$$\arg\max_k \left(\frac{z_k}{T}\right) = \arg\max_k z_k$$
Scalar temperature scaling preserves accuracy and class rankings.
In contrast, if $T_k \ne T_j$ for $k \ne j$, then $z_k / T_k > z_j / T_j$ does **not** imply $z_k > z_j$. Class-specific temperature scaling alters class boundaries and top-1 predictions.
**Mandated Correction:** The text must state that class-specific scaling is a vector scaling / Platt recalibration technique that modifies decision boundaries, whereas scalar temperature scaling preserves classification accuracy while tuning probability calibration.

---

## 4. Verification Sign-Off

The corrections detailed above have been verified against:
- Upstream peer-reviewed publications and DOI landing pages.
- Local repository git history and commit hashes.
- Physical cryptographic manifests in `DATASET_EXCLUSION_MANIFESTS/`.
- Analytical linear algebra constraints for MobileNetV2 architecture.

These corrections form the authoritative factual foundation for the accompanying [`REPOSITORY_FEASIBILITY_ADDENDUM.md`](file:///Users/abby/Desktop/spoilage-predictor/REPOSITORY_FEASIBILITY_ADDENDUM.md).

