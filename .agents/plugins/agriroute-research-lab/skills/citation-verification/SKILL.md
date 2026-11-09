---
name: citation-verification
description: Programmatically verify manuscript citations, DOIs, metadata, and citation context to prevent hallucinated references or misattributed claims.
---

# Objective
Perform an exhaustive verification audit on all citations and bibliographic references in the AgriRoute manuscript. Guarantee that every referenced paper exists, metadata is accurate, and the text accurately reflects the cited source's empirical findings.

# Workflow

1. **Extract In-Text Citations:**
   - Parse manuscript source files (`.tex`, `.md`, or `.docx`) for all citation keys or bracketed numbers `[1..N]`.
   - Map each citation key to its BibTeX entry.
2. **Verify DOI and Metadata via Scholarly APIs:**
   - Query Crossref API / OpenAlex API using the recorded DOI.
   - Cross-check:
     - Exact title match (case-insensitive, ignoring punctuation).
     - Author list (first author surname and full co-author list).
     - Publication venue (journal or conference name).
     - Year of publication, volume, issue, and page numbers.
   - Flag any citation without an authentic, resolvable DOI.
3. **Verify Claim Attribution:**
   - Inspect the sentence in the manuscript citing the reference.
   - Verify that the cited paper actually supports the asserted claim (e.g., if claiming "Smith et al. achieved 94% on strawberries", confirm that Smith et al. studied strawberries, not apples).
   - Flag misattributions or overgeneralizations.
4. **Clean and Standardize BibTeX:**
   - Format entries following Elsevier / Procedia Computer Science guidelines.
   - Remove duplicate keys, fix special character escapes, and ensure clean journal abbreviations.
5. **Generate Verification Audit Report:**
   - Record results in `research_memory/reference_library_index.md`.
   - Mark each entry as `VERIFIED_ACTIVE`, `METADATA_CORRECTED`, or `UNRESOLVED_FLAGGED`.

