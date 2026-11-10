# Stage 4.0 Authoritative Metric Definitions & Statistical Standards

**Document ID:** `STAGE4_METRIC_DEFINITIONS.md`  
**Role:** Principal Investigator & Lead Methodologist  
**Execution Timestamp:** November 10, 2026  
**Status:** Pre-Locked Mathematical Metric Specification  

---

## 1. Cardinal Evaluation Rules

1. **Separation of Evaluation Populations:** All metrics must be computed and reported separately across:
   - Primary In-Distribution Known Test (Group A)
   - External Known-Class Domain Shift (Group B)
   - Condition-Shift Unknown (Group C)
   - Semantic-Shift Unknown (Group D)
   - Special Cultivar Transfer (Malta Groups M1 & M2)
   Under no circumstances shall Condition Shift and Semantic Shift be collapsed into an aggregated single metric.
2. **Standardized Positive Class Assignment:** To prevent ambiguity in Precision-Recall and ROC analysis, the positive class designation is explicitly locked for every metric below.

---

## 2. Mathematical Definitions of the Twelve Evaluation Metrics

### 2.1 Metric 1: Known-Class Macro-F1
- **Evaluation Population:** Known-class in-distribution or domain-shift samples ($x \in \mathcal{D}_{\text{in}}$, where $y \in \{0, \dots, 5\}$).
- **Mathematical Form:**
  $$\text{Macro-F1} = \frac{1}{K} \sum_{k=1}^K \frac{2 \cdot \text{Precision}_k \cdot \text{Recall}_k}{\text{Precision}_k + \text{Recall}_k}$$
  where $K=6$. Unweighted arithmetic mean across all 6 classes.

### 2.2 Metric 2: Balanced Accuracy
- **Evaluation Population:** Known-class samples ($x \in \mathcal{D}_{\text{in}}$).
- **Mathematical Form:**
  $$\text{Balanced Accuracy} = \frac{1}{K} \sum_{k=1}^K \frac{\text{TP}_k}{\text{TP}_k + \text{FN}_k}$$
  Equivalent to the macro-averaged recall across all known classes, eliminating class-imbalance bias.

### 2.3 Metric 3: Out-of-Distribution AUROC (Area Under the ROC Curve)
- **Evaluation Population:** Union of In-Distribution Knowns ($\mathcal{D}_{\text{in}}$) and Out-of-Distribution Unknowns ($\mathcal{D}_{\text{out}}$).
- **Binary Label Assignment:**
  - Positive Class ($y = 1$): Out-of-Distribution / Unknown Sample ($x \in \mathcal{D}_{\text{out}}$).
  - Negative Class ($y = 0$): In-Distribution / Known Sample ($x \in \mathcal{D}_{\text{in}}$).
- **Mathematical Form:**
  Given OOD detector score $S(x)$ (where lower score indicates higher anomaly likelihood):
  $$\text{AUROC} = \int_{0}^1 \text{TPR}(\tau) \, d(\text{FPR}(\tau))$$
  $$\text{TPR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{out}} : S(x) < \tau\}|}{|\mathcal{D}_{\text{out}}|}, \quad \text{FPR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{in}} : S(x) < \tau\}|}{|\mathcal{D}_{\text{in}}|}$$
  AUROC measures discrimination independent of any single operational threshold.

### 2.4 Metric 4: AUPR-OUT (Precision-Recall Area on OOD)
- **Positive Class:** Out-of-Distribution / Unknown ($y = 1$).
- **Mathematical Form:** Area under the Precision-Recall curve treating OOD as the target class:
  $$\text{AUPR-OUT} = \sum_{k} (R_k - R_{k-1}) P_k$$
  where $P = \frac{\text{TP}_{\text{OOD}}}{\text{TP}_{\text{OOD}} + \text{FP}_{\text{OOD}}}$ and $R = \frac{\text{TP}_{\text{OOD}}}{|\mathcal{D}_{\text{out}}|}$. Highly sensitive to false alarms on rare anomalies.

### 2.5 Metric 5: AUPR-IN (Precision-Recall Area on In-Distribution)
- **Positive Class:** In-Distribution / Known ($y = 1$).
- **Mathematical Form:** Area under the Precision-Recall curve treating In-Distribution as the target class. Essential when OOD samples outnumber ID samples.

### 2.6 Metric 6: FPR@95% ID Acceptance
- **Evaluation Population:** $\mathcal{D}_{\text{in}} \cup \mathcal{D}_{\text{out}}$.
- **Mathematical Form:** The False Positive Rate (proportion of OOD anomalies incorrectly accepted as In-Distribution) when the True Acceptance Rate on In-Distribution is fixed at exactly $95.0\%$:
  $$\tau_{95} = \sup \{ \tau : \frac{|\{x \in \mathcal{D}_{\text{in}} : S(x) \ge \tau\}|}{|\mathcal{D}_{\text{in}}|} \ge 0.95 \}$$
  $$\text{FPR@95} = \frac{|\{x \in \mathcal{D}_{\text{out}} : S(x) \ge \tau_{95}\}|}{|\mathcal{D}_{\text{out}}|}$$
  Lower values indicate superior real-world safety screening.

### 2.7 Metric 7: Open-Set Classification Rate (OSCR)
- **Evaluation Population:** $\mathcal{D}_{\text{in}} \cup \mathcal{D}_{\text{out}}$.
- **Reference:** Dhamija et al. (ECCV 2020).
- **Mathematical Form:** Plots Correct Classification Rate ($\text{CCR}$) on knowns against False Positive Rate ($\text{FPR}$) on unknowns as decision threshold $\tau$ varies:
  $$\text{CCR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{in}} : \hat{y}(x) = y(x) \land S(x) \ge \tau\}|}{|\mathcal{D}_{\text{in}}|}$$
  $$\text{FPR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{out}} : S(x) \ge \tau\}|}{|\mathcal{D}_{\text{out}}|}$$
  $$\text{OSCR} = \int_{0}^1 \text{CCR}(\tau) \, d(\text{FPR}(\tau))$$
  Unifies closed-set classification accuracy with open-set rejection capability.

### 2.8 Metric 8: Unknown False Acceptance Rate (UFAR)
- **Evaluation Population:** Unknowns ($x \in \mathcal{D}_{\text{out}}$).
- **Mathematical Form:**
  $$\text{UFAR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{out}} : S(x) \ge \tau\}|}{|\mathcal{D}_{\text{out}}|}$$
  Measures the operational leak rate of uncharacterized produce into standard packaging lines.

### 2.9 Metric 9: Unknown-to-Fresh False Acceptance Rate (UFAR-Fresh)
- **Evaluation Population:** Unknowns ($x \in \mathcal{D}_{\text{out}}$).
- **Mathematical Form:** The proportion of unknown adulterated or foreign samples accepted and specifically misclassified into a commercial "Fresh" category:
  $$\text{UFAR-Fresh}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{out}} : S(x) \ge \tau \land \hat{y}(x) \in \{\text{fresh\_apple}, \text{fresh\_banana}, \text{fresh\_orange}\}\}|}{|\mathcal{D}_{\text{out}}|}$$
  This is the primary catastrophic failure metric in agricultural food safety.

### 2.10 Metric 10: Known-Class Rejection Rate (KRR / Abstention Rate)
- **Evaluation Population:** Knowns ($x \in \mathcal{D}_{\text{in}}$).
- **Mathematical Form:**
  $$\text{KRR}(\tau) = \frac{|\{x \in \mathcal{D}_{\text{in}} : S(x) < \tau\}|}{|\mathcal{D}_{\text{in}}|}$$
  Measures the economic cost of unnecessary manual benchtop inspections on valid commercial fruit.

### 2.11 Metric 11: Coverage-Risk Curves & Selective Risk
- **Reference:** Geifman & El-Yaniv (NeurIPS 2017).
- **Mathematical Form:** For a coverage target $c \in (0, 1]$:
  $$\text{Coverage}(c) = \frac{|\{x : S(x) \ge \tau_c\}|}{N}$$
  $$\text{Selective Risk}(c) = \frac{1}{|\{x : S(x) \ge \tau_c\}|} \sum_{i : S(x_i) \ge \tau_c} \ell(y_i, \hat{y}_i)$$
  Plots error rate strictly on the accepted fraction of samples.

### 2.12 Metric 12: In-Sample Calibration (ECE & Multiclass Brier Score)
- **Expected Calibration Error:**
  $$\text{ECE} = \sum_{m=1}^{10} \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$$
- **Multiclass Brier Score:**
  $$\text{Brier} = \frac{1}{N} \sum_{i=1}^N \sum_{k=1}^K (p_{ik} - y_{ik})^2$$

---

## 3. Statistical Uncertainty & Confidence Interval Standards

1. **Continuous Metrics (AUROC, AUPR, OSCR):** Report 95% non-parametric bootstrap confidence intervals (1,000 iterations).
2. **Rare Catastrophic Events (UFAR-Fresh at low error rates):** Report exact Clopper-Pearson binomial confidence intervals:
   $$\text{CI}_{95\%} = \left[ B\left(\frac{\alpha}{2}; k, n-k+1\right), B\left(1 - \frac{\alpha}{2}; k+1, n-k\right) \right]$$
3. **Cluster Resampling Constraint:** Where acquisition batch or capture session metadata is unavailable, image-level bootstrap must be explicitly labeled as assuming sample exchangeability. Resamples must not be treated as independent degrees of freedom for hypothesis tests.

---
*Specification Locked and Certified by Lead Methodologist.*

