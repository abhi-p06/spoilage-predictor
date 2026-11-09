---
name: fruit-classification-benchmark
description: Train, evaluate, and benchmark multiple vision backbones (MobileNetV2, EfficientNetB0, ResNet50) under identical training protocols and compute comparative performance metrics.
---

# Objective
Implement and execute a rigorous comparative benchmark of standard convolutional neural network architectures for post-harvest fruit freshness classification. Establish empirical trade-offs between classification performance, model complexity, and inference latency.

# Workflow

1. **Benchmark Model Suite:**
   - Implement three canonical architectures with identical input resolution ($224 \times 224$):
     - **MobileNetV2:** Edge baseline optimized for low-power IoT gateways.
     - **EfficientNetB0:** High-efficiency compound scaling benchmark.
     - **ResNet50:** Standard deep residual network benchmark.
2. **Unified Training Protocol:**
   - Standardize training conditions:
     - Optimizer: Adam or AdamW ($\beta_1=0.9, \beta_2=0.999$, weight decay $= 10^{-4}$).
     - Learning Rate Schedule: Cosine annealing or ReduceLROnPlateau with warm-up.
     - Batch Size: 32.
     - Transfer Learning: Pre-trained ImageNet weights; train top classification head for $E_{head}$ epochs, then fine-tune top convolutional blocks for $E_{fine}$ epochs.
     - Identical data augmentation pipeline across all models.
3. **Multi-Metric Evaluation:**
   - Compute comprehensive test metrics on leakage-free test partition:
     - Top-1 Accuracy.
     - Macro-Averaged Precision, Recall, and F1-Score.
     - Multi-Class Area Under ROC Curve (One-vs-Rest Macro AUC).
     - Brier Score and Expected Calibration Error (ECE).
4. **Computational Efficiency Profiling:**
   - Parameter Count (Total and Trainable parameters in Millions).
   - Multiply-Accumulate Operations (FLOPs / MACs).
   - Average Inference Latency (milliseconds per image on CPU and GPU over 1,000 runs).
   - Peak RAM / VRAM memory consumption.
5. **Output Synthesis:**
   - Generate LaTeX comparison table formatted for Procedia Computer Science.
   - Record results in `research_memory/model_comparison_matrix.md`.

