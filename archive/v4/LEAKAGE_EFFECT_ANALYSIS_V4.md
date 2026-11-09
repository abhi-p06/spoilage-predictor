# Controlled Leakage Analysis & Statistical Uncertainty (V4)

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Reproducibility Auditor:** Lead Scientific Reproducibility Engineer  
**Document ID:** `LEAKAGE_EFFECT_ANALYSIS_V4.md`  
**Execution Timestamp:** 2026-11-09  
**Git Branch:** `remediation/v4-evidence-consistency`  
**Associated Analysis Script:** [`scripts/analyze_leakage_effect.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/analyze_leakage_effect.py)  
**Authoritative Raw Data:** [`experiments/group_leakage_study/LEAKAGE_EFFECT_ANALYSIS_DATA.json`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/LEAKAGE_EFFECT_ANALYSIS_DATA.json)

---

## 1. Context & Methodological Refinement

The initial AgriRoute revision asserted that data leakage caused a causal inflation of test accuracy, comparing Model A (historical random split: $94.43\%$) with Model B (group-aware split: $97.55\%$). As noted by independent reviewers, cross-partition comparisons cannot establish causal inflation because the underlying test partitions differ.

To resolve this question rigorously, we evaluated Model A on the **exact deduplicated historical test partition** ($N=2,045$), directly comparing performance on samples whose base-image family was present in training versus samples whose base-image family was absent from training.

---

## 2. Within-Test Performance Breakdown

In accordance with strict reproducibility mandates, the performance difference is formally described as:
$$\textbf{“Observed within-test performance difference between filename-derived seen and unseen families”}$$

### 2.1 Deduplicated Partition Census ($N=2,045$)
- **Total Deduplicated Test Images:** Exactly 2,045 unique physical files (from 4,090 nested rows).
- **Total Unique Filename-Derived Base Families:** Exactly 406 groups.
- **Seen Base Families in Training (Leaked):** 316 groups ($77.83\%$ of test groups), comprising 1,499 images ($73.30\%$).
- **Unseen Base Families in Training (Clean):** 90 groups ($22.17\%$ of test groups), comprising 546 images ($26.70\%$).

### 2.2 Observed Point Estimates

| Metric | Overall Test ($N=2,045$) | Seen Base Families ($N=1,499$) | Unseen Base Families ($N=546$) | **Observed Point Difference ($\Delta$)** |
| :--- | :---: | :---: | :---: | :---: |
| **Accuracy** | 94.43% | **95.20%** | 92.31% | **+2.89 percentage points** |
| **Balanced Accuracy** | 93.59% | **94.50%** | 90.42% | **+4.08 percentage points** |
| **Macro Precision** | 95.30% | **95.83%** | 93.42% | **+2.41 percentage points** |
| **Macro Recall** | 93.59% | **94.50%** | 90.42% | **+4.08 percentage points** |
| **Macro F1-Score** | 94.08% | **95.00%** | 90.84% | **+4.16 percentage points** |
| **Group-Weighted Accuracy** | 96.14% | **96.60%** | 94.54% | **+2.06 percentage points** |

---

## 3. Cluster-Bootstrap Uncertainty Analysis

Because transformed variants originating from the same screenshot share underlying features, standard sample-level confidence intervals underestimate variance. We performed **cluster bootstrapping** (1,000 resamples), resampling at the **base-family cluster level** ($G_{\text{seen}} = 316$, $G_{\text{unseen}} = 90$ clusters):

| Evaluation Quantity | Observed Point Estimate | 95% Cluster-Bootstrap Confidence Interval |
| :--- | :---: | :---: |
| **Seen Base Families Accuracy** | 95.20% | [92.89%, 97.21%] |
| **Unseen Base Families Accuracy** | 92.31% | [86.96%, 96.89%] |
| **$\Delta$ Accuracy (Seen $-$ Unseen)** | **+2.89%** | **[-2.26%, +8.94%]** |
| **$\Delta$ Macro F1 (Seen $-$ Unseen)** | **+4.16%** | **[-1.51%, +10.80%]** |

---

## 4. Scientific Discussion & Methodological Limitations

### 4.1 Statistical Uncertainty & Interval Spanning Zero
As shown in the table above, the $95\%$ cluster-bootstrap confidence interval for the accuracy difference is **$[-2.26\%, +8.94\%]$**, and for macro F1 is **$[-1.51\%, +10.80\%]$**. 

Because both intervals include zero, **the observed point difference of $+2.89\%$ accuracy cannot be described as a statistically established causal inflation**. 

### 4.2 Reasons for Interval Width
1. **Limited Number of Unseen Clusters:** In the historical random split, $77.8\%$ of base families were scattered across splits, leaving only $G=90$ base families completely absent from training. This small cluster count limits statistical power.
2. **Class-Specific Asymmetry:** As detailed below, the drop is heavily concentrated in citrus, while bananas and apples remained robust.

### 4.3 Class-Wise Vulnerability
Inspection of class-specific F1 scores reveals that citrus classification suffered dramatically on unseen base families:

| Class Name | Seen F1-Score | Unseen F1-Score | Class F1 Delta ($\Delta$) | Support (Seen / Unseen) |
| :--- | :---: | :---: | :---: | :---: |
| `fresh_apple` | 0.9442 | 0.9524 | $+0.0082$ | 205 / 109 |
| `fresh_banana` | 0.9920 | 0.9885 | $-0.0035$ | 251 / 44 |
| **`fresh_orange`** | **0.9128** | **0.7358** | **$-0.1770$ ($-17.7\%$)** | **212 / 67** |
| `rotten_apple` | 0.9337 | 0.9348 | $+0.0011$ | 313 / 129 |
| `rotten_banana` | 0.9948 | 0.9920 | $-0.0028$ | 289 / 125 |
| **`rotten_orange`** | **0.9224** | **0.8466** | **$-0.0758$ ($-7.58\%$)** | **229 / 72** |

This confirms that the model had memorized background surface artifacts for oranges, which failed on novel captures.

### 4.4 Mandate on Specimen Identity
Filename-derived groups reflect distinct screenshot captures. They do not constitute verified biological specimen tracking. The manuscript will describe groups strictly as **"filename-derived base-image families"** and avoid inferring physical specimen counts.

