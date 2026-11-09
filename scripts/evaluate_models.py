#!/usr/bin/env python3
"""
scripts/evaluate_models.py
==========================
Comprehensive, leak-free evaluation of vision models on internal and external test sets.
Computes multi-class metrics, confusion matrices, ROC/PR curves, and 95% bootstrap CIs.

Usage:
  python scripts/evaluate_models.py --config experiments/configs/mobilenet_v2.yaml
"""

import os
import sys
import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_recall_fscore_support,
    classification_report, confusion_matrix, roc_auc_score, average_precision_score,
    roc_curve, precision_recall_curve
)
from sklearn.preprocessing import label_binarize
import tensorflow as tf
from tensorflow.keras.models import load_model

from train_vision_benchmark import build_tf_dataset, set_seed

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def compute_bootstrap_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    n_bootstraps: int = 1000,
    seed: int = 42
) -> Dict[str, Dict[str, float]]:
    """Compute non-parametric 95% bootstrap confidence intervals for key metrics."""
    rng = np.random.RandomState(seed)
    n_samples = len(y_true)
    num_classes = y_prob.shape[1]
    y_true_bin = label_binarize(y_true, classes=list(range(num_classes)))

    boot_acc = []
    boot_bal_acc = []
    boot_macro_f1 = []
    boot_roc_auc = []

    for _ in range(n_bootstraps):
        idx = rng.randint(0, n_samples, n_samples)
        y_t = y_true[idx]
        y_p = y_pred[idx]
        y_pr = y_prob[idx]

        # Ensure all classes are present in resample to avoid metric errors
        if len(np.unique(y_t)) < num_classes:
            continue

        boot_acc.append(accuracy_score(y_t, y_p))
        boot_bal_acc.append(balanced_accuracy_score(y_t, y_p))
        _, _, f1, _ = precision_recall_fscore_support(y_t, y_p, average="macro", zero_division=0)
        boot_macro_f1.append(f1)
        try:
            auc = roc_auc_score(y_true_bin[idx], y_pr, average="macro", multi_class="ovr")
            boot_roc_auc.append(auc)
        except Exception:
            pass

    def get_ci(vals):
        if not vals:
            return {"mean": 0.0, "ci_lower": 0.0, "ci_upper": 0.0}
        return {
            "mean": float(np.mean(vals)),
            "ci_lower": float(np.percentile(vals, 2.5)),
            "ci_upper": float(np.percentile(vals, 97.5))
        }

    return {
        "accuracy": get_ci(boot_acc),
        "balanced_accuracy": get_ci(boot_bal_acc),
        "macro_f1": get_ci(boot_macro_f1),
        "roc_auc_ovr": get_ci(boot_roc_auc)
    }


def plot_confusion_matrix(cm: np.ndarray, class_names: List[str], save_path: Path, title: str):
    """Plot and save standardized confusion matrix figure."""
    plt.figure(figsize=(7, 6))
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    sns.heatmap(
        cm_norm, annot=True, fmt=".2%", cmap="Blues",
        xticklabels=class_names, yticklabels=class_names, cbar=False
    )
    plt.title(title, fontsize=12, pad=10)
    plt.xlabel("Predicted Class", fontsize=10)
    plt.ylabel("True Class", fontsize=10)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def evaluate_partition(
    model: tf.keras.Model,
    manifest_path: Path,
    config: Dict,
    partition_name: str
) -> Dict:
    """Evaluate model on a specific manifest partition."""
    data_cfg = config["data"]
    input_res = tuple(data_cfg["input_resolution"][:2])
    batch_size = data_cfg["batch_size"]
    backbone = config["backbone"]
    classes = data_cfg["classes"]

    ds, n_samples = build_tf_dataset(
        manifest_path, input_res, batch_size, backbone,
        is_training=False, augment=False
    )

    print(f"📊 Evaluating on {partition_name} ({n_samples} samples)...")

    # Get predictions
    y_true_list = []
    y_prob_list = []
    for imgs, lbls in ds:
        probs = model.predict(imgs, verbose=0)
        y_prob_list.append(probs)
        y_true_list.append(lbls.numpy())

    y_prob = np.concatenate(y_prob_list, axis=0)
    y_true = np.concatenate(y_true_list, axis=0)
    y_pred = np.argmax(y_prob, axis=1)

    # Calculate metrics
    acc = accuracy_score(y_true, y_pred)
    bal_acc = balanced_accuracy_score(y_true, y_pred)
    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_true, y_pred, average="weighted", zero_division=0
    )

    y_true_bin = label_binarize(y_true, classes=list(range(len(classes))))
    try:
        roc_auc_ovr = roc_auc_score(y_true_bin, y_prob, average="macro", multi_class="ovr")
    except Exception:
        roc_auc_ovr = None
    try:
        pr_auc_macro = average_precision_score(y_true_bin, y_prob, average="macro")
    except Exception:
        pr_auc_macro = None

    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(classes))))
    class_report = classification_report(
        y_true, y_pred, target_names=classes, output_dict=True, zero_division=0
    )

    # Bootstrap CIs
    boot_cis = compute_bootstrap_ci(y_true, y_pred, y_prob, n_bootstraps=1000)

    # Plot Confusion Matrix
    fig_dir = PROJECT_ROOT / config["paths"]["figures_dir"]
    fig_dir.mkdir(parents=True, exist_ok=True)
    cm_path = fig_dir / f"confusion_matrix_{partition_name}.png"
    plot_confusion_matrix(cm, classes, cm_path, f"Confusion Matrix: {config['model_name']} ({partition_name})")

    # Save raw predictions for calibration analysis
    pred_df = pd.DataFrame(y_prob, columns=[f"prob_{c}" for c in classes])
    pred_df["y_true"] = y_true
    pred_df["y_pred"] = y_pred
    pred_save_path = PROJECT_ROOT / config["paths"]["log_dir"] / f"predictions_{partition_name}.csv"
    pred_df.to_csv(pred_save_path, index=False)

    return {
        "partition": partition_name,
        "sample_count": int(n_samples),
        "accuracy": float(acc),
        "balanced_accuracy": float(bal_acc),
        "macro_precision": float(prec_macro),
        "macro_recall": float(rec_macro),
        "macro_f1": float(f1_macro),
        "weighted_f1": float(f1_weighted),
        "roc_auc_ovr": float(roc_auc_ovr) if roc_auc_ovr is not None else None,
        "pr_auc_macro": float(pr_auc_macro) if pr_auc_macro is not None else None,
        "bootstrap_95ci": boot_cis,
        "confusion_matrix": cm.tolist(),
        "per_class": {
            cls: {
                "precision": float(class_report[cls]["precision"]),
                "recall": float(class_report[cls]["recall"]),
                "f1_score": float(class_report[cls]["f1-score"]),
                "support": int(class_report[cls]["support"])
            }
            for cls in classes if cls in class_report
        }
    }


def run_evaluation(config_path: str):
    """Execute full evaluation pipeline on both internal and external test sets."""
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg.get("seed", 42))

    model_path = PROJECT_ROOT / cfg["paths"]["checkpoint_dir"] / "best_model.keras"
    if not model_path.exists():
        raise FileNotFoundError(f"Checkpoint not found at {model_path}. Train the model first.")

    print(f"📦 Loading model from {model_path}...")
    model = load_model(str(model_path))

    # Evaluate internal test set
    test_int_manifest = PROJECT_ROOT / cfg["data"]["test_internal_manifest"]
    metrics_internal = evaluate_partition(model, test_int_manifest, cfg, "internal_test")

    # Evaluate external test set if available
    test_ext_manifest = PROJECT_ROOT / cfg["data"]["test_external_manifest"]
    metrics_external = None
    if test_ext_manifest.exists() and os.path.getsize(test_ext_manifest) > 100:
        metrics_external = evaluate_partition(model, test_ext_manifest, cfg, "external_test")

    # Calculate domain drop
    domain_drop = None
    if metrics_external:
        drop_acc = metrics_internal["accuracy"] - metrics_external["accuracy"]
        drop_f1 = metrics_internal["macro_f1"] - metrics_external["macro_f1"]
        domain_drop = {
            "accuracy_drop": float(drop_acc),
            "macro_f1_drop": float(drop_f1),
            "relative_f1_drop_pct": float((drop_f1 / metrics_internal["macro_f1"]) * 100)
        }
        print(f"\n📉 Domain Transfer Drop: ΔAcc = {drop_acc:.4f}, ΔMacro-F1 = {drop_f1:.4f} ({domain_drop['relative_f1_drop_pct']:.1f}%)")

    results = {
        "model_name": cfg["model_name"],
        "backbone": cfg["backbone"],
        "internal_test": metrics_internal,
        "external_test": metrics_external,
        "domain_generalisation_drop": domain_drop
    }

    metrics_save_path = PROJECT_ROOT / cfg["paths"]["metrics_file"]
    with open(metrics_save_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Evaluation complete. Metrics saved to {metrics_save_path}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate AgriRoute Vision Model")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    args = parser.parse_args()
    run_evaluation(args.config)

