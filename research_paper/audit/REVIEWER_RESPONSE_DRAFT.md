# Point-by-Point Response to ICMLDE Reviewers

**Manuscript Reference:** AgriRoute (Previously submitted, unpublished manuscript: ICMLDE 5.0, Paper ID: 1345)  
**Revised Working Title:** *Source-Stratified Evaluation of Out-of-Distribution Detection in Fruit-Quality Classification Under Species and Treatment-Labelled Shifts*  
**Target Publication:** *Procedia Computer Science* (Elsevier) / 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026)  
**Status:** Working Draft (Section references mapped; exact line and page numbers to be finalized upon full document compilation)  
**Document Location:** `research_paper/audit/REVIEWER_RESPONSE_DRAFT.md` (Companion copy at root [`REVIEWER_RESPONSE_DRAFT.md`](file:///Users/abby/Desktop/spoilage-predictor/REVIEWER_RESPONSE_DRAFT.md))  
**Date:** November 11, 2026 (Updated & Reconciled)  

---

## Author Preamble and Overview of Major Revision

We thank the Program Committee and the three anonymous reviewers for their thoughtful, rigorous, and constructive evaluations of our previously submitted, unpublished manuscript (Paper ID: 1345). The reviewers' critiques accurately exposed fundamental limitations in our earlier system-integration manuscript: specifically, the reliance on synthetic sensor data, unvalidated heuristic fusion weights, the absence of external multi-dataset evaluation, and claims of field utility based on a single demonstration run.

Taking this feedback to heart, we have executed a **substantive scientific restructuring** of the research rather than making cosmetic adjustments. As confirmed by the corresponding author, the earlier manuscript was never published. Specifically:

1. **Fundamental Scope Transformation:** We have pivoted from an unvalidated engineering system proposal to an **empirical computer vision and out-of-distribution (OOD) failure analysis**. We have removed the synthetic-data BiLSTM, the linear route heuristic, and unbenchmarked price forecasting from the revised manuscript and excluded them from our current empirical claims. The earlier synthetic BiLSTM results are not treated as valid evidence of physical IoT performance, and the old synthetic-data results are retained only as historical development context.
2. **Audited External Multi-Dataset Benchmark ($N = 13,465$ Evaluated Records):** Addressing the concern regarding internal Kaggle splits, we have benchmarked our frozen MobileNetV2 classifier across two major external datasets—**FruitVision** (Bijoy et al., 2025; 10,045 evaluated records) and **Sultana** (Sultana et al., 2022; 3,193 evaluated records)—structured across five rigorously audited partitions ($N = 13,465$ total evaluated records, distinct from published raw dataset totals).
3. **Established OOD Detection Baselines:** We systematically benchmark five established post-hoc OOD scoring algorithms (MSP, Energy, ODIN, Mahalanobis distance, OpenMax) and an operational Energy–MSP Dual-Gate cascade locked at validation $\tau_{95}$ operating thresholds ($\tau_{\text{Energy}} = 0.918451$, $\tau_{\text{MSP}} = 0.582610$).
4. **Source-Stratified Evaluation Design:** To prevent cross-repository camera and lighting confounding from masking true biological differences, we benchmark semantic and treatment shifts within shared image repositories. Source matching reduces cross-repository confounding while potential within-repository capture variation remains.
5. **Statistical and Uncertainty Rigor:** All reported metrics are backed by 1,000-iteration non-parametric bootstrap 95% confidence intervals and perceptual-hash (pHash) near-duplicate sensitivity auditing.
6. **Transparent Scientific Honesty:** We explicitly disclose that the study is an image-level benchmark evaluation. We disclaim prospective field deployment and analytical chemical detection from RGB images. Where reviewer requests cannot be satisfied from existing evidence (specifically Reviewer 1 Comment 5 requesting field data), we explicitly state that actual physical field data do not exist, and none are invented or implied.

*(Note on Resubmission Process: Per conference instructions, this point-by-point response will be included as the opening section of the single combined resubmission file `1345_revised_version.pdf`, with full page and line number references inserted upon camera-ready compilation of all manuscript sections.)*

---

## Response to Reviewer 1

### Comment 1.1:
> *"The abstract needs to clarify the meaning of the fusion score and the decisions made."*

**Status:** `Addressed, subject to final methodology verification`

**Response:**  
We agree entirely with the reviewer. In the previous draft, the abstract referred vaguely to a "fused risk score" without defining its mathematical composition, decision boundaries, or operational interpretation.

In the revised manuscript, we have eliminated the ad-hoc multimodal fusion layer. In its place:
1. The revised Abstract summarizes the operational Energy–MSP dual-gate cascade and reports that under fixed validation thresholds, $42.83\%$ of FruitVision treatment-labelled image records are accepted and assigned a Fresh class.
2. Section 1.6 (Contribution 4) introduces the operational false acceptance and rejection trade-offs: maintaining a $16.07\%$ UFAR on FruitVision unseen species incurs a $41.98\%$ KRR on FruitVision Known and $42.43\%$ across pooled Partition B ($525/1,193 = 44.01\%$ on Sultana Known).
3. The formal mathematical decision rule:
$$\text{ACCEPT}(x) \text{ if and only if: } S_{\text{Energy}}(x) \ge \tau_{\text{Energy}} = 0.918451 \land S_{\text{MSP}}(x) \ge \tau_{\text{MSP}} = 0.582610$$
$$\text{REJECT otherwise.}$$
where thresholds were calibrated on the primary validation partition using empirical order statistics and held fixed during external cohort evaluation (using $s_{(7)}$ to maintain $216/227 = 95.1542\%$ empirical known-class retention, $\tau_{95}$).

*(Note: While the operational cascade and trade-off metrics are introduced in the Abstract and Section 1.6, the full mathematical exposition of the decision rule and threshold derivations are formulated for Section 4.3 and Section 5.3, which are currently being drafted. This modification is therefore pending complete manuscript write-up and verification.)*

---

### Comment 1.2:
> *"The combination of MobileNetV2 with routing and market data is system integration without much novelty."*

**Status:** `Addressed through reframing, subject to committee acceptance`

**Response:**  
We acknowledge and accept this critical observation. Combining off-the-shelf components (a standard CNN, road distance calculations, and web-scraped market prices) represents software integration rather than a novel scientific contribution.

Rather than defending the novelty of the software pipeline, we have **fundamentally reframed the paper as an empirical computer vision study and failure analysis**. The revised paper disclaims algorithmic novelty; instead, it delivers three core empirical contributions to agricultural computer vision:
1. **Quantification of External Known-Class Performance Differences (RQ1):** Documenting a $28.56\text{ percentage-point}$ difference in top-1 accuracy between the primary in-distribution test partition (Partition A: $96.92\%$) and pooled external known-class image records (Partition B: $68.36\%$).
2. **Source-Matched Isolation of Semantic vs. Treatment Shifts (RQ2):** Demonstrating that while Energy-based OOD detection discriminates unseen produce species within a shared repository ($81.57\%$ AUROC), it exhibits lower discrimination on produce under the dataset-reported treatment-labelled condition ($53.13\%$ AUROC).
3. **Empirical Evaluation of Operational Threshold Trade-offs (RQ3):** Showing that ranking-based AUROC does not by itself describe false acceptance and known-class rejection at the fixed operational thresholds, where controlling external false acceptance ($16.07\%$ UFAR) imposes a $41.98\%$ known-class false rejection penalty on FruitVision Known ($42.43\%$ on pooled Partition B).

*(Revised in: Section 1.4, Section 1.5, Section 1.6, Section 5; subject to committee acceptance of scope change)*

---

### Comment 1.3:
> *"BiLSTM validation on artificial sequences leads to an unrealistic AUC of 1.000."*

**Status:** `Addressed through removal of synthetic evidence`

**Response:**  
The reviewer is completely correct. A validation AUC of $1.000$ was an artificial artifact resulting from deterministic, non-overlapping synthetic parameter ranges generated by our simulation script. It provided zero valid evidence of real-world IoT sensor performance.

In response, we have **removed the BiLSTM component, the synthetic sensor generation script, and the AUC = 1.000 claim from the revised manuscript and excluded them from our current empirical claims**. The earlier synthetic BiLSTM results are not treated as valid evidence of physical IoT performance, and the old synthetic-data results are retained only as historical development context. The manuscript is now focused exclusively on real photographic image records. In Section 7 (Limitations) and Section 8 (Future Work), we explicitly document this lesson: synthetic sensor distributions cannot substitute for physical in-transit logging, and we outline a prospective hardware logger protocol for future multi-sensor research.

*(Revised in: Abstract, Section 1.6, Section 7, Section 8)*

---

### Comment 1.4:
> *"The lack of a comparison with state-of-the-art post-harvest decision-making systems is apparent."*

**Status:** `Partially addressed; complete Related Work comparison still required`

**Response:**  
We agree that the original manuscript lacked a rigorous comparative foundation against modern literature.

In the revised manuscript, we contextualize our findings against recent literature in agricultural computer vision, open-set recognition (OSR), and out-of-distribution (OOD) detection (2020–2026):
1. **Scholarly Literature Comparison (Section 1.4 and Section 2):** We benchmark our scope against adjacent recent studies: Sattar et al. (2024, SensorNet multi-sensor adulteration detection), Wang et al. (2023, cross-domain fruit classification via unsupervised domain adaptation), Pehlivan & Kara (2026, one-shot open-set food recognition), Jansi & Kavitha (2026, PEOS-Net evidential open-set plant disease recognition), and Yan et al. (2026, PAG-MSBNet prototype-augmented crop disease recognition).
2. **Algorithmic OOD Baselines (Section 4 and Section 5):** Rather than evaluating our model in isolation, we benchmark five established post-hoc OOD scoring methods—Maximum Softmax Probability (Hendrycks & Gimpel, 2017), Energy-based scoring (Liu et al., 2020), ODIN (Liang et al., 2018), Mahalanobis feature distance (Lee et al., 2018), and OpenMax (Bendale & Boult, 2016)—across all evaluation cohorts.

*(Note: While Section 1.4 introduces this comparison, Section 2 Related Work is currently a planned stub that will be fully articulated and verified upon complete manuscript compilation.)*

---

### Comment 1.5:
> *"The conclusion should contain the field data, not the repository-level results."*

**Status:** `Not addressed: actual field data do not exist`

**Response:**  
We accept this critique unreservedly. The original submission asserted real-world farmer impact and commercial readiness based solely on laboratory and repository data.

We must state clearly: **Actual physical field data do not exist, and we have strictly refrained from inventing or simulating mock field data to satisfy this comment.**

In the revised manuscript, we have addressed this concern through **transparent scientific de-claiming and formal methodological scoping**:
1. **Explicit Disclosure of Physical Limitations:** We explicitly state in the Abstract, Section 1.6, and Section 7 that this study contains $N = 0$ physical transit shipments, no live in-transit loggers, and no independent analytical chemistry assays.
2. **Actionable Field Validation Protocol (Section 8.2):** Rather than offering vague generalities, we detail a prospective 4-phase field protocol describing crate-level sensor logging, destructive assays (Brix, firmness, acidity), arrival re-inspection, and Brier score calibration as design parameters to be finalized during a pilot.

*(Revised in: Abstract, Section 1.6, Section 7, Section 8)*

---

## Response to Reviewer 2

### Comment 2.1:
> *"The selection of fusion weights and their novelty need clarification."*

**Status:** `Addressed through validation-calibrated rejection policy`

**Response:**  
We agree. The original linear formula ($S = w_1 V + w_2 G$) lacked empirical derivation, sensitivity analysis, or theoretical justification.

In the revised manuscript, **we have completely eliminated the ad-hoc linear fusion formula**. In its place, Section 4.3 presents an operational **Energy–MSP Dual-Gate rejection cascade**:
$$\text{ACCEPT}(x) \text{ if and only if: } S_{\text{Energy}}(x) \ge \tau_{\text{Energy}} = 0.918451 \land S_{\text{MSP}}(x) \ge \tau_{\text{MSP}} = 0.582610$$
$$\text{REJECT otherwise.}$$
- **Threshold Derivation:** The operating thresholds were calibrated on the primary validation partition using empirical order statistics and held fixed during external cohort evaluation (using $s_{(7)}$ to maintain $216/227 = 95.1542\%$ empirical retention, $\tau_{95}$).
- **Novelty Disclaimer:** We explicitly disclaim mathematical novelty for the Dual-Gate heuristic, framing it strictly as an operational rejection policy designed to assess false acceptance under distribution shift.

*(Revised in: Section 1.6, Section 4.3)*

---

### Comment 2.2:
> *"The note “Specific roles can be updated before submission” suggests that the paper is not complete."*

**Status:** `Pending author approval and final CRediT contributions`

**Response:**  
We apologize for the incomplete author metadata and drafting placeholders in the original submission.

In the revised manuscript:
1. The document has been migrated to the official ICMLDE LaTeX template (`elsarticle.cls`, `ecrc.sty`, Procedia Computer Science format).
2. The draft manuscript currently uses a provisional anonymized author block (`Author Names Redacted for Peer Review`) pending confirmation of the conference's review policy for revised submissions.
3. An internal provisional role mapping has been recorded in the project progress log for the student research team from Somaiya University (Eshita Patil, Abhinay Pande, Bijeet Nayek, Vini Pandhare, Keerthana Thirunavukkarasu, and Bushra Shaikh). Contributor roles remain pending formal author review and approval. An approved CRediT author-contribution statement will be finalized upon author confirmation prior to camera-ready submission.

*(Status: Pending author approval and final CRediT contributions; provisional anonymization pending review policy confirmation)*

---

### Comment 2.3:
> *"The freshness model is not tested against the available fruit quality datasets."*

**Status:** `Addressed through external dataset evaluation`

**Response:**  
This was a vital critique that guided the core empirical work of our revision. Evaluating a classifier solely on random splits of a single Kaggle archive provides no evidence of external generalization.

To address this comprehensively, we scaled our evaluation to an audited **$13,465$-image evaluated record census** across three independent repositories:
1. **Primary Kaggle (Test Partition A):** 227 evaluated records.
2. **FruitVision Dataset (Bijoy et al., 2025; Data in Brief):** 10,045 evaluated records across Partition B ($N=4,157$), Partition C ($N=1,917$), Partition D1 ($N=2,776$), and Partition D2 ($N=1,195$).
3. **Sultana Dataset (Sultana et al., 2022; Data in Brief):** 3,193 evaluated records across Partition B ($N=1,193$) and Partition D1 ($N=2,000$).
*(Note: These figures reflect evaluated benchmark records across partitions, not published raw repository totals)*.

The results demonstrate the necessity of external multi-dataset evaluation: while our model achieved $96.92\%$ [$94.71\%$, $98.68\%$] top-1 accuracy on the primary test partition (Partition A), observed accuracy was lower at $68.36\%$ [$67.20\%$, $69.40\%$] on pooled external known-class image records (Partition B), with balanced accuracy dropping from $97.09\%$ to $68.66\%$.

*(Revised in: Section 1.6 (Contribution 1), Section 3, Section 5.1)*

---

## Response to Reviewer 3

### Comment 3.1:
> *"There is no research contribution other than application of existing approaches."*

**Status:** `Addressed through empirical reframing, subject to complete manuscript`

**Response:**  
We accept that the original software prototype did not constitute an adequate scientific contribution.

In response, we shifted the focus from applied software integration to an **in-depth empirical failure analysis**. The revised manuscript delivers core empirical insights for the agricultural vision community:
1. **Source-Matched Shift Isolation:** We demonstrate that post-hoc OOD detection performance depends heavily on the nature of the shift: while Energy scoring distinguishes unseen species with $81.57\%$ AUROC within a shared repository, its performance drops to $53.13\%$ on FruitVision images carrying the dataset-reported formalin-mixed label.
2. **Evaluation of Treatment-Labelled Image Records:** We provide empirical benchmark evidence showing that $42.83\%$ [$41.26\%$, $44.34\%$] ($821/1,917$) of treatment-labelled images bypass fixed validation rejection gates and are classified as "Fresh". The evaluated classifier and post-hoc OOD methods did not reliably distinguish this treatment-labelled cohort under the tested conditions.
3. **Operational Rejection Costs:** We reveal that enforcing a low false acceptance rate ($16.07\%$ UFAR) on FruitVision unseen species incurs a known-class false rejection rate of $41.98\%$ ($1,745/4,157$) on FruitVision Known and $42.43\%$ ($2,270/5,350$) on pooled Partition B, exposing a critical operational hurdle for edge sorting systems.

*(Revised in: Section 1.5, Section 1.6, Section 5, Section 6; subject to complete manuscript compilation)*

---

### Comment 3.2:
> *"There is only one demonstration shipment and it is not enough to test the system."*

**Status:** `Addressed through removal of the single demonstration as scientific evidence`

**Response:**  
We completely agree. Presenting a single software execution run (Guntur to Rajkot banana) as validation of an entire logistics platform was insufficient to establish generalization or field impact ($N=1$).

In response, **the single Guntur-to-Rajkot software demonstration has been removed as evidence of shipment-level validation. The revised study instead evaluates image-level records and makes no claims of multi-shipment, transit-level or field-system validation.** The revised paper evaluates **$N = 13,465$ individual image records** across five partitioned cohorts, incorporating exact-duplicate auditing and perceptual-hash (pHash) sensitivity analysis across Hamming distance radii $r \in \{0, 4, 8\}$.

*(Revised in: Section 1.6, Section 3, Section 7; physical shipment validation remains outside the current study)*

---

### Comment 3.3:
> *"A table comparing AgriRoute's characteristics to those of other agri-logistics platforms is needed."*

**Status:** `Partially addressed through scientific scope change; original comparison request requires explicit explanation`

**Response:**  
We carefully evaluated this recommendation. Because the manuscript has been **reframed from an applied logistics software platform to an empirical computer vision and out-of-distribution benchmark**, comparing our open-source vision evaluation against proprietary commercial logistics platforms (e.g., AgNext, CropIn, Intello Labs) is no longer methodologically appropriate. Commercial platforms are commercial products that generally do not disclose model architectures, release pre-trained checkpoints, or provide reproducible test splits.

Instead, in Section 2 (Related Work), we provide a **Scholarly Literature Comparison Table** synthesizing reported characteristics of recent peer-reviewed agricultural vision and open-set recognition studies (2022–2026) across model architectures, evaluation dataset scale, types of distribution shift evaluated, OOD algorithms tested, operational threshold policies, and uncertainty reporting.

*(Note: The substitution rationale will be explicitly articulated in Section 2 upon complete manuscript drafting.)*

---

### Comment 3.4:
> *"The conclusion recognizes limited validation, but suggests nothing about the field evaluation plan."*

**Status:** `Partially addressed by a proposed field protocol; physical field validation remains unperformed`

**Response:**  
We acknowledge that the original manuscript lacked an actionable, scientifically sound experimental protocol for field validation.

In Section 8.2 of the revised manuscript, we address this directly by describing a **prospective 4-phase field-evaluation protocol as future work**:
1. **Phase 1 (Transit Instrumentation):** Multi-sensor crate logging measuring ethylene, carbon dioxide, ambient temperature, and relative humidity, with sampling intervals and sensor specifications treated as design parameters to be finalized during a pilot.
2. **Phase 2 (Standardized Dispatch Photography & Analytical Assays):** Uniform diffuse-light photography at dispatch paired with destructive biochemical ground truth across representative fruit subsamples: soluble solids content via digital Brix refractometry, flesh firmness via penetrometry, and titratable acidity.
3. **Phase 3 (Multi-Horizon Destination Arrival Inspection):** Destructive and non-destructive re-evaluation upon arrival at destination markets across distinct transit durations (24h, 48h, and 72h).
4. **Phase 4 (Decision Calibration & Economic Utility):** Post-hoc probability calibration evaluated via reliability diagrams and Brier score against baseline sorting decisions.

*(Note: While the experimental protocol is formulated as a prospective plan, physical field validation trials themselves have not been performed.)*

---

## Summary of Revisions and Status of Reviewer Concerns

The table below provides a factual summary of how each reviewer objection is addressed in the current revision:

| Objection | Status Summary |
| :--- | :--- |
| **Reviewer 1, Comment 1 (Fusion score & decisions)** | Addressed via revised operational decision policy (Dual-Gate cascade), pending complete methodology write-up in Section 4.3. |
| **Reviewer 1, Comment 2 (Novelty of system integration)** | Addressed through major empirical reframing, subject to conference committee acceptance and completion of the manuscript. |
| **Reviewer 1, Comment 3 (Unrealistic synthetic BiLSTM AUC)** | Addressed: earlier synthetic evidence removed from the revised manuscript and excluded from current empirical claims. |
| **Reviewer 1, Comment 4 (Comparison with post-harvest SOTA)** | Partially addressed; scholarly literature comparison table is designed, but Section 2 Related Work write-up still requires completion. |
| **Reviewer 1, Comment 5 (Field data in conclusion)** | **Unfulfilled limitation:** actual field-data request remains unfulfilled because no physical field data exist; not invented or simulated. |
| **Reviewer 2, Comment 1 (Fusion weights & derivation)** | Addressed through validation-calibrated rejection policy with fixed empirical order statistic thresholds. |
| **Reviewer 2, Comment 2 (Incomplete author contribution note)** | Draft uses provisional anonymized author block; author contributions mapped internally, pending formal author team confirmation. |
| **Reviewer 2, Comment 3 (Evaluation on external fruit datasets)** | Addressed through external dataset evaluation across 13,465 evaluated records (FruitVision and Sultana). |
| **Reviewer 3, Comment 1 (Application of existing approaches)** | Addressed through empirical failure analysis reframing, subject to complete manuscript compilation. |
| **Reviewer 3, Comment 2 (Single demonstration shipment)** | Addressed: single-shipment demo removed as validation evidence; physical shipment validation remains absent from current study. |
| **Reviewer 3, Comment 3 (Comparison with logistics platforms)** | Original commercial platform comparison is not directly fulfilled; rationale for scientific scope change must be disclosed in Section 2. |
| **Reviewer 3, Comment 4 (Concrete field evaluation plan)** | Partially addressed: prospective protocol proposed in Future Work, but physical trials remain unperformed. |

*(Note: Per ICMLDE resubmission instructions, this response report will accompany the revised manuscript. Exact page and line references will be finalized upon complete document compilation.)*
