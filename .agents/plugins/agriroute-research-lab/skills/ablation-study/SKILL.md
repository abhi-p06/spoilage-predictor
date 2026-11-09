---
name: ablation-study
description: Systematically isolate and evaluate the individual contributions of vision, sensor, fusion weighting, and routing components within the AgriRoute architecture.
---

# Objective
Execute systematic ablation experiments to isolate the value added by each modular component of the AgriRoute architecture. Directly address reviewer critiques demanding empirical justification for multi-modal fusion and dynamic rerouting.

# Workflow

1. **Define Core Ablation Configurations:**
   - **Configuration A (Static Baseline):** Shortest-path routing (standard Dijkstra on distance) without perishability awareness or sensor integration.
   - **Configuration B (Vision-Only Risk):** Route optimization using only visual freshness classification scores ($R_{vision}$), setting sensor weight $\beta = 0$.
   - **Configuration C (Sensor-Only Risk):** Route optimization using only time-series cold-chain sensor predictions ($R_{sensor}$), setting vision weight $\alpha = 0$.
   - **Configuration D (Unweighted Fusion):** Multi-modal risk with naive equal weighting ($\alpha = 0.5, \beta = 0.5$).
   - **Configuration E (Proposed AgriRoute Multi-Modal):** Calibrated multi-modal risk with optimized fusion weights ($\alpha^*, \beta^*$).
   - **Configuration F (Dynamic Rerouting Enabled):** Dynamic in-transit waypoint re-optimization upon simulated temperature-abuse events.
2. **Standardize Evaluation Simulation Scenarios:**
   - Define a fixed suite of benchmark routing scenarios:
     - 20 synthetic / benchmark transit graphs (varying origin-destination distances, market nodes, perishable cargo decay rates).
     - Controlled thermal abuse injection (e.g., sudden refrigeration breakdown at $t = t_{mid}$).
3. **Compute Comparative Impact Metrics:**
   - **Estimated Spoilage Rate (% cargo lost upon arrival).**
   - **Total Transport Distance / Cost (km / fuel equivalent).**
   - **Delivered Economic Value ($ / kg perishable salvage value).**
   - **Decision Flip Frequency (% of routes where multi-modal state altered destination).**
4. **Sensitivity Analysis over Fusion Weights:**
   - Sweep $\alpha \in [0.0, 1.0]$ in increments of $0.05$ (with $\beta = 1 - \alpha$).
   - Plot objective cost vs. $\alpha$ to justify the chosen operating point empirically.
5. **Generate Ablation Summary Table:**
   - Format results into LaTeX ablation table.
   - Record findings in `research_memory/claims_evidence_ledger.md`.

