# ICMLDE Resubmission Requirements & Editorial Checklist

**Manuscript Reference:** AgriRoute (Previously submitted, unpublished manuscript: ICMLDE 5.0, Paper ID: 1345)  
**Target Publication:** *Procedia Computer Science* (Elsevier) / 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026)  
**Document Location:** `ICMLDE_RESUBMISSION_REQUIREMENTS_CHECKLIST.md` (Companion copy at `research_paper/audit/ICMLDE_RESUBMISSION_REQUIREMENTS_CHECKLIST.md`)  
**Auditor:** Senior Scientific Editor & Research Methodologist  
**Date:** November 11, 2026 (Updated & Reconciled)  
**Status:** ACTIVE VERIFICATION CHECKLIST  

---

## Executive Summary

This checklist establishes a formal verification framework derived directly from the official ICMLDE decision notification email and Elsevier *Procedia Computer Science* author instructions. Every requirement must be verified and checked off prior to portal upload.

---

## Requirements Verification Matrix

| # | Formal Requirement | Source / Rule | Verification Standard | Current Status | Notes & Action Required |
| :-: | :--- | :--- | :--- | :---: | :--- |
| **1** | **Point-by-Point Response Report** | ICMLDE Decision Email | Comprehensive response addressing every comment from Reviewer 1 (5 comments), Reviewer 2 (3 comments), and Reviewer 3 (4 comments) without omission. | **IN PROGRESS (DRAFT)** | Drafted and reconciled in `REVIEWER_RESPONSE_DRAFT.md` and `REVIEWER_RESPONSE_MATRIX.md`. Final compilation pending full manuscript. |
| **2** | **Page-by-Page Location Mapping** | ICMLDE Decision Email | Every response must indicate exact manuscript page numbers and line numbers where revisions occur. | **PENDING FULL COMPILED DRAFT** | Section references mapped. Exact page/line numbers will be populated upon compilation of all manuscript sections (`01`–`08`). |
| **3** | **Single Combined Submission File** | ICMLDE Decision Email | The response report and revised manuscript must be combined into **one single Word or PDF document** (response report positioned at the beginning or end). | **PLANNED** | Will combine response letter and manuscript into single PDF (`1345_revised_version.pdf`) at final release stage. |
| **4** | **Similarity Report $\le 10\%$** | ICMLDE Decision Email | Text similarity index must not exceed $10\%$. A formal similarity report must be uploaded as a supplementary file. *(Note: Do not exclude bibliography unless explicitly authorized by conference instructions.)* | **AUDIT REQUIRED** | An independent similarity checker (Turnitin/iThenticate) must be run on the final compiled text. No score may be claimed without verified tool output. |
| **5** | **Procedia Computer Science Compliance** | Conference Template | Single-column format ($192\text{ mm} \times 262\text{ mm}$ trim size, text area $160\text{ mm} \times 222\text{ mm}$), official fonts, CRC geometry, Elsevier heading styles. | **IN PROGRESS (DRAFT INSPECTED)** | LaTeX template compiles cleanly for Section 1; final compliance requires inspection of the complete, assembled manuscript. |
| **6** | **English Language Editing** | Conference / Procedia Policy | The manuscript must be thoroughly proofread and edited for English grammar, clarity, and scientific style before submission. | **PENDING FULL DRAFT** | Section 1 edited; full manuscript proofreading required upon completion of Sections 2–8. |
| **7** | **Attribution for Reused Figures** | Elsevier Policy | Any reused diagram or figure from previous literature must cite the original source with appropriate copyright permission. | **PENDING FINAL INSPECTION** | All current figures are original vector charts from project benchmark data; final manuscript inspection required to verify zero uncredited assets. |
| **8** | **Portal Resubmission via "Edit" Option** | ICMLDE Submission System | Upload via the submission portal using the "Edit" function under Paper ID 1345, preserving historical submission records. Do not create a new submission. | **PROCEDURAL HOLD** | Portal upload reserved until author team approves final compiled document and scope inquiry is clarified. |
| **9** | **Strict File Naming Convention** | ICMLDE Decision Email | Revised manuscript file must be named strictly: `1345_revised_version.pdf` (or `.doc`/`.docx`). | **PLANNED** | Final compiled combined PDF will be exported with exact filename `1345_revised_version.pdf`. |
| **10** | **Notification Receipt Acknowledgement** | ICMLDE Decision Email | Acknowledge receipt of the decision notification in a separate email to `info@icmlde.org` upon receipt. Do **not** reply to automated notification emails. | **AUTHOR CONFIRMATION REQUIRED** | The author team must confirm whether receipt of the decision notification has been acknowledged via `info@icmlde.org`. |
| **11** | **Revision Window & Extension Option** | ICMLDE Decision Email | Verify the original notification timestamp and portal deadline. The standard 4-day revision window from ICMLDE 5.0 must be verified against current portal status. If expired or insufficient, request an extension. | **CRITICAL AUDIT ITEM** | Administrative inquiry in `ICMLDE_SCOPE_CHANGE_QUERY_DRAFT.md` covers portal status and provides basis for extension request if needed. |
| **12** | **Double-Blind Review Anonymity** | Conference Policy | Conditional on conference revision instructions: if revision undergoes secondary blind review, redact identities; otherwise provide unblinded details. | **CONDITIONAL** | Maintained anonymized block in draft; author team must confirm whether revision round requires double-blind anonymity or unblinded author list. |
| **13** | **Historical Archive Preservation** | Research Ethics Rule 4 | Historical manuscripts, raw data archives, and legacy code must be preserved intact without overwriting. | **VERIFIED** | Original `AgriRoute_ICMLDE.pdf` and templates preserved in dedicated version-controlled directories. |

---

## Detailed Step-by-Step Verification Protocol

### Phase A: Content and Scientific Verification (Pre-Compilation)
- [x] All 12 reviewer objections mapped with exact verbatim quotations.
- [x] All historical synthetic metrics (BiLSTM AUC = 1.000, XGBoost >95%, single-route demo) excluded from empirical claims.
- [x] Canonical benchmark figures verified: 13,465 evaluated image records (Kaggle: 227; FruitVision: 10,045; Sultana: 3,193).
- [x] Rejection arithmetic verified: FruitVision Known KRR = $41.98\%$ ($1,745/4,157$); Sultana Known KRR = $44.01\%$ ($525/1,193$); Pooled Partition B KRR = $42.43\%$ ($2,270/5,350$); Treatment UFAR-Fresh = $42.83\%$ ($821/1,917$).
- [x] Dual-Gate formula verified: $\text{ACCEPT}(x) \text{ iff } S_{\text{Energy}}(x) \ge \tau_{\text{Energy}} = 0.918451 \land S_{\text{MSP}}(x) \ge \tau_{\text{MSP}} = 0.582610$; $\text{REJECT otherwise.}$

### Phase B: LaTeX manuscript compilation and verification
- [ ] Preserve the DOCX manuscript as an archival fallback only.
- [ ] Complete manuscript drafting across Sections 2 (`02_related_work.tex`) through 8 (`08_conclusion.tex`).
- [ ] Comprehensive English language proofreading and editing across all sections.
- [ ] Compile full manuscript to PDF with zero compilation warnings or unresolved `?` cross-references.
- [ ] Inspect complete manuscript for Procedia template compliance and figure originality.
- [ ] Extract exact page numbers and line numbers for all 12 reviewer responses.
- [ ] Generate combined PDF combining the point-by-point response report and revised manuscript. (Note: Pagination must be determined from the final assembled PDF; no assumed page ranges are asserted).

### Phase C: Similarity and Compliance Auditing (Pre-Submission)
- [ ] Run Turnitin / iThenticate similarity scan (including full text per instructions).
- [ ] Verify similarity score $\le 10\%$. (Do not assert or report any similarity figure until tool output is generated).
- [ ] Export similarity report as PDF (`1345_similarity_report.pdf`).
- [ ] Verify file size and typography against Elsevier Procedia specifications.

### Phase D: Administrative Portal Resubmission
- [ ] Verify notification receipt acknowledgement email sent to `info@icmlde.org`.
- [ ] Clarify scope change and revision window status via `info@icmlde.org`; request extension if needed.
- [ ] Confirm double-blind policy for revision round with organizers.
- [ ] Log in to ICMLDE portal and select "Edit" on Paper ID 1345.
- [ ] Upload primary file: `1345_revised_version.pdf`.
- [ ] Upload supplementary file: `1345_similarity_report.pdf`.
- [ ] Confirm submission completion with conference secretariat via `info@icmlde.org`.

---

*This checklist must be updated as each phase is executed.*
