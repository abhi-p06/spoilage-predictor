---
name: manuscript-revision
description: Execute rigorous, section-by-section academic rewrites of the AgriRoute paper, integrating updated empirical evidence, addressing reviewer critiques, and preserving change logs.
---

# Objective
Perform comprehensive, coordinated revisions of the AgriRoute manuscript text, equations, tables, and figures. Elevate the paper to peer-reviewed publication standards while preserving original drafts and maintaining transparent version control.

# Workflow

1. **Pre-Revision Safeguards:**
   - Verify that the original submitted manuscript is backed up and untouched in an archive directory.
   - Work exclusively in a versioned revision directory (e.g., `manuscript_revision_v2/`).
2. **Systematic Section Revisions:**
   - **Title & Abstract:** Ensure the title accurately captures system scope; write a structured, objective abstract with verified quantitative metrics and explicit uncertainty bounds.
   - **Section 1 (Introduction):** Reframe research contributions around verified gaps. Frame the work honestly as a prototype multi-modal framework evaluated on benchmark data and simulated transit scenarios.
   - **Section 2 (Related Work):** Incorporate the SOTA comparison matrix. Cite modern 2022–2026 references on post-harvest vision, IoT cold chain, and perishable routing.
   - **Section 3 (Proposed Methodology):**
     - Formalize image classification, sensor modeling, multi-modal risk calculation, and graph routing equations.
     - Eliminate undefined notations or phantom variables.
     - Justify fusion weighting with sensitivity analysis.
   - **Section 4 (Experimental Setup):**
     - Detail dataset provenance, group-aware split hygiene, and leakage prevention.
     - Document baseline architectures, hyperparameter configurations, and evaluation metrics.
   - **Section 5 (Results and Discussion):**
     - Present the vision backbone benchmark (MobileNetV2 vs. EfficientNetB0 vs. ResNet50).
     - Report external cross-dataset generalization metrics.
     - Present probability calibration curves (ECE, Brier Score).
     - Present component ablation studies and fusion sensitivity analysis.
     - Provide Grad-CAM interpretability visualizations.
   - **Section 6 (Limitations & Threats to Validity):**
     - Transparently disclose prototype limitations: $N=0$ physical fleet trial, reliance on benchmark sensor sequences, surface vision latency relative to internal biochemical decay, and edge hardware constraints.
   - **Section 7 (Conclusion & Future Work):** Summarize findings and lay out a roadmap for physical field deployment trials.
3. **Log All Edits in Change Log:**
   - For every substantive edit, log the section, original text snippet, revised text snippet, rationale, and supporting evidence in `research_memory/manuscript_change_log.md`.

