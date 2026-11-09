---
name: calibration-analysis
description: Assess model confidence calibration using Expected Calibration Error (ECE), Brier score, reliability diagrams, and implement post-hoc probability calibration techniques.
---

# Objective
Quantify and optimize the probability calibration of vision and sensor spoilage models. Ensure that predicted confidence scores reflect empirical ground-truth probabilities, which is crucial when feeding risks into the downstream routing cost function.

# Workflow

1. **Reliability Diagram Generation:**
   - Partition model predicted confidence scores $\hat{p} \in [0, 1]$ into $M = 10$ or $15$ equal-width bins $B_m$.
   - For each bin, compute:
     - Average Confidence: $\text{conf}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} \hat{p}_i$
     - Empirical Accuracy: $\text{acc}(B_m) = \frac{1}{|B_m|} \sum_{i \in B_m} \mathbf{1}(\hat{y}_i = y_i)$
   - Plot empirical accuracy vs. mean confidence against the ideal identity line ($y = x$).
2. **Compute Calibration Metrics:**
   - **Expected Calibration Error (ECE):**
     $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$$
   - **Maximum Calibration Error (MCE):**
     $$\text{MCE} = \max_{m \in \{1,\dots,M\}} |\text{acc}(B_m) - \text{conf}(B_m)|$$
   - **Brier Score:**
     $$\text{BS} = \frac{1}{N} \sum_{i=1}^N \sum_{k=1}^K (f_{ik} - y_{ik})^2$$
3. **Implement Post-Hoc Probability Calibration:**
   - **Temperature Scaling:** Learn scalar temperature parameter $T > 0$ on the validation set logits $\mathbf{z} / T$.
   - **Platt Scaling:** Fit a univariate logistic regression on raw model outputs.
   - **Isotonic Regression:** Fit a non-parametric monotonic step function.
4. **Evaluate Calibration Improvement:**
   - Re-evaluate ECE, MCE, and Brier score on held-out test data post-calibration.
   - Confirm that accuracy/AUC remains unchanged while ECE drops significantly.
5. **Report Calibration Parameters:**
   - Document optimal scaling parameters and calibration metrics in `research_memory/claims_evidence_ledger.md`.

