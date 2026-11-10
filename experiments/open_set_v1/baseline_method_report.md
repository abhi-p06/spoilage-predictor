# Baseline Method & Scoring Infrastructure Report

**Experiment Directory:** `experiments/open_set_v1/`  
**Document ID:** `baseline_method_report.md`  
**Execution Timestamp:** November 10, 2026  
**Model Under Test:** Model B V4.1 (`MODEL_B_V4_1_CHECKPOINT.keras`, SHA-256: `4a12f354...`)  
**Data Partitions Used:**
- Training ($N=1057$ raw images, `is_raw == 1`): Used for feature extraction, class centroids, Ledoit-Wolf covariance, and OpenMax MAVs/Weibull tail fitting.
- Validation ($N=227$ raw images, `is_raw == 1`): Used for ODIN validation checks, scalar temperature calibration, and score baseline assembly.
- External / Test Data: **Zero samples used.** Completely sealed.

---

## 1. Overview of Evaluated Baseline Scorers

To establish a rigorous, reproducible benchmark for post-harvest open-set fruit quality screening, five canonical out-of-distribution (OOD) / open-set recognition (OSR) scoring mechanisms were implemented.

All score functions are standardized such that:
$$\text{Higher Numerical Score } S(x) \implies \text{Greater In-Distribution (Known Class) Confidence}$$

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              BASELINE SCORER SUMMARY                                   │
├────┬────────────────────┬─────────────────────────────┬──────────────────┬─────────────┤
│ ID │ Scorer Name        │ Primary Mechanism           │ Data Source for  │ Parameter   │
│    │                    │                             │ Parameter Fit    │ Count       │
├────┼────────────────────┼─────────────────────────────┼──────────────────┼─────────────┤
│ A  │ MSP                │ Maximum Softmax Probability │ None (Zero-shot) │ 0           │
│ B  │ Energy             │ Helmholtz Free Energy       │ None (Zero-shot) │ 1 (T=1.0)   │
│ C  │ ODIN               │ Temp Scaling + Input Grad   │ Validation (eps) │ 2 (T, eps)  │
│ D  │ Mahalanobis (LW)   │ Centroid Dist + Covariance  │ Training (feats) │ 6 mu, 1 Cov │
│ E  │ OpenMax            │ MAVs + Weibull EVT Tails    │ Training (feats) │ 6 MAVs, 6 W │
└────┴────────────────────┴─────────────────────────────┴──────────────────┴─────────────┘
```

---

## 2. Detailed Mathematical Definitions & Implementation

### 2.1 Baseline A: Maximum Softmax Probability (MSP; Hendrycks & Gimpel, 2017)
- **Reference:** Dan Hendrycks and Kevin Gimpel. *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. ICLR 2017.
- **Mathematical Definition:**
  $$S_{\text{MSP}}(x) = \max_{k \in \{1,\dots,6\}} p_k(x) = \max_{k \in \{1,\dots,6\}} \frac{\exp(z_k(x))}{\sum_{j=1}^6 \exp(z_j(x))}$$
- **Direction:** $S_{\text{MSP}}(x) \in [1/6, 1.0]$. Higher values indicate higher ID confidence.
- **Fitted Parameters:** None. Directly evaluates the model's raw softmax distribution.

### 2.2 Baseline B: Energy-Based OOD Scoring (Liu et al., NeurIPS 2020)
- **Reference:** Weitang Liu, Xiaoyun Wang, John Owens, and Yixuan Li. *Energy-based Out-of-distribution Detection*. NeurIPS 2020.
- **Mathematical Definition:**
  The free energy of the input $x$ is defined as the negative log-partition function of the logits $z(x)$:
  $$E(x; T) = -T \cdot \log \sum_{k=1}^6 \exp\left(\frac{z_k(x)}{T}\right)$$
  Because lower physical energy corresponds to higher probability density under the Gibbs distribution, the In-Distribution confidence score is defined as the **negative energy**:
  $$S_{\text{Energy}}(x) = -E(x; T) = T \cdot \log \sum_{k=1}^6 \exp\left(\frac{z_k(x)}{T}\right)$$
- **Direction:** $S_{\text{Energy}}(x) \in (-\infty, \infty)$. Higher values represent higher In-Distribution confidence.
- **Fitted Parameters:** Temperature hyperparameter $T = 1.0$ (standard default in literature; does not require tuning on validation anomalies).

### 2.3 Baseline C: ODIN (Liang et al., ICLR 2018)
- **Reference:** Shiyu Liang, Yixuan Li, and R. Srikant. *Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks*. ICLR 2018.
- **Mathematical Definition:**
  ODIN applies temperature scaling $T_{\text{ODIN}}$ and small adversarial-like input perturbations to maximize the separation between ID and OOD samples:
  1. Input gradient computation:
     $$g(x) = \nabla_x \left( \max_{k \in \{1,\dots,6\}} \frac{z_k(x)}{T_{\text{ODIN}}} \right)$$
  2. Input perturbation:
     $$\widetilde{x} = \text{clip}\left( x - \epsilon_{\text{norm}} \cdot \text{sign}(-g(x)), -1.0, 1.0 \right)$$
  3. Perturbed score evaluation:
     $$S_{\text{ODIN}}(x) = \max_{k \in \{1,\dots,6\}} \frac{\exp(z_k(\widetilde{x}) / T_{\text{ODIN}})}{\sum_{j=1}^6 \exp(z_j(\widetilde{x}) / T_{\text{ODIN}})}$$
- **Direction:** $S_{\text{ODIN}}(x) \in [1/6, 1.0]$. Higher values indicate higher ID confidence.
- **Fitted Parameters:**
  - $T_{\text{ODIN}} = 1000.0$.
  - $\epsilon_{\text{norm}} = 0.0014$ (expressed in normalized $[-1.0, 1.0]$ model-input coordinates, equivalent to $0.0014 \times 127.5 \approx 0.178$ raw pixel units in $[0, 255]$).
  - Validation test on $N=10$ confirmed a monotonic positive perturbation gain ($+1.83 \times 10^{-7}$).

### 2.4 Baseline D: Ledoit-Wolf Regularized Mahalanobis Distance (Lee et al., NeurIPS 2018)
- **Reference:** Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin. *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. NeurIPS 2018.
- **Mathematical Definition:**
  Models the penultimate feature space $h(x) \in \mathbb{R}^{1280}$ as a mixture of class-conditional Gaussians with tied covariance:
  1. Class centroids computed strictly on training features ($N=1057$):
     $$\mu_k = \frac{1}{N_k} \sum_{i \in \mathcal{C}_k} h(x_i) \in \mathbb{R}^{1280}, \quad k \in \{0, \dots, 5\}$$
  2. Tied covariance with analytical Ledoit-Wolf shrinkage:
     $$\mathbf{\Sigma}_{\text{LW}} = (1 - \lambda^*) \mathbf{S} + \lambda^* \left(\frac{\text{tr}(\mathbf{S})}{D}\right) \mathbf{I}_{1280}$$
     where $\mathbf{S} = \frac{1}{N} \sum_{i} (h(x_i) - \mu_{y_i})(h(x_i) - \mu_{y_i})^T$ and $\lambda^* \in (0, 1)$.
  3. Minimum Mahalanobis distance:
     $$M(x) = \min_{k \in \{0,\dots,5\}} \sqrt{(h(x) - \mu_k)^T \mathbf{\Sigma}_{\text{LW}}^{-1} (h(x) - \mu_k)}$$
  4. In-Distribution Confidence Score:
     $$S_{\text{Maha}}(x) = -M(x)$$
- **Direction:** $S_{\text{Maha}}(x) \in (-\infty, 0]$. Higher values (closer to 0) indicate closer proximity to known class centroids (greater ID confidence).
- **Fitted Parameters (from Training Data):**
  - Six 1,280-dimensional centroid vectors $\mu_0, \dots, \mu_5$.
  - Regularized covariance matrix $\mathbf{\Sigma}_{\text{LW}} \in \mathbb{R}^{1280 \times 1280}$ with fitted shrinkage $\lambda^* = 0.097837$.
  - Inverted precision matrix $\mathbf{\Sigma}_{\text{LW}}^{-1} \in \mathbb{R}^{1280 \times 1280}$.

### 2.5 Baseline E: OpenMax (Bendale & Boult, CVPR 2016)
- **Reference:** Abhijit Bendale and Terrance E. Boult. *Towards Open Set Deep Networks*. CVPR 2016.
- **Mathematical Definition:**
  Applies Extreme Value Theory (EVT) to adjust class activation vectors and quantify probability of unknown classes:
  1. Mean Activation Vectors (MAVs):
     $$\mu_k = \frac{1}{|\mathcal{C}_k^{\text{correct}}|} \sum_{i \in \mathcal{C}_k^{\text{correct}}} h(x_i)$$
     computed across the 1,046 correctly classified training samples (98.96% training accuracy).
  2. Weibull Tail Fitting: For each class $k$, the Euclidean distances $\|h(x_i) - \mu_k\|_2$ of training samples are calculated. A two-parameter Weibull distribution is fitted to the largest $\eta = 20$ tail distances:
     $$W_k = \text{Weibull}(\text{shape}=\kappa_k, \text{scale}=\lambda_k)$$
  3. Outlier probability estimation for top $\alpha = 2$ classes:
     $$\omega_k(x) = \exp\left( - \left(\frac{\|h(x) - \mu_k\|_2}{\lambda_k}\right)^{\kappa_k} \right)$$
  4. Pseudo-activation for Unknown Class 0:
     $$v_0(x) = \sum_{k=1}^K z_k(x) (1 - \omega_k(x))$$
     Adjusted activations for known classes: $\hat{v}_k(x) = z_k(x) \omega_k(x)$.
  5. OpenMax probability distribution:
     $$p_{\text{openmax}}(k \mid x) = \frac{\exp(\hat{v}_k(x))}{\sum_{j=0}^K \exp(\hat{v}_j(x))}, \quad k \in \{0, 1, \dots, 6\}$$
  6. In-Distribution Confidence Score:
     $$S_{\text{OpenMax}}(x) = 1.0 - p_{\text{openmax}}(0 \mid x) = \sum_{k=1}^6 p_{\text{openmax}}(k \mid x)$$
- **Direction:** $S_{\text{OpenMax}}(x) \in [0.0, 1.0]$. Higher values represent lower unknown outlier probability.
- **Fitted Parameters (from Training Data):**
  - Six class MAVs $\mu_0, \dots, \mu_5 \in \mathbb{R}^{1280}$.
  - Six class Weibull models $(\kappa_k, \lambda_k)$:
    - Class 0 (`fresh_apple`): $\kappa = 9.8855, \lambda = 19.4079$
    - Class 1 (`fresh_banana`): $\kappa = 7.4435, \lambda = 21.1646$
    - Class 2 (`fresh_orange`): $\kappa = 25.3540, \lambda = 16.3487$
    - Class 3 (`rotten_apple`): $\kappa = 15.4995, \lambda = 19.9695$
    - Class 4 (`rotten_banana`): $\kappa = 17.8939, \lambda = 23.1288$
    - Class 5 (`rotten_orange`): $\kappa = 9.8020, \lambda = 20.8454$

---

## 3. Dual-Gate Screening Formulation

The proposed AgriRoute screening cascade operates as a two-stage filter:
- **Gate 1 (OOD Filter):** $S_{\text{Energy}}(x) \ge \tau_1$. Rejects general condition and semantic anomalies.
- **Gate 2 (Calibrated Selective Gate):** $S_{\text{Calibrated}}(x) \ge \tau_2$. Enforces risk-controlled abstention on accepted samples.

Both scores are pre-computed in `validation_scores.csv` to enable exhaustive threshold ablations without rerunning model inference.

---
*Certified by Lead ML Research Engineer.*

