---
name: gradcam-analysis
description: Generate and analyze Gradient-weighted Class Activation Mapping (Grad-CAM) heatmaps across fruit samples to verify anatomical localization of spoilage symptoms and detect background bias.
---

# Objective
Produce Gradient-weighted Class Activation Mapping (Grad-CAM) visualizations for convolutional feature maps to provide visual interpretability. Verify whether models focus on biological decay indicators (mold, skin necrosis, bruising) or spurious background artifacts (trays, labels, studio corners).

# Workflow

1. **Target Layer Selection:**
   - Identify the penultimate convolutional layer for each backbone:
     - MobileNetV2: `Conv_1` or last inverted residual block.
     - EfficientNetB0: `top_conv` or last MBConv block.
     - ResNet50: `conv5_block3_out`.
2. **Compute Gradient Activations:**
   - Forward pass input image through the network.
   - Compute gradient of score for target class $c$ ($y^c$) with respect to feature activation map $A^k$:
     $$\alpha_k^c = \frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^c}{\partial A_{i,j}^k}$$
   - Take weighted combination followed by ReLU:
     $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k^c A^k\right)$$
3. **Heatmap Overlay & Preprocessing:**
   - Bilinearly upsample $L_{\text{Grad-CAM}}^c$ to match input image resolution ($224 \times 224$).
   - Apply Jet / Turbo colormap and alpha-blend (typically $\alpha=0.4$) over original RGB image.
4. **Structured Qualitative Error Audit:**
   - Generate Grad-CAM for a curated cohort:
     - 10 True Positives (Fresh classified as Fresh).
     - 10 True Positives (Rotten classified as Rotten).
     - 10 False Positives (Fresh classified as Rotten).
     - 10 False Negatives (Rotten classified as Fresh).
   - Evaluate whether attention focuses on:
     - Biological lesions (stem necrosis, soft rot, surface bruising).
     - Irrelevant cues (shadows, background surface texture, camera reflections).
5. **Compile Figure Panels:**
   - Save high-resolution comparative composite figures for the manuscript.
   - Record visual audit notes in `research_memory/model_comparison_matrix.md`.

