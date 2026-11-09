---
name: audit-project-evidence
description: Perform a read-only forensic audit of the AgriRoute repository, manuscript, datasets, training scripts, checkpoints, logs and reported results. Use before changing the paper or code, especially after reviewer feedback.
---

# Objective

Establish what the project actually contains and which manuscript claims are supported. Do not modify files during this skill.

# Procedure

1. Inventory the workspace without traversing outside the project root. Record file paths, sizes, file types, timestamps where available, and likely roles. Identify the main manuscript, source code, notebooks, datasets, checkpoints, outputs, figures, tables, logs, requirements/environment files, and README/project notes.
2. Read the complete manuscript and any reviewer response drafts. Search for unfinished placeholders, including phrases such as `can be updated`, `before submission`, `TODO`, `TBD`, dummy author roles, sample values, and unexplained repository-level outputs.
3. Trace every reported experiment to code and raw inputs. For each result, identify the script/notebook, data source and version, preprocessing, split, random seed, checkpoint, metric implementation, and output file. Mark each item `VERIFIED`, `PARTIALLY VERIFIED`, or `NOT VERIFIED`.
4. Audit the BiLSTM sequence construction. Determine whether sequences are measured, simulated, interpolated, duplicated, or generated; inspect label-generation rules, train/test splitting, temporal leakage, and whether the same base examples appear across splits. Do not repeat or defend the AUC=1.000 without independent real data.
5. Audit the freshness model: fruit classes, freshness labels, class counts, image sources, image-level duplicates, augmentation lineage, preprocessing, split strategy, external test evidence, per-class metrics, and calibration. Flag any mismatch between model labels and the wording in the paper.
6. Audit routing and fusion: exact score formula, component units/ranges, normalization, weights, threshold selection, decision meanings, route objective, constraints, baseline comparators, market-data source and timestamp, and whether actual shipment outcomes are used.
7. Audit field claims: number of unique shipments, dates, origin/destination, fruit type, measured sensor fields, actual route observations, quality outcomes, missing data, and permission/privacy considerations. Separate live field measurements from simulated demonstrations and software tests.
8. Create a reviewer traceability matrix for every comment from Reviewers 1–3. Map each comment to evidence available, missing experiment, code location, manuscript section, and severity.

# Deliverables (save only new audit files in a new `revision_audit/` folder)

- `revision_audit/repository_inventory.md`
- `revision_audit/claim_evidence_ledger.csv`
- `revision_audit/reviewer_gap_matrix.md`
- `revision_audit/critical_validity_risks.md`
- `revision_audit/recommended_revision_sequence.md`

# Output format

Start with a concise executive assessment and the five highest-risk issues. For every finding, cite exact repository paths and line numbers or notebook cell identifiers where possible. Explicitly list what cannot be verified. End with the decisions the author must make before changes begin.
