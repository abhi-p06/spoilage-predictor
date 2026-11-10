# Dual-Gate Method Design: Asymmetric Risk-Aware Open-Set Fruit Quality Screening

**Role:** Principal Investigator & Theoretical Methodologist  
**Project:** AgriRoute / Spoilage-Predictor  
**Date:** November 10, 2026  
**Status:** Theoretical Specification & Algorithmic Formulation

---

## 1. Problem Formulation & Theoretical Foundations

### 1.1 The Operational Food-Safety Problem
In automated agricultural intake and cold-chain packhouse sorting, a machine vision system is deployed to classify arriving fruit lots into known commercial grades:
$$\mathcal{Y}_{\text{in}} = \{1, 2, \dots, K\}$$
where $K=6$ represents canonical organic states: `fresh_apple`, `fresh_banana`, `fresh_orange`, `rotten_apple`, `rotten_banana`, `rotten_orange`.

In the open real-world supply chain, inputs $x \in \mathcal{X}$ do not strictly originate from the training distribution $P_{\text{in}}(X)$. Instead, the incoming sample stream is a mixture:
$$x \sim (1 - \alpha - \beta) P_{\text{in}}^{\text{cov}}(X) + \alpha P_{\text{cond}}^{\text{OOD}}(X) + \beta P_{\text{sem}}^{\text{OOD}}(X)$$
where:
1. $P_{\text{in}}^{\text{cov}}$ represents **Known Classes under Covariate Domain Shift** (e.g., fresh apples from a different orchard, region, or camera setup).
2. $P_{\text{cond}}^{\text{OOD}}$ represents **Condition-Shift Safety Hazards** (e.g., apples subjected to illegal formalin/formaldehyde immersion or artificial preservatives).
3. $P_{\text{sem}}^{\text{OOD}}$ represents **Semantic-Shift Species Anomalies** (e.g., mangoes, guavas, or non-target produce).

### 1.2 The Asymmetric Loss Matrix
Standard multi-class accuracy assumes a symmetric zero-one loss $\ell(y, \hat{y}) = \mathbf{1}\{y \ne \hat{y}\}$. In food safety and supply chain logistics, this assumption is catastrophic.
Accepting a chemically adulterated or rotten fruit as "Fresh" exposes consumers to toxicity and triggers pathogen cross-contamination across entire refrigerated storage bays.

We define an **Asymmetric Food-Safety Cost Tensor** $C(y, \hat{y})$ with an explicit abstention action $\hat{y} = \text{\textcircled{r}}$ (Reject / Route to Benchtop Inspection):

| True State $y$ | Predicted $\widehat{y} = \text{Fresh}$ | Predicted $\widehat{y} = \text{Rotten}$ | Predicted $\widehat{y} = \text{\textcircled{r}}$ (Abstain) |
| :--- | :---: | :---: | :---: |
| **Known Fresh** | $0$ | $C_{\text{waste}}$ | $C_{\text{inspect}}$ |
| **Known Rotten** | $C_{\text{contam}}$ | $0$ | $C_{\text{inspect}}$ |
| **Condition OOD (Adulterated)** | $\mathbf{C_{\text{hazard}}^{\text{fatal}}}$ | $C_{\text{hazard}}^{\text{med}}$ | $C_{\text{inspect}}$ |
| **Semantic OOD (Unseen Fruit)** | $C_{\text{mismatch}}$ | $C_{\text{mismatch}}$ | $C_{\text{inspect}}$ |

**Operational Cost Ordering:**
$$\mathbf{C_{\text{hazard}}^{\text{fatal}}} \gg C_{\text{contam}} > C_{\text{waste}} > C_{\text{inspect}} > 0$$

Under this cost structure, any system lacking an open-set rejection and abstention mechanism incurs unbounded operational risk.

---

## 2. Mathematical Architecture of the Dual-Gate Framework

```
                          [ Input Image x ]
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Feature Extractor     │
                     │ Backbone: f_θ(x) ∈ ℝᵈ │
                     └───────────────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Logit Layer: z(x) ∈ ℝᴷ│
                     └───────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
┌───────────────────────────────┐           ┌───────────────────────────────┐
│           GATE 1              │           │           GATE 2              │
│    Open-Set OOD Filter        │           │    Selective Abstention       │
│                               │           │                               │
│  S_energy(x) =                │           │  p̂_k(x) = σ(z_k / T_k)        │
│  T · log ∑ exp(z_k(x) / T)    │           │  c(x) = max_k p̂_k(x)          │
│                               │           │                               │
│  Decision: S_energy(x) ≥ γ    │           │  Decision: c(x) ≥ τ_cov       │
└───────────────────────────────┘           └───────────────────────────────┘
           │                                           │
           │ (Passes: In-Distribution Candidate)       │ (High Confidence)
           ▼                                           ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                          UNIFIED DECISION RULE                            │
│                                                                           │
│   y*(x) = argmax_k p̂_k(x)    IF [S_energy(x) ≥ γ] AND [c(x) ≥ τ_cov]      │
│   y*(x) = Ⓡ (Abstain / Inspect)   OTHERWISE                               │
└───────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Feature Representation & Logit Computation
Let $f_\theta: \mathcal{X} \to \mathbb{R}^d$ be a deep convolutional feature extractor (MobileNetV2, parameterized by weights $\theta$). The raw logit vector $z(x) \in \mathbb{R}^K$ is given by:
$$z_k(x) = w_k^T f_\theta(x) + b_k, \quad k \in \{1, \dots, K\}$$

### 2.2 Gate 1: Energy-Based Out-of-Distribution Rejection
Standard Maximum Softmax Probability (MSP):
$$S_{\text{MSP}}(x) = \max_k \frac{\exp(z_k(x))}{\sum_{j=1}^K \exp(z_j(x))}$$
fails on out-of-distribution inputs because the softmax normalization $\sum_j \exp(z_j)$ forces probabilities to sum to 1, yielding artificially high confidence on inputs located far from the training manifold.

Following Liu et al. (2020), we map logits to the Helmholtz Free Energy $E(x; T_{\text{energy}})$:
$$E(x; T_{\text{energy}}) = - T_{\text{energy}} \cdot \log \sum_{k=1}^K \exp\left(\frac{z_k(x)}{T_{\text{energy}}}\right)$$

We define the **Gate 1 OOD Acceptance Score** as the negative free energy:
$$S_{\text{energy}}(x) = - E(x; T_{\text{energy}}) = T_{\text{energy}} \cdot \log \sum_{k=1}^K \exp\left(\frac{z_k(x)}{T_{\text{energy}}}\right)$$

**Gate 1 Decision Rule:**
$$G_1(x) = \begin{cases} 1 & \text{if } S_{\text{energy}}(x) \ge \gamma_{\text{OOD}} \\ 0 & \text{if } S_{\text{energy}}(x) < \gamma_{\text{OOD}} \quad (\text{Reject as Open-Set Anomaly})\end{cases}$$
where threshold $\gamma_{\text{OOD}}$ is tuned strictly on the In-Distribution validation split to satisfy a pre-specified True Positive Rate constraint (e.g., $95\%$ in-distribution acceptance, $\text{TPR}=0.95$).

### 2.3 Gate 2: Class-Conditional Calibrated Selective Prediction
Samples that pass Gate 1 ($G_1(x)=1$) are verified to reside near the known manifold. However, near the decision boundary between known classes (e.g., borderline fresh vs early-stage rot), model predictions can be ambiguous.

To ensure risk-bounded decision-making, Gate 2 performs **Class-Conditional Temperature Scaling (CCTS)**:
$$\hat{p}_k(x) = \frac{\exp\left(\frac{z_k(x)}{T_k}\right)}{\sum_{j=1}^K \exp\left(\frac{z_j(x)}{T_j}\right)}, \quad k \in \{1, \dots, K\}$$
where vector $T = [T_1, \dots, T_K]^T \in \mathbb{R}_+^K$ is optimized via class-weighted negative log-likelihood on the validation partition to minimize Expected Calibration Error (ECE):
$$T^* = \arg\min_T \sum_{i=1}^{N_{\text{val}}} -\log \hat{p}_{y_i}(x_i; T)$$

The maximum calibrated posterior confidence is:
$$c(x) = \max_{k \in \{1, \dots, K\}} \hat{p}_k(x), \quad \hat{y}(x) = \arg\max_{k \in \{1, \dots, K\}} \hat{p}_k(x)$$

**Gate 2 Decision Rule:**
$$G_2(x) = \begin{cases} 1 & \text{if } c(x) \ge \tau_{\text{cov}} \\ 0 & \text{if } c(x) < \tau_{\text{cov}} \quad (\text{Abstain due to Boundary Uncertainty})\end{cases}$$

### 2.4 The Unified Dual-Gate Decision Function
Combining Gate 1 and Gate 2 yields the complete selective classification rule:
$$y^*(x) = \begin{cases} \hat{y}(x) & \text{if } G_1(x) = 1 \text{ AND } G_2(x) = 1 \\ \text{\textcircled{r}} & \text{otherwise (Reject / Route to Inspection)} \end{cases}$$

---

## 3. Alternative OOD Scoring Formulations for Gate 1 Comparison

To rigorously establish whether Free Energy is superior, we implement and benchmark four alternative scoring functions for Gate 1 under identical feature representations:

### 3.1 Maximum Softmax Probability (MSP) (Hendrycks & Gimpel 2017)
$$S_{\text{MSP}}(x) = \max_k \frac{\exp(z_k(x))}{\sum_j \exp(z_j(x))}$$

### 3.2 ODIN (Out-of-Distribution Detector for Neural Networks) (Liang et al. 2018)
Computes perturbed input $\tilde{x} = x - \epsilon \cdot \text{sign}\left(-\nabla_x \log \frac{\exp(z_{\hat{y}}(x)/T_{\text{ODIN}})}{\sum_j \exp(z_j(x)/T_{\text{ODIN}})}\right)$, and evaluates:
$$S_{\text{ODIN}}(x) = \max_k \frac{\exp(z_k(\tilde{x}) / T_{\text{ODIN}})}{\sum_j \exp(z_j(\tilde{x}) / T_{\text{ODIN}})}$$

### 3.3 Feature-Space Mahalanobis Distance (Lee et al. 2018)
Fits class-conditional empirical Gaussian centroids $\mu_k = \frac{1}{N_k} \sum_{i: y_i=k} f(x_i)$ and tied covariance matrix $\Sigma = \frac{1}{N} \sum_{k=1}^K \sum_{i: y_i=k} (f(x_i) - \mu_k)(f(x_i) - \mu_k)^T$.
$$S_{\text{Mahalanobis}}(x) = - \min_{k} (f(x) - \mu_k)^T \Sigma^{-1} (f(x) - \mu_k)$$

### 3.4 OpenMax (Bendale & Boult 2016)
Fits Weibull distributions $\mathcal{W}_k$ on the distances between training samples and Mean Activation Vectors (MAVs) $\mu_k^{\text{MAV}}$. Modifies raw activation vector $v(x) = z(x)$ to recalibrate probability of the "unknown class" $p_0(x)$:
$$p_0(x) = \frac{\exp(v_0(x))}{\exp(v_0(x)) + \sum_{k=1}^K \exp(v_k(x))}, \quad S_{\text{OpenMax}}(x) = 1 - p_0(x)$$

---

## 4. Brutally Honest Methodological Novelty Audit

### 4.1 What is NOT Novel
1. **Energy OOD is not novel:** Proposed by Liu et al. (NeurIPS 2020).
2. **Selective classification via confidence thresholding is not novel:** Established by El-Yaniv & Wiener (2010), Geifman & El-Yaniv (2017).
3. **Temperature scaling is not novel:** Formalized by Guo et al. (ICML 2017).
4. **Cascading two filters is not a novel fundamental algorithm:** Sequenced screening exists widely in medical diagnostics and fraud detection.

### 4.2 Where the Scientific & Practical Novelty Actually Resides
1. **First Asymmetric Cost-Sensitive Formulation for Perishable Post-Harvest Hazards:** Mapping the non-linear risk of food-safety contamination directly to dual-gate threshold optimization.
2. **First Benchmark of Open-Set Chemical Condition Shifts in Agricultural Produce:** Systematically discovering whether standard deep vision backbones overconfidently accept uncharacterized preservative-treated lots as fresh produce.
3. **Formal Disentanglement of Domain Covariate Shift from Open-Set Hazard Shift:** Demonstrating that models can maintain high coverage on out-of-domain natural fruits (FruitVision/Sultana Fresh/Rotten) while achieving near-zero acceptance of chemical anomalies.

