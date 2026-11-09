"""
scripts/evaluate_model_b_v4_1.py
================================
Comprehensive evaluation pipeline for freshly retrained Model B (group_aware_mobilenet_v2_v4_1.keras).

Executes:
- Phase 3: Exact final test set evaluation (Primary: N=227 raw; Secondary: N=2,043 all variants).
  Mandatory assertion: every predicted row has merged_split_partition_v4 == 'test'.
- Phase 4: Temperature scaling calibration fitted strictly on FINAL_GROUP_VAL_V4.csv.
  Calculates ECE, MCE, NLL, Brier score, and builds 10-bin reliability table.
- Phase 5: Selective prediction at tau = 0.90 (documenting raw vs calibrated probabilities).
- Phase 6: External dataset benchmarking on FruitVision (N=4,157) and Sultana (N=1,193).

Generates:
- MODEL_B_V4_1_PREDICTIONS.csv
- MODEL_B_V4_1_METRICS.json
- MODEL_B_V4_1_CALIBRATION.json
- MODEL_B_V4_1_RELIABILITY_TABLE.csv
- MODEL_B_V4_1_SELECTIVE_RESULTS.json
- MODEL_B_V4_1_EXTERNAL_RESULTS.json
"""

import os
import sys
import json
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_recall_fscore_support,
    confusion_matrix, roc_auc_score, average_precision_score, log_loss, brier_score_loss
)
from sklearn.preprocessing import label_binarize
import tensorflow as tf
from tensorflow.keras.applications import mobilenet_v2

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CKPT_PATH = PROJECT_ROOT / "experiments" / "group_leakage_study" / "CHECKPOINTS" / "group_aware_mobilenet_v2_v4_1.keras"

CLASSES = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]
NUM_CLASSES = 6
INPUT_SHAPE = (224, 224, 3)
BATCH_SIZE = 64
TAU_THRESHOLD = 0.90

def compute_multiclass_brier_score(y_true, probs):
    y_one_hot = label_binarize(y_true, classes=list(range(NUM_CLASSES)))
    if y_one_hot.shape[1] == 1 and NUM_CLASSES > 1:
        y_one_hot = np.hstack([1 - y_one_hot, y_one_hot])
    return float(np.mean(np.sum((probs - y_one_hot) ** 2, axis=1)))

def compute_ece_and_bins(y_true, probs, n_bins=10):
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = (predictions == y_true)

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]

    ece = 0.0
    mce = 0.0
    bins_data = []

    for bin_idx, (b_lower, b_upper) in enumerate(zip(bin_lowers, bin_uppers)):
        if bin_idx == n_bins - 1:
            in_bin = (confidences >= b_lower) & (confidences <= b_upper)
        else:
            in_bin = (confidences >= b_lower) & (confidences < b_upper)

        prop_in_bin = float(np.mean(in_bin))
        n_in_bin = int(np.sum(in_bin))

        if n_in_bin > 0:
            accuracy_in_bin = float(np.mean(accuracies[in_bin]))
            avg_confidence_in_bin = float(np.mean(confidences[in_bin]))
            abs_diff = abs(accuracy_in_bin - avg_confidence_in_bin)
            weighted_diff = abs_diff * prop_in_bin
            ece += weighted_diff
            mce = max(mce, abs_diff)
        else:
            accuracy_in_bin = 0.0
            avg_confidence_in_bin = (b_lower + b_upper) / 2.0
            abs_diff = 0.0
            weighted_diff = 0.0

        bins_data.append({
            "bin_index": bin_idx + 1,
            "bin_lower": float(b_lower),
            "bin_upper": float(b_upper),
            "bin_range": f"[{b_lower:.1f}, {b_upper:.1f}{']' if bin_idx == n_bins - 1 else ')'}",
            "sample_count": n_in_bin,
            "proportion_of_total": prop_in_bin,
            "accuracy_in_bin": accuracy_in_bin,
            "mean_confidence_in_bin": avg_confidence_in_bin,
            "calibration_error_abs": abs_diff,
            "weighted_ece_contribution": weighted_diff
        })

    return float(ece), float(mce), bins_data

def evaluate_manifest_extract_logits(model, manifest_path: Path):
    df = pd.read_csv(manifest_path)
    file_paths = []
    for fp in df["filepath"]:
        p = Path(fp)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        file_paths.append(str(p))

    labels = df["label_idx"].values.astype(np.int32)

    def load_img(path_t):
        raw = tf.io.read_file(path_t)
        img = tf.image.decode_image(raw, channels=3, expand_animations=False)
        img = tf.image.resize(img, [INPUT_SHAPE[0], INPUT_SHAPE[1]])
        img.set_shape([INPUT_SHAPE[0], INPUT_SHAPE[1], 3])
        return mobilenet_v2.preprocess_input(img)

    ds = tf.data.Dataset.from_tensor_slices(file_paths)
    ds = ds.map(load_img, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    dense_layer = model.get_layer("predictions")
    feat_model = tf.keras.Model(inputs=model.inputs, outputs=dense_layer.input)

    logits_list = []
    for batch_x in ds:
        feats = feat_model(batch_x, training=False)
        logits_batch = tf.matmul(feats, dense_layer.kernel) + dense_layer.bias
        logits_list.append(logits_batch.numpy())

    raw_logits = np.concatenate(logits_list, axis=0)
    raw_probs = tf.nn.softmax(raw_logits).numpy()

    return df, raw_logits, raw_probs, labels

def fit_temperature(val_logits, val_labels):
    def nll_obj(T):
        scaled = val_logits / T[0]
        p = tf.nn.softmax(scaled).numpy()
        return log_loss(val_labels, p, labels=list(range(NUM_CLASSES)))

    res = minimize(nll_obj, [1.0], bounds=[(0.05, 10.0)], method="L-BFGS-B")
    return float(res.x[0])

def compute_classification_metrics(y_true, probs):
    preds = np.argmax(probs, axis=1)
    acc = accuracy_score(y_true, preds)
    bal_acc = balanced_accuracy_score(y_true, preds)
    p_mac, r_mac, f1_mac, _ = precision_recall_fscore_support(y_true, preds, average="macro", zero_division=0)
    p_wgt, r_wgt, f1_wgt, _ = precision_recall_fscore_support(y_true, preds, average="weighted", zero_division=0)
    cm = confusion_matrix(y_true, preds, labels=list(range(NUM_CLASSES))).tolist()

    try:
        roc_ovr = float(roc_auc_score(y_true, probs, multi_class="ovr"))
    except Exception:
        roc_ovr = None

    try:
        y_bin = label_binarize(y_true, classes=list(range(NUM_CLASSES)))
        pr_mac = float(average_precision_score(y_bin, probs, average="macro"))
    except Exception:
        pr_mac = None

    nll = float(log_loss(y_true, probs, labels=list(range(NUM_CLASSES))))
    brier = compute_multiclass_brier_score(y_true, probs)
    ece, mce, bins = compute_ece_and_bins(y_true, probs)

    # Class-wise metrics
    class_p, class_r, class_f1, class_supp = precision_recall_fscore_support(y_true, preds, labels=list(range(NUM_CLASSES)), zero_division=0)
    class_metrics = {}
    for i, cname in enumerate(CLASSES):
        class_metrics[cname] = {
            "precision": float(class_p[i]),
            "recall": float(class_r[i]),
            "f1": float(class_f1[i]),
            "support": int(class_supp[i])
        }

    return {
        "n_samples": len(y_true),
        "accuracy": float(acc),
        "balanced_accuracy": float(bal_acc),
        "macro_precision": float(p_mac),
        "macro_recall": float(r_mac),
        "macro_f1": float(f1_mac),
        "weighted_f1": float(f1_wgt),
        "roc_auc_ovr": roc_ovr,
        "pr_auc_macro": pr_mac,
        "nll": nll,
        "brier_score": brier,
        "ece": ece,
        "mce": mce,
        "confusion_matrix": cm,
        "class_metrics": class_metrics
    }

def main():
    print("==================================================================")
    print("🚀 AgriRoute Phase 3-6: Comprehensive Model B (V4.1) Evaluation")
    print("==================================================================")

    assert CKPT_PATH.exists(), f"Missing checkpoint: {CKPT_PATH}"
    print(f"Loading checkpoint: {CKPT_PATH}")
    model = tf.keras.models.load_model(CKPT_PATH)

    val_manifest = PROJECT_ROOT / "FINAL_GROUP_VAL_V4.csv"
    test_manifest = PROJECT_ROOT / "FINAL_GROUP_TEST_V4.csv"
    assert val_manifest.exists() and test_manifest.exists()

    # 1. Validation Inference & Temperature Fitting (Phase 4)
    print("\n--- Phase 4: Validation Set Inference & Temperature Scaling ---")
    df_val, logits_val, probs_val, y_val = evaluate_manifest_extract_logits(model, val_manifest)
    T_star = fit_temperature(logits_val, y_val)
    probs_cal_val = tf.nn.softmax(logits_val / T_star).numpy()
    val_ece_raw, _, _ = compute_ece_and_bins(y_val, probs_val)
    val_ece_cal, _, _ = compute_ece_and_bins(y_val, probs_cal_val)
    print(f"Validation N={len(y_val)}: Optimal Temperature T* = {T_star:.4f}")
    print(f"Validation ECE: {val_ece_raw:.5f} (raw) -> {val_ece_cal:.5f} (calibrated)")

    # 2. Final Test Set Evaluation (Phase 3)
    print("\n--- Phase 3: Final Test Set Evaluation (FINAL_GROUP_TEST_V4.csv) ---")
    df_test, logits_test, probs_test, y_test = evaluate_manifest_extract_logits(model, test_manifest)

    # MANDATORY ASSERTION: Every predicted row must have merged_split_partition_v4 == 'test'
    assert (df_test["merged_split_partition_v4"] == "test").all(), "CRITICAL LEAK: Non-test sample detected in test manifest!"
    print(f"✅ Automated Assertion Passed: All {len(df_test)} test samples have merged_split_partition_v4 == 'test'.")

    # Scale test logits
    probs_cal_test = tf.nn.softmax(logits_test / T_star).numpy()

    # A. Secondary Analysis: All variants (N=2,043)
    metrics_all_raw = compute_classification_metrics(y_test, probs_test)
    metrics_all_cal = compute_classification_metrics(y_test, probs_cal_test)
    ece_all_raw, mce_all_raw, bins_all_raw = compute_ece_and_bins(y_test, probs_test)
    ece_all_cal, mce_all_cal, bins_all_cal = compute_ece_and_bins(y_test, probs_cal_test)

    print(f"\nModel B V4.1 Test (All Variants, N={len(y_test)}):")
    print(f"  Accuracy:      {metrics_all_raw['accuracy']*100:.2f}%")
    print(f"  Balanced Acc:  {metrics_all_raw['balanced_accuracy']*100:.2f}%")
    print(f"  Macro F1:      {metrics_all_raw['macro_f1']*100:.2f}%")
    print(f"  ROC-AUC (OvR): {metrics_all_raw['roc_auc_ovr']:.4f}")
    print(f"  PR-AUC:        {metrics_all_raw['pr_auc_macro']:.4f}")
    print(f"  ECE (Raw):     {ece_all_raw:.5f} (NLL: {metrics_all_raw['nll']:.4f})")
    print(f"  ECE (Cal):     {ece_all_cal:.5f} (NLL: {metrics_all_cal['nll']:.4f}, Brier: {metrics_all_cal['brier_score']:.4f})")

    # B. Primary Analysis: Raw Screenshots Only (N=227)
    raw_mask = (df_test["is_raw"] == 1).values
    y_test_raw = y_test[raw_mask]
    probs_test_raw = probs_test[raw_mask]
    probs_cal_test_raw = probs_cal_test[raw_mask]

    metrics_raw_only = compute_classification_metrics(y_test_raw, probs_test_raw)
    metrics_raw_cal = compute_classification_metrics(y_test_raw, probs_cal_test_raw)
    ece_raw_only, mce_raw_only, bins_raw_only = compute_ece_and_bins(y_test_raw, probs_test_raw)
    ece_raw_cal, mce_raw_cal, bins_raw_cal = compute_ece_and_bins(y_test_raw, probs_cal_test_raw)

    print(f"\nModel B V4.1 Test (Primary: Raw Screenshots Only, N={len(y_test_raw)}):")
    print(f"  Accuracy:      {metrics_raw_only['accuracy']*100:.2f}%")
    print(f"  Balanced Acc:  {metrics_raw_only['balanced_accuracy']*100:.2f}%")
    print(f"  Macro F1:      {metrics_raw_only['macro_f1']*100:.2f}%")
    print(f"  ROC-AUC (OvR): {metrics_raw_only['roc_auc_ovr']:.4f}")
    print(f"  PR-AUC:        {metrics_raw_only['pr_auc_macro']:.4f}")
    print(f"  ECE (Raw):     {ece_raw_only:.5f}")
    print(f"  ECE (Cal):     {ece_raw_cal:.5f}")

    # Build 37-column prediction DataFrame
    print("\nBuilding authoritative 37-column prediction table...")
    pred_rows = []
    max_conf_raw = np.max(probs_test, axis=1)
    max_conf_cal = np.max(probs_cal_test, axis=1)
    preds_raw = np.argmax(probs_test, axis=1)

    for i in range(len(df_test)):
        r = df_test.iloc[i]
        rel_p = str(Path(r["filepath"]).relative_to(PROJECT_ROOT)) if Path(r["filepath"]).is_absolute() else str(r["filepath"])
        decision = "ACCEPTED" if max_conf_raw[i] >= TAU_THRESHOLD else "ABSTAINED"

        row_dict = {
            "sample_id": f"TEST_V4_1_{i:04d}",
            "dataset_name": "Kaggle_FreshRotten",
            "split_name": "final_group_test_v4",
            "model_name": "Model_B_V4_1_Group_Aware",
            "relative_path": rel_p,
            "filename": r["filename"],
            "base_filename": r["base_filename"],
            "base_group_id": r["group_id"],
            "variant_type": r["variant_type"],
            "is_raw": int(r["is_raw"]),
            "md5": r["md5"],
            "ground_truth_label": CLASSES[int(y_test[i])],
            "ground_truth_idx": int(y_test[i]),
            "predicted_label": CLASSES[int(preds_raw[i])],
            "predicted_idx": int(preds_raw[i]),
            "max_confidence": float(max_conf_raw[i]),
            "tau_threshold": TAU_THRESHOLD,
            "decision": decision,
            "temperature_T": float(T_star)
        }
        for c_idx, cname in enumerate(CLASSES):
            row_dict[f"prob_{cname}"] = float(probs_test[i, c_idx])
        for c_idx, cname in enumerate(CLASSES):
            row_dict[f"prob_cal_{cname}"] = float(probs_cal_test[i, c_idx])
        for c_idx, cname in enumerate(CLASSES):
            row_dict[f"logit_{cname}"] = float(logits_test[i, c_idx])

        pred_rows.append(row_dict)

    df_preds_v4_1 = pd.DataFrame(pred_rows)
    pred_csv_path = PROJECT_ROOT / "MODEL_B_V4_1_PREDICTIONS.csv"
    df_preds_v4_1.to_csv(pred_csv_path, index=False)
    print(f"✅ Saved {pred_csv_path} ({len(df_preds_v4_1)} rows, 37 columns)")

    # Save Reliability Table CSV (Phase 4)
    df_rel_table = pd.DataFrame(bins_all_cal)
    rel_table_path = PROJECT_ROOT / "MODEL_B_V4_1_RELIABILITY_TABLE.csv"
    df_rel_table.to_csv(rel_table_path, index=False)
    print(f"✅ Saved {rel_table_path}")

    # Phase 5: Selective Prediction Analysis
    print("\n--- Phase 5: Selective Prediction Analysis (tau = 0.90) ---")
    accepted_mask = (max_conf_raw >= TAU_THRESHOLD)
    n_accepted = int(np.sum(accepted_mask))
    n_abstained = int(len(df_test) - n_accepted)
    cov_ratio = float(n_accepted / len(df_test))
    acc_accepted = float(accuracy_score(y_test[accepted_mask], preds_raw[accepted_mask])) if n_accepted > 0 else 0.0
    err_accepted = 1.0 - acc_accepted

    # Class-wise selective performance
    class_selective = {}
    for c_idx, cname in enumerate(CLASSES):
        c_mask = (y_test == c_idx)
        c_acc_mask = c_mask & accepted_mask
        n_c_total = int(np.sum(c_mask))
        n_c_acc = int(np.sum(c_acc_mask))
        c_cov = float(n_c_acc / n_c_total) if n_c_total > 0 else 0.0
        c_acc = float(accuracy_score(y_test[c_acc_mask], preds_raw[c_acc_mask])) if n_c_acc > 0 else 0.0
        class_selective[cname] = {
            "total_samples": n_c_total,
            "accepted_samples": n_c_acc,
            "coverage": c_cov,
            "accepted_accuracy": c_acc
        }

    selective_data = {
        "operating_point_tau": TAU_THRESHOLD,
        "confidence_type": "raw_softmax_probability",
        "total_test_samples": len(df_test),
        "accepted_samples": n_accepted,
        "abstained_samples": n_abstained,
        "coverage_ratio": cov_ratio,
        "accepted_accuracy": acc_accepted,
        "accepted_error_rate": err_accepted,
        "class_wise_selective": class_selective
    }
    sel_path = PROJECT_ROOT / "MODEL_B_V4_1_SELECTIVE_RESULTS.json"
    with open(sel_path, "w") as f:
        json.dump(selective_data, f, indent=2)
    print(f"✅ Saved {sel_path}")
    print(f"  Coverage: {cov_ratio*100:.2f}% | Accepted Acc: {acc_accepted*100:.2f}% | Error: {err_accepted*100:.2f}%")

    # Phase 6: External Dataset Benchmarking
    print("\n--- Phase 6: External Dataset Benchmarking (FruitVision & Sultana) ---")
    fv_manifest = PROJECT_ROOT / "experiments" / "group_leakage_study" / "fruitvision_clean.csv"
    sul_manifest = PROJECT_ROOT / "experiments" / "group_leakage_study" / "sultana_clean.csv"

    # FruitVision
    df_fv, logits_fv, probs_fv, y_fv = evaluate_manifest_extract_logits(model, fv_manifest)
    probs_cal_fv = tf.nn.softmax(logits_fv / T_star).numpy()
    metrics_fv = compute_classification_metrics(y_fv, probs_fv)

    # FruitVision Selective
    conf_fv = np.max(probs_fv, axis=1)
    acc_fv_mask = (conf_fv >= TAU_THRESHOLD)
    n_fv_acc = int(np.sum(acc_fv_mask))
    cov_fv = float(n_fv_acc / len(df_fv))
    preds_fv = np.argmax(probs_fv, axis=1)
    acc_acc_fv = float(accuracy_score(y_fv[acc_fv_mask], preds_fv[acc_fv_mask])) if n_fv_acc > 0 else 0.0

    print(f"FruitVision (N={len(df_fv)}): Acc={metrics_fv['accuracy']*100:.2f}%, F1={metrics_fv['macro_f1']*100:.2f}%, ROC-AUC={metrics_fv['roc_auc_ovr']:.4f}")
    print(f"  Selective (tau=0.90): Coverage={cov_fv*100:.2f}%, Acc@Accepted={acc_acc_fv*100:.2f}%")

    # Sultana
    df_sul, logits_sul, probs_sul, y_sul = evaluate_manifest_extract_logits(model, sul_manifest)
    probs_cal_sul = tf.nn.softmax(logits_sul / T_star).numpy()
    metrics_sul = compute_classification_metrics(y_sul, probs_sul)

    # Sultana Selective
    conf_sul = np.max(probs_sul, axis=1)
    acc_sul_mask = (conf_sul >= TAU_THRESHOLD)
    n_sul_acc = int(np.sum(acc_sul_mask))
    cov_sul = float(n_sul_acc / len(df_sul))
    preds_sul = np.argmax(probs_sul, axis=1)
    acc_acc_sul = float(accuracy_score(y_sul[acc_sul_mask], preds_sul[acc_sul_mask])) if n_sul_acc > 0 else 0.0

    print(f"Sultana (N={len(df_sul)}): Acc={metrics_sul['accuracy']*100:.2f}%, F1={metrics_sul['macro_f1']*100:.2f}%, ROC-AUC={metrics_sul['roc_auc_ovr']:.4f}")
    print(f"  Selective (tau=0.90): Coverage={cov_sul*100:.2f}%, Acc@Accepted={acc_acc_sul*100:.2f}%")

    external_results = {
        "metadata": {
            "model_identifier": "Model_B_V4_1_Group_Aware",
            "checkpoint_sha256": hashlib.sha256(open(CKPT_PATH, "rb").read()).hexdigest(),
            "internal_temperature_T": float(T_star),
            "disclaimer": "Internal temperature T* fitted on Kaggle validation set. Scores are temperature-scaled, NOT externally calibrated."
        },
        "fruitvision": {
            "n_samples": len(df_fv),
            "accuracy": metrics_fv["accuracy"],
            "balanced_accuracy": metrics_fv["balanced_accuracy"],
            "macro_precision": metrics_fv["macro_precision"],
            "macro_recall": metrics_fv["macro_recall"],
            "macro_f1": metrics_fv["macro_f1"],
            "roc_auc_ovr": metrics_fv["roc_auc_ovr"],
            "pr_auc_macro": metrics_fv["pr_auc_macro"],
            "raw_ece": metrics_fv["ece"],
            "raw_nll": metrics_fv["nll"],
            "selective_prediction": {
                "tau_threshold": TAU_THRESHOLD,
                "coverage_ratio": cov_fv,
                "accepted_samples": n_fv_acc,
                "accepted_accuracy": acc_acc_fv
            }
        },
        "sultana": {
            "n_samples": len(df_sul),
            "accuracy": metrics_sul["accuracy"],
            "balanced_accuracy": metrics_sul["balanced_accuracy"],
            "macro_precision": metrics_sul["macro_precision"],
            "macro_recall": metrics_sul["macro_recall"],
            "macro_f1": metrics_sul["macro_f1"],
            "roc_auc_ovr": metrics_sul["roc_auc_ovr"],
            "pr_auc_macro": metrics_sul["pr_auc_macro"],
            "raw_ece": metrics_sul["ece"],
            "raw_nll": metrics_sul["nll"],
            "selective_prediction": {
                "tau_threshold": TAU_THRESHOLD,
                "coverage_ratio": cov_sul,
                "accepted_samples": n_sul_acc,
                "accepted_accuracy": acc_acc_sul
            }
        }
    }
    ext_path = PROJECT_ROOT / "MODEL_B_V4_1_EXTERNAL_RESULTS.json"
    with open(ext_path, "w") as f:
        json.dump(external_results, f, indent=2)
    print(f"✅ Saved {ext_path}")

    # Save comprehensive metrics JSON
    all_metrics = {
        "metadata": {
            "model_identifier": "Model_B_V4_1_Group_Aware",
            "checkpoint_sha256": hashlib.sha256(open(CKPT_PATH, "rb").read()).hexdigest(),
            "manifest_verified": "FINAL_GROUP_TEST_V4.csv",
            "merged_supergroups": 226,
            "filename_derived_groups": 227,
            "total_test_samples": len(df_test),
            "raw_screenshots_count": len(y_test_raw),
            "transformed_variants_count": len(df_test) - len(y_test_raw)
        },
        "primary_analysis_raw_only": metrics_raw_only,
        "secondary_analysis_all_variants": {
            "uncalibrated": metrics_all_raw,
            "calibrated": metrics_all_cal
        }
    }
    metrics_path = PROJECT_ROOT / "MODEL_B_V4_1_METRICS.json"
    with open(metrics_path, "w") as f:
        json.dump(all_metrics, f, indent=2)
    print(f"✅ Saved {metrics_path}")

    # Save calibration JSON
    cal_data = {
        "validation_temperature_T": float(T_star),
        "validation_samples": len(y_val),
        "test_samples": len(y_test),
        "uncalibrated_ece": ece_all_raw,
        "uncalibrated_mce": mce_all_raw,
        "uncalibrated_nll": metrics_all_raw["nll"],
        "calibrated_ece": ece_all_cal,
        "calibrated_mce": mce_all_cal,
        "calibrated_nll": metrics_all_cal["nll"],
        "multiclass_brier_score": metrics_all_cal["brier_score"],
        "reliability_bins": bins_all_cal
    }
    cal_path = PROJECT_ROOT / "MODEL_B_V4_1_CALIBRATION.json"
    with open(cal_path, "w") as f:
        json.dump(cal_data, f, indent=2)
    print(f"✅ Saved {cal_path}")

    print("\n🎉 Phase 3-6 execution completed successfully!")

if __name__ == "__main__":
    main()
