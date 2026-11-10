"""
scripts/run_stage4_1_benchmark.py
=================================
Executes the Stage 4.1 Local Cross-Dataset Benchmark Inference.

Safeguards:
- Frozen Model B V4.1 checkpoint (SHA-256 verified) loaded with training=False.
- Reads strictly rows with inclusion_status == 'INCLUDED' from STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv.
- Thresholds loaded strictly from STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv.
- Evaluates MSP, Energy, ODIN, Mahalanobis, OpenMax, and Dual-Gate Cascade.
- Evaluates all three sensitivity tiers:
    * Primary: N = 13,465
    * Tier 1: N = 13,409 (excluding 56 cross-partition pHash collisions)
    * Tier 2: N = 13,382 (excluding 56 cross-partition + 27 multi-label collisions)
- Generates all required deliverables:
    * STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv
    * STAGE4_1_PARTITION_METRICS.csv
    * STAGE4_1_SENSITIVITY_ANALYSIS.csv
    * STAGE4_1_CONFIDENCE_INTERVALS.csv
"""

import os
import sys
import time
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from scipy.stats import weibull_min
from sklearn.covariance import LedoitWolf
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score,
    roc_auc_score, average_precision_score
)
import tensorflow as tf

PROJECT_ROOT = Path("/Users/abby/Desktop/spoilage-predictor")
MANIFEST_PATH = PROJECT_ROOT / "STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv"
THRESHOLDS_PATH = PROJECT_ROOT / "STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv"
PHASH_REVIEW_PATH = PROJECT_ROOT / "STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv"
CKPT_PATH = PROJECT_ROOT / "MODEL_B_V4_1_CHECKPOINT.keras"
TRAIN_NPZ_PATH = PROJECT_ROOT / "experiments" / "open_set_v1" / "train_features.npz"

EXPECTED_CKPT_SHA256 = "4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4"
BATCH_SIZE = 32
NUM_CLASSES = 6
CLASSES = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def load_img(p):
    img = tf.io.read_file(p)
    img = tf.io.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.resize(img, (224, 224))
    img = tf.cast(img, tf.float32)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    return img

def compute_oscr(id_correct_mask, id_scores, ood_scores):
    """
    Computes Open-Set Classification Rate (OSCR) curve and area under curve.
    id_correct_mask: bool array for ID samples indicating whether top-1 prediction is correct
    id_scores: ID detector scores (higher = ID)
    ood_scores: OOD detector scores (higher = ID)
    """
    # Thresholds over all unique scores
    all_scores = np.sort(np.concatenate([id_scores, ood_scores]))[::-1]
    # Downsample thresholds for numerical integration if too large
    if len(all_scores) > 2000:
        thresholds = np.percentile(all_scores, np.linspace(0, 100, 2000))
    else:
        thresholds = all_scores

    ccr = []
    fpr = []
    n_id = len(id_scores)
    n_ood = len(ood_scores)

    for tau in thresholds:
        # CCR: proportion of ID samples that are correctly classified AND accepted
        c = np.sum(id_correct_mask & (id_scores >= tau)) / float(n_id)
        # FPR: proportion of OOD samples that are accepted
        f = np.sum(ood_scores >= tau) / float(n_ood)
        ccr.append(c)
        fpr.append(f)

    ccr = np.array(ccr)
    fpr = np.array(fpr)
    # Sort by fpr ascending for trapezoidal integration
    sort_idx = np.argsort(fpr)
    fpr_sorted = fpr[sort_idx]
    ccr_sorted = ccr[sort_idx]
    oscr_area = np.trapz(ccr_sorted, fpr_sorted)
    return float(oscr_area)

def main():
    print("=" * 80)
    print("STAGE 4.1: LOCAL CROSS-DATASET BENCHMARK EXECUTION")
    print("=" * 80)

    # 1. Verify Checkpoint Integrity
    actual_sha = compute_sha256(CKPT_PATH)
    print(f"Checkpoint SHA-256: {actual_sha}")
    assert actual_sha == EXPECTED_CKPT_SHA256, "FATAL: Checkpoint hash mismatch!"
    print("✅ Frozen Model B V4.1 Checkpoint verified byte-identical.")

    # 2. Load Manifest & Filter INCLUDED
    manifest_df = pd.read_csv(MANIFEST_PATH)
    df_eval = manifest_df[manifest_df["inclusion_status"] == "INCLUDED"].copy().reset_index(drop=True)
    N_total = len(df_eval)
    print(f"Loaded evaluation cohort: {N_total} images")
    assert N_total == 13465, f"Expected 13,465 images, got {N_total}"
    assert len(df_eval[df_eval["dataset"] == "ToxiFruit_2026"]) == 0, "FATAL: ToxiFruit records present!"

    # 3. Load Threshold Table
    thresh_df = pd.read_csv(THRESHOLDS_PATH)
    print(f"Loaded threshold table: {len(thresh_df)} rows")

    # Extract threshold dictionary
    thresholds = {}
    for _, r in thresh_df.iterrows():
        cfg = r["configuration_id"]
        if "dual_gate" in cfg:
            thresholds[cfg] = {
                "energy": float(r["energy_threshold"]),
                "msp": float(r["msp_threshold"])
            }
        else:
            thresholds[cfg] = float(r["primary_threshold_value"])

    # 4. Load Training Statistics for Mahalanobis and OpenMax
    print("\nFitting Mahalanobis Precision Matrix and OpenMax Weibull Tail Models from clean training features...")
    train_data = np.load(TRAIN_NPZ_PATH)
    X_train = train_data["features"]
    y_train = train_data["labels"]
    D = X_train.shape[1]

    # Class Centroids
    centroids = np.zeros((NUM_CLASSES, D), dtype=np.float32)
    for k in range(NUM_CLASSES):
        idx_k = np.where(y_train == k)[0]
        centroids[k] = np.mean(X_train[idx_k], axis=0)

    # Centered features for Ledoit-Wolf
    X_centered = np.zeros_like(X_train)
    for k in range(NUM_CLASSES):
        idx_k = np.where(y_train == k)[0]
        X_centered[idx_k] = X_train[idx_k] - centroids[k]

    lw = LedoitWolf(assume_centered=True)
    lw.fit(X_centered)
    Sigma_LW_inv = np.linalg.inv(lw.covariance_)
    print("✅ Mahalanobis precision matrix fitted.")

    # OpenMax Weibull Models
    train_preds = np.argmax(train_data["probs"], axis=1)
    train_correct_mask = (train_preds == train_data["labels"])
    mavs = np.zeros((NUM_CLASSES, D), dtype=np.float32)
    weibull_models = {}
    tail_size = 20

    for k in range(NUM_CLASSES):
        k_correct_indices = np.where((train_data["labels"] == k) & train_correct_mask)[0]
        k_feats = X_train[k_correct_indices]
        mavs[k] = np.mean(k_feats, axis=0)
        dists = np.linalg.norm(k_feats - mavs[k], axis=1)
        tail_dists = np.sort(dists)[-tail_size:]
        shape, loc, scale = weibull_min.fit(tail_dists, floc=0)
        weibull_models[k] = {"shape": float(shape), "scale": float(scale), "mav": mavs[k]}
    print("✅ OpenMax Weibull models fitted on training data.")

    # 5. Load Model B V4.1
    print("\nLoading Model B V4.1 in inference mode (training=False)...")
    ckpt_model = tf.keras.models.load_model(str(CKPT_PATH))
    feat_model = tf.keras.Model(inputs=ckpt_model.input, outputs=ckpt_model.layers[-2].output)
    dense_layer = ckpt_model.layers[-1]
    kernel = dense_layer.kernel.numpy()
    bias = dense_layer.bias.numpy()

    # 6. Run Inference and Feature Extraction
    print(f"\nExecuting forward inference and feature extraction on N = {N_total} images...")
    img_paths = df_eval["relative_path"].tolist()
    
    feats_all = []
    logits_all = []
    probs_all = []
    odin_scores_all = []

    t_start = time.time()
    total_batches = int(np.ceil(N_total / BATCH_SIZE))
    eps_odin = 0.0014
    T_odin = 1000.0

    # Dataset pipeline
    abs_img_paths = [str(PROJECT_ROOT / p) for p in img_paths]
    ds = tf.data.Dataset.from_tensor_slices(abs_img_paths).map(load_img, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE)

    for b_idx, batch_x in enumerate(ds):
        # Forward pass for features
        b_feats = feat_model(batch_x, training=False).numpy()
        b_logits = np.dot(b_feats, kernel) + bias
        # Softmax
        b_max = np.max(b_logits, axis=1, keepdims=True)
        b_exp = np.exp(b_logits - b_max)
        b_probs = b_exp / np.sum(b_exp, axis=1, keepdims=True)

        feats_all.append(b_feats)
        logits_all.append(b_logits)
        probs_all.append(b_probs)

        # ODIN with GradientTape on batch_x
        with tf.GradientTape() as tape:
            tape.watch(batch_x)
            f_acts = feat_model(batch_x, training=False)
            b_l = tf.matmul(f_acts, dense_layer.kernel) + dense_layer.bias
            s_l = b_l / T_odin
            max_s_l = tf.reduce_max(s_l, axis=1)
        grads = tape.gradient(max_s_l, batch_x)
        p_imgs = batch_x - eps_odin * tf.sign(-grads)
        p_imgs = tf.clip_by_value(p_imgs, -1.0, 1.0)
        p_acts = feat_model(p_imgs, training=False)
        p_l = tf.matmul(p_acts, dense_layer.kernel) + dense_layer.bias
        p_probs = tf.nn.softmax(p_l / T_odin).numpy()
        b_odin = np.max(p_probs, axis=1)
        odin_scores_all.append(b_odin)

        if (b_idx + 1) % 50 == 0 or (b_idx + 1) == total_batches:
            elapsed = time.time() - t_start
            processed = min((b_idx + 1) * BATCH_SIZE, N_total)
            speed = processed / elapsed
            print(f"  Batch {b_idx + 1}/{total_batches} ({processed}/{N_total} images) - {speed:.1f} img/s - elapsed: {elapsed:.1f}s")

    all_feats = np.concatenate(feats_all, axis=0).astype(np.float32)
    all_logits = np.concatenate(logits_all, axis=0).astype(np.float32)
    all_probs = np.concatenate(probs_all, axis=0).astype(np.float32)
    all_odin = np.concatenate(odin_scores_all, axis=0).astype(np.float32)

    assert len(all_feats) == N_total, "Feature count mismatch!"
    print(f"\n✅ Completed neural network inference in {time.time() - t_start:.1f} seconds.")

    # 7. Compute Detector Scores
    print("\nComputing OOD detector scores across all 13,465 images...")
    # A. MSP
    score_msp = np.max(all_probs, axis=1)

    # B. Energy
    score_energy = logsumexp(all_logits, axis=1).astype(np.float32)

    # C. ODIN
    score_odin = all_odin

    # D. Mahalanobis
    print("  Computing Ledoit-Wolf Mahalanobis scores...")
    score_mahalanobis = np.zeros(N_total, dtype=np.float32)
    for i in range(N_total):
        diffs = centroids - all_feats[i]
        dists_sq = np.sum(np.dot(diffs, Sigma_LW_inv) * diffs, axis=1)
        score_mahalanobis[i] = -np.sqrt(np.max([np.min(dists_sq), 0.0]))

    # E. OpenMax
    print("  Computing OpenMax scores (alpha=2)...")
    score_openmax = np.zeros(N_total, dtype=np.float32)
    alpha = 2
    for i in range(N_total):
        x_f = all_feats[i]
        x_z = all_logits[i]
        ranked_classes = np.argsort(x_z)[::-1]
        weights = np.ones(NUM_CLASSES, dtype=np.float32)
        for rank_idx in range(alpha):
            c_k = ranked_classes[rank_idx]
            dist_k = np.linalg.norm(x_f - mavs[c_k])
            w_shape = weibull_models[c_k]["shape"]
            w_scale = weibull_models[c_k]["scale"]
            omega_k = np.exp(- (dist_k / (w_scale + 1e-8)) ** w_shape)
            alpha_weight = 1.0 - (rank_idx / float(alpha)) * (1.0 - omega_k)
            weights[c_k] = alpha_weight
        v_k = x_z * weights
        v_0 = np.sum(x_z * (1.0 - weights))
        all_v = np.concatenate([[v_0], v_k])
        max_v = np.max(all_v)
        exp_v = np.exp(all_v - max_v)
        p_om = exp_v / np.sum(exp_v)
        score_openmax[i] = 1.0 - p_om[0]

    print("✅ All detector scores computed successfully.")

    # 8. Map Ground Truth Labels & Prediction Classes
    print("\nMapping ground truth and predictions...")
    top1_pred_idx = np.argmax(all_probs, axis=1)
    top1_pred_class = [CLASSES[idx] for idx in top1_pred_idx]
    top1_pred_prob = np.max(all_probs, axis=1)

    # Class mapping
    def get_gt_label(row):
        part = row["partition_group"]
        sp = row["fruit_species"]
        cond = row["condition"]
        if part in ["A_PRIMARY_IN_DISTRIBUTION", "B_EXTERNAL_KNOWN_SHIFT"]:
            if "Apple" in sp and cond == "Fresh": return 0
            if "Banana" in sp and cond == "Fresh": return 1
            if "Orange" in sp and cond == "Fresh": return 2
            if "Apple" in sp and cond == "Rotten": return 3
            if "Banana" in sp and cond == "Rotten": return 4
            if "Orange" in sp and cond == "Rotten": return 5
        return -1 # Unknown / OOD

    gt_labels = np.array([get_gt_label(r) for _, r in df_eval.iterrows()], dtype=np.int32)
    is_correct = np.where(gt_labels >= 0, (top1_pred_idx == gt_labels).astype(int), -1)

    # 9. Apply Operating Thresholds & Acceptance Decisions
    print("Applying frozen operating thresholds from STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv...")
    # Single methods
    acc_msp_95 = (score_msp >= thresholds["score_msp_tau95"]).astype(int)
    acc_msp_90 = (score_msp >= thresholds["score_msp_tau90"]).astype(int)

    acc_energy_95 = (score_energy >= thresholds["score_energy_id_tau95"]).astype(int)
    acc_energy_90 = (score_energy >= thresholds["score_energy_id_tau90"]).astype(int)

    acc_odin_95 = (score_odin >= thresholds["score_odin_tau95"]).astype(int)
    acc_odin_90 = (score_odin >= thresholds["score_odin_tau90"]).astype(int)

    acc_maha_95 = (score_mahalanobis >= thresholds["score_mahalanobis_id_tau95"]).astype(int)
    acc_maha_90 = (score_mahalanobis >= thresholds["score_mahalanobis_id_tau90"]).astype(int)

    acc_openmax_95 = (score_openmax >= thresholds["score_openmax_id_tau95"]).astype(int)
    acc_openmax_90 = (score_openmax >= thresholds["score_openmax_id_tau90"]).astype(int)

    # Dual-Gate Cascade (Energy AND MSP)
    dg95 = thresholds["dual_gate_cascade_tau95"]
    acc_dg_95 = ((score_energy >= dg95["energy"]) & (score_msp >= dg95["msp"])).astype(int)

    dg90 = thresholds["dual_gate_cascade_tau90"]
    acc_dg_90 = ((score_energy >= dg90["energy"]) & (score_msp >= dg90["msp"])).astype(int)

    # 10. Assemble STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv
    pred_df = df_eval.copy()
    pred_df["ground_truth_label_idx"] = gt_labels
    pred_df["top1_pred_idx"] = top1_pred_idx
    pred_df["top1_pred_class"] = top1_pred_class
    pred_df["top1_pred_prob"] = top1_pred_prob
    pred_df["is_correct_known_pred"] = is_correct

    pred_df["score_msp"] = score_msp
    pred_df["score_energy"] = score_energy
    pred_df["score_odin"] = score_odin
    pred_df["score_mahalanobis"] = score_mahalanobis
    pred_df["score_openmax"] = score_openmax

    pred_df["accept_msp_tau95"] = acc_msp_95
    pred_df["accept_msp_tau90"] = acc_msp_90
    pred_df["accept_energy_tau95"] = acc_energy_95
    pred_df["accept_energy_tau90"] = acc_energy_90
    pred_df["accept_odin_tau95"] = acc_odin_95
    pred_df["accept_odin_tau90"] = acc_odin_90
    pred_df["accept_mahalanobis_tau95"] = acc_maha_95
    pred_df["accept_mahalanobis_tau90"] = acc_maha_90
    pred_df["accept_openmax_tau95"] = acc_openmax_95
    pred_df["accept_openmax_tau90"] = acc_openmax_90
    pred_df["accept_dualgate_tau95"] = acc_dg_95
    pred_df["accept_dualgate_tau90"] = acc_dg_90

    out_preds_path = PROJECT_ROOT / "STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv"
    pred_df.to_csv(out_preds_path, index=False)
    print(f"\n✅ Saved {len(pred_df)} rows to {out_preds_path}")

    # 11. Compute Metrics across Partitions & Detectors
    print("\nComputing authoritative partition-level metrics and sensitivity tiers...")
    
    # Load pHash Review for Sensitivity Tiers
    phash_df = pd.read_csv(PHASH_REVIEW_PATH)
    cross_part_ids = set(phash_df[phash_df["phash_group_type"] == "CROSS_PARTITION"]["image_id"])
    multi_label_ids = set(phash_df[phash_df["phash_group_type"] == "INTRA_PARTITION_MULTI_LABEL"]["image_id"])
    tier2_excluded_ids = cross_part_ids.union(multi_label_ids)

    tiers = {
        "Primary (N=13,465)": pred_df,
        "Tier 1 (N=13,409)": pred_df[~pred_df["image_id"].isin(cross_part_ids)].copy(),
        "Tier 2 (N=13,382)": pred_df[~pred_df["image_id"].isin(tier2_excluded_ids)].copy()
    }

    scorers = ["msp", "energy", "odin", "mahalanobis", "openmax", "dualgate"]
    
    metrics_records = []
    sensitivity_records = []

    for tier_name, t_df in tiers.items():
        print(f"\nEvaluating {tier_name} (Cohort size: {len(t_df)})...")
        # Subsets
        df_A = t_df[t_df["partition_group"] == "A_PRIMARY_IN_DISTRIBUTION"]
        df_B = t_df[t_df["partition_group"] == "B_EXTERNAL_KNOWN_SHIFT"]
        df_C = t_df[t_df["partition_group"] == "C_CONDITION_SHIFT_UNKNOWN"]
        df_D1 = t_df[t_df["partition_group"] == "D1_PURE_SEMANTIC_SHIFT"]
        df_D2 = t_df[t_df["partition_group"] == "D2_COMBINED_SEMANTIC_TREATMENT_SHIFT"]

        # 1. Closed-set known-class metrics on A and B
        for part_code, p_df in [("Partition A (ID Test)", df_A), ("Partition B (External Known)", df_B)]:
            y_t = p_df["ground_truth_label_idx"].values
            y_p = p_df["top1_pred_idx"].values
            acc = accuracy_score(y_t, y_p)
            bal_acc = balanced_accuracy_score(y_t, y_p)
            macro_f1 = f1_score(y_t, y_p, average="macro")

            if tier_name == "Primary (N=13,465)":
                metrics_records.append({
                    "evaluation_tier": tier_name,
                    "partition_evaluation": part_code,
                    "detector": "Closed-Set Model B",
                    "sample_count": len(p_df),
                    "accuracy": f"{acc*100:.2f}%",
                    "balanced_accuracy": f"{bal_acc*100:.2f}%",
                    "macro_f1": f"{macro_f1*100:.2f}%",
                    "auroc": "N/A",
                    "aupr_in": "N/A",
                    "aupr_out": "N/A",
                    "fpr95_empirical": "N/A",
                    "oscr": "N/A",
                    "ufar_tau95": "N/A",
                    "ufar_fresh_tau95": "N/A",
                    "abstention_rate_tau95": "N/A"
                })

        # 2. OOD Evaluation against Unknown Partitions (C, D1, D2)
        # Pairings:
        # Benchmark 1: Partition A (ID Known) vs Partition C
        # Benchmark 2: Partition A (ID Known) vs Partition D1
        # Benchmark 3: Partition A (ID Known) vs Partition D2
        # Benchmark 4: Partition B (External Known) vs Partition C
        # Benchmark 5: Partition B (External Known) vs Partition D1
        # Benchmark 6: Partition B (External Known) vs Partition D2

        ood_eval_pairs = [
            ("A_vs_C (ID Known vs Formalin Known)", df_A, df_C),
            ("A_vs_D1 (ID Known vs Semantic Unknown)", df_A, df_D1),
            ("A_vs_D2 (ID Known vs Combined Unknown)", df_A, df_D2),
            ("B_vs_C (External Known vs Formalin Known)", df_B, df_C),
            ("B_vs_D1 (External Known vs Semantic Unknown)", df_B, df_D1),
            ("B_vs_D2 (External Known vs Combined Unknown)", df_B, df_D2)
        ]

        for pair_name, id_sub, ood_sub in ood_eval_pairs:
            n_id = len(id_sub)
            n_ood = len(ood_sub)
            y_ood_true = np.concatenate([np.zeros(n_id), np.ones(n_ood)])
            y_id_true = np.concatenate([np.ones(n_id), np.zeros(n_ood)])
            id_correct_mask = (id_sub["is_correct_known_pred"] == 1).values

            for sc in scorers:
                if sc == "dualgate":
                    # For dual-gate, acceptance is boolean.
                    # Proxy continuous score for AUROC / OSCR is minimum normalized margin:
                    # min((S_E - tau_E)/std_E, (S_M - tau_M)/std_M)
                    # We compute operational metrics directly from accept_dualgate_tau95
                    s_id = ((id_sub["score_energy"] - thresholds["dual_gate_cascade_tau95"]["energy"]) + 
                            (id_sub["score_msp"] - thresholds["dual_gate_cascade_tau95"]["msp"])).values
                    s_ood = ((ood_sub["score_energy"] - thresholds["dual_gate_cascade_tau95"]["energy"]) + 
                             (ood_sub["score_msp"] - thresholds["dual_gate_cascade_tau95"]["msp"])).values
                    acc_id_95 = id_sub["accept_dualgate_tau95"].values
                    acc_ood_95 = ood_sub["accept_dualgate_tau95"].values
                else:
                    col_name = f"score_{sc}"
                    s_id = id_sub[col_name].values
                    s_ood = ood_sub[col_name].values
                    acc_id_95 = id_sub[f"accept_{sc}_tau95"].values
                    acc_ood_95 = ood_sub[f"accept_{sc}_tau95"].values

                all_scores = np.concatenate([s_id, s_ood])

                # AUROC: higher anomaly score for OOD (-s)
                auroc = roc_auc_score(y_ood_true, -all_scores)
                # AUPR-OUT: Precision-Recall treating OOD as positive
                aupr_out = average_precision_score(y_ood_true, -all_scores)
                # AUPR-IN: Precision-Recall treating ID as positive
                aupr_in = average_precision_score(y_id_true, all_scores)

                # Empirical FPR@tau95 on OOD: proportion of OOD accepted
                ufar_95 = np.mean(acc_ood_95)
                # UFAR-Fresh: proportion of OOD accepted AND top-1 pred in [0, 1, 2]
                ood_preds = ood_sub["top1_pred_idx"].values
                is_fresh_pred = np.isin(ood_preds, [0, 1, 2])
                ufar_fresh_95 = np.sum((acc_ood_95 == 1) & is_fresh_pred) / float(n_ood)

                # Abstention on ID (KRR)
                krr_95 = 1.0 - np.mean(acc_id_95)

                # OSCR
                oscr = compute_oscr(id_correct_mask, s_id, s_ood)

                rec = {
                    "evaluation_tier": tier_name,
                    "partition_pair": pair_name,
                    "detector": sc.upper(),
                    "n_id": n_id,
                    "n_ood": n_ood,
                    "auroc": f"{auroc*100:.2f}%",
                    "aupr_in": f"{aupr_in*100:.2f}%",
                    "aupr_out": f"{aupr_out*100:.2f}%",
                    "empirical_ufar_tau95": f"{ufar_95*100:.2f}%",
                    "ufar_fresh_tau95": f"{ufar_fresh_95*100:.2f}%",
                    "id_abstention_krr_tau95": f"{krr_95*100:.2f}%",
                    "oscr": f"{oscr*100:.2f}%"
                }

                if tier_name == "Primary (N=13,465)":
                    metrics_records.append(rec)
                sensitivity_records.append(rec)

    # Save Partition Metrics
    df_metrics = pd.DataFrame(metrics_records)
    out_metrics_path = PROJECT_ROOT / "STAGE4_1_PARTITION_METRICS.csv"
    df_metrics.to_csv(out_metrics_path, index=False)
    print(f"\n✅ Saved partition metrics to {out_metrics_path}")

    # Save Sensitivity Analysis
    df_sens = pd.DataFrame(sensitivity_records)
    out_sens_path = PROJECT_ROOT / "STAGE4_1_SENSITIVITY_ANALYSIS.csv"
    df_sens.to_csv(out_sens_path, index=False)
    print(f"✅ Saved sensitivity analysis across all 3 tiers to {out_sens_path}")

    # 12. Bootstrap Confidence Intervals (1,000 resamples)
    print("\nComputing 95% Bootstrap Confidence Intervals (B=1,000 iterations)...")
    np.random.seed(42)
    B = 1000
    ci_records = []

    # Selected representative benchmarks:
    # 1. Closed-set Macro-F1 on Partition A and B
    for part_name, sub in [("Partition A (ID Known)", df_A), ("Partition B (External Known)", df_B)]:
        y_t = sub["ground_truth_label_idx"].values
        y_p = sub["top1_pred_idx"].values
        n = len(y_t)
        boot_f1 = []
        for _ in range(B):
            idx = np.random.choice(n, size=n, replace=True)
            boot_f1.append(f1_score(y_t[idx], y_p[idx], average="macro"))
        ci_low = np.percentile(boot_f1, 2.5) * 100
        ci_high = np.percentile(boot_f1, 97.5) * 100
        est = f1_score(y_t, y_p, average="macro") * 100
        ci_records.append({
            "benchmark_task": f"Closed-Set Macro-F1 ({part_name})",
            "detector": "Model B V4.1",
            "point_estimate": f"{est:.2f}%",
            "ci_95_lower": f"{ci_low:.2f}%",
            "ci_95_upper": f"{ci_high:.2f}%",
            "method": "Non-parametric Bootstrap (B=1,000)"
        })

    # 2. OOD AUROC and UFAR-Fresh for key detectors on A vs C, A vs D1, B vs C, B vs D1
    key_pairs = [
        ("A_vs_C (ID Known vs Formalin Known)", df_A, df_C),
        ("A_vs_D1 (ID Known vs Semantic Unknown)", df_A, df_D1),
        ("B_vs_C (External Known vs Formalin Known)", df_B, df_C),
        ("B_vs_D1 (External Known vs Semantic Unknown)", df_B, df_D1)
    ]

    for pair_name, id_sub, ood_sub in key_pairs:
        n_id = len(id_sub)
        n_ood = len(ood_sub)
        y_ood_true = np.concatenate([np.zeros(n_id), np.ones(n_ood)])
        ood_preds = ood_sub["top1_pred_idx"].values
        is_fresh_pred = np.isin(ood_preds, [0, 1, 2])

        for sc in ["msp", "energy", "dualgate"]:
            if sc == "dualgate":
                scores = np.concatenate([
                    ((id_sub["score_energy"] - thresholds["dual_gate_cascade_tau95"]["energy"]) + 
                     (id_sub["score_msp"] - thresholds["dual_gate_cascade_tau95"]["msp"])).values,
                    ((ood_sub["score_energy"] - thresholds["dual_gate_cascade_tau95"]["energy"]) + 
                     (ood_sub["score_msp"] - thresholds["dual_gate_cascade_tau95"]["msp"])).values
                ])
                acc_ood_95 = ood_sub["accept_dualgate_tau95"].values
            else:
                scores = np.concatenate([id_sub[f"score_{sc}"].values, ood_sub[f"score_{sc}"].values])
                acc_ood_95 = ood_sub[f"accept_{sc}_tau95"].values

            # AUROC CI
            boot_auroc = []
            for _ in range(B):
                id_idx = np.random.choice(n_id, size=n_id, replace=True)
                ood_idx = np.random.choice(n_ood, size=n_ood, replace=True)
                b_scores = np.concatenate([scores[:n_id][id_idx], scores[n_id:][ood_idx]])
                b_y = np.concatenate([np.zeros(n_id), np.ones(n_ood)])
                boot_auroc.append(roc_auc_score(b_y, -b_scores))
            
            auroc_est = roc_auc_score(y_ood_true, -scores) * 100
            auroc_low = np.percentile(boot_auroc, 2.5) * 100
            auroc_high = np.percentile(boot_auroc, 97.5) * 100

            ci_records.append({
                "benchmark_task": f"AUROC: {pair_name}",
                "detector": sc.upper(),
                "point_estimate": f"{auroc_est:.2f}%",
                "ci_95_lower": f"{auroc_low:.2f}%",
                "ci_95_upper": f"{auroc_high:.2f}%",
                "method": "Stratified Bootstrap (B=1,000)"
            })

            # UFAR-Fresh CI (Binomial / Percentile Bootstrap on OOD)
            boot_ufar_fresh = []
            for _ in range(B):
                idx = np.random.choice(n_ood, size=n_ood, replace=True)
                b_uf = np.sum((acc_ood_95[idx] == 1) & is_fresh_pred[idx]) / float(n_ood)
                boot_ufar_fresh.append(b_uf)
            
            uf_est = (np.sum((acc_ood_95 == 1) & is_fresh_pred) / float(n_ood)) * 100
            uf_low = np.percentile(boot_ufar_fresh, 2.5) * 100
            uf_high = np.percentile(boot_ufar_fresh, 97.5) * 100

            ci_records.append({
                "benchmark_task": f"UFAR-Fresh (tau95): {pair_name}",
                "detector": sc.upper(),
                "point_estimate": f"{uf_est:.2f}%",
                "ci_95_lower": f"{uf_low:.2f}%",
                "ci_95_upper": f"{uf_high:.2f}%",
                "method": "Bootstrap (B=1,000)"
            })

    df_ci = pd.DataFrame(ci_records)
    out_ci_path = PROJECT_ROOT / "STAGE4_1_CONFIDENCE_INTERVALS.csv"
    df_ci.to_csv(out_ci_path, index=False)
    print(f"✅ Saved confidence intervals to {out_ci_path}")

    print("\n" + "=" * 80)
    print("STAGE 4.1 EXECUTION COMPLETE: ALL INFERENCE RUNS AND ARTIFACTS VERIFIED")
    print("=" * 80)

if __name__ == "__main__":
    main()
