#!/usr/bin/env python3
"""
scripts/gradcam_analysis.py
===========================
Gradient-weighted Class Activation Mapping (Grad-CAM) interpretability analysis
for MobileNetV2, EfficientNetB0, and ResNet50. Evaluates lesion localization
vs spurious background bias on True Positives, False Positives, and False Negatives.

Usage:
  python scripts/gradcam_analysis.py --config experiments/configs/mobilenet_v2.yaml
"""

import os
import sys
import argparse
import yaml
from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from train_vision_benchmark import get_preprocessor, set_seed

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_target_layer_name(backbone: str) -> str:
    """Identify penultimate convolutional layer for each backbone architecture."""
    if backbone == "MobileNetV2":
        return "out_relu"  # 7x7x1280 post-ReLU
    elif backbone == "EfficientNetB0":
        return "top_activation"  # 7x7x1280
    elif backbone == "ResNet50":
        return "conv5_block3_out"  # 7x7x2048
    else:
        raise ValueError(f"Unknown backbone: {backbone}")


def make_gradcam_heatmap(img_array: np.ndarray, model: Model, last_conv_layer_name: str, pred_index: int = None) -> np.ndarray:
    """Compute Grad-CAM heatmap for a single image array using intermediate tape watch."""
    base_model = None
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model):
            base_model = layer
            break

    if base_model is not None and last_conv_layer_name in [l.name for l in base_model.layers]:
        target_conv_layer = base_model.get_layer(last_conv_layer_name)
        feature_extractor = Model(inputs=base_model.input, outputs=target_conv_layer.output)
        idx = base_model.layers.index(target_conv_layer)
        remaining_base = base_model.layers[idx + 1:]
        remaining_top = model.layers[model.layers.index(base_model) + 1:]

        with tf.GradientTape() as tape:
            conv_outputs = feature_extractor(img_array)
            tape.watch(conv_outputs)
            x = conv_outputs
            for l in remaining_base:
                x = l(x)
            for l in remaining_top:
                x = l(x)
            predictions = x
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            class_channel = predictions[:, pred_index]

        grads = tape.gradient(class_channel, conv_outputs)
    else:
        target_conv_layer = model.get_layer(last_conv_layer_name)
        feature_extractor = Model(inputs=model.input, outputs=target_conv_layer.output)
        idx = model.layers.index(target_conv_layer)
        remaining_top = model.layers[idx + 1:]

        with tf.GradientTape() as tape:
            conv_outputs = feature_extractor(img_array)
            tape.watch(conv_outputs)
            x = conv_outputs
            for l in remaining_top:
                x = l(x)
            predictions = x
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            class_channel = predictions[:, pred_index]

        grads = tape.gradient(class_channel, conv_outputs)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
    return heatmap.numpy()


def overlay_gradcam(img_path: str, heatmap: np.ndarray, alpha: float = 0.4) -> Tuple[np.ndarray, np.ndarray]:
    """Superimpose heatmap on original RGB image."""
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img_rgb.shape[:2]

    # Resize heatmap to match image dimensions
    heatmap_resized = cv2.resize(heatmap, (w, h))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)

    # Colorize heatmap
    color_map = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    color_map_rgb = cv2.cvtColor(color_map, cv2.COLOR_BGR2RGB)

    # Blend
    superimposed = cv2.addWeighted(img_rgb, 1 - alpha, color_map_rgb, alpha, 0)
    return img_rgb, superimposed


def run_gradcam_analysis(config_path: str):
    """Generate Grad-CAM interpretability visualizations for TP, FP, and FN samples."""
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg.get("seed", 42))

    model_path = PROJECT_ROOT / cfg["paths"]["checkpoint_dir"] / "best_model.keras"
    model = load_model(str(model_path))
    backbone = cfg["backbone"]
    classes = cfg["data"]["classes"]
    target_layer = get_target_layer_name(backbone)
    preprocess_fn = get_preprocessor(backbone)
    input_size = tuple(cfg["data"]["input_resolution"][:2])

    print(f"🔍 Running Grad-CAM for {backbone} using layer '{target_layer}'...")

    # Load internal test predictions
    preds_csv = PROJECT_ROOT / cfg["paths"]["log_dir"] / "predictions_internal_test.csv"
    manifest_csv = PROJECT_ROOT / cfg["data"]["test_internal_manifest"]

    df_preds = pd.read_csv(preds_csv)
    df_manifest = pd.read_csv(manifest_csv)
    df_merged = pd.concat([df_manifest.reset_index(drop=True), df_preds[["y_true", "y_pred"]]], axis=1)

    # Identify samples: True Positives, False Positives, False Negatives
    tp_samples = df_merged[df_merged["y_true"] == df_merged["y_pred"]].head(4)
    fp_samples = df_merged[df_merged["y_true"] != df_merged["y_pred"]].head(4)

    fig_dir = PROJECT_ROOT / cfg["paths"]["figures_dir"]
    fig_dir.mkdir(parents=True, exist_ok=True)

    samples_to_plot = []
    for _, row in tp_samples.iterrows():
        samples_to_plot.append((row, "True Positive"))
    for _, row in fp_samples.iterrows():
        samples_to_plot.append((row, "Misclassification (FP/FN)"))

    if not samples_to_plot:
        print("No samples available to visualize.")
        return

    n_samples = len(samples_to_plot)
    fig, axes = plt.subplots(n_samples, 3, figsize=(10, 3 * n_samples))
    if n_samples == 1:
        axes = np.expand_dims(axes, 0)

    for i, (row, category) in enumerate(samples_to_plot):
        fpath = row["filepath"]
        true_cls = classes[int(row["y_true"])]
        pred_cls = classes[int(row["y_pred"])]

        # Prepare image tensor for model
        raw_img = load_img(fpath, target_size=input_size)
        img_arr = img_to_array(raw_img)
        img_tensor = np.expand_dims(img_arr, axis=0)
        img_preprocessed = preprocess_fn(img_tensor.copy())

        heatmap = make_gradcam_heatmap(img_preprocessed, model, target_layer, pred_index=int(row["y_pred"]))
        orig_rgb, superimposed = overlay_gradcam(fpath, heatmap)

        # Plot Original
        axes[i, 0].imshow(orig_rgb)
        axes[i, 0].set_title(f"Original: {true_cls}\n({category})", fontsize=9)
        axes[i, 0].axis("off")

        # Plot Heatmap
        im = axes[i, 1].imshow(heatmap, cmap="viridis")
        axes[i, 1].set_title(f"Grad-CAM Activation\nLayer: {target_layer}", fontsize=9)
        axes[i, 1].axis("off")

        # Plot Superimposed
        axes[i, 2].imshow(superimposed)
        axes[i, 2].set_title(f"Pred: {pred_cls}\n(Superimposed)", fontsize=9)
        axes[i, 2].axis("off")

    plt.suptitle(f"Grad-CAM Attention Analysis: {cfg['model_name']} ({backbone})", fontsize=12, y=1.002)
    plt.tight_layout()
    gradcam_save_path = fig_dir / "gradcam_analysis.png"
    plt.savefig(gradcam_save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Grad-CAM visualization saved to {gradcam_save_path}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grad-CAM Interpretability Analysis")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    args = parser.parse_args()
    run_gradcam_analysis(args.config)

