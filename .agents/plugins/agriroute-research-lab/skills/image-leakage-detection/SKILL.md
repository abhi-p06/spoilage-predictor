---
name: image-leakage-detection
description: Detect identical and near-duplicate images across train, validation, and test splits using MD5 checksums, perceptual hashing (pHash), and metadata group auditing.
---

# Objective
Detect and eliminate data leakage between training, validation, and testing partitions in fruit image datasets. Ensure that identical fruits, video-burst frames, or augmented variants do not contaminate evaluation splits.

# Workflow

1. **Exact Duplicate Detection:**
   - Compute MD5 hashes for all images across all dataset partitions.
   - Flag any identical file hashes present in both `train` and `test` or `val` and `test`.
2. **Perceptual Near-Duplicate Detection (pHash):**
   - Compute 64-bit Perceptual Hash (pHash) or Difference Hash (dHash) for every image.
   - Perform pairwise Hamming distance comparison across partition boundaries.
   - Flag image pairs with Hamming Distance $\le 4$ as probable near-duplicates (e.g., identical fruit with slight rotation, slight crop, or consecutive burst capture).
3. **Audit Grouping & Session Lineage:**
   - Analyze file naming conventions and capture timestamps.
   - Identify whether images from the same harvest batch, background tray, or capture session are split randomly across train and test.
   - Flag instances of IID random splitting where grouped splitting should have been enforced.
4. **Leakage Remediation Protocol:**
   - Quarantine leaking test instances.
   - Construct a strict Group-Aware Split: all frames/crops from a given fruit instance or session must reside entirely in either train, val, or test.
   - Recompute clean partition sizes and log audit results in `research_memory/claims_evidence_ledger.md`.

