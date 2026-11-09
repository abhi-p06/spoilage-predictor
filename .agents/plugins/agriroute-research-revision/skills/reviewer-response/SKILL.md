---
name: reviewer-response
description: Prepare a point-by-point response to Reviewers 1–3, tied to verified changes, exact manuscript sections and final page/line numbers.
---

# Objective

Create a transparent reviewer response that makes it easy for reviewers to verify real corrections. Use only after the manuscript and relevant experiments have been updated.

# Rules

- Never say a change was made unless the revised manuscript contains it and the corresponding experiment/file exists.
- Keep `completed`, `partially completed`, and `not completed` distinct.
- If a request cannot be completed within the revision window, explain the limitation and the exact substitute evidence provided; do not pretend it was addressed.
- Do not invent page numbers. Use section/figure/table identifiers during drafting and replace with final page/line numbers after the template-rendered document is frozen.
- Preserve every reviewer comment verbatim in the response document. Respond respectfully and specifically.

# Mandatory response structure

For every comment, write:
1. Reviewer comment.
2. Response: a concise explanation of the action actually taken and scientific rationale.
3. Changes made: exact section/subsection, figure/table/equation, and final page/line reference.
4. Evidence: experiment name, dataset/source/version, result file, and reproducible script/notebook path where relevant.
5. Status: `Addressed`, `Partially addressed`, or `Not addressed (with reason)`.

# Required reviewer coverage

Reviewer 1:
- Define fusion score and decision mapping in abstract and methods.
- Explain whether the contribution goes beyond component integration.
- Audit/remove or replace the artificial-sequence BiLSTM AUC=1.000.
- Add a fair state-of-the-art comparison.
- Report real field results separately from repository/software tests.

Reviewer 2:
- Explain the selection and evidence behind fusion weights; include sensitivity/ablation.
- Remove all incomplete author-role or drafting notes, including `Specific roles can be updated before submission`.
- Validate freshness on suitable public fruit-quality datasets with compatible labels and a defensible external test.

Reviewer 3:
- State the exact contribution and evidence, or narrow the claim.
- Report independent shipment count and limits; do not treat one demonstration as broad validation.
- Add a sourced comparison table against relevant agri-logistics platforms.
- Include a prospective field protocol with outcomes, data collection, sampling, and evaluation plan.

# Deliverables

- `reviewer_response_draft.md` with no invented page numbers.
- `reviewer_change_checklist.md` with a pass/fail evidence gate for each comment.
- After final pagination, a response file with the exact page-by-page and line-by-line mapping requested by the committee.
