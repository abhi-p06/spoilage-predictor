---
name: scientific-figure-generation
description: Generate publication-quality vector charts, multi-panel comparison figures, calibration curves, and network diagrams complying with Elsevier / Procedia guidelines.
---

# Objective
Create high-resolution, vector-quality scientific visualizations and diagrams for the revised AgriRoute manuscript. Ensure visual clarity, accessibility (colorblind-friendly palettes), consistent typography, and compliance with Elsevier Procedia formatting rules.

# Workflow

1. **Adhere to Elsevier / Procedia Formatting Standards:**
   - Single-column width: 90 mm (approx. 3.5 inches).
   - Double-column width: 180 mm (approx. 7.1 inches).
   - Minimum font size in figures: 8 pt (labels and ticks), 10 pt (axis titles).
   - Fonts: Helvetica, Arial, or Computer Modern (matching LaTeX body text).
   - Format: Vector graphics (`.pdf` or `.eps`) preferred for charts; uncompressed high-DPI (`.png` $\ge 300$ DPI) for photographic Grad-CAM overlays.
2. **Color Palette Accessibility:**
   - Use perceptually uniform, colorblind-safe color schemes (e.g., `viridis`, `cividis`, or ColorBrewer Set2 / Dark2).
   - Avoid red-green distinctions without distinct marker shapes (circles, squares, triangles) or line dashes.
3. **Generate Core Manuscript Visualizations:**
   - **Figure 1 (System Architecture):** End-to-end operational flow from packing-station vision capture to IoT in-transit telemetry, multi-modal risk engine, and graph rerouting.
   - **Figure 2 (Grad-CAM Qualitative Panels):** Side-by-side comparison of original RGB fruit image, convolutional heatmap, and overlay for fresh vs. spoiled classes.
   - **Figure 3 (Calibration Reliability Diagrams):** Expected vs. empirical accuracy across 10 bins before and after temperature scaling.
   - **Figure 4 (Multi-Model ROC & PR Curves):** Macro-averaged ROC and Precision-Recall curves with shaded 95% bootstrap confidence bands for MobileNetV2, EfficientNetB0, and ResNet50.
   - **Figure 5 (Ablation Sensitivity Curve):** Delivered economic value and spoilage rate plotted as a continuous function of fusion weight $\alpha \in [0, 1]$.
   - **Figure 6 (Dynamic Rerouting Scenario):** Geographic/graph visualization illustrating a baseline destination vs. in-transit diversion to a closer secondary market upon spoilage risk escalation.
4. **Export and Verification:**
   - Script generation using `matplotlib` / `seaborn` with strict deterministic parameters (`bbox_inches='tight'`, `dpi=300`).
   - Save source plotting scripts alongside rendered PDF/PNG artifacts in `figures/`.

