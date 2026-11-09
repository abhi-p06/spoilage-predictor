#!/usr/bin/env python3
"""
scripts/calibrate_and_abstain.py
================================
Probability calibration (Temperature Scaling), Expected Calibration Error (ECE),
Brier score computation, reliability diagrams, and selective prediction (abstention).

Usage:
  python scripts/calibrate_and_abstain.py --config experiments/configs/mobilenet_v2.yaml
"""

import os
import sys
import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from scipy.special import softmax
from sklearn.metrics import brier_score_loss, log_loss, accuracy_score
from sklearn.preprocessing import label_binarize
import tensorflow as tf
from tensorflow.keras.models import load_model

from train_vision_benchmark import build_tf_dataset, set_seed

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def compute_ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 15) -> Tuple[float, float, List[Dict]]:
    """
    Compute Expected Calibration Error (ECE) and Maximum Calibration Error (MCE).
    """
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == labels)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    mce = 0.0
    bin_details = []

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            abs_diff = np.abs(avg_confidence_in_bin - accuracy_in_bin)
            ece += abs_diff * prop_in_bin
            mce = max(mce, abs_diff)
            bin_details.append({
                "bin_lower": float(bin_lower),
                "bin_upper": float(bin_upper),
                "count": int(np.sum(in_bin)),
                "accuracy": float(accuracy_in_bin),
                "confidence": float(avg_confidence_in_bin),
                "calibration_gap": float(abs_diff)
            })
        else:
            bin_details.append({
                "bin_lower": float(bin_lower),
                "bin_upper": float(bin_upper),
                "count": 0,
                "accuracy": 0.0,
                "confidence": float((bin_lower + bin_upper) / 2),
                "calibration_gap": 0.0
            })

    return float(ece), float(mce), bin_details


def compute_multiclass_brier(probs: np.ndarray, labels: np.ndarray, num_classes: int) -> float:
    """Compute multi-class Brier score."""
    y_true_bin = label_binarize(labels, classes=list(range(num_classes)))
    return float(np.mean(np.sum((probs - y_true_bin) ** 2, axis=1)))


def extract_logits_and_labels(model: tf.keras.Model, manifest_path: Path, config: Dict) -> Tuple[np.ndarray, np.ndarray]:
    """Extract pre-softmax logits or log probabilities from model."""
    data_cfg = config["data"]
    input_res = tuple(data_cfg["input_resolution"][:2])
    batch_size = data_cfg["batch_size"]
    backbone = config["backbone"]

    ds, _ = build_tf_dataset(
        manifest_path, input_res, batch_size, backbone,
        is_training=False, augment=False
    )

    # In Keras functional models, extract penultimate layer activations before softmax if possible,
    # or calculate log(probs + 1e-12)
    probs_list = []
    labels_list = []
    for imgs, lbls in ds:
        p = model.predict(imgs, verbose=0)
        probs_list.append(p)
        labels_list.append(lbls.numpy())

    probs = np.concatenate(probs_list, axis=0)
    labels = np.concatenate(labels_list, axis=0)
    # Numerical inverted logits: z = log(p + 1e-12)
    logits = np.log(np.clip(probs, 1e-12, 1.0))
    return logits, probs, labels


def fit_temperature(val_logits: np.ndarray, val_labels: np.ndarray) -> float:
    """Find optimal temperature T on validation set using Brent's method."""
    def nll_eval(T):
        scaled_logits = val_logits / T
        scaled_probs = softmax(scaled_logits, axis=1)
        scaled_probs = np.clip(scaled_probs, 1e-12, 1.0 - 1e-12)
        return log_loss(val_labels, scaled_probs)

    res = minimize_scalar(nll_eval, bounds=(0.05, 10.0), method="bounded")
    return float(res.x)


def plot_reliability_diagram(
    pre_bins: List[Dict], post_bins: List[Dict],
    pre_ece: float, post_ece: float,
    opt_temp: float, save_path: Path, model_name: str
):
    """Plot publication-quality comparative reliability diagram."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)

    # Pre-calibration
    ax = axes[0]
    confs = [b["confidence"] for b in pre_bins if b["count"] > 0]
    accs = [b["accuracy"] for b in pre_bins if b["count"] > 0]
    ax.bar(confs, accs, width=0.05, alpha=0.7, color="#d95f02", edgecolor="black", label="Outputs")
    ax.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
    ax.set_title(f"Uncalibrated (ECE = {pre_ece:.3f})", fontsize=11)
    ax.set_xlabel("Confidence", fontsize=10)
    ax.set_ylabel("Accuracy", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")

    # Post-calibration
    ax = axes[1]
    confs_post = [b["confidence"] for b in post_bins if b["count"] > 0]
    accs_post = [b["accuracy"] for b in post_bins if b["count"] > 0]
    ax.bar(confs_post, accs_post, width=0.05, alpha=0.7, color="#1b9e77", edgecolor="black", label="Temperature Scaled")
    ax.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
    ax.set_title(f"Calibrated (T*={opt_temp:.2f}, ECE = {post_ece:.3f})", fontsize=11)
    ax.set_xlabel("Confidence", fontsize=10)
    ax.set_xlim(0, 1)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")

    plt.suptitle(f"Reliability Diagrams: {model_name}", fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def evaluate_selective_prediction(probs: np.ndarray, labels: np.ndarray) -> List[Dict]:
    """Evaluate coverage vs. error rate across confidence thresholds."""
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    n_total = len(labels)

    thresholds = np.linspace(0.4, 0.99, 30)
    curve_data = []

    for t in thresholds:
        accepted = (confidences >= t)
        n_accepted = np.sum(accepted)
        coverage = n_accepted / n_total

        if n_accepted > 0:
            acc_accepted = accuracy_score(labels[accepted], predictions[accepted])
            error_accepted = 1.0 - acc_accepted
        else:
            acc_accepted = 1.0
            error_accepted = 0.0

        curve_data.append({
            "threshold": float(t),
            "coverage": float(coverage),
            "accepted_accuracy": float(acc_accepted),
            "accepted_error_rate": float(error_accepted),
            "abstention_count": int(n_total - n_accepted)
        })

    return curve_data


def plot_selective_prediction_curve(curve_data: List[Dict], save_path: Path, model_name: str):
    """Plot risk-coverage trade-off curve."""
    coverages = [d["coverage"] * 100 for d in curve_data]
    error_rates = [d["accepted_error_rate"] * 100 for d in curve_data]

    plt.figure(figsize=(6.5, 4.5))
    plt.plot(coverages, error_rates, marker="o", markersize=4, color="#7570b3", linewidth=2, label="Selective Prediction")
    plt.title(f"Risk-Coverage Profile: {model_name}", fontsize=12)
    plt.xlabel("Coverage (% of samples automated)", fontsize=10)
    plt.ylabel("Error Rate on Accepted Samples (%)", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.xlim(0, 105)
    plt.ylim(0, max(error_rates) * 1.2 if error_rates and max(error_rates) > 0 else 10)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def run_calibration_pipeline(config_path: str):
    """Run temperature scaling, calibration error estimation, and selective prediction."""
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg.get("seed", 42))

    model_path = PROJECT_ROOT / cfg["paths"]["checkpoint_dir"] / "best_model.keras"
    model = load_model(str(model_path))

    val_manifest = PROJECT_ROOT / cfg["data"]["val_manifest"]
    test_manifest = PROJECT_ROOT / cfg["data"]["test_internal_manifest"]
    classes = cfg["data"]["classes"]
    num_classes = len(classes)

    print("🔧 Extracting validation logits to optimize temperature...")
    val_logits, val_probs, val_labels = extract_logits_and_labels(model, val_manifest, cfg)
    opt_temp = fit_temperature(val_logits, val_labels)
    print(f"Optimal Temperature Parameter T* = {opt_temp:.4f}")

    print("📊 Evaluating calibration on Internal Test partition...")
    test_logits, test_probs_raw, test_labels = extract_logits_and_labels(model, test_manifest, cfg)

    # Pre-calibration metrics
    pre_ece, pre_mce, pre_bins = compute_ece(test_probs_raw, test_labels, n_bins=15)
    pre_brier = compute_multiclass_brier(test_probs_raw, test_labels, num_classes)
    pre_nll = float(log_loss(test_labels, np.clip(test_probs_raw, 1e-12, 1.0 - 1e-12)))

    # Apply Temperature Scaling
    test_probs_cal = softmax(test_logits / opt_temp, axis=1)

    # Post-calibration metrics
    post_ece, post_mce, post_bins = compute_ece(test_probs_cal, test_labels, n_bins=15)
    post_brier = compute_multiclass_brier(test_probs_cal, test_labels, num_classes)
    post_nll = float(log_loss(test_labels, np.clip(test_probs_cal, 1e-12, 1.0 - 1e-12)))

    print(f"--- Calibration Results ({cfg['model_name']}) ---")
    print(f"Pre-calibration:  ECE = {pre_ece:.4f}, Brier = {pre_brier:.4f}, NLL = {pre_nll:.4f}")
    print(f"Post-calibration: ECE = {post_ece:.4f}, Brier = {post_brier:.4f}, NLL = {post_nll:.4f} (ΔECE = {pre_ece - post_ece:.4f})")

    # Reliability diagram
    fig_dir = PROJECT_ROOT / cfg["paths"]["figures_dir"]
    fig_dir.mkdir(parents=True, exist_ok=True)
    rel_diag_path = fig_dir / "reliability_diagram.png"
    plot_reliability_diagram(pre_bins, post_bins, pre_ece, post_ece, opt_temp, rel_diag_path, cfg["model_name"])

    # Selective Prediction
    sel_data = evaluate_selective_prediction(test_probs_cal, test_labels)
    sel_plot_path = fig_dir / "selective_prediction_curve.png"
    plot_selective_prediction_curve(sel_data, sel_plot_path, cfg["model_name"])

    # Check 90% and 95% confidence operating points
    op_90 = next((d for d in sel_data if d["threshold"] >= 0.90), sel_data[-1])
    op_95 = next((d for d in sel_data if d["threshold"] >= 0.95), sel_data[-1])
    print(f"At τ=0.90: Coverage={op_90['coverage']*100:.1f}%, Error={op_90['accepted_error_rate']*100:.2f}%")
    print(f"At τ=0.95: Coverage={op_95['coverage']*100:.1f}%, Error={op_95['accepted_error_rate']*100:.2f}%")

    out_metrics = {
        "model_name": cfg["model_name"],
        "optimal_temperature": opt_temp,
        "pre_calibration": {
            "ece": pre_ece,
            "mce": pre_mce,
            "brier_score": pre_brier,
            "nll": pre_nll
        },
        "post_calibration": {
            "ece": post_ece,
            "mce": post_mce,
            "brier_score": post_brier,
            "nll": post_nll
        },
        "ece_reduction": pre_ece - post_ece,
        "selective_prediction": {
            "at_tau_0_90": op_90,
            "at_tau_0_95": op_95,
            "full_curve": sel_data
        }
    }

    cal_metrics_path = PROJECT_ROOT / "experiments" / "metrics" / f"{cfg['model_name']}_calibration.json"
    with open(cal_metrics_path, "w") as f:
        json.dump(out_metrics, f, indent=2)

    print(f"✅ Calibration analysis saved to {cal_metrics_path}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrate AgriRoute Vision Model")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    args = parser.parse_args()
    run_calibration_pipeline(args.config)

