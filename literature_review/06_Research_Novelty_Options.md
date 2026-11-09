# Research Novelty Options & Falsifiable Contribution Packages

> **Document:** `literature_review/06_Research_Novelty_Options.md`  
> **Auditor/Analyst:** AgriRoute Literature Specialist & Principal Investigator  
> **Scope:** Delineation of three distinct, rigorous, and defensible research contribution packages for the revised AgriRoute manuscript.

---

## Strategic Overview

Reviewers 1 and 2 explicitly challenged AgriRoute's novelty, questioning whether the paper represents anything more than an "engineering plumbing exercise combining standard MobileNetV2, an off-the-shelf BiLSTM, and Leaflet routing." 

To overcome this objection definitively, the revised paper must ground its novelty not in claiming to have invented a new deep learning layer from scratch, but in establishing a **rigorously formulated, empirical, and falsifiable scientific contribution**. Below are three alternative research contribution formulations for author selection.

---

## Contribution Package A: Closed-Loop Multi-Modal Risk Coupling in Perishable Agri-Logistics

### 1. What Existing Studies Already Do
- Computer vision studies (Gulzar, 2023; Chen et al., 2024; Zhang et al., 2024) evaluate fruit freshness at a single stationary inspection point (pack-house or farm gate) in total isolation from downstream logistics.
- Perishable vehicle routing literature (Li et al., 2026; Esteso et al., 2021; Pérez Lechuga et al., 2024) models vehicle dispatch under perishability using mathematical optimization (MILP, ACO), but assumes uniform, pristine initial quality ($V_0 = 1.0$) across all cargo.
- IoT tracking studies (Ali et al., 2023) monitor in-transit temperature without pre-dispatch visual inspection.

### 2. What Existing Studies Do NOT Establish
- No study has established how pre-dispatch visual freshness scores should quantitatively parameterize in-transit dynamic perishability decay functions.
- Existing systems cannot dynamically adjust in-transit rerouting decisions when initial produce quality varies across heterogeneous farm batches.

### 3. How AgriRoute Differs
AgriRoute formalizes a **closed-loop multi-modal coupling mechanism** where the pre-dispatch visual quality distribution directly modulates the time-dependent spoilage risk function $R_{\mathrm{transit}}(t)$ used by the dynamic routing and market selection engine. Initial latent visual degradation accelerates the effective kinetic shelf-life decay rate under in-transit thermal exposure.

### 4. What Experiment Proves the Difference
- **Experiment:** An empirical simulation across 20 diverse transit topologies comparing:
  - Baseline 1 (Decoupled SOTA): Stationary visual sorting + Standard static shortest-path routing.
  - Baseline 2 (Sensor-Only SOTA): Static initial quality ($V_0 = 1.0$) + In-transit temperature monitoring.
  - Proposed AgriRoute: Joint visual state + In-transit thermal exposure + Dynamic salvage rerouting.
- **Metric:** Total cargo economic loss (% salvage value preserved upon arrival) and delivery rejection frequency under unexpected cold-chain thermal abuse events. A statistically significant reduction ($p < 0.01$ via Wilcoxon signed-rank test) proves operational superiority.

### 5. What Evidence Falsifies the Novelty Claim
- If an empirical sensitivity sweep over the visual coupling parameter $\alpha$ shows that setting $\alpha = 0$ (sensor-only) yields identical economic salvage outcomes to joint coupling across all transit distances, the claim of multi-modal synergy is falsified.

---

## Contribution Package B: Uncertainty-Calibrated Edge Computer Vision with Selective Decision Deferral for Rural Food Supply Chains

### 1. What Existing Studies Already Do
- Standard agricultural computer vision models report high top-1 benchmark accuracy (94%–98%) on curated datasets, but rely on raw, uncalibrated softmax logits (Rizzo et al., 2023; Hassan et al., 2025).
- Studies universally ignore probability calibration error (ECE) and out-of-distribution confidence degradation.

### 2. What Existing Studies Do NOT Establish
- How uncalibrated neural overconfidence directly causes false-alarm route diversions and unnecessary financial loss in agricultural supply chains.
- How post-hoc calibration (Temperature Scaling) and selective prediction (abstention) perform when lightweight edge backbones are subjected to cross-dataset domain shifts in rural packing environments.

### 3. How AgriRoute Differs
AgriRoute integrates an **uncertainty-calibrated edge computer vision architecture** specifically optimized for rural food supply chains. By incorporating post-hoc Temperature Scaling and a selective classification boundary, AgriRoute maps raw visual logits into well-calibrated posterior probabilities ($ECE < 0.03$), automatically deferring ambiguous edge predictions to manual inspection while guaranteeing reliable probability inputs to downstream logistics cost functions.

### 4. What Experiment Proves the Difference
- **Experiment:** Reliability diagram evaluation and calibration assessment across MobileNetV2, EfficientNetB0, and ResNet50 on in-domain (Kaggle) and out-of-domain (external market) test partitions before and after temperature scaling.
- **Metric:** Expected Calibration Error (ECE) and Brier Score. Demonstrating a $> 60\%$ reduction in ECE alongside a selective prediction curve showing that rejecting the top 5% most uncertain samples increases effective operational decision precision from 88% to 97%.

### 5. What Evidence Falsifies the Novelty Claim
- If post-hoc temperature scaling fails to reduce ECE on held-out test partitions or if selective prediction yields no improvement in downstream decision reliability compared to uncalibrated thresholding, the contribution is falsified.

---

## Contribution Package C: Multi-Task Lightweight Vision Stacking with Physics-Constrained Kinetic Degradation

### 1. What Existing Studies Already Do
- Machine learning models for post-harvest decay either use purely empirical black-box regression (random forests, standard LSTMs) or purely classical physical differential equations (Arrhenius, USDA tables) (Liang et al., 2024; Sultan et al., 2025).
- Studies report artificial perfect metrics (AUC=1.000) when synthetic sensor sequences are generated with disjoint thresholds.

### 2. What Existing Studies Do NOT Establish
- How to constrain lightweight neural sequence models with post-harvest biological ripening kinetics (Arrhenius respiration and logistic climacteric ethylene production) without requiring expensive laboratory spectroscopy.

### 3. How AgriRoute Differs
AgriRoute proposes a **hybrid architecture combining edge multi-task vision with a physics-constrained kinetic degradation model**. Rather than treating decay as an unconstrained regression, AgriRoute anchors temporal spoilage prediction in the biophysical law of climacteric ripening, eliminating synthetic target leakage and guaranteeing biologically plausible predictions across varying ambient transport temperatures.

### 4. What Experiment Proves the Difference
- **Experiment:** Comparative evaluation of unconstrained BiLSTM vs. Physics-constrained sequence modeling on noisy, non-linearly separable cold-chain sensor traces with thermal fluctuations.
- **Metric:** Mean Absolute Error (MAE in hours to spoilage) and physical consistency violation rate (percentage of predictions violating monotonic respiration kinetics). Demonstrating that the physics-constrained formulation prevents catastrophic divergence under out-of-distribution thermal spikes.

### 5. What Evidence Falsifies the Novelty Claim
- If unconstrained empirical models consistently outperform the physics-constrained model across all thermal abuse regimes without violating physical bounds, the utility of the physics constraint is falsified.

---

## Recommendation for the AgriRoute Paper Revision

**The Principal Investigator recommends selecting Contribution Package A as the primary contribution, reinforced by Package B:**
- Package A directly answers Reviewer 1 (Comment R1.2) and Reviewer 3 (Comment R3.1) by establishing a genuine systems-level and algorithmic novelty: **the closed-loop coupling of calibrated visual freshness with dynamic transport routing under perishability constraints**.
- Package B provides the rigorous mathematical and statistical foundation (ECE, calibration curves, bootstrap CIs) demanded by Reviewer 1 (Comment R1.1, R1.3).

