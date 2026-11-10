# Experimental Design & Evaluation Protocol: Open-Set Fruit Quality Screening

**Role:** Principal Investigator & Lead Benchmark Methodologist  
**Project:** AgriRoute / Spoilage-Predictor  
**Date:** November 10, 2026  
**Status:** Complete Experimental Specification

---

## 1. Experimental Objectives

This benchmark design evaluates the following core scientific hypotheses:
1. **Hypothesis 1 (Closed-Set Vulnerability):** Standard closed-set vision backbones (MobileNetV2, EfficientNetB0, ResNet50) evaluated on unseen chemical condition shifts (formalin-dipped fruits) exhibit catastrophic overconfidence, mistakenly classifying adulterated commodities as "Fresh" at rates exceeding $30\%$.
2. **Hypothesis 2 (OOD Scoring Hierarchy):** Energy-based OOD scoring significantly outperforms Maximum Softmax Probability (MSP) and ODIN in separating condition-shift anomalies from natural organic decay, reducing FPR at 95% TPR by at least 15 percentage points.
3. **Hypothesis 3 (Dual-Gate Superiority):** Cascading an energy-based OOD filter (Gate 1) with class-conditional calibrated selective prediction (Gate 2) provides a Pareto-optimal operating curve on the Open-Set Classification Rate (OSCR) and Coverage-Risk trade-off compared to all single-stage baselines.

---

## 2. Experimental Data Partitioning & Protocols

To guarantee absolute scientific integrity and prevent target leakage, all methods are trained and tuned on an identical, strictly isolated primary source, and evaluated on identical external test distributions.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PRIMARY TRAINING & CALIBRATION POOL                   │
│               Kaggle Fresh/Rotten Base-Group Manifest V4.1             │
├────────────────────────────────────────────────────────────────────────┤
│ • Training Split (N = 1,057 raw screenshots, is_raw=1, 6 classes)      │
│   → Feature extraction & representation learning                       │
│ • Validation Split (N = 227 raw screenshots, is_raw=1, 6 classes)      │
│   → Hyperparameter tuning, CCTS calibration, threshold selection       │
│ • Primary In-Distribution Test Split (N = 227 raw screenshots)         │
│   → Closed-set reference accuracy & in-distribution calibration        │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL EVALUATION BENCHMARKS                    │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 1: Covariate Shift on Knowns (ID Shift)                           │
│   • FruitVision Fresh & Rotten Apple/Banana/Orange (N = 4,185)         │
│   • Sultana Fresh & Rotten Apple/Banana/Orange (N = 1,200)             │
│   → Metric: Known Macro-F1 under camera, lighting, and origin shifts   │
│                                                                        │
│ TIER 2: Condition-Shift Safety OOD (Adulteration Anomalies)            │
│   • FruitVision Formalin-mixed Apple/Banana/Orange (N = 1,950)         │
│   • ToxiFruit Formalin-treated Apple/Malta/Banana (N = 2,700)          │
│   → Metric: OOD AUROC, FPR95, Unknown False Acceptance Rate (UFAR)     │
│                                                                        │
│ TIER 3: Semantic-Shift Species OOD (Unseen Fruit Varieties)            │
│   • FruitVision Unseen Species (Grape, Mango; N = 4,019)               │
│   • Sultana Unseen Species (Grape, Guava, Jujube, etc.; N = 2,000)     │
│   → Metric: Open-Set Classification Rate (OSCR), Semantic Rejection    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Evaluated Baselines & Implementation Specifications

All baselines utilize the **identical sealed Model B MobileNetV2 backbone** (or identically trained EfficientNetB0 / ResNet50 backbones) to ensure that performance deltas reflect the decision scoring rule rather than backbone capacity discrepancies.

### 3.1 Baseline 1: Maximum Softmax Probability (MSP) (Hendrycks & Gimpel 2017)
- **Scoring Function:** $S(x) = \max_{k \in \{1, \dots, K\}} \frac{\exp(z_k(x))}{\sum_j \exp(z_j(x))}$
- **Rejection Criterion:** Reject if $S(x) < \tau_{\text{MSP}}$.

### 3.2 Baseline 2: ODIN (Liang et al. 2018)
- **Hyperparameters:** Temperature $T_{\text{ODIN}} = 1000$; perturbation magnitude $\epsilon = 0.0014$.
- **Scoring Function:** Temperature-scaled softmax on adversarial gradient-perturbed input $\tilde{x}$.

### 3.3 Baseline 3: Energy-Based OOD Detection (Liu et al. 2020)
- **Hyperparameters:** Temperature $T_{\text{energy}} = 1.0$.
- **Scoring Function:** $S(x) = T_{\text{energy}} \cdot \log \sum_{k=1}^K \exp(z_k(x) / T_{\text{energy}})$.
- **Rejection Criterion:** Reject if $S(x) < \gamma_{\text{energy}}$.

### 3.4 Baseline 4: Feature-Space Mahalanobis Detector (Lee et al. 2018)
- **Feature Extraction:** Penultimate layer global average pooling vectors $f(x) \in \mathbb{R}^{1280}$.
- **Centroids & Covariance:** Empirical class means $\mu_k$ and tied regularized covariance $\Sigma + 10^{-4} I$.
- **Scoring Function:** $S(x) = - \min_k (f(x) - \mu_k)^T \Sigma^{-1} (f(x) - \mu_k)$.

### 3.5 Baseline 5: OpenMax (Bendale & Boult 2016)
- **Hyperparameters:** Tail size $\eta = 20$; alpha rank $\alpha = 3$.
- **Weibull Fitting:** Fitted per class on Euclidean distances to Mean Activation Vectors (MAVs).
- **Scoring Function:** $S(x) = 1 - p_0(x)$ (probability of belonging to known classes).

### 3.6 Proposed Method: Dual-Gate Risk-Aware Screening
- **Gate 1:** Free Energy Filter ($T=1.0$, threshold $\gamma_{\text{OOD}}$ tuned for $95\%$ In-Distribution TPR on validation set).
- **Gate 2:** Class-Conditional Temperature Scaling (CCTS) with selective threshold $\tau_{\text{cov}}$ tuned for target residual risk $\le 2\%$.

---

## 4. Mathematical Definitions of Evaluation Metrics

Every evaluation metric is formally defined below to prevent ambiguity or inflated reporting:

### 4.1 Known-Class Macro-Averaged F1 (Macro-F1)
Evaluates classification quality across the $K=6$ known classes on accepted samples:
$$\text{Macro-F1} = \frac{1}{K} \sum_{k=1}^K \frac{2 \cdot P_k \cdot R_k}{P_k + R_k}$$
where $P_k$ and $R_k$ are precision and recall for class $k \in \mathcal{Y}_{\text{in}}$.

### 4.2 OOD Area Under the ROC Curve (OOD AUROC)
Area under the Receiver Operating Characteristic curve plotting True Positive Rate (TPR, accepting In-Distribution) against False Positive Rate (FPR, accepting Out-of-Distribution) across all possible threshold values $\tau \in (-\infty, \infty)$:
$$\text{AUROC} = \int_{-\infty}^\infty \text{TPR}(\tau) \cdot \text{FPR}'(\tau) \, d\tau$$
Threshold-independent metric ($0.50$ = random guess, $1.00$ = perfect OOD separation).

### 4.3 OOD Area Under the Precision-Recall Curve (OOD AUPR-In and AUPR-Out)
Area under the Precision-Recall curve. Crucial when test distributions have severe class imbalance between known and unknown instances:
$$\text{AUPR} = \int_0^1 \text{Precision}(R) \, dR$$
- **AUPR-In:** Treats In-Distribution as the positive class.
- **AUPR-Out:** Treats Out-of-Distribution (adulterated/unseen) as the positive class.

### 4.4 False Positive Rate at 95% True Positive Rate (FPR@95%TPR / FPR95)
The probability that an Out-of-Distribution sample is mistakenly accepted as In-Distribution when the threshold is set to accept $95\%$ of true In-Distribution samples:
$$\text{FPR95} = \text{FPR}(\tau^*) \quad \text{where } \tau^* = \inf \{ \tau \mid \text{TPR}(\tau) \ge 0.95 \}$$
Lower is strictly better ($0.0\%$ = optimal).

### 4.5 Open-Set Classification Rate (OSCR)
The foundational metric for Open-Set Recognition (Dhamija et al. 2020), which simultaneously evaluates correct classification of knowns and rejection of unknowns. It plots the **Correct Classification Rate (CCR)** on known classes against the **False Positive Rate (FPR)** on unknown classes:
$$\text{CCR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{in}} \mid \hat{y}(x) = y(x) \text{ and } S(x) \ge \tau\}|}{|\mathcal{D}_{\text{in}}|}$$
$$\text{FPR}_{\text{open}}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{out}} \mid S(x) \ge \tau\}|}{|\mathcal{D}_{\text{out}}|}$$
$$\text{OSCR} = \int_0^1 \text{CCR}(\tau) \, d\text{FPR}_{\text{open}}(\tau)$$

### 4.6 Unknown False Acceptance Rate (UFAR)
The proportion of unsafe/adulterated fruit samples that breach the rejection gates and are assigned to a known commercial class (especially "Fresh"):
$$\text{UFAR} = \frac{|\{x \in \mathcal{D}_{\text{cond}}^{\text{OOD}} \mid y^*(x) \ne \text{\textcircled{r}}\}|}{|\mathcal{D}_{\text{cond}}^{\text{OOD}}|}$$
In food safety inspection, this metric represents dangerous public health risk and must approach zero.

### 4.7 Known-Class Rejection Rate (KRR)
The proportion of benign In-Distribution fruits that are unnecessarily rejected or routed to secondary inspection:
$$\text{KRR} = \frac{|\{x \in \mathcal{D}_{\text{in}} \mid y^*(x) = \text{\textcircled{r}}\}|}{|\mathcal{D}_{\text{in}}|}$$
Represents operational packaging-line friction.

### 4.8 Coverage-Risk Curve (RC Curve) & Selective Risk
Following Geifman & El-Yaniv (2017), the **coverage** $\Phi(\tau)$ is the fraction of total samples accepted by the system:
$$\Phi(\tau) = \frac{1}{N} \sum_{i=1}^N \mathbf{1}\{y^*(x_i) \ne \text{\textcircled{r}}\}$$
The **selective risk** $R(\tau)$ is the empirical error on accepted samples:
$$R(\tau) = \frac{\sum_{i=1}^N \ell(y_i, y^*(x_i)) \cdot \mathbf{1}\{y^*(x_i) \ne \text{\textcircled{r}}\}}{\sum_{i=1}^N \mathbf{1}\{y^*(x_i) \ne \text{\textcircled{r}}\}}$$
The curve plots $R(\tau)$ as a function of $\Phi(\tau)$ from full coverage ($\Phi=1.0$) down to selective abstention ($\Phi \to 0$).

### 4.9 Probability Calibration (ECE & Brier Score)
- **Expected Calibration Error (ECE):**
  $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
  computed across $M=10$ equal-width probability bins.
- **Brier Score:**
  $$\text{Brier} = \frac{1}{N} \sum_{i=1}^N \sum_{k=1}^K (\hat{p}_k(x_i) - \mathbf{1}\{y_i = k\})^2$$

---

## 5. Statistical Rigor Protocol

1. **Non-Parametric Bootstrap Confidence Intervals:** All reported metrics (Macro-F1, AUROC, FPR95, OSCR, ECE) must include $95\%$ bootstrap confidence intervals computed over $B=1,000$ resamples:
   $$\text{CI}_{95\%} = [\hat{\theta}^*_{0.025}, \hat{\theta}^*_{0.975}]$$
2. **Significance Testing:** Paired comparisons between Dual-Gate and baselines must report two-sided Wilcoxon signed-rank test $p$-values.
3. **No Test-Set Snooping:** Rejection thresholds ($\gamma_{\text{OOD}}$, $\tau_{\text{cov}}$) are locked on the Kaggle validation set before running inference on FruitVision, ToxiFruit, or Sultana. Zero post-hoc threshold adjustment is permitted.

