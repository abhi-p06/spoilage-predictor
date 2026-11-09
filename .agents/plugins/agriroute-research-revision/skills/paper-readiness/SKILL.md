---
name: paper-readiness
description: Run a final scientific, editorial, citation, figure, similarity, AI-disclosure and Procedia Computer Science submission-readiness check.
---

# Objective

Check that the final revised paper is complete, internally consistent, properly sourced, and prepared in the required conference/publisher template.

# Checks

## Scientific completeness
- Abstract states the problem, approach, meaning of fusion score, decision outputs, actual validation data, and measured results without overstating them.
- Introduction states the specific gap and research questions, not only system features.
- Related work compares directly relevant studies and clearly separates peer-reviewed research from commercial platform descriptions.
- Methods fully define datasets, labels, image preprocessing, splits, models, fusion formula, weight selection, thresholds, route objective, baselines, and field protocol.
- Results are reproducible and agree with saved outputs. The abstract, tables, figures, discussion and conclusion use identical numbers.
- Discussion explains failures, dataset shift, limits, uncertainty, and the difference between simulation and field evidence.
- Conclusion reports actual field data if collected; otherwise explicitly says no multi-shipment field validation was completed and gives a realistic next-stage evaluation plan.

## Editorial completeness
- Remove placeholders, draft notes, unresolved roles, TODO markers, comments, tracked changes, and inconsistent author information.
- Proofread English for grammar, terminology, tense, clarity, and consistency. Do not change scientific meaning.
- Verify every figure/table is cited in the text and every borrowed/adapted visual has a proper citation and permission/licence where required.
- Confirm all equations, symbols, abbreviations, units, acronyms and table/figure numbers are defined and consistent.
- Use the exact current conference template supplied for this submission; verify page limit, columns, margins, header/footer, captions, equations and references after exporting to PDF.

## References and similarity
- Verify every reference against the original publisher/DOI record. Check in-text citations ↔ reference list in both directions.
- Do not paraphrase merely to lower a similarity score. Cite reused content and rewrite the authors' own explanations in original language.
- Similarity must be checked with a legitimate institutional/licensed tool if available. Do not promise or engineer a particular score.

## AI disclosure
- Check the current applicable Elsevier and conference rules. If generative AI materially changed manuscript wording or structure, include the required disclosure statement. If AI helped with research design, code, analysis or interpretation, describe that use in Methods where applicable. Authors must verify and take responsibility.
- Do not include a disclosure statement that falsely describes how tools were used. Use actual tools and actual purposes.

## Submission package
- One final manuscript/reviewer-response file in the requested order and filename `1345_revised_version` (confirm file extension and portal instructions).
- Similarity report as a separate supplementary file.
- Preserve the original portal files; upload a new version as instructed.
- Acknowledge the decision email through the designated contact address, not by replying to a no-reply sender.
- Confirm the exact resubmission deadline and time zone with the conference before assuming the 4-day window's cutoff.

# Output

Produce a checklist with `PASS`, `FAIL`, or `NOT VERIFIED`, exact file/page evidence, and a short blocking-issues section. Do not label the paper ready while any critical scientific validity item remains `FAIL` or `NOT VERIFIED`.
