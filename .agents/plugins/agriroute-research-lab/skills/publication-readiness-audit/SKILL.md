---
name: publication-readiness-audit
description: Final comprehensive pre-submission audit checking text integrity, author metadata, reference resolution, figure resolution, mathematical consistency, and ethics/AI disclosures.
---

# Objective
Conduct a final, rigorous forensic pre-submission audit on the complete revised manuscript package. Verify that all claims are backed by evidence, placeholders are eliminated, formatting matches target journal guidelines, and ethical/AI-disclosure declarations are fully compliant.

# Workflow

1. **Placeholder & Draft Artifact Scan:**
   - Run automated regex scans across manuscript source files for:
     - Placeholder tags: `TODO`, `TBD`, `XXX`, `[?]`, `can be updated`, `sample value`, `before submission`, `dummy`, `FIXME`.
     - Undefined references: `??`, `\ref{?}`, `\cite{?}`, `Error! Reference source not found`.
2. **Mathematical & Notation Consistency Check:**
   - Verify that every variable, parameter, and index used in equations is formally defined in the text.
   - Confirm dimensional consistency (e.g., matrix dimensions, risk score bounded intervals $[0, 1]$).
   - Ensure consistent symbol use across all sections (e.g., avoid using $R$ for both risk score and graph route).
3. **Figure and Table Verification:**
   - Verify that every figure and table is explicitly referenced and discussed in the narrative.
   - Confirm that figure resolutions meet journal standards ($\ge 300$ DPI for bitmaps, vector for charts).
   - Ensure table notes explicitly state confidence interval levels (e.g., "Values reported as mean $\pm 95\%$ bootstrap CI").
4. **Citation & Bibliography Cross-Check:**
   - Ensure every cited key in the text exists in the bibliography.
   - Ensure no orphan references exist in the bibliography that are never cited in the text.
   - Confirm all external web URLs or software repositories are pinned to permanent archive releases or DOIs.
5. **Ethics, Data Availability, and Generative AI Disclosure:**
   - Include a clear **Data and Code Availability Statement** providing reproducible repository links.
   - Include an explicit **Generative AI Disclosure Statement** compliant with Elsevier / COPE guidelines (e.g., acknowledging AI tools used solely for editing, grammar, and scripting assistance, with full scientific responsibility held by the authors).
   - Verify author affiliations, conflict of interest statements, and funding acknowledgments.
6. **Issue Final Publication Readiness Certificate:**
   - Produce a final audit summary report.
   - Mark manuscript status as `READY_FOR_SUBMISSION` or detail remaining blockers.

