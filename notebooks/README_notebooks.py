"""
01_cnn_training — notebook preamble
=====================================
This file documents the CNN notebook structure.
Open notebooks/01_cnn_training.ipynb in Jupyter to run the full training.

The notebook contains these cells (in order):

  Cell 1  — Imports & config
  Cell 2  — Dataset verification (list image counts per class)
  Cell 3  — Build tf.data pipeline with augmentation
  Cell 4  — Build MobileNetV2 transfer learning model
  Cell 5  — Phase 1: Train top layers (frozen base)
  Cell 6  — Phase 2: Fine-tune last 30 layers
  Cell 7  — Plot training curves
  Cell 8  — Evaluate on validation set (accuracy, confusion matrix)
  Cell 9  — Save model → models/cnn_freshness.h5

Target: val_accuracy > 85%
Dataset: data/images/ (Kaggle Fresh & Rotten Fruits)
"""
