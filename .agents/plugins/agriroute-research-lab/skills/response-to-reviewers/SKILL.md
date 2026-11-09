---
name: response-to-reviewers
description: Draft comprehensive, respectful, point-by-point rebuttal responses to peer reviewers, linking every objection to verified experiments, updated text, and line numbers.
---

# Objective
Generate an exhaustive, highly structured, and collegial point-by-point response letter to the editor and reviewers. Demonstrate that every comment, critique, and suggestion has been thoroughly addressed with concrete empirical evidence and manuscript updates.

# Workflow

1. **Rebuttal Document Structure:**
   - **Executive Summary:** Express gratitude to the editors and reviewers for their constructive insights; summarize major enhancements made during revision:
     - De-biasing and leakage auditing of dataset partitions.
     - Multi-model benchmarking (MobileNetV2, EfficientNetB0, ResNet50) with 95% CIs.
     - External cross-dataset generalization evaluation.
     - Mathematical justification and sensitivity analysis of multi-modal fusion weights.
     - Extensive ablation studies and probability calibration (ECE / Brier Score).
     - Transparent framing of prototype status and field deployment design.
2. **Point-by-Point Item Structure:**
   - For every reviewer critique item (referenced by its ID from `research_memory/reviewer_objections.md`):
     - **Reviewer Comment:** Quote the reviewer's exact comment in an italicized blockquote.
     - **Author Response:** Provide a direct, polite, and detailed explanation of the authors' response and scientific rationale.
     - **Manuscript Modification:** Cite exact section numbers, page numbers, line numbers, and figure/table numbers where changes were incorporated.
     - **Explanatory Snippet / Data Table:** Insert the exact revised text excerpt, LaTeX table snippet, or figure reference directly within the response document so reviewers do not have to hunt for changes.
3. **Handle Disagreements with Evidence:**
   - Where a reviewer's assumption differs from experimental reality, respond with rigorous scientific literature citations and empirical benchmark data rather than defensive dismissals.
4. **Editorial & Formatting Compliance:**
   - Ensure clear visual distinction between reviewer remarks, author responses, and revised manuscript excerpts (e.g., using shaded boxes or colored headings in LaTeX/Markdown).

