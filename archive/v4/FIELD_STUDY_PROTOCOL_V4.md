# Observational Prospective Cohort Field Study Protocol (V4)

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Reproducibility Auditor:** Lead Scientific Reproducibility Engineer  
**Document ID:** `FIELD_STUDY_PROTOCOL_V4.md`  
**Execution Timestamp:** 2026-11-09  
**Git Branch:** `remediation/v4-evidence-consistency`  
**Design Category:** **Observational Prospective Clustered Cohort Study (Unregistered)**  
**Current Empirical Observations:** **$N = 0$** (Field study is prospective; zero field data collected to date)  
**Associated Power Analysis Script:** [`scripts/calculate_field_study_power.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/calculate_field_study_power.py)  
**Statistical Calculation Output:** [`experiments/group_leakage_study/FIELD_STUDY_POWER_CALCULATION.json`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/FIELD_STUDY_POWER_CALCULATION.json)

---

## 1. Executive Summary & Protocol Architecture

To address Reviewers 1, 2, and 3 regarding the absence of empirical field validation, AgriRoute outlines a comprehensive, statistically powered, observational prospective cohort protocol. 

The protocol resolves the physical conflict between non-destructive longitudinal imaging and destructive flesh firmness/Brix testing by partitioning consignments into two distinct cohorts:

```
Total Specimen Collection: 600 Fruits across 40 Shipments
 ├── 1. Longitudinal Tracked Cohort: 40 shipments × 10 fruits = 400 Tracked Fruits
 │    ├── Non-destructive individual QR/RFID pedicel tags
 │    ├── Dispatch High-Res RGB Lightbox Photograph (MobileNetV2 VDS_uncal)
 │    ├── Continuous Transit Exposure (Sensirion SHT31 logger: Temp/Humidity)
 │    └── Arrival High-Res RGB Lightbox Photograph & Blinded Wholesale Quality Grade
 │
 └── 2. Sacrificial Baseline Cohort: 40 shipments × 5 fruits = 200 Sacrificial Fruits
      ├── Sampled at dispatch from the identical crate/grower lot
      ├── Destructive Digital Penetrometer Testing (Flesh Firmness in N)
      ├── Destructive Digital Refractometer Testing (Total Soluble Solids, °Brix)
      └── Establishes baseline physiological maturity without damaging Cohort 1
```

---

## 2. Crop Scope & Model Compatibility

The AgriRoute vision model is fine-tuned and validated exclusively on:
1. **Apples** (*Malus domestica*)
2. **Bananas** (*Musa acuminata*)
3. **Oranges** (*Citrus sinensis*)

### Phase 1 Crop Restriction
Earlier notes proposed including mangoes (*Mangifera indica*). Because the current vision model contains zero classes, weights, or calibration parameters for mangoes, **mangoes are formally excluded from Phase 1**. The pilot is strictly restricted to commercial banana, apple, and orange transit corridors in western India (Maharashtra and Gujarat).

---

## 3. Statistical Power & Sample Size Reassessment

### 3.1 Primary Objective & Endpoints
- **Primary Endpoint:** Commercial arrival quality status (binary: *Marketable Grade A/B* vs. *Downgraded/Spoiled* requiring sorting or price discount).
- **Primary Hypothesis ($H_1$):** Dispatch Visual Defect Score ($\text{VDS}_{\text{uncal}}$) and Transit Stress Index ($\text{TSI}_{\text{proto}}$) significantly predict arrival spoilage odds in a mixed-effects logistic regression:
  $$\operatorname{logit}\left(P(\text{Spoiled}_{ij} = 1)\right) = \beta_0 + \beta_1 \cdot \text{Duration}_j + \beta_2 \cdot \text{VDS}_{ij} + \beta_3 \cdot \text{TSI}_j + u_j$$
  where $u_j \sim \mathcal{N}(0, \sigma_u^2)$ represents shipment-level random intercepts ($j = 1 \dots 40$).

### 3.2 Executable Power Calculation & Findings
The power analysis was executed via [`scripts/calculate_field_study_power.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/calculate_field_study_power.py):
- **Nominal Tracked Sample Size ($N$):** $K = 40$ shipments $\times$ $m = 10$ fruits = $400$ specimens.
- **Specimen Attrition Allowance:** $5\%$ tag loss during transit $\to N_{\text{analyzable}} = 380$ specimens ($m_{\text{eff}} = 9.5$).
- **Intraclass Correlation Coefficient (ICC, $\rho$):** $\rho = 0.12$ based on empirical reefer transport studies (Jedermann et al., 2014; Defraeye et al., 2016).
- **Variance Inflation Factor (Design Effect):**
  $$\text{VIF} = 1 + (m_{\text{eff}} - 1)\rho = 1 + (9.5 - 1)(0.12) = 2.02$$
- **Effective Sample Size ($N_{\text{eff}}$):**
  $$N_{\text{eff}} = \frac{N_{\text{analyzable}}}{\text{VIF}} = \frac{380}{2.02} \approx 188.1 \text{ independent units}$$
- **Baseline Spoilage Prevalence ($p_0$):** $15\%$ in commercial ambient road transport.
- **Power Findings:**
  - For a binary comparison of high-risk vs. low-risk shipments at an Odds Ratio $\text{OR} = 2.2$ ($\alpha = 0.05$, two-sided), the statistical power is **$58.23\%$** (not $>85\%$, resolving the earlier unverified claim).
  - To achieve **$>80\%$ power** under this discrete threshold model, an effect size of **$\text{OR} \ge 2.8$** is required ($81.4\%$ power), or the shipment count must be expanded to **$K = 65$ shipments** ($80.5\%$ power at $\text{OR}=2.2$).
  - When analyzed as a **continuous multivariable mixed-effects model**, statistical power increases substantially ($>80\%$ across the continuous VDS risk gradient).

### 3.3 Sensitivity Grid (from `FIELD_STUDY_POWER_CALCULATION.json`)

| Odds Ratio ($\text{OR}$) | ICC ($\rho$) | VIF | Effective Sample ($N_{\text{eff}}$) | Statistical Power |
| :---: | :---: | :---: | :---: | :---: |
| 1.8 | 0.12 | 2.02 | 188.1 | 35.8% |
| 2.0 | 0.12 | 2.02 | 188.1 | 47.4% |
| **2.2 (Baseline)** | **0.12** | **2.02** | **188.1** | **58.2%** |
| 2.4 | 0.12 | 2.02 | 188.1 | 68.0% |
| 2.6 | 0.12 | 2.02 | 188.1 | 75.9% |
| **2.8** | **0.12** | **2.02** | **188.1** | **81.4%** |
| 2.2 | 0.05 | 1.425 | 266.7 | 73.5% |
| 2.2 | 0.20 | 2.70 | 140.7 | 46.2% |

---

## 4. Sampling & Laboratory Protocols

### 4.1 Cohort 1: Longitudinal Tracked Fruits ($N=400$)
1. **Identification:** Attached with food-safe QR code silicone wristbands to the pedicel.
2. **Dispatch Imaging:** Photographed under a portable calibrated LED lightbox ($224 \times 224$ crop, standardized distance of $30\text{ cm}$). Scored for $\text{VDS}_{\text{uncal}}$.
3. **In-Transit Logging:** Consignments carry a Sensirion SHT31 logger (recording temperature $\pm 0.2^\circ\text{C}$ and relative humidity $\pm 2\%$ every 5 minutes).
4. **Arrival Imaging & Blind Grading:** Re-photographed upon arrival at destination wholesale depot; graded by independent post-harvest inspectors blinded to dispatch scores.

### 4.2 Cohort 2: Sacrificial Baseline Fruits ($N=200$)
1. **Timing:** Sampled at dispatch from the identical crate lot.
2. **Flesh Firmness:** Measured across three equatorial locations using an FT-327 digital penetrometer ($8\text{ mm}$ stainless probe, recording maximum force in Newtons).
3. **Total Soluble Solids (TSS):** Juice pressed and read on an Atago PAL-1 digital refractometer ($^\circ\text{Brix} \pm 0.1$).

---

## 5. Absolute Scientific Honesty Statements

1. **Empirical Status:** Empirical field observations remain **$N = 0$**. 
2. **Study Type:** Formally declared as an **Unregistered Observational Prospective Cohort Study**.
3. **No Causal Claim:** Without randomized re-routing interventions, this protocol establishes observational association, not causal waste reduction.

