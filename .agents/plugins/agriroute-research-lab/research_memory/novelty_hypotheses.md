# Novelty Hypotheses & Delineation of Contributions

This document defines the defensible, verifiable novelty claims of the revised AgriRoute paper, establishing clear boundaries between prior art and our empirical contributions.

---

## 1. What AgriRoute Is NOT (Scoping & Boundaries)
- **Not a New Deep Learning Backbone:** AgriRoute does not invent a novel convolutional kernel, attention mechanism, or neural architecture. It utilizes established vision backbones (MobileNetV2, EfficientNetB0, ResNet50) adapted via transfer learning.
- **Not a Proven Commercial Deployment:** AgriRoute is not yet deployed across commercial transport fleets ($N=0$ physical fleet trials). It is a validated software prototype and algorithmic framework evaluated on benchmark data and simulated transit scenarios.
- **Not a Biochemical Spoilage Detector:** Surface RGB vision cannot detect internal enzymatic or anaerobic respiration shifts that precede visual surface lesions.

---

## 2. Delineated Novelty Hypotheses

### Hypothesis 1: Closed-Loop Multi-Modal Risk Coupling
> **Claim:** Unlike prior agricultural systems that decouple packing-house visual sorting from downstream in-transit refrigeration monitoring, AgriRoute formalizes a closed-loop coupling mechanism where the initial visual decay state initializes the time-dependent degradation rate used by in-transit telemetry.
>
> **Evidence Required:** Mathematical formulation of the joint risk score $R_{transit}(t) = f(R_{vision}, \int_{0}^t \phi(T(\tau), H(\tau)) d\tau)$ and comparative ablation demonstrating superior arrival cargo preservation versus decoupled systems.

### Hypothesis 2: Calibrated Spoilage Risk in Dynamic Vehicle Routing
> **Claim:** Standard Vehicle Routing Problems under Perishability (DVRP-P) assume deterministic linear decay constants. AgriRoute integrates an empirical, calibrated probability score into the dynamic edge cost function, dynamically altering delivery destinations (diverting from distant primary markets to nearer processing facilities) when cumulative risk breaches salvage thresholds.
>
> **Evidence Required:** Empirical verification of Expected Calibration Error (ECE) reduction and simulation showing higher salvaged economic value compared to static shortest-path and uncalibrated routing.

### Hypothesis 3: Edge-Feasible Multi-Task Architecture
> **Claim:** A unified multi-task vision pipeline can accurately classify fruit type and freshness simultaneously on resource-constrained edge computing hardware (e.g. Raspberry Pi / NVIDIA Jetson) with sub-100ms latency, enabling real-time inspection at rural collection centers.
>
> **Evidence Required:** Profiling of parameter counts, FLOPs, and inference latency across CPU and embedded targets.

