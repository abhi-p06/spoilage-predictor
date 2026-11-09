---
name: audit-reviewer-comments
description: Ingest, categorize, and cross-reference peer review comments into an actionable research objection register with strict traceability to experiments and paper sections.
---

# Objective
Deconstruct all peer review feedback from Reviewers 1, 2, and 3 into discrete, traceable atomic critique items. Map each objection to required empirical experiments, manuscript sections, code locations, and severity ratings.

# Workflow

1. **Ingest Review Comments:**
   - Read reviewer feedback files or transcripts.
   - Separate overarching editorial comments from specific technical objections.
2. **Deconstruct into Atomic Objections:**
   - Break compound paragraphs down into single, testable critique items (e.g., separate "synthetic data is unrealistic" from "AUC=1.000 implies target leakage").
   - Assign a unique identifier to each objection (e.g., `REV1-OBJ01`, `REV2-OBJ03`).
3. **Categorize by Research Dimension:**
   - `Novelty & Literature`: Gaps in comparison with modern SOTA (2022–2026).
   - `Data & Leakage`: Synthetic generation artifacts, image split contamination, lack of provenance.
   - `Evaluation & Baselines`: Unrealistic metrics (AUC=1.000), absence of error bars, missing baseline models.
   - `Multi-Modal Fusion`: Arbitrary fusion weights ($\alpha, \beta$), lack of optimization or sensitivity analysis.
   - `Field Viability & Systems`: Lack of real-world deployment, sensor latency, biological decay lag.
4. **Determine Required Resolution Strategy:**
   - **Empirical Experiment:** Requires retraining, benchmarking, or new statistical testing.
   - **Textual Clarification / Reframing:** Requires honest scoping, limitation disclosure, or methodological rewrites.
   - **Literature Comparison:** Requires citation addition and tabular feature benchmarking.
5. **Populate the Objection Register:**
   - Record findings in `research_memory/reviewer_objections.md`.
   - Assign ownership to relevant agents (`computer-vision-researcher`, `data-integrity-auditor`, `statistical-methodologist`, etc.).

