# Stage 4.0 Pre-Specified Threshold & Calibration Specification

**Document ID:** `STAGE4_THRESHOLD_CALIBRATION_SPEC.md`  
**Role:** Principal Investigator & Lead Methodologist  
**Execution Timestamp:** November 10, 2026  
**Status:** Pre-Locked Protocol Specification (Prior to External Test Unsealing)  
**Calibration Source:** Strictly `FINAL_GROUP_VAL_V4_1.csv` filtered by `is_raw == 1` ($N=227$)  

---

## 1. Cardinal Integrity Rules for Calibration

To ensure complete scientific objectivity and eliminate researcher degrees of freedom:
1. **Absolute Sealing of External Sets:** Under no circumstances shall thresholds, temperatures, hyperparameters, or shrinkage coefficients be tuned, adapted, or selected using FruitVision, ToxiFruit, Sultana, or primary test set observations.
2. **Pre-Locked Operating Points:** All operating thresholds must be locked *ex ante* using validation knowns prior to executing external inference.
3. **Prohibition of Post-Hoc Threshold Tuning:** Reporting results from thresholds cherry-picked after inspecting test performance is strictly prohibited.
4. **Fair Coverage-Matched Comparison:** All baseline detectors and the Dual-Gate cascade must be evaluated at standardized In-Distribution (ID) acceptance coverage levels to ensure fair comparative benchmarking.

---

## 2. Standardized Operating Points

In out-of-distribution (OOD) and open-set recognition (OSR) benchmarks, operating thresholds are established by fixing the True Positive Rate on known in-distribution data:
- **Primary Operating Point ($\tau_{95}$):** Calibrated to achieve exactly **95.0% ID acceptance coverage** on validation knowns (permitting an in-distribution false rejection / abstention rate of $\le 5.0\%$).
- **Secondary Operating Point ($\tau_{90}$):** Calibrated to achieve exactly **90.0% ID acceptance coverage** on validation knowns (permitting an in-distribution false rejection / abstention rate of $\le 10.0\%$).

Because $N_{\text{val}} = 227$ samples, the 5th percentile corresponds to sample rank $k = \lceil 227 \times 0.05 \rceil = 12$ rejected samples ($94.71\%$ empirical coverage), and the 10th percentile corresponds to sample rank $k = \lceil 227 \times 0.10 \rceil = 23$ rejected samples ($89.87\%$ empirical coverage).

---

## 3. Authoritative Locked Threshold Table

The following threshold values were computed strictly from [`experiments/open_set_v1/validation_scores.csv`](file:///Users/abby/Desktop/spoilage-predictor/experiments/open_set_v1/validation_scores.csv) and are **LOCKED** for all subsequent external evaluations:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PRE-LOCKED OPERATING THRESHOLDS TABLE                           │
├────┬────────────────────────┬──────────────────┬───────────────────┬───────────────────┤
│ ID │ Scorer / Baseline      │ Score Symbol     │ Primary Operating │ Secondary Oper.   │
│    │                        │                  │ Point (tau_95)    │ Point (tau_90)    │
├────┼────────────────────────┼──────────────────┼───────────────────┼───────────────────┤
│ 1  │ Maximum Softmax Prob.  │ S_MSP(x)         │ 0.702499          │ 0.794850          │
│ 2  │ Free Energy (ID Score) │ S_Energy(x)      │ 1.063041          │ 1.338210          │
│ 3  │ ODIN (T=1000, eps=0.0014) S_ODIN(x)       │ 0.167167          │ 0.167209          │
│ 4  │ Ledoit-Wolf Mahalanobis│ S_Maha(x)        │ -64.977946        │ -58.126742        │
│ 5  │ OpenMax (eta=20, alpha=2) S_OpenMax(x)    │ 0.779116          │ 0.840834          │
│ 6  │ Calibrated Confidence  │ S_Calib(x)       │ 0.702499          │ 0.794850          │
└────┴────────────────────────┴──────────────────┴───────────────────┴───────────────────┘
```

*Decision Rule for All Baselines:*
$$\text{Accept as Known ID if } S(x) \ge \tau; \quad \text{Reject / Abstain as Unknown if } S(x) < \tau$$

---

## 4. Dual-Gate Screening Cascade Specification

The Dual-Gate screening architecture cascades an OOD filter (Gate 1) with risk-sensitive selective classification (Gate 2).

### 4.1 Cascade Decision Rule
For an incoming input $x$:
1. **Gate 1 (Coarse OOD Rejection):**
   $$g_1(x) = \mathbf{1}\{ S_{\text{Energy}}(x) \ge \tau_{1} \}$$
   If $g_1(x) = 0$, immediately **Abstain / Route to Manual Safety Inspection** ($\hat{y} = \text{\textcircled{r}}$).
2. **Gate 2 (Calibrated Selective Acceptance):**
   If $g_1(x) = 1$, evaluate top-1 calibrated confidence:
   $$g_2(x) = \mathbf{1}\{ S_{\text{Calib}}(x) \ge \tau_{2} \}$$
   If $g_2(x) = 0$, **Abstain / Route to Benchtop Inspection** ($\hat{y} = \text{\textcircled{r}}$).
   If $g_2(x) = 1$, **Accept Classification** $\hat{y} = \arg\max_{k \in \{1,\dots,6\}} p_k(x)$.

### 4.2 Standardized Operating Combinations
To evaluate whether cascading yields a genuine Pareto improvement over single-stage filters, the cascade is evaluated under two pre-locked configurations:
- **Configuration Alpha (Balanced Gate):**
  - $\tau_1 = \tau_{95}^{\text{Energy}} = 1.063041$
  - $\tau_2 = \tau_{95}^{\text{Calib}} = 0.702499$
- **Configuration Beta (Conservative Gate):**
  - $\tau_1 = \tau_{90}^{\text{Energy}} = 1.338210$
  - $\tau_2 = \tau_{90}^{\text{Calib}} = 0.794850$

---

## 5. Statistical Power & Risk Certification Limitations

1. **Absence of Guaranteed Risk:** As proven in `STAGE1_CORRECTION_LOG.md` (§CORR-11), $N_{\text{val}} = 227$ yields an empirical 95% Clopper-Pearson binomial margin of $\pm 3.9\%$ around low error rates. The paper must not claim a "guaranteed $\le 2\%$ residual risk certificate".
2. **Full-Spectrum Reporting:** In addition to discrete operating points ($\tau_{95}, \tau_{90}$), the entire continuous coverage-risk trade-off curve across all coverage levels $c \in [0.10, 1.00]$ must be generated and reported.

---
*Specification Locked and Certified by Lead Methodologist.*

