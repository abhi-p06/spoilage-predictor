---
name: cross-dataset-validation
description: Evaluate vision models across external, independently collected fruit datasets to quantify out-of-distribution generalization, domain shift degradation, and real-world robustness.
---

# Objective
Evaluate the generalization performance of AgriRoute fruit classification models on external, out-of-distribution (OOD) datasets collected under distinct environmental conditions, lighting, and camera sensors. Directly answer reviewer demands for external validation.

# Workflow

1. **Acquire & Prepare External Benchmarks:**
   - Ingest secondary external datasets (e.g., secondary Kaggle Fruit Freshness sets, real-world market images, or independent academic repositories).
   - Verify that test categories align with primary model ontology (e.g., map external class names to canonical classes: fresh/rotten apple, banana, orange).
2. **Execute Zero-Shot Out-of-Distribution Evaluation:**
   - Load pre-trained models without fine-tuning or retraining on the external dataset.
   - Run inference across the full external evaluation set.
   - Compute in-domain (test split) vs. out-of-domain (external dataset) performance drop:
     $$\Delta \text{F1} = \text{F1}_{\text{in-domain}} - \text{F1}_{\text{out-of-domain}}$$
3. **Analyze Domain Shift Vulnerabilities:**
   - Categorize failure modes:
     - Background interference (orchard soil, market stalls, plastic packaging vs. white studio backgrounds).
     - Illumination variance (direct sunlight, shadows, fluorescent warehouse lights).
     - Morphological variance (unseen cultivars, irregular fruit shapes, early-stage vs. late-stage rot).
4. **Domain Adaptation Sensitivity (Optional Probe):**
   - Perform few-shot linear probe calibration (retraining only the final dense layer on 5–10 external samples per class) to quantify how rapidly domain shift can be mitigated.
5. **Document Generalization Profile:**
   - Format results into cross-dataset generalization tables.
   - Record findings in `research_memory/model_comparison_matrix.md` and draft frank discussion of domain sensitivity for the manuscript.

