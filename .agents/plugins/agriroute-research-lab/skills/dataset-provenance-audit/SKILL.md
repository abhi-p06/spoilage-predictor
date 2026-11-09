---
name: dataset-provenance-audit
description: Forensic audit of training, validation, and test datasets, tracking upstream source repositories, download dates, licensing terms, checksums, and class distributions.
---

# Objective
Establish an airtight chain of custody and provenance record for every image and tabular dataset utilized in the AgriRoute system. Prevent licensing violations, undocumented preprocessing artifacts, and ambiguity regarding dataset origin.

# Workflow

1. **Inventory Raw Data Assets:**
   - Scan data directories (`data/`, `dataset/`, `raw_data/`).
   - Record total file counts, subdirectories, image formats (`.jpg`, `.png`), and tabular file sizes.
2. **Trace Upstream Provenance:**
   - Identify the canonical origin for each dataset component:
     - Primary Fruit Freshness dataset (e.g., Kaggle Fruit Fresh/Rotten, Kaggle Fruit 360).
     - External evaluation benchmark datasets.
     - Environmental sensor logs or simulation traces.
   - Record repository URL, original publication DOI, author/maintainer, and date accessed.
3. **Audit License & Terms of Use:**
   - Inspect dataset license terms (Creative Commons CC-BY, CC-BY-SA, CC0, MIT, or Non-Commercial restrictions).
   - Verify compatibility with academic publication and code release.
4. **Compute Cryptographic Checksums:**
   - Compute SHA-256 and MD5 hashes for all raw archive files and top-level directory manifests.
   - Store hashes in `research_memory/dataset_inventory.md` for reproducible verification across machines.
5. **Analyze Class Distributions & Metadata:**
   - Count raw sample counts per class (e.g., fresh apples, rotten apples, fresh bananas, rotten bananas, fresh oranges, rotten oranges).
   - Report class imbalance ratios and label naming conventions.
   - Check image metadata (EXIF data, resolution ranges, color depth, aspect ratios).

