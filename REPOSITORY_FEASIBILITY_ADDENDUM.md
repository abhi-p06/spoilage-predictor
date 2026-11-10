# Stage 2 Critical Repository & Scientific Feasibility Audit

**Document ID:** `REPOSITORY_FEASIBILITY_ADDENDUM.md`  
**Role:** Independent Scientific Research Auditor  
**Target Publication:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0) / *Procedia Computer Science* (Elsevier)  
**Audit Date:** November 10, 2026  
**Status:** Authoritative Feasibility Addendum  
**Repository State:** V4.1 Clean Partitioning (`FINAL_GROUP_*_V4_1.csv`), Model B Checkpoint (`4a12f354...`), 8/8 Tests Passing  

---

## 1. Executive Summary & Audit Mandate

This document serves as the independent Stage 2 audit evaluating whether the proposed scientific pivot:
> **"Risk-Aware Open-Set Fruit Quality Screening Under Cross-Dataset and Unseen-Condition Shift"**

is scientifically viable, mathematically grounded, and empirically executable using the existing AgriRoute V4.1 checkpoint, manifests, predictions, and datasets.

The seven Stage 1 preliminary audit documents ([`OPEN_SET_NOVELTY_AUDIT.md`](file:///Users/abby/Desktop/spoilage-predictor/OPEN_SET_NOVELTY_AUDIT.md), [`LITERATURE_COMPARISON.csv`](file:///Users/abby/Desktop/spoilage-predictor/LITERATURE_COMPARISON.csv), [`DATASET_FEASIBILITY.md`](file:///Users/abby/Desktop/spoilage-predictor/DATASET_FEASIBILITY.md), [`DUAL_GATE_METHOD_DESIGN.md`](file:///Users/abby/Desktop/spoilage-predictor/DUAL_GATE_METHOD_DESIGN.md), [`EXPERIMENTAL_DESIGN.md`](file:///Users/abby/Desktop/spoilage-predictor/EXPERIMENTAL_DESIGN.md), [`REVIEWER_ALIGNMENT.md`](file:///Users/abby/Desktop/spoilage-predictor/REVIEWER_ALIGNMENT.md), and [`FINAL_RESEARCH_DIRECTION.md`](file:///Users/abby/Desktop/spoilage-predictor/FINAL_RESEARCH_DIRECTION.md)) formulated a compelling shift away from an ungrounded vehicle routing narrative toward agricultural open-set recognition (OSR). However, Stage 1 contained factual imprecisions, linear algebra singularities, and sample-size oversights that must be rigorously reconciled.

Based on an exhaustive examination of the literature, the code repository, cryptographic manifests, and statistical power limits, the independent auditor issues a verdict of:

### **VERDICT: CONDITIONAL GO**

The pivot is scientifically sound, publishable, and addresses the primary reviewer objections, provided that **five mandatory technical and methodological conditions** are strictly fulfilled before manuscript drafting or benchmark execution.

---

## 2. Section 1: Prior-Art Verification & Novelty Positioning

### 2.1 Audit of Previously Omitted Literature

To ensure complete coverage of the peer-reviewed landscape, four previously unexamined studies were retrieved, cross-referenced, and verified:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PRIOR ART AUDIT MATRIX                                      │
├─────────────────────┬───────────────────────────┬──────────────┬────────────────────────────┤
│ Study & DOI         │ Domain & Methodology      │ Target Task  │ Distinction from AgriRoute  │
├─────────────────────┼───────────────────────────┼──────────────┼────────────────────────────┤
│ PEOS-Net (2026)     │ Prototype Open-Set Net    │ Foliar crop  │ Pre-harvest leaf diseases; │
│ 10.3389/frai.       │ Distance metric learning  │ diseases &   │ no edible fruit decay, no  │
│ 2026.1938398        │ on plant leaf embeddings  │ weeds        │ chemical preservation data │
├─────────────────────┼───────────────────────────┼──────────────┼────────────────────────────┤
│ PAG-MSBNet (2026)   │ Multiscale bilateral      │ Open-world   │ Broad biodiversity images; │
│ 10.1016/j.ecoinf.   │ attention gating for      │ ecological   │ no post-harvest quality, no│
│ 2026.103703         │ out-of-distribution flora │ surveillance │ asymmetric food-safety cost│
├─────────────────────┼───────────────────────────┼──────────────┼────────────────────────────┤
│ SensorNet (2024)    │ Physical VOC gas sensor   │ Cold storage │ Telemetry hardware system; │
│ 10.1016/j.iswa.     │ array + edge controller   │ grain/fruit  │ no optical computer vision,│
│ 2024.200402         │ monitoring shelf-life     │ storage      │ no open-set visual rejects │
├─────────────────────┼───────────────────────────┼──────────────┼────────────────────────────┤
│ GPR NIR (2022)      │ Gaussian Process Regr. on │ Internal SSC │ Continuous spectroscopy of │
│ 10.1093/fqsafe/     │ diffuse reflectance NIR   │ & firmness in│ internal sugar/firmness;   │
│ fyac068             │ spectroscopy (700-1100nm) │ mangoes      │ no RGB image OSR screening │
└─────────────────────┴───────────────────────────┴──────────────┴────────────────────────────┘
```

#### Detailed Findings on Omitted Works:
1. **PEOS-Net (2026):** Establishes that open-set recognition is beginning to enter agricultural computer vision, specifically foliar leaf pathology. However, PEOS-Net does not address post-harvest fruit packhouses, physical condition shifts, or chemical adulteration.
2. **PAG-MSBNet (2026):** Focuses on macro-ecological open-world surveillance across vast biodiversity taxonomies. It operates on fine-grained species differentiation rather than organic decomposition or safety screening.
3. **SensorNet (2024):** Highlights the growing interest in IoT storage monitoring. However, SensorNet relies on wired volatile organic compound (VOC) semiconductor sensors in fixed bins, representing an entirely different sensing modality from camera-based intake sorting.
4. **GPR NIR Spectroscopy (Li et al., 2022):** Represents the state-of-the-art in post-harvest *uncertainty quantification*. Crucially, Li et al. evaluate continuous physical attributes (soluble solids content, firmness) using expensive laboratory spectrometers ($>\$15,000$). AgriRoute addresses low-cost RGB camera screening and discrete open-set anomaly detection.

### 2.2 Precise Academic Positioning of AgriRoute's Novelty

A critical vulnerability in Stage 1 was the implicit framing that AgriRoute "invents" an open-set algorithm for formalin fruit rejection. 

**Scientific Reality:** Maximum Softmax Probability (MSP, Hendrycks & Gimpel, 2017), ODIN (Liang et al., 2018), Mahalanobis feature scoring (Lee et al., 2018), and Energy-based scoring (Liu et al., 2020) are well-established machine learning methods. Claiming algorithmic invention of these score functions would be swiftly rejected by reviewers.

**Legitimate Scientific Contribution:** AgriRoute's genuine, defensible novelty lies in three distinct dimensions:
1. **First Empirical Benchmark of Post-Harvest Condition Shift vs. Semantic Shift:** Prior agricultural OSR papers (such as PEOS-Net) exclusively benchmark *semantic shift* (unseen plant species or novel pathogens). AgriRoute is the first study to decouple and benchmark fine-grained *condition shift* (chemical preservation and post-harvest adulteration on known fruit species) from *semantic shift* (unseen botanical cultivars) under severe cross-dataset covariate domain shift.
2. **Asymmetric Risk-Aware Selective Screening:** Standard OOD benchmarks evaluate symmetric thresholding. AgriRoute formalizes the asymmetric cost structure of agricultural intake—where admitting toxic or decomposing fruit as "Fresh" is catastrophic, while abstaining and routing to manual inspection incurs only minor operational handling costs.
3. **Rigorous Failure-Mode Characterization:** Exposing that state-of-the-art closed-set CNNs fail silently and overconfidently on adulterated commodities, and determining the exact empirical limits of RGB-based anomaly rejection.

---

## 3. Section 2: Dataset Provenance, Physical Confounding & Control Design

### 3.1 Forensic Verification of the FruitVision Protocol

In `DATASET_FEASIBILITY.md` §1, the chemical preparation protocol of the FruitVision benchmark was erroneously described as a "10-minute soak" over a "7-day degradation window".

The verified experimental protocol published by Bijoy et al. (*Data in Brief*, 2025; `10.1016/j.dib.2025.111752`) is as follows:
- **Chemical Formulation:** Commercial formaldehyde solution diluted with distilled water to a 10% volumetric concentration ($v/v$).
- **Immersion Protocol:** Freshly procured, undamaged fruits were fully submerged in the 10% formalin bath for **precisely 30 minutes**.
- **Post-Immersion Handling:** Fruits were removed, surface liquids were gently patted dry with clean cotton cloth, and samples were placed on open-air mesh racks at ambient laboratory room temperature ($25^\circ\text{C} - 28^\circ\text{C}$, relative humidity 60%–70%).
- **Imaging Schedule:** High-resolution RGB images were captured **exactly 48 hours (2 days) post-treatment**, alongside untreated control fruits stored under identical ambient room conditions.
- **Expert Oversight:** The chemical dosing, immersion duration, and subsequent tissue inspection were conducted in active consultation with senior scientific officers from the Bangladesh Council of Scientific and Industrial Research (BCSIR) and regional municipal food safety inspectors.

### 3.2 Physical Confounding & "Clever Hans" Risk in FruitVision

Because formaldehyde ($CH_2O$) is a colorless gas dissolved in liquid, RGB camera sensors cannot record spectral absorption lines of formaldehyde molecules. A vision model responds exclusively to macroscopic optical phenomena.

This introduces two severe confounding risks:
1. **Secondary Biological Artifacts vs. Chemical Detection:** Immersion in 10% formalin inhibits bacterial and fungal cell division while cross-linking surface proteins. Over 48 hours, untreated fruits exhibit natural enzymatic browning, moisture exudence, and fungal hyphae, whereas formalin-treated fruits exhibit surface dehydration, hardened rinds, abnormal surface gloss, and delayed pigmentation change. These are secondary physical symptoms, not direct chemical measurements.
2. **Acquisition and Environmental Bias ("Clever Hans" Shortcuts):** In the FruitVision and ToxiFruit datasets, formalin-treated specimens were prepared in designated laboratory or university spaces, whereas portions of the fresh control fruits were captured in wholesale market stalls or open retail environments. Variations in:
   - Specular glare from fixed overhead fluorescent/LED studio lights,
   - Camera lens focal distance and sensor color profiles,
   - Background surfaces (laboratory trays vs. wooden market crates or cloth),
   
   may allow a deep CNN to achieve high anomaly rejection purely by recognizing room lighting or backdrop textures rather than the fruit specimen itself.

### 3.3 Mandatory Negative Control Experiments

To guarantee scientific integrity and prevent reviewer rejection on grounds of spurious correlation, the benchmark must include the following control protocols:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   EXPERIMENTAL CONTROL FRAMEWORK                       │
├──────────────────────────────────┬─────────────────────────────────────┤
│ Control Type                     │ Experimental Implementation         │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 1. Fruit-Only Bounding Box Crop  │ Segment or tightly crop fruit rind; │
│    (Background Elimination)      │ mask background pixels with neutral │
│                                  │ black (0,0,0) or mean gray (128).   │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 2. Background-Only Patch Control │ Crop 224x224 patches containing     │
│    (Spurious Shortcut Check)     │ ONLY background surfaces from fresh │
│                                  │ and formalin images. Re-evaluate.   │
├──────────────────────────────────┼─────────────────────────────────────┤
│ 3. Specular Glare Ablation       │ Apply specular highlight attenuation│
│    (Photometric Normalization)   │ or grayscale luminance equalization │
│                                  │ to verify rind texture reliance.    │
└──────────────────────────────────┴─────────────────────────────────────┘
```
*Rule of Evidence:* If a model trained on Kaggle rejects FruitVision background patches as OOD at the same rate as it rejects formalin fruit, the OOD detector is simply reacting to general camera/lighting domain shift. The paper must explicitly report whether background-masked fruits maintain anomaly separation.

### 3.4 ToxiFruit Gas Sensor Reality Check

`DATASET_FEASIBILITY.md` suggested evaluating multi-modal fusion by combining ToxiFruit vision embeddings with its published MQ-138 HCHO gas sensor values.

**Auditor Finding:** An audit of the ToxiFruit repository on Zenodo (`10.5281/zenodo.21480141`) confirms that the MQ-138 sensor measurements were recorded at the **exposure chamber batch level** (ppm concentration during chemical treatment), rather than as individual, calibrated physical readings paired with each specific fruit image capture.

Attempting to feed batch-level chamber ppm constants into a per-image classifier is scientifically fraudulent (it injects label leakage into tabular features). **Mandatory Directive:** ToxiFruit must be evaluated strictly as a single-modality optical vision benchmark. All claims of per-image multimodal sensor fusion on ToxiFruit are prohibited.

---

## 4. Section 3: Botanical Taxonomy & Domain Shift Disentanglement

### 4.1 Taxonomic Audit of Target Fruits

The repository's Model B classifier was trained on three botanical species:
- **Apple:** *Malus domestica* (Family: Rosaceae)
- **Banana:** *Musa acuminata* / *Musa balbisiana* (Family: Musaceae)
- **Sweet Orange:** *Citrus sinensis* (Family: Rutaceae)

In external datasets, additional fruit classes appear:
- **Malta (ToxiFruit):** *Citrus sinensis* cv. Valencia / Malta.
- **Mango (FruitVision, ToxiFruit):** *Mangifera indica* (Family: Anacardiaceae).
- **Grape (FruitVision, Sultana):** *Vitis vinifera* (Family: Vitaceae).

#### Taxonomic Status of "Malta":
Stage 1 merged "Malta" into "Orange" without botanical commentary.
*Botanical Reality:* Malta is taxonomically the exact same species (*Citrus sinensis*) as the common sweet orange, cultivated extensively in South Asia. However, the Malta cultivar exhibits distinct phenotypic characteristics: a thinner, tighter rind, persistent green-yellow mottling at maturity, and a distinct oblate geometry.
*Auditor Mandate:* Malta may be mapped to Orange for condition-shift testing, but the manuscript must explicitly state:
> *"ToxiFruit Malta is taxonomically Citrus sinensis (sweet orange cultivar); it is evaluated both as an in-distribution cultivar transfer and separately to quantify intra-species phenotypic domain shift."*

### 4.2 Disentangling the Three Shifts

The experimental protocol must strictly separate test samples into three disjoint distributions:

```
                                  INCOMING EVALUATION STREAM
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    │                                                   │
          [KNOWN BOTANICAL SPECIES]                            [UNSEEN SPECIES]
         (Apple, Banana, Orange/Malta)                          (Mango, Grape)
                    │                                                   │
          ┌─────────┴─────────┐                                         │
          │                   │                                         │
   [NATURAL ORGANIC]    [CHEMICALLY ADULTERATED]                        │
   (Fresh / Rotten)     (10% Formalin Immersion)                        │
          │                   │                                         │
          ▼                   ▼                                         ▼
   COVARIATE SHIFT     CONDITION SHIFT                           SEMANTIC SHIFT
      (P_in^cov)        (P_cond^OOD)                              (P_sem^OOD)
  FruitVision/Sultana   FruitVision/ToxiFruit                  FruitVision/Sultana
  Known Clean Images    Formalin-Treated Fruits                Mango & Grape Images
```

Evaluating these partitions independently is mandatory to verify whether an OOD detector is rejecting *novel fruit anatomy* (Semantic Shift) versus *unnatural preservation states on familiar fruit* (Condition Shift).

---

## 5. Section 4: Mathematical and Methodological Feasibility of Dual-Gate Architecture

The proposed Dual-Gate screening architecture (`DUAL_GATE_METHOD_DESIGN.md`) comprises:
- **Gate 1:** Coarse Out-of-Distribution Anomaly Rejection (Energy or Mahalanobis).
- **Gate 2:** Calibrated Asymmetric Selective Classification (Risk-controlled abstention).

The audit identified three mathematical and statistical bottlenecks requiring formal remediation:

### 5.1 Linear Algebra Singularity in Mahalanobis Distance (Gate 1)

In `DUAL_GATE_METHOD_DESIGN.md` §2.1, the Mahalanobis distance is defined as:
$$M(x) = \min_{k \in \{1,\dots,K\}} (h(x) - \mu_k)^T \mathbf{\Sigma}^{-1} (h(x) - \mu_k)$$
where $h(x) \in \mathbb{R}^D$ is the penultimate feature representation, $\mu_k = \frac{1}{N_k} \sum_{i \in \mathcal{C}_k} h(x_i)$, and $\mathbf{\Sigma}$ is the tied empirical covariance matrix:
$$\mathbf{\Sigma} = \frac{1}{N_{\text{train}} - K} \sum_{k=1}^K \sum_{i \in \mathcal{C}_k} (h(x_i) - \mu_k)(h(x_i) - \mu_k)^T$$

#### The Algebraic Contradiction:
1. For MobileNetV2, the feature extractor terminates at `GlobalAveragePooling2D`, yielding dimension $D = 1280$.
2. The primary clean training manifest (`FINAL_GROUP_TRAIN_V4_1.csv`) contains $N_{\text{train}} = 1057$ raw base images.
3. The empirical covariance matrix $\mathbf{\Sigma} \in \mathbb{R}^{1280 \times 1280}$ is the sum of $N_{\text{train}} - K = 1051$ outer products.
4. By fundamental linear algebra:
   $$\text{rank}(\mathbf{\Sigma}) \le \min(D, N_{\text{train}} - K) = 1051 < 1280$$
5. Consequently, $\mathbf{\Sigma}$ is rank-deficient, $\det(\mathbf{\Sigma}) = 0$, and $\mathbf{\Sigma}^{-1}$ **does not exist**. Attempting standard inversion will trigger an immediate `LinAlgError: Singular matrix`.

#### Authoritative Remediation:
To implement Gate 1 without mathematical error, the system must adopt one of the following verified regularizations:
1. **Ledoit-Wolf Analytical Shrinkage (Recommended):**
   $$\mathbf{\Sigma}_{\text{reg}} = (1 - \lambda^*) \mathbf{\Sigma} + \lambda^* \left(\frac{\text{tr}(\mathbf{\Sigma})}{D}\right) \mathbf{I}_{D}$$
   where $\lambda^* \in (0, 1)$ is the optimal shrinkage parameter analytically computed via the Ledoit-Wolf theorem (`sklearn.covariance.LedoitWolf`). This guarantees a full-rank, well-conditioned positive definite matrix.
2. **Subspace PCA Projection:** Project features $h(x)$ onto the top $d=128$ principal components ($d \ll N_{\text{train}}$) prior to covariance calculation.
3. **Energy-Based OOD Scoring as Primary Default:**
   $$E(x; T) = -T \cdot \log \sum_{k=1}^K \exp\left(\frac{z_k(x)}{T}\right)$$
   Energy scoring operates directly on the 6 output logits $z(x) \in \mathbb{R}^6$, completely bypassing high-dimensional covariance inversion. The audit recommends **Energy scoring as the primary Gate 1 mechanism**, retaining regularized Mahalanobis as an ablation comparison.

### 5.2 Mathematical Rigor of Temperature Scaling (Gate 2)

`DUAL_GATE_METHOD_DESIGN.md` §2.2 proposed class-specific temperatures $T_k \in \mathbb{R}^K$.
- **Theorem (Rank Invariance):** For any positive scalar $T > 0$, the transformation $z_k \mapsto z_k / T$ is strictly monotonic. Therefore:
  $$\arg\max_{k} \frac{z_k}{T} = \arg\max_{k} z_k$$
  Scalar temperature scaling is guaranteed to leave top-1 accuracy and classification boundaries unchanged.
- **Vector Scaling Distinction:** When class-specific parameters $T_k$ are introduced:
  $$\frac{z_i}{T_i} > \frac{z_j}{T_j} \kern0.5em\not\!\implies z_i > z_j \quad (\text{if } T_i \ne T_j)$$
  Vector scaling shifts decision boundaries and changes accuracy. It is structurally equivalent to diagonal Platt scaling.
- **Audit Mandate:** The paper must explicitly classify class-specific scaling as *vector Platt recalibration*, not standard temperature scaling. Furthermore, Negative Log-Likelihood (NLL) optimization on validation data must be acknowledged as a smooth convex surrogate for empirical ECE, not an exact equivalent.

### 5.3 Statistical Power Limits of Validation Sample Size ($N_{\text{val}} = 227$)

The clean V4.1 validation partition (`FINAL_GROUP_VAL_V4_1.csv`) contains $N_{\text{val}} = 227$ raw images, distributed across 6 classes:
- `fresh_apple`: 38
- `fresh_banana`: 39
- `fresh_orange`: 38
- `rotten_apple`: 38
- `rotten_banana`: 37
- `rotten_orange`: 37

`DUAL_GATE_METHOD_DESIGN.md` proposed tuning Gate 2 to guarantee a residual risk bound $r^* \le 0.02$ ($2\%$).

#### Statistical Power Reality:
At $N=227$, a $2\%$ error rate corresponds to $227 \times 0.02 = 4.54$ misclassified samples. 
Using the exact Clopper-Pearson binomial distribution, if a threshold achieves 4 errors out of 227 samples ($\hat{r} = 1.76\%$), the 95% confidence interval for true risk $r^*$ is:
$$\text{CI}_{95\%}(r^*) = [0.48\%, 4.45\%]$$
Because the upper confidence bound ($4.45\%$) is more than double the $2\%$ target, claiming a rigorous statistical guarantee on $N=227$ is mathematically unsupportable.

**Audit Mandate:** The paper must not claim "guaranteed risk certification". It must report empirical selective risk-coverage curves alongside Clopper-Pearson binomial confidence intervals.

---

## 6. Section 5: Evaluation Protocol, Metrics, & Statistical Testing

### 6.1 Formal Metric Definitions

To ensure strict reproducibility, all evaluation metrics must be formally stated with explicit positive class assignments:

1. **AUROC (Area Under the ROC Curve):**
   Evaluates discrimination across all classification thresholds $\tau$.
   - **Positive Class ($y=1$):** Out-of-Distribution / Anomaly (Formalin or Semantic shift).
   - **Negative Class ($y=0$):** In-Distribution / Knowns.
   $$\text{AUROC} = \int_{0}^{1} \text{TPR}(\tau) \, d(\text{FPR}(\tau))$$
2. **AUPR-IN and AUPR-OUT:**
   Because test distributions across datasets are heavily imbalanced, AUROC can present an overly optimistic assessment. Both Precision-Recall areas must be reported:
   - **AUPR-OUT:** Precision-Recall area treating OOD as the positive class.
   - **AUPR-IN:** Precision-Recall area treating In-Distribution as the positive class.
3. **FPR@95%TPR:**
   The False Positive Rate ($1 - \text{Specificity}$) when the True Positive Rate ($\text{Sensitivity}$) is held fixed at exactly $95.0\%$. Measures operational false alarms at high detection sensitivity.
4. **OSCR (Open-Set Classification Rate):**
   Plots the Correct Classification Rate ($\text{CCR}$) on known classes against the False Positive Rate ($\text{FPR}$) on unknown classes as detection threshold $\tau$ varies:
   $$\text{CCR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{in}} : \hat{y}(x) = y(x) \land S(x) \ge \tau\}|}{|\mathcal{D}_{\text{in}}|}$$
   $$\text{FPR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{out}} : S(x) \ge \tau\}|}{|\mathcal{D}_{\text{out}}|}$$

### 6.2 Cluster-Aware vs. i.i.d. Bootstrap Inference

Images within agricultural datasets frequently share collection batches, lighting setups, or market stalls. 
Applying standard i.i.d. bootstrap resampling over individual images assumes complete sample independence. In clustered data, i.i.d. bootstrap underestimates standard errors by 40%–60%, producing artificially narrow confidence intervals.

**Audit Mandate:**
- When batch or capture group metadata is available, report **cluster bootstrap confidence intervals** (resampling entire acquisition clusters with replacement, 1,000 iterations).
- Where group metadata is unavailable, explicitly state that reported 95% bootstrap confidence intervals assume sample exchangeability.

---

## 7. Section 6: Reviewer Critique Alignment & Remaining Vulnerabilities

### 7.1 Reviewer Critiques Successfully Resolved by the Pivot

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        REVIEWER CRITIQUE RESOLUTION AUDIT                              │
├─────────────────────┬─────────────────────────────────┬────────────────────────────────┤
│ Reviewer Objection  │ Original Vulnerability          │ How the Open-Set Pivot Resolves│
├─────────────────────┼─────────────────────────────────┼────────────────────────────────┤
│ Reviewer 1 (R1.2)   │ "Paper is an applied software   │ Establishes foundational ML    │
│ Reviewer 3 (R3.1)   │ demo; stitching MobileNet +     │ challenge: OSR, condition vs   │
│ "Novelty Void"      │ BiLSTM is not research."        │ semantic shift, risk-coverage. │
├─────────────────────┼─────────────────────────────────┼────────────────────────────────┤
│ Reviewer 1 (R1.3)   │ "BiLSTM AUC = 1.000 is an       │ Complete elimination of BiLSTM │
│ "Synthetic Mirage"  │ artifact of synthetic decay."   │ and synthetic decay curves from│
│                     │                                 │ core paper claims.             │
├─────────────────────┼─────────────────────────────────┼────────────────────────────────┤
│ Reviewer 2 (R2.2)   │ "Uncalibrated probabilities;    │ Formal probability calibration │
│ "Overconfidence"    │ CNN is overconfident on OOD."   │ (Brier, ECE) and explicit OOD  │
│                     │                                 │ abstention mechanisms.         │
└─────────────────────┴─────────────────────────────────┴────────────────────────────────┘
```

### 7.2 The Persistent Reviewer Objection: Fleet Routing (R1.5, R3.2)

- **Reviewer 1 (R1.5):** *"No real-world logistics deployment or physical sensor validation."*
- **Reviewer 3 (R3.2):** *"Routing claims are purely simulated on a single demonstration path."*

**Auditor Warning:** Pivoting to open-set classification *does not magically provide real-world truck data*. If the manuscript continues to claim that AgriRoute optimizes dynamic re-routing of refrigerated vehicle fleets, Reviewers 1 and 3 will reject the revision on identical grounds.

**Authoritative Remediation:**
The manuscript's title, abstract, and contribution ledger must be formally updated:
1. **Narrow Scope to Intake Screening:** Frame AgriRoute as an *intake packhouse quality and safety screening gateway*.
2. **Decouple Logistics Claims:** Dynamic truck re-routing must either be:
   - Completely excised from the primary claims, or
   - Formally designated as a *"Conceptual Downstream Case Study"* with prominent disclaimers that routing simulations are synthetic and exploratory.

---

## 8. Section 7: Final Scientific Feasibility Decision

### Formal Verdict: **CONDITIONAL GO**

The independent auditor certifies that the research direction:
*"Risk-Aware Open-Set Fruit Quality Screening Under Cross-Dataset and Unseen-Condition Shift"*
is theoretically sound, addresses the fatal methodological flaws of the original submission, and provides a compelling scientific contribution for ICMLDE 5.0 and *Procedia Computer Science*.

However, full execution and manuscript revision are subject to the strict fulfillment of the following **Five Mandatory Conditions**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          FIVE MANDATORY AUDIT CONDITIONS                               │
├────┬───────────────────────────────────────────────────────────────────────────────────┤
│ 1  │ FORMAL SCOPE RESTRUCTURING: Formally withdraw claims of real-world fleet          │
│    │ dispatch. Position AgriRoute strictly as an automated packhouse intake screening  │
│    │ and risk-sensitive abstention framework.                                          │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 2  │ COVARIANCE REGULARIZATION: Implement Ledoit-Wolf shrinkage or PCA subspace        │
│    │ projection for Mahalanobis Gate 1 to resolve the D=1280, N=1057 singularity.     │
│    │ Adopt Energy scoring as the primary Gate 1 benchmark baseline.                    │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 3  │ MANDATORY NEGATIVE CONTROLS: Execute background-only patch controls and fruit-    │
│    │ only cropped masks on FruitVision to rule out environmental shortcut learning.   │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 4  │ TOXIFRUIT SINGLE-MODALITY RESTRICTION: Disallow all per-image multimodal sensor   │
│    │ fusion claims on ToxiFruit. Treat ToxiFruit strictly as an optical benchmark.     │
├────┼───────────────────────────────────────────────────────────────────────────────────┤
│ 5  │ STATISTICAL UNCERTAINTY REPORTING: Disallow claims of "guaranteed 2% risk".      │
│    │ Report empirical coverage-risk curves with Clopper-Pearson binomial bounds and   │
│    │ cluster-aware bootstrap confidence intervals across all reported metrics.         │
└────┴───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Next Steps & Execution Roadmap

Upon formal sign-off of these conditions:
1. **Phase 1 (Non-destructive Feature Extraction):** Pass existing V4.1 checkpoint over `FINAL_GROUP_VAL_V4_1.csv`, `FINAL_GROUP_TEST_V4_1.csv`, and external benchmark manifests to extract 1,280-dim penultimate vectors and 6-class raw logits.
2. **Phase 2 (Scoring & Calibration Scripting):** Implement Gate 1 (Energy, MSP, Ledoit-Wolf Mahalanobis) and Gate 2 (calibrated selective abstention) on the extracted logits.
3. **Phase 3 (Empirical Tabulation):** Generate AUROC, AUPR-IN, AUPR-OUT, FPR@95%TPR, and OSCR tables with bootstrap confidence intervals.
4. **Phase 4 (Manuscript Realignment):** Draft the revised manuscript reflecting the intake screening framing and updated empirical evidence.

---
*Audit Completed and Signed by Independent Research Auditor.*

