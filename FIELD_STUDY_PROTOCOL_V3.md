# Prospective Field-Validation Protocol (V3)

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Integrity Auditor:** Lead Scientific Integrity Engineer  
**Document ID:** `FIELD_STUDY_PROTOCOL_V3.md`  
**Execution Timestamp:** 2026-11-09  
**Git Branch:** `remediation/scientific-audit-repair`  
**Supersedes:** `FIELD_STUDY_PROTOCOL.md` and `FIELD_PROTOCOL_RECONCILIATION.md`  
**Registration Status:** **UNREGISTERED PROSPECTIVE PROTOCOL** (Not yet deposited in public trial registries)  
**Empirical Field Data Census:** **$N = 0$** (No field observations completed; protocol is prospective)

---

## 1. Executive Summary & Forensic Corrections

Reviewers 1, 2, and 3 noted that the original submitted paper lacked empirical field validation, presenting repository-level benchmark metrics as supply-chain decision proof. While prospective field studies were outlined in earlier drafts, previous documentation contained conflicting sample sizes ($N=120$ vs $N=400$), lacked an accounting for destructive firmness testing, proposed crops not supported by the vision model (mangoes), and cited fabricated references for clustering coefficients.

This authoritative document establishes a reconciled, statistically sound prospective protocol designed for execution in harvest seasons 2026–2027.

---

## 2. Crop Selection & Model Compatibility

The current AgriRoute vision system is trained, calibrated, and benchmarked exclusively on three produce types:
1. **Apples** (*Malus domestica*)
2. **Bananas** (*Musa acuminata*)
3. **Oranges** (*Citrus sinensis*)

### 2.1 Formal Exclusion of Mangoes from Phase 1
Earlier drafts suggested including mangoes (*Mangifera indica*). However:
- The vision backbone contains zero training weights or label mappings for mangoes.
- Evaluating mangoes without prior transfer learning and benchmark validation violates scientific integrity guidelines.
- **Protocol Mandate:** The Phase 1 field validation is strictly restricted to **commercial banana and orange transit corridors**. Mangoes are formally excluded until a dedicated six-class mango training and OOD validation program is completed.

---

## 3. Statistical Power & Sample Size Justification

### 3.1 Primary Objective & Hypothesis
- **Primary Outcome:** Commercial arrival quality grade (binary classification: *Grade A/B Marketable* vs. *Downgraded/Spoiled* requiring sorting or distress sale).
- **Primary Hypothesis ($H_1$):** Dispatch visual defect score ($\text{VDS}_{\text{uncal}}$) combined with transit exposure heuristic ($\text{TSI}_{\text{proto}}$) significantly predicts arrival spoilage odds above route duration alone:
  $$\operatorname{logit}\left(P(\text{Spoilage}_{ij} = 1)\right) = \beta_0 + \beta_1 \cdot \text{Duration}_j + \beta_2 \cdot \text{VDS}_{ij} + \beta_3 \cdot \text{TSI}_j + u_j$$
  where $i$ indexes individual fruit specimens and $j$ indexes shipment consignments ($u_j \sim \mathcal{N}(0, \sigma_u^2)$).

### 3.2 Clustered Shipment Model & Variance Inflation Factor
Specimens traveling in the same vehicle share environmental exposures (ambient heat, rough roads, driver delays), creating intra-cluster correlation.
- **Number of Shipments (Clusters, $K$):** $K = 40$ commercial haulage trips.
- **Tracked Specimens per Shipment ($m$):** $m = 10$ tagged specimens.
- **Total Tracked Cohort ($N$):** $N = K \times m = 40 \times 10 = 400$ specimens.
- **Intraclass Correlation Coefficient ($\rho$):** Estimated at $\rho = 0.12$ based on empirical post-harvest literature for refrigerated and ventilated horticultural transit (e.g., Jedermann et al., 2014; Defraeye et al., 2016).
- **Design Effect / Variance Inflation Factor (VIF):**
  $$\text{VIF} = 1 + (m - 1)\rho = 1 + (10 - 1)(0.12) = 1 + 1.08 = 2.08$$
- **Effective Sample Size ($N_{\text{eff}}$):**
  $$N_{\text{eff}} = \frac{N}{\text{VIF}} = \frac{400}{2.08} \approx 192 \text{ independent observations}$$

### 3.3 Power Calculation
Assuming a baseline arrival spoilage rate of $15\%$ in regional ambient logistics and an anticipated odds ratio $\text{OR} \ge 2.2$ per standard-deviation increase in combined risk index, an effective sample size of $N_{\text{eff}} = 192$ achieves **$>85\%$ statistical power** at a two-sided significance level of $\alpha = 0.05$. Accounting for a conservative $5\%$ specimen tag loss during transit, $N=400$ specimens across $K=40$ shipments provides robust statistical coverage.

---

## 4. Sampling Strategy & Destructive Measurement Separation

A critical flaw in earlier drafts was prescribing destructive penetrometer firmness testing on the same individual fruit at both dispatch and arrival. 

To resolve this physical impossibility, the sampling framework partitions consignments into two distinct cohorts:

```
Consignment Lot (100+ crates)
 ├── Cohort 1: Longitudinal Tracked Cohort (N=10 per shipment, 400 total)
 │    ├── Non-destructive individual RFID/QR labeling
 │    ├── Dispatch High-Res RGB Imaging (MobileNetV2 grading)
 │    ├── Continuous transit exposure (temperature/humidity logger)
 │    └── Arrival High-Res RGB Imaging & Visual Inspection
 │
 └── Cohort 2: Sacrificial Baseline Cohort (N=5 per shipment, 200 total)
      ├── Sampled at dispatch from the identical grower batch
      ├── Immediate destructive digital penetrometer testing (flesh firmness in N)
      ├── Immediate destructive digital refractometer testing (Total Soluble Solids, °Brix)
      └── Establishes lot-level baseline physiological maturity without harming Cohort 1
```

### 4.1 Cohort 1: Non-Destructive Longitudinal Tracking ($N=400$)
- **Lot Identification:** Each specimen is labeled with a food-safe, tamper-evident QR code tag on an elastic pedicel band.
- **Dispatch Grading:** Standardized lightbox photograph ($224 \times 224$ crop) scored via AgriRoute edge inference; visual inspection by trained agricultural extension officer.
- **Transit Exposure:** Consignment equipped with an autonomous multi-sensor data logger (Sensirion SHT31, logging temperature $\pm 0.2^\circ\text{C}$ and relative humidity $\pm 2\%$ at 5-minute intervals).
- **Arrival Grading:** Re-photographed under identical lightbox geometry; independent post-harvest quality assessment by a receiving wholesale grader blinded to dispatch predictions.

### 4.2 Cohort 2: Sacrificial Baseline Cohort ($N=200$)
- $5$ fruit per shipment selected randomly from the same packing crate at dispatch.
- **Flesh Firmness:** Measured across three equatorial points using an FT-327 digital penetrometer ($8\text{ mm}$ probe for apples, $11\text{ mm}$ probe for citrus).
- **Soluble Solids Content (SSC):** Homogenized juice extracted and analyzed via Atago PAL-1 digital refractometer ($^\circ\text{Brix} \pm 0.1$).

---

## 5. Field Study Limitations & Honest Disclosures

1. **Unregistered Status:** Because this protocol has not yet been deposited in a public registry (such as OSF Registries), it is explicitly declared as an **Unregistered Prospective Protocol**.
2. **Current Observation Count:** The revised paper will explicitly state: *"Field validation is currently prospective ($N=0$ empirical observations). Results reported in this paper reflect laboratory benchmark and external open-access OOD datasets."*
3. **Logistical Constraints:** The study relies on cooperating packhouses and haulage operators in Maharashtra and Gujarat, subject to seasonal crop availability.

