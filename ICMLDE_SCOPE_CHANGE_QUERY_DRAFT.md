# Administrative Inquiry Draft: ICMLDE Scope Reframing Query

**Target Recipient:** ICMLDE Conference Secretariat (`info@icmlde.org`) / Program Committee Chairs  
**Subject:** Query regarding Major Scientific Revision Scope for Paper ID: 1345 (AgriRoute)  
**Document Location:** `ICMLDE_SCOPE_CHANGE_QUERY_DRAFT.md` (Companion copy at `research_paper/audit/ICMLDE_SCOPE_CHANGE_QUERY_DRAFT.md`)  
**Date:** November 11, 2026 (Updated & Reconciled)  
**Status:** DRAFT FOR AUTHOR REVIEW — DO NOT TRANSMIT AUTOMATICALLY  

> [!IMPORTANT]
> **Administrative Notice for Authors:**  
> This communication draft is prepared for internal author team review. It must **not** be sent automatically. The corresponding author should review, adjust, and approve this inquiry before transmitting it from their institutional email account to `info@icmlde.org`.

---

## Draft Email Text

**To:** `info@icmlde.org`  
**From:** [Corresponding Author Email, e.g., eshita.patil@somaiya.edu]  
**Date:** [Insert Date]  
**Subject:** ICMLDE 2026 — Revision Scope Query for Paper ID 1345 (AgriRoute)

Dear ICMLDE 2026 Program Chairs and Organizing Committee,

We are writing with regard to our previously submitted, unpublished manuscript to ICMLDE 5.0:

* **Paper ID:** 1345
* **Original Title:** *AgriRoute: A Vision-Based Post-Harvest Risk System*
* **Decision Received:** Revision and Resubmission

We received detailed, constructive, and valuable reviews from Reviewers 1, 2, and 3. In particular, the reviewers highlighted that:
1. Validating a BiLSTM on synthetic sensor sequences yielded an unrealistic AUC of 1.000 (Reviewer 1, Comment 3).
2. Combining MobileNetV2 with routing heuristics and market scraping represented engineering integration rather than a novel scientific contribution (Reviewer 1, Comment 2; Reviewer 3, Comment 1).
3. The visual classifier had not been evaluated against external fruit quality datasets (Reviewer 2, Comment 3).
4. Demonstrating the system on a single shipment run ($N = 1$) was insufficient to establish generalization or operational utility (Reviewer 3, Comment 2).
5. Conclusions claimed field utility without actual field measurements (Reviewer 1, Comment 5; Reviewer 3, Comment 4).

### Nature of the Scientific Revision
Taking these critiques seriously, our research team decided against cosmetic patches. Instead, we executed a substantive scientific restructuring:
- We **removed the earlier synthetic sensor model, the ad-hoc linear route heuristic, and unbenchmarked price forecasting from the revised manuscript and excluded them from our current empirical claims**. The earlier synthetic BiLSTM results are not treated as valid evidence of physical IoT performance, and the old synthetic-data results are retained only as historical development context.
- We re-scoped the research as an **empirical computer vision and out-of-distribution (OOD) failure study**, benchmarking a frozen MobileNetV2 produce classifier across an audited **$13,465$-image evaluated record census** from three independent photographic repositories (Kaggle/Primary, FruitVision, and Sultana) across five source-stratified evaluation partitions.
- We benchmarked five established post-hoc OOD scoring algorithms (MSP, Energy, ODIN, Mahalanobis distance, OpenMax) and an operational Dual-Gate rejection cascade, backed by 1,000-iteration bootstrap 95% confidence intervals and perceptual-hash sensitivity auditing.
- We formally de-claimed all live supply-chain claims, scoping our conclusions strictly to image-level benchmark evaluations and detailing a prospective 4-phase field evaluation protocol as future work.
- The revised study does not contain physical field shipment measurements or independent chemical assays. It is limited to image-level benchmark evaluation, with a prospective field-validation protocol proposed as future work.

In line with this refined focus, our revised working title is:  
**"Source-Stratified Evaluation of Out-of-Distribution Detection in Fruit-Quality Classification Under Species and Treatment-Labelled Shifts"**

### Administrative Question
The original decision notification instructed authors to use the existing "Edit" option in the submission portal to submit revised materials. Because the scientific scope of our manuscript has changed substantially in response to the reviewers' methodological critiques:

1. **Acceptance of Scope Reframing under Paper ID 1345:** Could the Program Committee kindly confirm whether this substantive empirical reframing and failure analysis can be considered as a revision under Paper ID 1345 via the "Edit" portal option, accompanied by our point-by-point response report? Or does the Committee recommend handling it as a new regular paper submission for ICMLDE 2026?
2. **Revision Portal Status & Window:** If the revision should be submitted under Paper ID 1345, could you kindly confirm whether the portal upload window remains open for this revision cycle?

We are currently preparing the substantially revised manuscript and point-by-point response. Before completing the submission package, we seek the committee's guidance on whether this major change in scientific scope can be considered under Paper ID 1345 or should be handled as a new submission.

We greatly appreciate your guidance on this procedural question.

Sincerely,

The Author Team of Paper ID 1345  
Department of Artificial Intelligence and Data Science  
K. J. Somaiya College of Engineering, Somaiya Vidyavihar University  
Mumbai, India  
