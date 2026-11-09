# Research Questions

The AgriRoute revision is structured around four core research questions (RQs) designed to directly resolve reviewer objections and establish scientifically rigorous contributions:

---

### RQ1: Comparative Vision Architecture Performance & Efficiency
> **Question:** How do lightweight edge convolutional architectures (MobileNetV2, EfficientNetB0) compare against standard deep residual networks (ResNet50) in terms of classification accuracy, macro F1, parameter footprint, and inference latency when classifying post-harvest fruit decay under identical training protocols?
>
> **Hypothesis:** EfficientNetB0 will achieve competitive or superior macro F1 relative to ResNet50 while retaining a parameter count and inference latency viable for edge IoT deployment in refrigerated transport units.
>
> **Evaluation Plan:** Unified benchmark across identical group-aware splits; 95% bootstrap confidence intervals; FLOPs and latency profiling on CPU and GPU.

---

### RQ2: Out-of-Distribution Generalization & Visual Attribution
> **Question:** To what extent do models trained on curated laboratory fruit datasets generalize to out-of-distribution external datasets collected under variable lighting, natural backgrounds, and distinct cultivars, and do convolutional attention heatmaps localize to authentic biological decay?
>
> **Hypothesis:** Zero-shot cross-dataset evaluation will exhibit measurable domain degradation ($\Delta \text{F1} \approx 10\text{--}25\%$), primarily driven by background clutter and illumination shifts; Grad-CAM analysis will demonstrate whether early-stage rot localization remains biologically faithful across domains.
>
> **Evaluation Plan:** Cross-dataset evaluation on independent external datasets; Grad-CAM visualization across true positive and failure cohorts.

---

### RQ3: Multi-Modal Spoilage Risk Fusion & Weight Sensitivity
> **Question:** Does combining pre-dispatch visual freshness state with in-transit environmental sensor telemetry provide a statistically significant reduction in post-harvest spoilage risk over uni-modal baselines, and what is the optimal fusion weighting between visual inspection and sensor history?
>
> **Hypothesis:** Joint multi-modal risk estimation outperforms vision-only and sensor-only estimators across simulated transit disturbances; the objective cost curve possesses a clear convex minimum across the fusion parameter $\alpha \in [0, 1]$.
>
> **Evaluation Plan:** Component ablation study across 20 diverse transit topologies; systematic parameter sweep of fusion weight $\alpha$; Wilcoxon signed-rank significance testing.

---

### RQ4: Probability Calibration in Risk-Aware Dynamic Routing
> **Question:** How does post-hoc probability calibration (e.g. Temperature Scaling, Platt Scaling) affect the Expected Calibration Error (ECE) of spoilage predictors, and does calibrating risk scores prevent premature or suboptimal route diversion in dynamic routing engines?
>
> **Hypothesis:** Raw softmax confidence scores are overconfident, resulting in inflated false rerouting decisions; probability calibration reduces ECE significantly and stabilizes dynamic dispatch thresholds under real-world perishability constraints.
>
> **Evaluation Plan:** ECE and Brier score evaluation on held-out validation data before and after calibration; comparative route cost and cargo salvage value simulation.

