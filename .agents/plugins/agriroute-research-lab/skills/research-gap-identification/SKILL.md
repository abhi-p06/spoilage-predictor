---
name: research-gap-identification
description: Synthesize literature search findings to identify critical empirical gaps, define precise novelty hypotheses, and construct rigorous state-of-the-art comparison matrices.
---

# Objective
Analyze the surveyed literature to establish genuine, defensible research gaps that AgriRoute addresses. Ground the paper's claims in authentic incremental advancements rather than inflated claims of global novelty.

# Workflow

1. **Construct Multi-Dimensional Comparison Matrix:**
   - Map competing systems across key capability dimensions:
     - Modality: Vision-only vs. Sensor-only vs. Joint Multi-Modal.
     - Spoilage Model: Static classification vs. Temporal progression vs. Dynamic decay kinetics.
     - Decision Coupling: Standalone diagnosis vs. Closed-loop dynamic routing / dispatch.
     - Validation: Controlled lab images vs. In-situ field imagery.
     - Calibration & Uncertainty: Deterministic thresholding vs. Calibrated probabilistic risk.
2. **Identify Primary Gaps in Prior Work:**
   - *Gap 1 (Decoupled Systems):* Existing systems perform either post-harvest vision sorting at packing facilities OR transit tracking via IoT data loggers, rarely coupling real-time vision state with transit routing.
   - *Gap 2 (Uncalibrated Scores in Decision Models):* Prior agricultural routing systems assume known linear shelf-life decay constants, failing to account for empirical prediction uncertainty.
   - *Gap 3 (Computational Feasibility):* High-accuracy vision transformers require heavy GPU resources incompatible with edge IoT gateways in transport refrigerated units (TRUs).
3. **Formulate Novelty Hypotheses:**
   - Draft testable, bounded novelty statements in `research_memory/novelty_hypotheses.md`.
   - Ensure claims avoid unsupported superlatives ("first ever", "unprecedented", "flawless").
4. **Link to Paper Sections:**
   - Integrate comparison matrix into Section 2 (Related Work).
   - Anchor the Introduction around verified research gaps.

