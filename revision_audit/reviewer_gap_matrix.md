# AgriRoute Reviewer Traceability & Gap Matrix

> **Audit Date:** 2026-11-08  
> **Audited Manuscript:** `~/Downloads/main.tex`  
> **Review Scope:** Reviewer 1, Reviewer 2, Reviewer 3 reports (as defined in research-revision plugin)

---

## 1. Traceability Matrix Overview

| Reviewer & Item | Focus Area | Severity | Current Manuscript Section | Repository Evidence Status | Resolution Feasibility |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R1.1** | Fusion score & decision thresholds | **Major** | Abstract, Sec. IV-D, Sec. VI-C | **NOT VERIFIED** (Ghost equations in paper; XGBoost/fallback in code) | High (align paper with code) |
| **R1.2** | Scientific contribution beyond integration | **Major** | Sec. I, Sec. III (Table I) | **PARTIALLY VERIFIED** (Presents system integration) | High (reframe contribution) |
| **R1.3** | Remove/audit artificial BiLSTM AUC=1.000 | **CRITICAL** | README, Sec. IV-E, Sec. VI-D | **NOT VERIFIED** (Severe target leakage in synthetic generator) | High (retract AUC=1.000, explain artifact) |
| **R1.4** | Fair state-of-the-art comparison | **Major** | Sec. II, Sec. III | **PARTIALLY VERIFIED** (Only 4 broad categories; no empirical table) | Medium (add literature comparison table) |
| **R1.5** | Distinguish field results from software tests | **CRITICAL** | Abstract, Sec. VII-A | **NOT VERIFIED** (Single local mock run presented as live field run) | High (transparently relabel as software demo) |
| **R2.1** | Fusion weight selection, evidence & ablation | **CRITICAL** | Sec. VI-C, Table V | **NOT VERIFIED** (Weights $w_1, w_2$ do not exist; Table V missing) | High (document XGBoost feature importance/ablation) |
| **R2.2** | Remove incomplete author notes & placeholders | **Major** | Preamble, Author block, Sec. VI | **CONFIRMED DEFECT** (Drafting notes, dummy surnames, Table V tags) | Immediate (clean LaTeX source) |
| **R2.3** | Validate freshness on public external datasets | **CRITICAL** | Sec. II-A, Sec. VI-A | **PARTIALLY VERIFIED** (Only Kaggle 3-class; crashed on test eval) | Medium (run leak-free evaluation on public datasets) |
| **R3.1** | Narrow claims to verified evidence | **Major** | Title, Abstract, Sec. X | **CONFIRMED OVERCLAIM** (Claims 4 crops, live API, field deployable) | High (reframe and de-claim) |
| **R3.2** | Shipment count: do not treat one mock run as validation | **CRITICAL** | Sec. VII-A, Sec. VIII | **NOT VERIFIED** (Shipment count = 0; only 1 local web app demo) | High (admit N=0 shipments; specify pilot protocol) |
| **R3.3** | Sourced comparison against agri-logistics platforms | **Major** | Sec. II-C, Sec. III | **PARTIALLY VERIFIED** (Mentions generic cold chain; no platform matrix) | Medium (construct verified comparison matrix) |
| **R3.4** | Prospective multi-shipment field evaluation protocol | **Major** | Sec. VI-E, Sec. VII-B | **PARTIALLY VERIFIED** (Brief sketch; lacks sampling, power, metrics) | Medium (design rigorous field trial protocol) |

---

## 2. Point-by-Point Forensic Gap Analysis

### Reviewer 1

#### Comment R1.1: Define fusion score and decision mapping in abstract and methods
- **Reviewer Critique:** The abstract and methods vaguely describe a "weighted risk-fusion formulation" and "traffic-light alerts" without providing explicit, verifiable mappings, mathematical formulations, or decision boundary criteria.
- **Current Manuscript Status:**
  - Abstract lines 70–72: Mentions "weighted spoilage-risk score, a days-to-spoilage estimate, and a sell-by recommendation".
  - Section VI-C, Eq. (3): States $S = w_1 V + w_2 G$ with $w_1 + w_2 = 1$, but states "the exact values of $w_1, w_2$... remain implementation details pending confirmation in Table V". Table V does not exist.
- **Repository Evidence:**
  - In `app/predict.py`:
    - Fusion is actually an `XGBClassifier` + `XGBRegressor` trained on `[cnn_score, lstm_risk, days, cold_chain, produce_id]`.
    - Alert mapping is hardcoded in `get_alert()`:
      - $P_{\mathrm{spoilage}} < 0.35 \implies \text{GREEN}$
      - $0.35 \le P_{\mathrm{spoilage}} < 0.70 \implies \text{YELLOW}$
      - $P_{\mathrm{spoilage}} \ge 0.70 \implies \text{RED}$
    - Heuristic fallback formula: $\text{spoilage} = 0.45(1 - \text{cnn}) + 0.40(\text{lstm}) + 0.15(\text{days}/\text{shelf})$.
- **Missing Evidence:** The linear convex combination $S = w_1 V + w_2 G$ does not exist in code.
- **Required Action:** Replace Eq. (3) with the actual decision architecture: document the XGBoost stacking classifier and regressor, state the explicit feature vector, and provide the exact probability threshold rules for Green/Yellow/Red.

---

#### Comment R1.2: Explain whether the contribution goes beyond component integration
- **Reviewer Critique:** AgriRoute appears to be an engineering plumbing exercise combining standard MobileNetV2, an off-the-shelf BiLSTM, and OSRM routing. What is the fundamental scientific or methodological contribution?
- **Current Manuscript Status:**
  - Section I (lines 85–86) claims 4 contributions, primarily framing the integration of existing tools as a novel contribution.
- **Repository Evidence:**
  - MobileNetV2 is standard ImageNet transfer learning (`notebooks/01_cnn_training.py`).
  - BiLSTM is a standard Keras 2-layer model (`notebooks/02_lstm_training.py`).
  - Mandi module is a basic API client / MD5 fallback (`app/mandi_prices.py`).
- **Missing Evidence:** No theoretical novelty or custom loss was successfully implemented (the ODE physics loss was never coded).
- **Required Action:** Honestly reposition AgriRoute as an **empirical, low-cost multimodal decision framework** for resource-constrained smallholders. Focus the novelty on: (1) multimodal early-warning fusing visual surface cues with atmospheric gas trends and price risk; (2) empirical evaluation of domain shift when deploying computer vision in rural mandis; and (3) realistic sensitivity analysis of how transport distance affects quality risk.

---

#### Comment R1.3: Audit/remove or replace the artificial-sequence BiLSTM AUC=1.000
- **Reviewer Critique:** An AUC of 1.000 on time-series sensor data indicates severe data leakage, artificial separation, or trivial synthetic artifacts. It cannot be presented as genuine predictive validity.
- **Current Manuscript Status:**
  - Mentioned in README, Viva pitch, and logs. `main.tex` avoids stating 1.000 directly but cites the model in Section IV-E and Table II.
- **Repository Evidence:**
  - `generate_sensor_data.py` (lines 68–80) reveals the fatal leakage mechanism:
    - Fresh CO2 $\in [400, 900]$ ppm; Spoiled CO2 $\in [1000, 3500]$ ppm.
    - Fresh Humidity $\in [65, 85]\%$; Spoiled Humidity $\in [85, 98]\%$.
    - Fresh Temp $\in [10, 22]^\circ\text{C}$; Spoiled Temp $\in [20, 30]^\circ\text{C}$.
  - The classes are separated by hard boundaries with zero variance overlap. A simple decision stump on any single channel achieves 100% accuracy.
- **Missing Evidence:** No evaluation exists on overlapping synthetic noise, real sensor traces, or experimental decay datasets.
- **Required Action:** **Completely retract AUC=1.000**. Provide an open, honest post-mortem in the methodology section explaining why the initial synthetic benchmark yielded AUC=1.000 (disjoint range artifacts), and evaluate the model under realistic sensor noise and partial observations.

---

#### Comment R1.4: Add a fair state-of-the-art comparison
- **Reviewer Critique:** Related work lacks quantitative and qualitative comparisons with contemporary post-harvest decision systems and agri-logistics platforms.
- **Current Manuscript Status:**
  - Section II reviews literature broadly in text; Table I only lists high-level categories (Image-only, Sensor-only, Price forecasters, Cold-chain optimizers).
- **Repository Evidence:**
  - `reports/research_brief.md` contains an extensive survey of 2024–2026 literature (e.g. SPADE, CruiseBench, FactoryNet, PULSE).
- **Missing Evidence:** A structured feature-by-feature matrix comparing AgriRoute against published state-of-the-art systems (e.g. Intello Labs, AgNext, Ecozen, recent CEA journal literature).
- **Required Action:** Build a comprehensive comparison matrix in Section II/III evaluating modalities (Vision, IoT, Price, Route), deployment hardware cost, target user (fleet vs smallholder), and offline capability.

---

#### Comment R1.5: Report real field results separately from repository/software tests
- **Reviewer Critique:** The manuscript blurs the line between simulated demonstrations, software tests, and real-world agricultural field measurements.
- **Current Manuscript Status:**
  - Section VII-A presents a "live run of the deployed system" for a banana shipment from Guntur to Rajkot (1580.3 km).
- **Repository Evidence:**
  - No physical shipment occurred.
  - The banana photo was a stock image.
  - The 1580.3 km distance was generated by OSRM but had zero impact on prediction.
  - The price drop (1803 $\to$ 1767) was generated by an MD5 hash fallback function (`_build_estimated_mandi`).
- **Missing Evidence:** Zero field sensor readings, zero actual produce tracked, zero ground-truth spoilage outcomes.
- **Required Action:** Explicitly relabel Section VII-A as an **"End-to-End Software Workflow Demonstration"**. Clearly state that no physical shipments were tracked and delineate software integration tests from prospective field validation.

---

### Reviewer 2

#### Comment R2.1: Explain the selection and evidence behind fusion weights; include sensitivity/ablation
- **Reviewer Critique:** The manuscript posits fusion weights $w_1, w_2$ and parameters $\alpha, \beta$ without explaining how they were calibrated, optimized, or validated. Sensitivity analysis and ablations are completely absent.
- **Current Manuscript Status:**
  - Section VI-B, VI-C: Continually defers $\alpha, \beta, w_1, w_2$ to "Table V". Table V is missing.
- **Repository Evidence:**
  - In `logs/fusion_training.log`, XGBoost feature importances are recorded:
    - `cnn_score`: 78.4%
    - `days`: 12.8%
    - `cold_chain`: 4.4%
    - `produce_id`: 2.8%
    - `lstm_risk`: 1.6%
- **Missing Evidence:** No sensitivity analysis or ablation study comparing multimodal fusion against unimodal baselines (Vision-only vs Sensor-only vs Metadata-only).
- **Required Action:**
  1. Remove all references to the fictional $\alpha, \beta, w_1, w_2$ equations.
  2. Document the empirical feature importances learned by XGBoost.
  3. Include a formal ablation study showing performance drops when removing modalities.

---

#### Comment R2.2: Remove all incomplete author-role or drafting notes
- **Reviewer Critique:** The manuscript contains visible drafting notes, unfinished placeholder text, and notes such as `Specific roles can be updated before submission`.
- **Current Manuscript Status:**
  - Preamble lines 6–42: `NOTES TO THE AUTHOR -- read before submitting, then delete this block.`
  - Author line 57: `Esh [Surname---to confirm]`
  - Author line 61: `[email---to confirm]@somaiya.edu`
  - Body lines: Multiple instances of `(see Table V)`, `pending confirmation in Table V`.
- **Repository Evidence:**
  - All found in `~/Downloads/main.tex`.
- **Required Action:** Clean up all placeholders, confirm author names/affiliations, remove drafting instructions, and ensure every table and figure referenced in the text exists.

---

#### Comment R2.3: Validate freshness on suitable public fruit-quality datasets with compatible labels and defensible external tests
- **Reviewer Critique:** The freshness classifier was trained on a Kaggle dataset that contains only 3 fruit types, and lacks external cross-dataset validation or per-class reporting.
- **Current Manuscript Status:**
  - Claims 97.22% accuracy across produce.
- **Repository Evidence:**
  - Kaggle dataset `sriramr/fruits-fresh-and-rotten-for-classification` contains only Apple, Banana, and Orange.
  - No Mango or Tomato images exist in the dataset.
  - In `logs/cnn_training.log`, `notebooks/01_cnn_training.py` crashed at line 396 with `KeyError: 'accuracy'`, so no per-class classification report or confusion matrix was logged.
- **Missing Evidence:** No evaluation on external fruit quality datasets (e.g. Fruit-360, FIDS30, or real market images).
- **Required Action:**
  1. Fix the evaluation script bug in `01_cnn_training.py` to extract full per-class precision, recall, F1, and confusion matrices.
  2. Clearly state that the visual model was evaluated on Apple, Banana, and Orange.
  3. Perform an external test on a secondary public dataset or explicitly document out-of-distribution limitations for Tomato and Mango.

---

### Reviewer 3

#### Comment R3.1: State the exact contribution and evidence, or narrow the claim
- **Reviewer Critique:** The paper makes broad claims of solving post-harvest risk and route optimization for smallholder farmers, but the evidence presented is limited to prototype code.
- **Current Manuscript Status:**
  - Abstract and Section I overclaim operational readiness and decision-support efficacy.
- **Repository Evidence:**
  - The prototype web app is functional, but relies on heuristics when models are missing and does not optimize routes (it only displays them via Leaflet).
- **Required Action:** Narrow the paper's claimed scope: frame AgriRoute as a **feasibility prototype and unified architectural framework**, honestly presenting the prototype's empirical limits.

---

#### Comment R3.2: Report independent shipment count and limits; do not treat one demonstration as broad validation
- **Reviewer Critique:** Describing a single run of the software on one simulated shipment as validation is scientifically unacceptable.
- **Current Manuscript Status:**
  - Section VII-A reports a single run (Guntur $\to$ Rajkot) as an "illustrative case study".
- **Repository Evidence:**
  - Unique shipments tracked: **0**.
- **Required Action:** Formally state in Section VII-A and Section VIII that the reported shipment count is $N=0$ physical shipments. Present the Guntur–Rajkot scenario strictly as an interface and pipeline execution walk-through.

---

#### Comment R3.3: Add a sourced comparison table against relevant agri-logistics platforms
- **Reviewer Critique:** The paper needs a structured comparison with real-world Indian and international agricultural logistics and quality-assaying systems.
- **Current Manuscript Status:**
  - General mentions of cold chains; no comparative table of commercial or research platforms.
- **Repository Evidence:**
  - Survey notes in `reports/research_brief.md` review academic literature, but lack commercial platform comparisons.
- **Required Action:** Add a structured comparison table in Section III benchmarking AgriRoute against prominent platforms (e.g., AgNext, Intello Labs, CropIn, Ecozen Eco-Frost, Stellapps) across sensing modalities, cost, target user, and decision outputs.

---

#### Comment R3.4: Include a prospective field protocol with outcomes, data collection, sampling, and evaluation plan
- **Reviewer Critique:** If real field data cannot be collected for this revision, the authors must provide a rigorous, prospective experimental protocol for future field validation.
- **Current Manuscript Status:**
  - Section VI-E / VII-B provides a high-level 2-stage sketch, lacking statistical rigor, sample size calculations, sensor specifications, and ground-truth validation methods.
- **Repository Evidence:**
  - `reports/pitch_preparation.md` outlines practical deployment thoughts (Raspberry Pi + MQ-136 + DHT22).
- **Required Action:** Expand Section VI-E and Section VII-B into a complete, publishable prospective field trial protocol detailing: target crop cohorts, sample size per route, sensor logging intervals, destructive quality assaying (Brix, firmness, titratable acidity), and statistical evaluation metrics.

