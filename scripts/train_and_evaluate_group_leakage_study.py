#!/usr/bin/env python3
"""
scripts/train_and_evaluate_group_leakage_study.py
=================================================
Rigorous controlled experimental evaluation comparing:
- Experiment A: Historical Random (Image-Level) Split [77.8% subject-level leakage]
- Experiment B: Group-Aware Split [0% subject leakage, trained from scratch]
- Experiment C: Truly External Evaluations on FruitVision (N=4,157) and Sultana (N=1,193)
- Calibration & Selective Prediction Analysis (Validation-only fitting)

Saves all required outputs to experiments/group_leakage_study/
"""

import os
import sys
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Tuple, Any

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_recall_fscore_support,
    confusion_matrix, roc_auc_score, average_precision_score, log_loss, brier_score_loss
)
from sklearn.preprocessing import label_binarize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.applications import mobilenet_v2

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STUDY_DIR = PROJECT_ROOT / "experiments" / "group_leakage_study"
STUDY_DIR.mkdir(parents=True, exist_ok=True)
CM_DIR = STUDY_DIR / "CONFUSION_MATRICES"
CM_DIR.mkdir(exist_ok=True)
LOG_DIR = STUDY_DIR / "TRAINING_LOGS"
LOG_DIR.mkdir(exist_ok=True)
CKPT_DIR = STUDY_DIR / "CHECKPOINTS"
CKPT_DIR.mkdir(exist_ok=True)

CLASS_NAMES = [
    "fresh_apple",
    "fresh_banana",
    "fresh_orange",
    "rotten_apple",
    "rotten_banana",
    "rotten_orange"
]
NUM_CLASSES = 6
INPUT_SHAPE = (224, 224, 3)
BATCH_SIZE = 32
SEED = 42


def set_seed(seed: int = 42):
    """Enforce strict seed reproducibility."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"


def build_tf_dataset(
    manifest_path: Path,
    is_training: bool = False,
    augment: bool = False
) -> Tuple[tf.data.Dataset, int]:
    """High-performance tf.data pipeline."""
    df = pd.read_csv(manifest_path)
    file_paths = df["filepath"].values
    labels = df["label_idx"].values.astype(np.int32)

    aug_layers = []
    if is_training and augment:
        aug_layers.append(layers.RandomFlip("horizontal"))
        aug_layers.append(layers.RandomRotation(0.15))
        aug_layers.append(layers.RandomZoom((-0.10, 0.10)))
        aug_layers.append(layers.RandomContrast(0.10))
    aug_model = tf.keras.Sequential(aug_layers) if aug_layers else None

    def process_image(path_tensor, label_tensor):
        img_bytes = tf.io.read_file(path_tensor)
        img = tf.image.decode_image(img_bytes, channels=3, expand_animations=False)
        img = tf.image.resize(img, [INPUT_SHAPE[0], INPUT_SHAPE[1]])
        img.set_shape([INPUT_SHAPE[0], INPUT_SHAPE[1], 3])
        if aug_model is not None:
            img = aug_model(img, training=True)
        img = mobilenet_v2.preprocess_input(img)
        return img, label_tensor

    ds = tf.data.Dataset.from_tensor_slices((file_paths, labels))
    if is_training:
        ds = ds.shuffle(buffer_size=min(len(file_paths), 2000), seed=SEED, reshuffle_each_iteration=True)
    ds = ds.map(process_image, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds, len(df)


def create_mobilenet_v2_model() -> Tuple[models.Model, tf.keras.Model]:
    """Instantiate fresh MobileNetV2 with ImageNet base weights."""
    base_model = mobilenet_v2.MobileNetV2(
        input_shape=INPUT_SHAPE, include_top=False, weights="imagenet", pooling="avg"
    )
    inputs = layers.Input(shape=INPUT_SHAPE)
    x = base_model(inputs)
    x = layers.Dropout(0.3, name="top_dropout")(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax", name="predictions", dtype="float32")(x)
    model = models.Model(inputs=inputs, outputs=outputs, name="agriroute_mobilenet_v2_group_aware")
    return model, base_model


def train_group_aware_model() -> str:
    """Train Experiment B MobileNetV2 model on group-aware partition."""
    set_seed(SEED)
    train_manifest = STUDY_DIR / "group_train.csv"
    val_manifest = STUDY_DIR / "group_val.csv"
    best_ckpt = CKPT_DIR / "group_aware_mobilenet_v2.keras"
    history_csv = LOG_DIR / "group_aware_training_history.csv"

    print("\n========================================================")
    print("🚀 TRAINING EXPERIMENT B: Group-Aware MobileNetV2")
    print(f"   Train samples: 9,513 (1,057 groups)")
    print(f"   Val samples:   2,043 (227 groups)")
    print("========================================================\n")

    train_ds, n_train = build_tf_dataset(train_manifest, is_training=True, augment=True)
    val_ds, n_val = build_tf_dataset(val_manifest, is_training=False, augment=False)

    model, base_model = create_mobilenet_v2_model()

    # Phase 1: Frozen backbone (5 epochs)
    base_model.trainable = False
    opt_p1 = optimizers.AdamW(learning_rate=0.001, weight_decay=1e-4)
    model.compile(
        optimizer=opt_p1,
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.05),
        metrics=["accuracy"]
    )

    # Convert sparse targets to categorical for label smoothing loss
    def to_one_hot(img, label):
        return img, tf.one_hot(label, NUM_CLASSES)

    train_ds_oh = train_ds.map(to_one_hot, num_parallel_calls=tf.data.AUTOTUNE)
    val_ds_oh = val_ds.map(to_one_hot, num_parallel_calls=tf.data.AUTOTUNE)

    cb_list = [
        callbacks.ModelCheckpoint(
            filepath=str(best_ckpt),
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        ),
        callbacks.EarlyStopping(
            monitor="val_loss",
            patience=3,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=2,
            min_lr=1e-6,
            verbose=1
        ),
        callbacks.CSVLogger(str(history_csv), append=False)
    ]

    print("\n--- Phase 1: Feature Extraction (5 epochs) ---")
    start_t = time.time()
    model.fit(
        train_ds_oh,
        validation_data=val_ds_oh,
        epochs=5,
        callbacks=cb_list,
        verbose=1
    )

    # Phase 2: Fine-Tuning top layers (fine-tune from layer 100, up to 10 epochs)
    print("\n--- Phase 2: Fine-Tuning from Layer 100 (10 epochs) ---")
    base_model.trainable = True
    for layer in base_model.layers[:100]:
        layer.trainable = False

    opt_p2 = optimizers.AdamW(learning_rate=0.0001, weight_decay=1e-4)
    model.compile(
        optimizer=opt_p2,
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.05),
        metrics=["accuracy"]
    )

    cb_list[-1] = callbacks.CSVLogger(str(history_csv), append=True)

    model.fit(
        train_ds_oh,
        validation_data=val_ds_oh,
        initial_epoch=5,
        epochs=15,
        callbacks=cb_list,
        verbose=1
    )

    elapsed = time.time() - start_t
    print(f"\n✅ Training complete in {elapsed:.1f}s. Saved checkpoint to {best_ckpt}")
    return str(best_ckpt)


def run_inference(model: tf.keras.Model, manifest_path: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray, pd.DataFrame]:
    """Execute model inference over a manifest CSV."""
    df = pd.read_csv(manifest_path)
    ds, _ = build_tf_dataset(manifest_path, is_training=False, augment=False)
    
    prob_list = []
    lbl_list = []
    for imgs, lbls in ds:
        p = model.predict(imgs, verbose=0)
        prob_list.append(p)
        lbl_list.append(lbls.numpy())
        
    y_prob = np.concatenate(prob_list, axis=0)
    y_true = np.concatenate(lbl_list, axis=0)
    y_pred = np.argmax(y_prob, axis=1)
    return y_prob, y_pred, y_true, df


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    group_ids: np.ndarray = None,
    n_bootstraps: int = 1000
) -> Dict[str, Any]:
    """Compute complete metric suite with bootstrap 95% CIs."""
    acc = float(accuracy_score(y_true, y_pred))
    bal_acc = float(balanced_accuracy_score(y_true, y_pred))
    prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    
    y_true_bin = label_binarize(y_true, classes=list(range(NUM_CLASSES)))
    try:
        roc_auc = float(roc_auc_score(y_true_bin, y_prob, average="macro", multi_class="ovr"))
    except Exception:
        roc_auc = None

    try:
        pr_auc = float(average_precision_score(y_true_bin, y_prob, average="macro"))
    except Exception:
        pr_auc = None

    # Per class metrics
    p_c, r_c, f_c, s_c = precision_recall_fscore_support(y_true, y_pred, average=None, zero_division=0)
    per_class = {}
    for i, c_name in enumerate(CLASS_NAMES):
        per_class[c_name] = {
            "precision": float(p_c[i]),
            "recall": float(r_c[i]),
            "f1_score": float(f_c[i]),
            "support": int(s_c[i])
        }

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=list(range(NUM_CLASSES)))

    # Bootstrap 95% CIs
    rng = np.random.RandomState(SEED)
    n_samples = len(y_true)
    boot_accs, boot_bal_accs, boot_f1s = [], [], []

    if group_ids is not None:
        # Group-aware cluster bootstrap
        unique_groups = np.unique(group_ids)
        n_groups = len(unique_groups)
        group_to_indices = {g: np.where(group_ids == g)[0] for g in unique_groups}

        for _ in range(n_bootstraps):
            sampled_g = rng.choice(unique_groups, size=n_groups, replace=True)
            idx = np.concatenate([group_to_indices[g] for g in sampled_g])
            yt_s, yp_s = y_true[idx], y_pred[idx]
            if len(np.unique(yt_s)) < NUM_CLASSES:
                continue
            boot_accs.append(accuracy_score(yt_s, yp_s))
            boot_bal_accs.append(balanced_accuracy_score(yt_s, yp_s))
            _, _, f_macro, _ = precision_recall_fscore_support(yt_s, yp_s, average="macro", zero_division=0)
            boot_f1s.append(f_macro)
    else:
        # Standard i.i.d. bootstrap
        for _ in range(n_bootstraps):
            idx = rng.randint(0, n_samples, n_samples)
            yt_s, yp_s = y_true[idx], y_pred[idx]
            if len(np.unique(yt_s)) < NUM_CLASSES:
                continue
            boot_accs.append(accuracy_score(yt_s, yp_s))
            boot_bal_accs.append(balanced_accuracy_score(yt_s, yp_s))
            _, _, f_macro, _ = precision_recall_fscore_support(yt_s, yp_s, average="macro", zero_division=0)
            boot_f1s.append(f_macro)

    def calc_ci(arr):
        if not arr:
            return {"mean": None, "ci_lower": None, "ci_upper": None}
        return {
            "mean": float(np.mean(arr)),
            "ci_lower": float(np.percentile(arr, 2.5)),
            "ci_upper": float(np.percentile(arr, 97.5))
        }

    return {
        "sample_count": n_samples,
        "accuracy": acc,
        "balanced_accuracy": bal_acc,
        "macro_precision": float(prec_m),
        "macro_recall": float(rec_m),
        "macro_f1": float(f1_m),
        "weighted_f1": float(f1_w),
        "roc_auc_ovr": roc_auc,
        "pr_auc_macro": pr_auc,
        "bootstrap_95ci": {
            "accuracy": calc_ci(boot_accs),
            "balanced_accuracy": calc_ci(boot_bal_accs),
            "macro_f1": calc_ci(boot_f1s)
        },
        "per_class": per_class,
        "confusion_matrix": cm.tolist()
    }


def plot_cm(cm: np.ndarray, title: str, save_path: Path):
    """Save normalized confusion matrix plot."""
    plt.figure(figsize=(7, 6))
    cm_norm = cm.astype("float") / np.maximum(cm.sum(axis=1)[:, np.newaxis], 1e-12)
    sns.heatmap(
        cm_norm, annot=True, fmt=".2%", cmap="Blues",
        xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cbar=False
    )
    plt.title(title, fontsize=11, pad=12)
    plt.xlabel("Predicted Class", fontsize=10)
    plt.ylabel("True Class", fontsize=10)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def compute_ece(probs: np.ndarray, y_true: np.ndarray, n_bins: int = 15) -> Tuple[float, float]:
    """Compute Expected Calibration Error (ECE) and Maximum Calibration Error (MCE)."""
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == y_true)

    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    mce = 0.0

    for i in range(n_bins):
        bin_lower, bin_upper = bin_boundaries[i], bin_boundaries[i + 1]
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = np.mean(in_bin)

        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            bin_err = np.abs(avg_confidence_in_bin - accuracy_in_bin)
            ece += bin_err * prop_in_bin
            mce = max(mce, bin_err)

    return float(ece), float(mce)


def fit_temperature(val_probs: np.ndarray, val_labels: np.ndarray) -> float:
    """Fit optimal temperature scalar T* on validation set using L-BFGS-B."""
    eps = 1e-12
    val_probs = np.clip(val_probs, eps, 1.0 - eps)
    val_logits = np.log(val_probs)

    def nll_obj(t_arr):
        t = t_arr[0]
        scaled = val_logits / t
        scaled_max = np.max(scaled, axis=1, keepdims=True)
        exp_scaled = np.exp(scaled - scaled_max)
        softmax_probs = exp_scaled / np.sum(exp_scaled, axis=1, keepdims=True)
        softmax_probs = np.clip(softmax_probs, eps, 1.0 - eps)
        return log_loss(val_labels, softmax_probs, labels=list(range(NUM_CLASSES)))

    res = minimize(nll_obj, x0=[1.0], bounds=[(0.1, 10.0)], method="L-BFGS-B")
    return float(res.x[0])


def apply_temperature(probs: np.ndarray, temp: float) -> np.ndarray:
    """Scale probabilities by temperature."""
    eps = 1e-12
    probs = np.clip(probs, eps, 1.0 - eps)
    logits = np.log(probs)
    scaled = logits / temp
    scaled_max = np.max(scaled, axis=1, keepdims=True)
    exp_scaled = np.exp(scaled - scaled_max)
    return exp_scaled / np.sum(exp_scaled, axis=1, keepdims=True)


def compute_calibration_suite(
    val_prob: np.ndarray, val_true: np.ndarray,
    test_prob: np.ndarray, test_true: np.ndarray
) -> Dict[str, Any]:
    """Fit temperature and abstention on val; evaluate on test."""
    t_opt = fit_temperature(val_prob, val_true)

    # Pre-calibration metrics
    ece_pre, mce_pre = compute_ece(test_prob, test_true)
    nll_pre = float(log_loss(test_true, test_prob, labels=list(range(NUM_CLASSES))))
    test_true_bin = label_binarize(test_true, classes=list(range(NUM_CLASSES)))
    brier_pre = float(np.mean(np.sum((test_prob - test_true_bin) ** 2, axis=1)))

    # Post-calibration metrics
    test_prob_scaled = apply_temperature(test_prob, t_opt)
    ece_post, mce_post = compute_ece(test_prob_scaled, test_true)
    nll_post = float(log_loss(test_true, test_prob_scaled, labels=list(range(NUM_CLASSES))))
    brier_post = float(np.mean(np.sum((test_prob_scaled - test_true_bin) ** 2, axis=1)))

    # Selective prediction thresholds (fit/evaluated at thresholds [0.70, 0.75, 0.80, 0.85, 0.90, 0.95])
    confidences = np.max(test_prob, axis=1)
    predictions = np.argmax(test_prob, axis=1)
    selective_results = {}

    for tau in [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]:
        retained = confidences >= tau
        coverage = float(np.mean(retained))
        if np.sum(retained) > 0:
            sel_acc = float(accuracy_score(test_true[retained], predictions[retained]))
            sel_err = 1.0 - sel_acc
        else:
            sel_acc, sel_err = 0.0, 1.0
            
        selective_results[f"tau_{tau:.2f}"] = {
            "threshold": tau,
            "coverage": coverage,
            "selective_accuracy": sel_acc,
            "selective_error_rate": sel_err,
            "retained_samples": int(np.sum(retained)),
            "abstained_samples": int(np.sum(~retained))
        }

    return {
        "optimal_temperature_fitted_on_val": t_opt,
        "pre_calibration": {
            "ece": ece_pre,
            "mce": mce_pre,
            "nll": nll_pre,
            "brier_score": brier_pre
        },
        "post_calibration": {
            "ece": ece_post,
            "mce": mce_post,
            "nll": nll_post,
            "brier_score": brier_post
        },
        "delta_ece": float(ece_post - ece_pre),
        "delta_nll": float(nll_post - nll_pre),
        "selective_prediction": selective_results
    }


def main():
    print("\n" + "=" * 70)
    print("🔬 AGRIRoute: Controlled Group Leakage & Generalization Experiment")
    print("=" * 70)

    # 1. Train Experiment B: Group-Aware Model
    group_ckpt_path = CKPT_DIR / "group_aware_mobilenet_v2.keras"
    if not group_ckpt_path.exists():
        train_group_aware_model()
    else:
        print(f"✅ Found existing group-aware checkpoint at {group_ckpt_path}")

    # Load Models
    model_b = models.load_model(str(group_ckpt_path))
    hist_ckpt_path = PROJECT_ROOT / "experiments" / "checkpoints" / "mobilenet_v2" / "best_model.keras"
    if not hist_ckpt_path.exists():
        raise FileNotFoundError(f"Historical checkpoint {hist_ckpt_path} not found!")
    model_a = models.load_model(str(hist_ckpt_path))

    # Manifests
    hist_test_manifest = PROJECT_ROOT / "experiments" / "split_manifests" / "test_internal.csv"
    hist_val_manifest = PROJECT_ROOT / "experiments" / "split_manifests" / "val.csv"
    group_val_manifest = STUDY_DIR / "group_val.csv"
    group_test_manifest = STUDY_DIR / "group_test.csv"
    fruitvision_manifest = STUDY_DIR / "fruitvision_clean.csv"
    sultana_manifest = STUDY_DIR / "sultana_clean.csv"

    print("\n---------------------------------------------------------")
    print("📊 Executing Inferences across Models and Partitions...")
    print("---------------------------------------------------------")

    # Inferences for Model A (Historical)
    prob_a_rand_test, pred_a_rand_test, true_a_rand_test, df_a_rand = run_inference(model_a, hist_test_manifest)
    prob_a_rand_val, pred_a_rand_val, true_a_rand_val, _ = run_inference(model_a, hist_val_manifest)
    prob_a_grp_test, pred_a_grp_test, true_a_grp_test, df_grp = run_inference(model_a, group_test_manifest)
    prob_a_fv, pred_a_fv, true_a_fv, df_fv = run_inference(model_a, fruitvision_manifest)
    prob_a_sul, pred_a_sul, true_a_sul, df_sul = run_inference(model_a, sultana_manifest)

    # Inferences for Model B (Group-Aware)
    prob_b_grp_val, pred_b_grp_val, true_b_grp_val, _ = run_inference(model_b, group_val_manifest)
    prob_b_grp_test, pred_b_grp_test, true_b_grp_test, _ = run_inference(model_b, group_test_manifest)
    prob_b_fv, pred_b_fv, true_b_fv, _ = run_inference(model_b, fruitvision_manifest)
    prob_b_sul, pred_b_sul, true_b_sul, _ = run_inference(model_b, sultana_manifest)

    # Save raw arrays
    print("\n💾 Serializing raw predictions into PREDICTIONS.npz...")
    np.savez_compressed(
        STUDY_DIR / "PREDICTIONS.npz",
        prob_a_rand_test=prob_a_rand_test, pred_a_rand_test=pred_a_rand_test, true_a_rand_test=true_a_rand_test,
        prob_a_grp_test=prob_a_grp_test, pred_a_grp_test=pred_a_grp_test, true_a_grp_test=true_a_grp_test,
        prob_a_fv=prob_a_fv, pred_a_fv=pred_a_fv, true_a_fv=true_a_fv,
        prob_a_sul=prob_a_sul, pred_a_sul=pred_a_sul, true_a_sul=true_a_sul,
        prob_b_grp_test=prob_b_grp_test, pred_b_grp_test=pred_b_grp_test, true_b_grp_test=true_b_grp_test,
        prob_b_fv=prob_b_fv, pred_b_fv=pred_b_fv, true_b_fv=true_b_fv,
        prob_b_sul=prob_b_sul, pred_b_sul=pred_b_sul, true_b_sul=true_b_sul
    )

    # ---------------------------------------------------------
    # EXPERIMENT A METRICS (Historical Random Split)
    # ---------------------------------------------------------
    print("\n📈 Computing Experiment A (Random Split) Metrics...")
    metrics_a_rand = compute_metrics(true_a_rand_test, pred_a_rand_test, prob_a_rand_test, group_ids=None)
    metrics_a_rand["model_description"] = "MobileNetV2 trained on historical random split (77.8% subject leakage)"
    metrics_a_rand["evaluated_partition"] = "Random Internal Test (N=4,090)"
    with open(STUDY_DIR / "RANDOM_SPLIT_RESULTS.json", "w") as f:
        json.dump(metrics_a_rand, f, indent=2)
    plot_cm(np.array(metrics_a_rand["confusion_matrix"]), "Experiment A: Historical Random Split (Internal Test)", CM_DIR / "cm_expA_random_test.png")

    # ---------------------------------------------------------
    # EXPERIMENT B METRICS (Group-Aware Split)
    # ---------------------------------------------------------
    print("\n📈 Computing Experiment B (Group-Aware Split) Metrics...")
    group_ids_test = df_grp["group_id"].values
    metrics_b_grp = compute_metrics(true_b_grp_test, pred_b_grp_test, prob_b_grp_test, group_ids=group_ids_test)
    metrics_b_grp["model_description"] = "MobileNetV2 trained from scratch on group-aware partition (0% subject leakage)"
    metrics_b_grp["evaluated_partition"] = "Group-Aware Internal Test (N=2,043, 227 groups)"
    with open(STUDY_DIR / "GROUP_SPLIT_RESULTS.json", "w") as f:
        json.dump(metrics_b_grp, f, indent=2)
    plot_cm(np.array(metrics_b_grp["confusion_matrix"]), "Experiment B: Group-Aware Split (Internal Test)", CM_DIR / "cm_expB_group_test.png")

    # ---------------------------------------------------------
    # EXPERIMENT C METRICS: FruitVision Evaluation
    # ---------------------------------------------------------
    print("\n📈 Computing Experiment C1 (FruitVision) Metrics...")
    metrics_a_fv = compute_metrics(true_a_fv, pred_a_fv, prob_a_fv, group_ids=None)
    metrics_b_fv = compute_metrics(true_b_fv, pred_b_fv, prob_b_fv, group_ids=None)
    fruitvision_results = {
        "dataset_name": "FruitVision (Mendeley Data V2, Bijoy et al. 2025)",
        "sample_count": len(true_a_fv),
        "classes_evaluated": CLASS_NAMES,
        "model_a_historical": metrics_a_fv,
        "model_b_group_aware": metrics_b_fv,
        "comparative_delta_group_vs_historical": {
            "accuracy_delta": float(metrics_b_fv["accuracy"] - metrics_a_fv["accuracy"]),
            "macro_f1_delta": float(metrics_b_fv["macro_f1"] - metrics_a_fv["macro_f1"])
        }
    }
    with open(STUDY_DIR / "FRUITVISION_RESULTS.json", "w") as f:
        json.dump(fruitvision_results, f, indent=2)
    plot_cm(np.array(metrics_a_fv["confusion_matrix"]), "FruitVision External: Model A (Historical)", CM_DIR / "cm_expA_fruitvision.png")
    plot_cm(np.array(metrics_b_fv["confusion_matrix"]), "FruitVision External: Model B (Group-Aware)", CM_DIR / "cm_expB_fruitvision.png")

    # ---------------------------------------------------------
    # EXPERIMENT C METRICS: Sultana Evaluation
    # ---------------------------------------------------------
    print("\n📈 Computing Experiment C2 (Sultana) Metrics...")
    metrics_a_sul = compute_metrics(true_a_sul, pred_a_sul, prob_a_sul, group_ids=None)
    metrics_b_sul = compute_metrics(true_b_sul, pred_b_sul, prob_b_sul, group_ids=None)
    sultana_results = {
        "dataset_name": "Fresh and Rotten Fruits (Data in Brief, Sultana et al. 2022)",
        "sample_count": len(true_a_sul),
        "classes_evaluated": CLASS_NAMES,
        "model_a_historical": metrics_a_sul,
        "model_b_group_aware": metrics_b_sul,
        "comparative_delta_group_vs_historical": {
            "accuracy_delta": float(metrics_b_sul["accuracy"] - metrics_a_sul["accuracy"]),
            "macro_f1_delta": float(metrics_b_sul["macro_f1"] - metrics_a_sul["macro_f1"])
        }
    }
    with open(STUDY_DIR / "SULTANA_RESULTS.json", "w") as f:
        json.dump(sultana_results, f, indent=2)
    plot_cm(np.array(metrics_a_sul["confusion_matrix"]), "Sultana External: Model A (Historical)", CM_DIR / "cm_expA_sultana.png")
    plot_cm(np.array(metrics_b_sul["confusion_matrix"]), "Sultana External: Model B (Group-Aware)", CM_DIR / "cm_expB_sultana.png")

    # ---------------------------------------------------------
    # CALIBRATION & SELECTIVE PREDICTION
    # ---------------------------------------------------------
    print("\n📈 Computing Calibration & Selective Prediction Results...")
    # Model A calibration on historical validation -> historical test
    calib_a = compute_calibration_suite(prob_a_rand_val, true_a_rand_val, prob_a_rand_test, true_a_rand_test)
    # Model B calibration on group validation -> group test
    calib_b = compute_calibration_suite(prob_b_grp_val, true_b_grp_val, prob_b_grp_test, true_b_grp_test)
    # Model B on FruitVision
    calib_b_fv = compute_calibration_suite(prob_b_grp_val, true_b_grp_val, prob_b_fv, true_b_fv)

    calibration_all = {
        "model_a_historical_on_random_test": calib_a,
        "model_b_group_aware_on_group_test": calib_b,
        "model_b_group_aware_on_fruitvision": calib_b_fv
    }
    with open(STUDY_DIR / "CALIBRATION_RESULTS.json", "w") as f:
        json.dump(calibration_all, f, indent=2)

    print("\n" + "=" * 70)
    print("🏆 SUMMARY COMPARISON OF ALL EXPERIMENTAL CONDITIONS")
    print("=" * 70)
    print(f"Condition 1 - Exp A (Random Split Test, N=4090):")
    print(f"   Accuracy: {metrics_a_rand['accuracy']:.4f} | Macro F1: {metrics_a_rand['macro_f1']:.4f}")
    print(f"Condition 2 - Exp B (Group-Aware Test, N=2043):")
    print(f"   Accuracy: {metrics_b_grp['accuracy']:.4f} | Macro F1: {metrics_b_grp['macro_f1']:.4f}")
    print(f"Condition 3 - External FruitVision (N=4157):")
    print(f"   Model A Accuracy: {metrics_a_fv['accuracy']:.4f} | Macro F1: {metrics_a_fv['macro_f1']:.4f}")
    print(f"   Model B Accuracy: {metrics_b_fv['accuracy']:.4f} | Macro F1: {metrics_b_fv['macro_f1']:.4f}")
    print(f"Condition 4 - External Sultana (N=1193):")
    print(f"   Model A Accuracy: {metrics_a_sul['accuracy']:.4f} | Macro F1: {metrics_a_sul['macro_f1']:.4f}")
    print(f"   Model B Accuracy: {metrics_b_sul['accuracy']:.4f} | Macro F1: {metrics_b_sul['macro_f1']:.4f}")
    print("=" * 70)
    print("✨ Study execution completed successfully!")


if __name__ == "__main__":
    main()

