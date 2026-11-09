---
name: statistical-reporting
description: Compute non-parametric bootstrap confidence intervals, hypothesis test p-values, effect sizes, and format standardized statistical tables for publication.
---

# Objective
Calculate and format rigorous statistical metrics for all empirical claims in the AgriRoute manuscript. Eliminate bare point estimates by accompanying every metric with 95% confidence intervals, sample sizes, and hypothesis testing.

# Workflow

1. **Bootstrap Confidence Interval Computation:**
   - For all reported test set metrics (Accuracy, Macro F1, Precision, Recall, AUC, Brier Score, ECE):
     - Perform non-parametric bootstrap resampling ($B = 1,000$ iterations).
     - Compute the empirical percentile interval ($2.5\%$ to $97.5\%$) to obtain the $95\%$ Confidence Interval:
       $$\text{Metric} \pm \text{CI}_{95\%} \quad [\text{Lower}, \text{Upper}]$$
2. **Paired Statistical Significance Testing:**
   - **For Classification Models (MobileNet vs. ResNet vs. EfficientNet):**
     - Conduct McNemar's test for paired binary / multi-class classification outcomes on the exact test sample cohort.
     - Report test statistic ($\chi^2$), degrees of freedom ($df$), and $p$-value.
   - **For Routing Algorithms (Static vs. Dynamic / Ablations):**
     - Conduct Wilcoxon signed-rank test on paired route costs and spoilage loss across simulated delivery trips.
     - Report $W$-statistic, standardized $Z$-score, and two-tailed $p$-value.
3. **Effect Size Estimation:**
   - Report Cohen's $d$ or Rank-Biserial Correlation ($r$) alongside $p$-values to communicate practical effect magnitude.
4. **Multiple Testing Correction:**
   - Apply Benjamini-Hochberg False Discovery Rate (FDR) or Bonferroni adjustments when testing multiple model pairs or ablation configurations.
5. **Format Standardized Academic Tables:**
   - Format numbers cleanly: metrics to 3 decimal places (e.g., $0.942 \pm 0.008$), $p$-values formatted as $p < 0.001$ or exact values.
   - Update `research_memory/claims_evidence_ledger.md`.

