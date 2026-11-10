# Forensic Audit and Comparative Analysis: Historical AgriRoute Paper vs. Current V4.1 Manuscript

**Document:** `OLD_VS_CURRENT_PAPER_AUDIT.md` (Companion copy at `research_paper/audit/OLD_VS_CURRENT_PAPER_AUDIT.md`)  
**Reference Document (Old Paper):** `/Users/abby/Downloads/AgriRoute_ICMLDE.pdf` (Previously submitted, unpublished manuscript: ICMLDE 5.0, Paper ID: 1345; Decision: Revision and Resubmission; Never Published)  
**Working Manuscript (Current):** ICMLDE 2026 LaTeX Template (`research_paper/manuscript/`)  
**Numerical Ground Truth:** Stage 4.1.2.1.1 Canonical Results (`STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md`, `STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv`, `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv`)  
**Auditor:** Senior Scientific Editor & Research Methodologist  
**Date:** November 11, 2026 (Updated & Reconciled)  
**Status:** RECONCILED — SCIENTIFIC PROVENANCE AND BENCHMARK ARITHMETIC VERIFIED  

---

## Executive Summary: System Integration Prototype vs. Empirical OOD Study

The historical document (`AgriRoute_ICMLDE.pdf`, Paper ID: 1345, previously submitted, unpublished manuscript to ICMLDE 5.0) represents an **implemented software prototype and system-integration study** with repository-reported model results and a software execution demonstration. That earlier manuscript reported:
1. A MobileNetV2 produce condition model (repository-reported validation accuracy of 97.22% on an internal Kaggle split).
2. A temporal sensor-risk BiLSTM over 24-hour synthetic sequences (ethylene, CO₂, humidity, temperature) generated from USDA Handbook 66 ranges (repository-reported validation AUC of 1.000).
3. An XGBoost multimodal fusion model (repository-reported held-out accuracy of >95%).
4. A route-risk exposure heuristic based on road distance, transport type, and cold-chain availability ($G = \text{clip}(\alpha \tau D - \beta c, 0, 100)$).
5. An AGMARKNET market module retrieving destination wholesale prices with lightweight trend display.
6. A farmer-facing dashboard application with route mapping, risk outputs, mandi prices, SMS alerts, and downloadable reports, demonstrated on an illustrative Guntur-to-Rajkot banana shipment run ($N = 1$).

Crucially, the historical paper acknowledged several validation limitations: it disclosed that sensor sequences were synthetic (model-development validation, not IoT field validation), route risk was a proxy heuristic rather than an environmental measurement, and no prospective field dataset linked image, transit, and observed spoilage outcomes. The manuscript was not an unexecuted mock-up, but an implemented prototype whose empirical claims were limited by synthetic inputs, heuristic weights, and a single illustrative execution run that was insufficient to establish generalization or field impact.

In contrast, the **Current V4.1 Study** represents an **empirical, source-stratified computer vision and out-of-distribution (OOD) failure analysis**. Rather than pursuing a multimodal software pipeline relying on synthetic sensor inputs and uncalibrated linear proxies, the current research isolates the computer vision component. It investigates the behavior of a frozen MobileNetV2 classifier across an audited $13,465$-image evaluated record census from three independent repositories (Kaggle/Primary, FruitVision, Sultana), systematically benchmarking five established post-hoc OOD detection scoring methods (MSP, Energy, ODIN, Mahalanobis distance, OpenMax) and an operational Dual-Gate rejection cascade under covariate domain, unseen-species semantic, and treatment-labelled condition shifts.

---

## 1. Content That Remains Scientifically Valid

The following foundational concepts from the historical paper remain scientifically sound and provide the background context for the current paper:

1. **Agricultural Loss Context & Problem Scale:**
   - Post-harvest deterioration in domestic transit corridors is a critical cause of produce loss in India.
   - The Indian Council of Agricultural Research (ICAR-CIPHET, Jha et al., 2015) nationwide survey provides empirical commercial fruit loss ranges between $6.70\%$ and $15.88\%$ (apple: $10.39\%$, banana: $7.76\%$, citrus: $15.88\%$).
   - The operational bottleneck of manual visual sorting: subjective, labour-intensive, fatigue-prone, and unscalable to high-throughput consolidation facilities.

2. **Choice of Vision Architecture (MobileNetV2):**
   - The rationale for lightweight CNN backbones remains valid: depthwise separable convolutions, inverted residuals, and linear bottlenecks achieve high efficiency with parameter budgets under $4.0\text{ million}$ weights ($\approx 2.26\text{M}$ parameters in Model B V4.1).
   - Low latency and minimal memory footprint are essential for execution on commodity edge devices and mobile phones in rural environments.

3. **Vulnerabilities of the Closed-Set Assumption:**
   - The observation that standard supervised classifiers rely on an independent and identically distributed (i.i.d.) closed set ($\mathcal{Y} = \{1, \dots, K\}$), whereas operational deployments frequently encounter non-target produce and unfamiliar capture environments.
   - Standard softmax normalization produces overconfident posterior probabilities that peak near $1.0$ even on corrupted or out-of-distribution inputs.

4. **Early Methodological Honesty:**
   - The historical paper correctly recognized (Section 6.3) that uncalibrated model outputs must not be termed "spoilage probabilities," adopting the designation "Post-Harvest Risk Score" instead.
   - The historical paper openly disclosed that the sensor sequences were synthetic and could not represent field IoT validation.

---

## 2. Background and Literature: Reusable vs. Unusable

### A. Reusable Literature (Verified and Retained)
- **Jha et al. (2015) [1]:** ICAR-CIPHET monograph on Indian harvest and post-harvest losses (ISBN 978-81-901418-7-9).
- **Gross et al. (2016) [17]:** USDA Agricultural Handbook No. 66 on commercial storage conditions.
- **Sandler et al. (2018) [7]:** MobileNetV2 architecture (IEEE CVPR 2018).
- **Bhargava & Bansal (2021) [19]:** Computer vision review for fruits and vegetables quality evaluation (*J. King Saud Univ.*).
- **Kumar et al. (2025) [20]:** Smartphone-based computer vision for smallholder crop quality assessment (*Comput. Electron. Agric.*).
- **Verified Produce Classifiers:** Zhang et al. (2024), Chen et al. (2024), Gulzar (2023), Rizzo et al. (2023).

### B. Incomplete or Informal Citations to Purge
- **Reference [18] (Undergraduate Report):** `"Post-harvest spoilage predictor for small farmers in India. Unpublished undergraduate project report..."` (*Purged; not peer-reviewed scientific literature*).
- **Fragmentary Anonymous Entries:** References [4], [5], [6], [13], [14], [16], [21], and [23] in the old paper lacked author lists, volume/issue numbers, and DOIs (*Purged*).
- **Secondary Logistics:** Disconnected brinjal price forecasting [10] and generic location-routing optimization [15] (*Purged as outside empirical vision scope*).

### C. Essential Foundations Integrated in Current V4.1 Manuscript
1. **OOD Detection & OSR Baselines:** Scheirer et al. (2013), Bendale & Boult (2016 OpenMax), Hendrycks & Gimpel (2017 MSP), Guo et al. (2017 calibration), Liang et al. (2018 ODIN), Lee et al. (2018 Mahalanobis), Liu et al. (2020 Energy), Vaze et al. (2022), Yang et al. (2024 survey).
2. **Primary Dataset Publications:** Sultana et al. (2022 *Data in Brief*), Bijoy et al. (FruitVision, 2025 *Data in Brief*), Abayomi-Alli et al. (FruitQ, 2024).
3. **Adjacent Agricultural OSR/Adulteration Work:** Sattar et al. (2024 SensorNet), Wang et al. (2023 domain adaptation), Pehlivan & Kara (2026), Jansi & Kavitha (PEOS-Net, 2026), Yan et al. (PAG-MSBNet, 2026).

---

## 3. Methodology Evolution: Old System vs. Current V4.1

| Component | Historical Paper (`AgriRoute_ICMLDE.pdf`) | Current V4.1 Implementation | Methodological Rationale for Transformation |
| :--- | :--- | :--- | :--- |
| **Primary Scope** | Implemented multimodal decision-support prototype (vision + route + synthetic IoT + market + alerts). | Rigorous empirical evaluation & failure diagnosis of post-hoc OOD detectors on a frozen vision model. | Isolates the visual inspection modality and replaces synthetic sensor data with an audited multi-source image benchmark. |
| **Vision Model** | MobileNetV2 trained on Kaggle images, reporting 97.22% repository validation accuracy. | Frozen MobileNetV2 checkpoint (`MODEL_B_V4_1_CHECKPOINT.keras`, SHA-256: `4a12f354...`) evaluated across 13,465 image records. | Evaluation must use a frozen checkpoint across independent external cohorts to measure empirical performance differences. |
| **Evaluated Record Census** | Internal split of single Kaggle dataset. | **13,465 Evaluated Records:**<br>• Primary Kaggle: 227 (Partition A)<br>• FruitVision: 10,045 (B: 4,157; C: 1,917; D1: 2,776; D2: 1,195)<br>• Sultana: 3,193 (B: 1,193; D1: 2,000)<br>*(Note: Reflects evaluated benchmark records, not published repository totals)*. | Resolves single-dataset limitation and establishes rigorous source-stratified test partitions. |
| **Sensor Component** | BiLSTM over synthetic 24-hr sequences (reported $\text{AUC} = 1.000$). | **Removed from Current Benchmark.** Retained only as historical development context. | The earlier synthetic BiLSTM results are not treated as valid evidence of physical IoT performance; perfect AUC was an artifact of deterministic formula simulation. |
| **Route & Market** | Linear heuristic $G = \text{clip}(\alpha \tau D - \beta c, 0, 100)$ and AGMARKNET price trend display. | **Removed from Current Benchmark.** Excluded from current empirical claims; discussed only in future scope context. | Uncalibrated linear formulas and unbenchmarked price trends diluted the core focus on visual reliability. |
| **Decision / Fusion Layer** | XGBoost combining image score, synthetic LSTM, route heuristic, and market price ($>95\%$ acc). | **Five Established Post-Hoc OOD Scorers:** MSP, Energy, ODIN, Mahalanobis, OpenMax. | Established post-hoc OOD detectors provide reproducible, mathematically grounded anomaly detection without synthetic inputs. |
| **Rejection Mechanism** | None (forced continuous classification). | **Operational Dual-Gate Cascade:** Conjunctive rule locked at validation $\tau_{95}$ operating thresholds. | Agricultural sorting requires an explicit, audited rejection gate for anomalous or out-of-distribution inputs. |
| **Dual-Gate Acceptance Rule** | *N/A* (not present in old paper). | $\text{ACCEPT}(x) \text{ if and only if: } S_{\text{Energy}}(x) \ge \tau_{\text{Energy}} = 0.918451 \land S_{\text{MSP}}(x) \ge \tau_{\text{MSP}} = 0.582610$; $\text{REJECT otherwise.}$ | Authoritative Stage 4.0.3 specification calibrated via empirical order statistic $s_{(7)}$ on internal validation data ($216/227 = 95.1542\%$ empirical retention). |
| **Evaluation Design** | Single internal validation split + 1 qualitative banana transit demonstration. | **Source-Stratified 5-Partition Benchmark Census ($N = 13,465$):** Partitions A, B, C, D1, D2 across 3 repositories. | Source matching reduces cross-repository confounding while potential within-repository capture variation remains. |
| **Uncertainty Audit** | None (isolated point estimates). | **1,000-Iteration Bootstrap 95% Confidence Intervals** across all 60 primary metrics. | Enforces statistical rigor; eliminates unsupported single-point claims. |

---

## 4. Obsolete Experimental Results to Exclude

The experimental results reported in the historical paper are obsolete and must **never** be cited as current experimental findings or substituted for V4.1 results:

1. **Old Table 4 (Repository-Reported Model Results):**
   - *Reported:* MobileNetV2 Validation Accuracy = `97.22%`.  
     *Historical Status:* Evaluated on an internal Kaggle split. In V4.1, the frozen classifier achieves **$96.92\%$** [$94.71\%$, $98.68\%$] top-1 accuracy and **$97.09\%$** balanced accuracy on Primary Test Partition A ($N = 227$). On pooled external known-class image records (Partition B, $N = 5,350$), observed accuracy was lower at **$68.36\%$** [$67.20\%$, $69.40\%$] (balanced accuracy **$68.66\%$**). The $28.56\text{ pp}$ difference represents the external known-class performance difference between V4.1 Partition A and pooled Partition B; it must not be compared directly with the old 97.22% figure.
   - *Reported:* BiLSTM Validation AUC = `1.000`.  
     *Historical Status:* Degenerate artifact of evaluating on synthetic sequences generated from deterministic formulas. The earlier synthetic BiLSTM results are not treated as valid evidence of physical IoT performance.
   - *Reported:* XGBoost Held-Out Classifier Accuracy = `>95%`.  
     *Historical Status:* Evaluated on a hybrid feature space containing synthetic sensor values.
2. **Old Table 3 (Proposed Baseline and Ablation Matrix):**
   - Baselines B1 through B6 were marked `"To be evaluated"`. Baseline B7 repeated the unverified `>95%` figure.
   - *Status:* Replaced by the completed 6-detector $\times$ 4-cohort source-stratified evaluation matrix with verified empirical point estimates and bootstrap CIs.
3. **Illustrative End-to-End Case Study (Section 8.7, Figures 2–4):**
   - The single Guntur-to-Rajkot software demonstration has been removed as evidence of shipment-level validation. The revised study instead evaluates image-level records and makes no claims of multi-shipment, transit-level or field-system validation.

---

## 5. Claims That Are No Longer Supported

The following claims from the historical paper or earlier drafts must be explicitly avoided in the revision:

1. **"AgriRoute reduces post-harvest loss and improves smallholder farmer income":**  
   *Correction:* No prospective randomized controlled trial, longitudinal field deployment, or economic impact study was conducted. The manuscript limits claims to image-level benchmark performance and diagnostic failure modes.
2. **"The system predicts in-transit spoilage probability":**  
   *Correction:* Without paired in-transit environmental loggers and destination biological ground truth, the model evaluates visual quality at dispatch, not transit probability.
3. **"RGB computer vision can detect chemical formalin adulteration" or claims of demonstrating chemical detection:**  
   *Correction:* In the evaluated FruitVision treatment-labelled cohort (Cohort B), the frozen classifier and tested post-hoc OOD scoring methods did not reliably distinguish FruitVision images carrying the dataset-reported formalin-mixed label from the natural known-class cohort (Energy AUROC $53.13\%$ [$52.16\%$, $54.09\%$], and Dual-Gate operational UFAR-Fresh $42.83\%$, with $821/1,917$ treatment-labelled images passing the gate and classified as Fresh). The manuscript must not claim that these results demonstrate universal physical or chemical limitations of RGB sensing, nor make analytical chemistry or food-safety claims, but frame this strictly as an image-level classifier and OOD-gate outcome under a dataset-reported treatment-associated visual condition shift.
4. **"The Dual-Gate linear margin proxy is a new predictive model":**  
   *Correction:* The operational Dual-Gate is a discrete heuristic acceptance rule ($\text{ACCEPT}(x) \text{ iff } S_{\text{Energy}}(x) \ge 0.918451 \land S_{\text{MSP}}(x) \ge 0.582610$). The continuous linear proxy is purely a diagnostic visualization.
5. **"Source matching eliminates cross-repository confounding":**  
   *Correction:* Source matching reduces cross-repository confounding while potential within-repository capture variation remains.
6. **Priority claims ("First", "Unprecedented"):**  
   *Correction:* Eliminate priority assertions. Describe findings as empirical benchmark results on the evaluated image cohorts.
7. **"Real-world false acceptance":**  
   *Correction:* Use "benchmark operational trade-offs" when discussing test cohort rejection and false acceptance rates.

---

## 6. Research Objectives and Contributions: Reframing Matrix

| Dimension | Historical Paper (`AgriRoute_ICMLDE.pdf`) | Current V4.1 Scientific Paper |
| :--- | :--- | :--- |
| **Central Research Question** | "Does integrating visual condition, route exposure, sensor risk, and market context into a smartphone app improve dispatch decisions?" | **RQ1:** How does closed-set accuracy change when evaluated on external repositories containing the same known fruit classes?<br>**RQ2:** How effectively do established OOD detectors discriminate unseen species vs. treatment shifts in source-matched cohorts?<br>**RQ3:** How do fixed validation rejection thresholds ($\tau_{95}$) affect unknown false acceptance (UFAR) and known-class retention (KRR)? |
| **Contribution 1** | Implemented smartphone pipeline combining vision, route, and market information. | **Audited Benchmark Census ($N = 13,465$):** 5 source-stratified partitions across 3 repositories with exact-duplicate and pHash sensitivity auditing. |
| **Contribution 2** | MobileNetV2 with repository-reported 97.22% validation accuracy. | **Quantification of Closed-Set Performance Differences Across Partitions:** Documenting a $28.56\text{ pp}$ external known-class performance difference between Partition A ($96.92\%$) and pooled Partition B ($68.36\%$), and analyzing cultivar error patterns. |
| **Contribution 3** | BiLSTM sensor-risk model and XGBoost fusion with synthetic data disclosure. | **Source-Matched Evaluation Across Semantic and Treatment Cohorts:** Demonstrating strong discrimination within FruitVision semantic shift ($81.57\%$ AUROC) while observed AUROC was lower on treatment-labelled images ($53.13\%$) and external cultivars ($67.52\%$). |
| **Contribution 4** | A farmer-facing Streamlit/FastAPI application with route mapping and alerts. | **Diagnostic Evaluation of Treatment-Labelled Images and Operational Trade-Offs:** Showing that $42.83\%$ ($821/1,917$) of treatment-labelled images are accepted as Fresh, and achieving $16.07\%$ UFAR on FruitVision unseen species incurs $41.98\%$ ($1,745/4,157$) known-class false rejection on FruitVision Known ($42.43\%$ on pooled Partition B: $2,270/5,350$; Sultana Known: $525/1,193 = 44.01\%$). |

---

## 7. Visual Assets Audit & Recreation Plan

| Old Figure (`AgriRoute_ICMLDE.pdf`) | Limitation of Old Asset | Recommended V4.1 Scientific Figure |
| :--- | :--- | :--- |
| **Fig. 1: Conceptual Architecture** (Page 3) | Depicted a hybrid system including synthetic BiLSTM, AGMARKNET API, and XGBoost fusion. | **Fig. 1: AgriRoute V4.1 Empirical Evaluation Framework.** Clean vector diagram: Input Image $\to$ Frozen MobileNetV2 $\to$ Logits/Features $\to$ 5 OOD Scorers $\to$ Dual-Gate Cascade $\to$ Partitions A–D2. |
| **Fig. 2: Route Map Screenshot** (Page 8) | Generic Google Maps screenshot for Guntur-to-Rajkot. | **Fig. 2: Benchmark Partition Hierarchy.** Diagram illustrating the 13,465-image census across Kaggle, FruitVision, and Sultana. |
| **Fig. 3: UI Dials Screenshot** (Page 8) | Software UI screenshot with uncalibrated score dials. | **Fig. 3: Closed-Set Performance Comparison.** Grouped bar chart comparing Partition A ($96.92\%$) with FruitVision B ($69.14\%$) and Sultana B ($65.63\%$). |
| **Fig. 4: AGMARKNET Price Graph** (Page 9) | 3-day line chart without statistical baseline. | **Fig. 4: Multi-Detector AUROC Matrix.** Grouped bar chart comparing all 5 detectors across Cohorts A, B, and D. |
| *[None in Old Paper]* | No ROC curves or score distribution plots. | **Fig. 5: ROC Curves & Score Distributions.** Demonstrating strong Energy separation for Cohort A (AUROC $81.57\%$) vs substantial overlap for Cohort B (AUROC $53.13\%$). |
| *[None in Old Paper]* | No qualitative error analysis. | **Fig. 6: Diagnostic Failure Gallery.** High-resolution mosaic of misclassified russeted apples, pale citrus, and accepted formalin-mixed image records. |

---

## 8. Publication and Authorship Provenance

### A. Author Attribution Policy
The historical paper lists six student authors:
- **Eshita Patil**, **Abhinay Pande**, **Bijeet Nayek**, **Vini Pandhare**, **Keerthana Thirunavukkarasu**, and **Bushra Shaikh**  
  *Affiliation:* Department of Artificial Intelligence and Data Science, K. J. Somaiya College of Engineering, Somaiya Vidyavihar University, Mumbai, India.  
  *Emails:* `eshita.patil@somaiya.edu`, `abhinay.p@somaiya.edu`, `bijeet.nayek@somaiya.edu`, `vini.p@somaiya.edu`

**Policy Determination:** Do **not** automatically copy these names into the new manuscript. Maintain the anonymous peer-review author block (`"Author Names Redacted for Peer Review"`) until the current paper's contributors, author roles, and formal author approvals are confirmed by the team. Status remains: **Pending author approval and final CRediT contributions**.

### B. Historical Paper Provenance (Paper ID: 1345)
- The historical manuscript (`AgriRoute_ICMLDE.pdf`, Paper ID: 1345) is a **previously submitted, unpublished manuscript** submitted to the 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0).
- It received a **revision-and-resubmission** decision from the program committee, accompanied by reviews from Reviewers 1, 2, and 3.
- As confirmed by the corresponding author, it was **never published**. (Note: claims regarding whether it was indexed or presented have not been independently confirmed and are not asserted). Therefore, it is treated as a previously submitted, unpublished manuscript. It must not be cited as a published document.
- The current V4.1 manuscript develops from this previously submitted version under a fundamental empirical reframing that directly addresses the committee and reviewer critique.

---

*This audit document completes the required historical comparison and corrective reconciliation.*
