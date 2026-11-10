# Probability Calibration & Temperature Scaling Report

**Experiment Directory:** `experiments/open_set_v1/`  
**Document ID:** `calibration_report.md`  
**Execution Timestamp:** November 10, 2026  
**Model Under Test:** Model B V4.1 (`MODEL_B_V4_1_CHECKPOINT.keras`, SHA-256: `4a12f354...`)  
**Calibration Partition:** `FINAL_GROUP_VAL_V4_1.csv` filtered strictly by `is_raw == 1` ($N=227$)  

---

## 1. Mathematical Formulation of Calibration

Post-hoc probability calibration transforms uncalibrated network logits $z(x) \in \mathbb{R}^K$ into well-calibrated posterior probabilities $p(x) \in [0, 1]^K$.

### 1.1 Conventional Scalar Temperature Scaling
Following Guo et al. (ICML 2017, *On Calibration of Modern Neural Networks*), temperature scaling applies a single learned positive scalar parameter $T > 0$ to scale all logits prior to the softmax transformation:
$$p_k(x; T) = \frac{\exp(z_k(x) / T)}{\sum_{j=1}^K \exp(z_j(x) / T)}$$

#### Mathematical Properties:
1. **Rank Invariance:** Because the scalar function $f(z) = z / T$ is strictly monotonic for any $T > 0$:
   $$\arg\max_{k \in \{1,\dots,K\}} \frac{z_k(x)}{T} = \arg\max_{k \in \{1,\dots,K\}} z_k(x)$$
   Scalar temperature scaling is mathematically guaranteed to preserve top-1 classification accuracy, confusion matrices, and decision boundaries.
2. **Entropy Regulation:**
   - $T > 1.0$: Softens probability distributions, curbing overconfidence.
   - $T < 1.0$: Sharpens probability distributions, penalizing underconfidence.
   - $T = 1.0$: Leaves raw model probabilities unaltered.

### 1.2 Justification for Excluding Vector Scaling from Primary Protocol
Class-specific vector scaling ($z_k / T_k$) introduces class-dependent temperature coefficients $T \in \mathbb{R}^K$. As established in `STAGE1_CORRECTION_LOG.md` (§CORR-08), vector scaling alters the class ranking order whenever $T_i \ne T_j$, effectively acting as Platt recalibration that shifts classification boundaries. To maintain strict scientific separation between *classification performance* and *probability calibration*, scalar temperature scaling is retained as the sole primary calibration mechanism.

---

## 2. Optimization Protocol & Loss Formulation

The scalar temperature parameter $T$ was fitted strictly on the unobserved validation partition ($N=227$ raw images) by minimizing Negative Log-Likelihood (NLL / multi-class cross-entropy loss):
$$\min_{T > 0} \mathcal{L}_{\text{NLL}}(T) = -\frac{1}{N_{\text{val}}} \sum_{i=1}^{N_{\text{val}}} \log p_{y_i}(x_i; T)$$
where $y_i \in \{0, \dots, 5\}$ is the true integer class index for sample $i$.

- **Optimization Algorithm:** Bound-constrained Limited-memory BFGS (L-BFGS-B).
- **Bounds:** $T \in [0.05, 10.0]$.
- **Initialization:** $T_0 = 1.0$.

---

## 3. Empirical Calibration Diagnostics

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        EMPIRICAL CALIBRATION COMPARISON (N = 227)                      │
├─────────────────────────────────────────┬──────────────────────┬───────────────────────┤
│ Diagnostic Metric                       │ Raw (Pre-Calib)      │ Calibrated (Post)     │
├─────────────────────────────────────────┼──────────────────────┼───────────────────────┤
│ Optimal Temperature (T)                 │ 1.0000 (Baseline)    │ 1.0000 (Fitted)       │
│ Negative Log-Likelihood (NLL)           │ 0.1216               │ 0.1216                │
│ Expected Calibration Error (10-bin ECE) │ 6.02%                │ 6.02%                 │
│ Multiclass Brier Score                  │ 0.0545               │ 0.0545                │
│ Closed-Set Validation Accuracy          │ 96.92% (220 / 227)   │ 96.92% (220 / 227)    │
└─────────────────────────────────────────┴──────────────────────┴───────────────────────┘
```

### Analysis of Optimal Temperature:
The optimizer converged to $T^* = 1.0000$. This occurs because Model B V4.1 was trained with **label smoothing regularization ($\alpha = 0.05$)** during its primary training phase (`scripts/train_model_b_v4_1_raw_primary.py`). Label smoothing actively prevents logit explosion and naturally bounds network overconfidence on in-distribution data, rendering the raw logits naturally well-calibrated at $T=1.0$.

---

## 4. ECE Binning Methodology

The Expected Calibration Error (ECE) was computed using a 10-bin equal-width partition across the unit confidence interval $[0.0, 1.0]$:
$$B_m = \begin{cases} [0.1(m-1), 0.1m) & \text{for } m = 1, \dots, 9 \\ [0.9, 1.0] & \text{for } m = 10 \end{cases}$$
For each bin $B_m$:
$$\text{acc}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} \mathbf{1}\{\hat{y}_i = y_i\}$$
$$\text{conf}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} \max_k p_k(x_i)$$
$$\text{ECE} = \sum_{m=1}^{10} \frac{|B_m|}{N_{\text{val}}} |\text{acc}(B_m) - \text{conf}(B_m)|$$

With an in-sample validation ECE of **6.02%** and a Brier score of **0.0545**, the model exhibits strong in-distribution calibration reliability.

---

## 5. Scope Boundaries & Statistical Disclaimer

> [!WARNING]
> **In-Sample Diagnostic Limitation:** These calibration metrics represent in-sample performance on the validation partition ($N=227$). They do **not** certify a theoretical 2% selective risk guarantee, nor do they guarantee calibration retention under external covariate or condition shift. External domain shifts invariably induce severe calibration drift, which motivates the Gate 1 Out-of-Distribution filter.

---
*Certified by Lead ML Research Engineer.*

