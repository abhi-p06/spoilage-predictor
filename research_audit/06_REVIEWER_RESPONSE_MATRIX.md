# Reviewer Response & Requirement Traceability Matrix

> **Audit Date:** 2026-11-09  
> **Auditor:** Independent Scientific Auditor  
> **Audited Manuscript:** `~/Downloads/main.tex` (ICMLDE 5.0, Paper ID: 1345)  
> **Scope:** Reviewers 1, 2, and 3 critiques deconstructed into actionable engineering requirements.

---

## 1. Traceability Overview Matrix

| Reviewer & Objection ID | Core Reviewer Objection | Severity | Requirement Statement | Current Manuscript Status | Repository Evidence Status | Resolution Strategy |
|---|---|---|---|---|---|---|
| **REV1-01** | Vague fusion formulation & decision boundaries | **MAJOR** | Formulate exact multi-modal decision logic, feature inputs, and probability thresholds. | Section IV-D, VI-C; Eq. (3) $S = w_1 V + w_2 G$ | **NOT VERIFIED** (Ghost equations; code uses XGBoost + fallback) | Replace Eq. (3) with XGBoost stacking architecture and explicit thresholds ($<0.35, 0.35\text{--}0.70, \ge 0.70$). |
| **REV1-02** | Incremental contribution / engineering plumbing | **MAJOR** | Delineate clear scientific contributions beyond off-the-shelf library integration. | Section I, Section III | **PARTIALLY VERIFIED** (Presents system integration) | Reframe novelty around closed-loop multi-modal risk coupling and edge-feasible calibration under perishability constraints. |
| **REV1-03** | Artificial BiLSTM AUC=1.000 | **CRITICAL** | Retract AUC=1.000; audit synthetic leakage; report realistic noisy metrics or reposition as simulation. | Abstract, Section IV-E, Section VI-D | **SYNTHETIC ARTIFACT** (CO₂ & Humidity linearly disjoint) | Formally retract AUC=1.000; explain synthetic artifact transparently; reframe as designed framework or noisy simulation. |
| **REV1-04** | Lack of fair state-of-the-art comparison | **MAJOR** | Construct structured comparative matrix benchmarking AgriRoute against published post-harvest systems (2020–2026). | Section II, Section III | **PARTIALLY VERIFIED** (Generic narrative categories only) | Add quantitative SOTA comparison table benchmarking architectures, sensing modalities, and decision coupling. |
| **REV1-05** | Confusing software mock tests with field trials | **CRITICAL** | Clearly separate live field evaluation from laboratory and software demonstrations. | Abstract, Section VII-A | **UNSUPPORTED** (Single mock run presented as live field run) | Disclose $N=0$ physical shipments; relabel Guntur–Rajkot case study as software architecture demonstration. |
| **REV2-01** | Unjustified fusion weights & missing Table V | **CRITICAL** | Provide empirical justification, sensitivity analysis, or feature importance for fusion weighting. | Section VI-C, Table V tags | **UNSUPPORTED** (Weights $\alpha, \beta, w_1, w_2$ and Table V do not exist) | Remove phantom Table V references; present XGBoost feature importances and ablation sensitivity curve over $\alpha \in [0, 1]$. |
| **REV2-02** | Unresolved placeholders and author notes | **MAJOR** | Eliminate all drafting notes, placeholder tags, dummy author surnames, and incomplete citations. | Lines 6–46, Line 57, Line 61, Section VI | **CONFIRMED DEFECT** (Drafting notes, dummy emails, Table V tags) | Perform thorough editorial scan; finalize author affiliations; remove all internal drafting notes. |
| **REV2-03** | Lack of external validation & class omissions | **CRITICAL** | Evaluate visual classifier on external public datasets; resolve missing Tomato and Mango data. | Section II-A, Section VI-A | **UNSUPPORTED** (Kaggle dataset only has 3 fruits; test eval crashed) | Report test metrics with 95% CIs; conduct out-of-distribution evaluation; explicitly disclose true fruit scope. |
| **REV3-01** | Overclaiming operational readiness | **MAJOR** | Narrow claims to verifiable empirical evidence; de-claim field transformation claims. | Title, Abstract, Section X | **OVERCLAIMED** (Claims field-deployed decision tool) | Reframe AgriRoute as an algorithmic framework and working software prototype; state operational boundaries. |
| **REV3-02** | Treating single software run as validation | **CRITICAL** | Disclose independent shipment count ($N=0$); specify commercial limits. | Section VII-A, Section VIII | **UNSUPPORTED** (Shipment count = 0) | Explicitly acknowledge $N=0$ physical shipments in Abstract, Results, and Limitations. |
| **REV3-03** | Missing comparison with agri-logistics platforms | **MAJOR** | Provide a structured comparison with commercial agricultural quality and cold-chain platforms. | Section II-C, Section III | **PARTIALLY VERIFIED** (Mentions cold chain generally) | Add comparative matrix benchmarking AgriRoute against AgNext, Intello Labs, CropIn, Ecozen, and Stellapps. |
| **REV3-04** | Missing prospective field trial protocol | **MAJOR** | Detail a rigorous prospective field evaluation protocol with sampling, power, and ground-truth assays. | Section VI-E, Section VII-B | **PARTIALLY VERIFIED** (Brief 2-stage sketch only) | Expand into complete 4-phase field evaluation protocol detailing cohort sizes, destructive assays (Brix, firmness), and metrics. |

---

## 2. Manuscript Textual Flaws & Unresolved Placeholders

A comprehensive scan of `~/Downloads/main.tex` identified the following specific textual defects:

1. **Pre-Submission Drafting Notes in Source:**
   - Lines 6–46 contain a raw Markdown drafting memo:
     ```latex
     % NOTES TO THE AUTHOR -- read before submitting, then delete this block.
     % - The paper currently describes an implemented, working software prototype...
     % - Table V: You need to insert your actual numbers for alpha, beta, w1, w2...
     ```
2. **Dummy Author Metadata:**
   - Line 57: `\IEEEauthorblockN{Esh {[}Surname---to confirm{]}\textsuperscript{*}}`
   - Line 61: `{[}email---to confirm{]}@somaiya.edu`
3. **Ghost References to Non-Existent Table V:**
   - Line 188: *"The exact composition of the dataset behind the CNN's training... is left to Table V rather than stated here..."*
   - Line 217: *"The fitted values of $\alpha$ and $\beta$ are scoring-function implementation details, reported once confirmed in Table V..."*
   - Line 239: *"The exact values of $w_1$, $w_2$, and that calibration curve remain implementation details pending confirmation in Table V..."*
4. **Contradictory Figure Caption:**
   - Figure 2 caption (line 253): *"Case-study risk component breakdown (Eq.~\eqref{eq:visual}--\eqref{eq:fusion}) for the illustrative banana shipment."*
   - The figure is an empty LaTeX box (`\fbox{\rule{0pt}{2.2cm}\rule{0.85\linewidth}{0pt}}`), and the breakdown refers to equations that do not exist in the code.
5. **Ghost Physics-Consistency Loss:**
   - Section VI-D (lines 244–268) provides complex differential equations (Eqs. 4 and 5) for a "Physics-Constrained BiLSTM Extension".
   - Line 266 admits: *"no physics loss has been coded, no DIY rig has been built, and no paired real-sensor dataset exists."*

---

## 3. Detailed Action Plan per Reviewer

### Reviewer 1 Requirements:
- **REQ-R1.1:** Rewrite Section IV-D and VI-C to document the real XGBoost feature set `[cnn_score, lstm_risk, days, cold_chain, produce_id]` and hardcoded alert thresholds.
- **REQ-R1.2:** Rewrite Section I and III to emphasize the novel closed-loop coupling between pre-dispatch visual quality and perishable transit constraints.
- **REQ-R1.3:** Remove claims of empirical BiLSTM AUC=1.000. Re-evaluate on noisy synthetic sequences or designate the BiLSTM as a proposed architectural extension.
- **REQ-R1.4:** Insert a 6-row SOTA literature comparison table in Section II benchmarking against recent 2022–2026 agricultural AI systems.
- **REQ-R1.5:** Relabel Section VII-A from "Illustrative Case Study" to "Software Execution Walkthrough", stating clearly that zero physical fruit was transported.

### Reviewer 2 Requirements:
- **REQ-R2.1:** Eliminate all references to Table V and parameters $w_1, w_2, \alpha, \beta$. Provide an empirical ablation curve sweeping fusion weight $\alpha \in [0, 1]$.
- **REQ-R2.2:** Remove lines 6–46, update author surname and email, and eliminate all bracketed drafting reminders.
- **REQ-R2.3:** Retrain the CNN on clean, leakage-free partitions; compute per-class precision, recall, and F1; evaluate out-of-distribution generalization on public images; clarify that Tomato and Mango are future extensions.

### Reviewer 3 Requirements:
- **REQ-R3.1:** De-claim the paper's title and abstract: present AgriRoute as a "Prototype Decision-Support Framework".
- **REQ-R3.2:** Explicitly disclose $N=0$ physical shipments in Abstract, Results, and Limitations.
- **REQ-R3.3:** Add a structured comparison table in Section III benchmarking AgriRoute against AgNext, Intello Labs, CropIn, and Ecozen.
- **REQ-R3.4:** Expand Section VI-E and VII-B into a formal prospective field trial protocol detailing sample size calculations, destructive Brix/firmness testing, and logistics tracking.

