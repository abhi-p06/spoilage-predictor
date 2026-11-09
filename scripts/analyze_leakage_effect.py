#!/usr/bin/env python3
"""
scripts/analyze_leakage_effect.py
=================================
Quantifies the exact impact of base-image-family leakage within the historical
random-split test set (Model A evaluation).

1. Maps all test_internal.csv images to their filename-derived base-image family.
2. Deduplicates nested MD5 duplicates (from 4,090 to 2,045 unique physical files).
3. Identifies which base families were present in train.csv (Seen) vs absent from train.csv (Unseen).
4. Compares predictions, class distributions, accuracy, balanced accuracy, precision, recall, macro F1.
5. Computes cluster-bootstrap confidence intervals (clustering by base-image family).
6. Computes group-weighted performance (macro-averaging across groups).
7. Outputs full statistical summary to LEAKAGE_EFFECT_ANALYSIS_DATA.json and CSV.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, precision_recall_fscore_support, confusion_matrix

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PREFIX_REGEX = re.compile(r"^(rotated_by_\d+_|translation_|saltandpepper_|vertical_flip_)")

def parse_base_filename(filename: str):
    m = PREFIX_REGEX.match(filename)
    if m:
        prefix = m.group(1)
        base = filename[len(prefix):]
    else:
        base = filename
    return base

def main():
    print("Loading manifests and predictions...")
    train_df = pd.read_csv(PROJECT_ROOT / "experiments" / "split_manifests" / "train.csv")
    test_df = pd.read_csv(PROJECT_ROOT / "experiments" / "split_manifests" / "test_internal.csv")
    preds = np.load(PROJECT_ROOT / "experiments" / "group_leakage_study" / "PREDICTIONS.npz")

    prob_a_test = preds["prob_a_rand_test"] # (4090, 6)
    pred_a_test = preds["pred_a_rand_test"] # (4090,)
    true_a_test = preds["true_a_rand_test"] # (4090,)

    assert (test_df["label_idx"].values == true_a_test).all()

    # Parse base filenames for train
    train_df["base_filename"] = train_df["filename"].apply(parse_base_filename)
    train_base_set = set(zip(train_df["class_name"], train_df["base_filename"]))
    print(f"Train base-image families: {len(train_base_set)}")

    # Add columns to test_df
    test_df["base_filename"] = test_df["filename"].apply(parse_base_filename)
    test_df["base_family_key"] = list(zip(test_df["class_name"], test_df["base_filename"]))
    test_df["y_pred"] = pred_a_test
    test_df["confidence"] = np.max(prob_a_test, axis=1)
    for c in range(6):
        test_df[f"prob_{c}"] = prob_a_test[:, c]

    # Deduplicate nested MD5 duplicates (historical random split contained 2 identical nested trees)
    print(f"Total test rows: {len(test_df)}")
    test_dedup = test_df.drop_duplicates(subset=["md5"]).copy().reset_index(drop=True)
    print(f"Deduplicated test rows: {len(test_dedup)}")
    assert len(test_dedup) == 2045

    # Tag seen vs unseen
    test_dedup["seen_in_train"] = test_dedup["base_family_key"].apply(lambda k: k in train_base_set)

    seen_df = test_dedup[test_dedup["seen_in_train"]].copy()
    unseen_df = test_dedup[~test_dedup["seen_in_train"]].copy()

    n_total = len(test_dedup)
    n_seen = len(seen_df)
    n_unseen = len(unseen_df)

    seen_families = set(seen_df["base_family_key"])
    unseen_families = set(unseen_df["base_family_key"])
    total_families = set(test_dedup["base_family_key"])

    print(f"\n--- Base-Image Family Breakdown ---")
    print(f"Total unique base families in test: {len(total_families)}")
    print(f"Seen base families (in train): {len(seen_families)} ({len(seen_families)/len(total_families)*100:.2f}%)")
    print(f"Unseen base families (NOT in train): {len(unseen_families)} ({len(unseen_families)/len(total_families)*100:.2f}%)")
    print(f"Test images in seen families: {n_seen} ({n_seen/n_total*100:.2f}%)")
    print(f"Test images in unseen families: {n_unseen} ({n_unseen/n_total*100:.2f}%)")

    # Metrics computation helper
    classes = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]
    def compute_all_metrics(sub_df):
        y_t = sub_df["label_idx"].values
        y_p = sub_df["y_pred"].values
        acc = accuracy_score(y_t, y_p)
        bal_acc = balanced_accuracy_score(y_t, y_p)
        prec, rec, f1, supp = precision_recall_fscore_support(y_t, y_p, labels=range(6), zero_division=0)
        macro_prec = np.mean(prec)
        macro_rec = np.mean(rec)
        macro_f1 = np.mean(f1)
        cm = confusion_matrix(y_t, y_p, labels=range(6))
        return {
            "n_samples": int(len(sub_df)),
            "accuracy": float(acc),
            "balanced_accuracy": float(bal_acc),
            "macro_precision": float(macro_prec),
            "macro_recall": float(macro_rec),
            "macro_f1": float(macro_f1),
            "class_precision": {classes[i]: float(prec[i]) for i in range(6)},
            "class_recall": {classes[i]: float(rec[i]) for i in range(6)},
            "class_f1": {classes[i]: float(f1[i]) for i in range(6)},
            "class_support": {classes[i]: int(supp[i]) for i in range(6)},
            "confusion_matrix": cm.tolist()
        }

    m_all = compute_all_metrics(test_dedup)
    m_seen = compute_all_metrics(seen_df)
    m_unseen = compute_all_metrics(unseen_df)

    delta_acc = m_seen["accuracy"] - m_unseen["accuracy"]
    delta_bal_acc = m_seen["balanced_accuracy"] - m_unseen["balanced_accuracy"]
    delta_f1 = m_seen["macro_f1"] - m_unseen["macro_f1"]

    print(f"\n--- Comparative Performance ---")
    print(f"Overall Test (N={n_total}): Accuracy = {m_all['accuracy']*100:.2f}%, Macro F1 = {m_all['macro_f1']*100:.2f}%")
    print(f"Seen in Train (N={n_seen}):  Accuracy = {m_seen['accuracy']*100:.2f}%, Macro F1 = {m_seen['macro_f1']*100:.2f}%")
    print(f"Unseen in Train (N={n_unseen}): Accuracy = {m_unseen['accuracy']*100:.2f}%, Macro F1 = {m_unseen['macro_f1']*100:.2f}%")
    print(f"Within-Test Leakage Delta (Seen - Unseen):")
    print(f"  Δ Accuracy:         {delta_acc*100:+.2f} percentage points")
    print(f"  Δ Balanced Acc:     {delta_bal_acc*100:+.2f} percentage points")
    print(f"  Δ Macro F1:         {delta_f1*100:+.2f} percentage points")

    # Cluster Bootstrap for Seen, Unseen, and Delta (clustering by base_family_key)
    print("\nComputing Cluster-Bootstrap 95% Confidence Intervals (1,000 resamples by base-image family)...")
    np.random.seed(42)
    B = 1000

    def cluster_bootstrap(df_subset, n_boot=1000):
        # group dataframe by base_family_key
        groups = [group for _, group in df_subset.groupby("base_family_key")]
        G = len(groups)
        accs, f1s = [], []
        for _ in range(n_boot):
            sampled_indices = np.random.choice(G, size=G, replace=True)
            boot_df = pd.concat([groups[idx] for idx in sampled_indices], ignore_index=True)
            y_t = boot_df["label_idx"].values
            y_p = boot_df["y_pred"].values
            accs.append(accuracy_score(y_t, y_p))
            _, _, f1, _ = precision_recall_fscore_support(y_t, y_p, labels=range(6), zero_division=0)
            f1s.append(np.mean(f1))
        return {
            "acc_mean": float(np.mean(accs)),
            "acc_ci_low": float(np.percentile(accs, 2.5)),
            "acc_ci_high": float(np.percentile(accs, 97.5)),
            "f1_mean": float(np.mean(f1s)),
            "f1_ci_low": float(np.percentile(f1s, 2.5)),
            "f1_ci_high": float(np.percentile(f1s, 97.5)),
        }

    ci_seen = cluster_bootstrap(seen_df, B)
    ci_unseen = cluster_bootstrap(unseen_df, B)

    # Bootstrap delta
    # Sample seen and unseen independently
    groups_seen = [group for _, group in seen_df.groupby("base_family_key")]
    groups_unseen = [group for _, group in unseen_df.groupby("base_family_key")]
    G_seen = len(groups_seen)
    G_unseen = len(groups_unseen)
    delta_accs, delta_f1s = [], []
    for _ in range(B):
        idx_s = np.random.choice(G_seen, size=G_seen, replace=True)
        boot_s = pd.concat([groups_seen[i] for i in idx_s], ignore_index=True)
        idx_u = np.random.choice(G_unseen, size=G_unseen, replace=True)
        boot_u = pd.concat([groups_unseen[i] for i in idx_u], ignore_index=True)

        acc_s = accuracy_score(boot_s["label_idx"].values, boot_s["y_pred"].values)
        acc_u = accuracy_score(boot_u["label_idx"].values, boot_u["y_pred"].values)
        delta_accs.append(acc_s - acc_u)

        _, _, f1_s, _ = precision_recall_fscore_support(boot_s["label_idx"].values, boot_s["y_pred"].values, labels=range(6), zero_division=0)
        _, _, f1_u, _ = precision_recall_fscore_support(boot_u["label_idx"].values, boot_u["y_pred"].values, labels=range(6), zero_division=0)
        delta_f1s.append(np.mean(f1_s) - np.mean(f1_u))

    ci_delta = {
        "delta_acc_mean": float(np.mean(delta_accs)),
        "delta_acc_ci_low": float(np.percentile(delta_accs, 2.5)),
        "delta_acc_ci_high": float(np.percentile(delta_accs, 97.5)),
        "delta_f1_mean": float(np.mean(delta_f1s)),
        "delta_f1_ci_low": float(np.percentile(delta_f1s, 2.5)),
        "delta_f1_ci_high": float(np.percentile(delta_f1s, 97.5)),
    }

    print(f"Seen Accuracy 95% CI:   [{ci_seen['acc_ci_low']*100:.2f}%, {ci_seen['acc_ci_high']*100:.2f}%]")
    print(f"Unseen Accuracy 95% CI: [{ci_unseen['acc_ci_low']*100:.2f}%, {ci_unseen['acc_ci_high']*100:.2f}%]")
    print(f"Delta Accuracy 95% CI:  [{ci_delta['delta_acc_ci_low']*100:+.2f}%, {ci_delta['delta_acc_ci_high']*100:+.2f}%]")
    print(f"Delta Macro F1 95% CI:  [{ci_delta['delta_f1_ci_low']*100:+.2f}%, {ci_delta['delta_f1_ci_high']*100:+.2f}%]")

    # Group-weighted performance (accuracy aggregated per group, then averaged)
    def compute_group_weighted_acc(df_subset):
        grp_accs = []
        for _, g_df in df_subset.groupby("base_family_key"):
            grp_accs.append(accuracy_score(g_df["label_idx"].values, g_df["y_pred"].values))
        return float(np.mean(grp_accs))

    grp_acc_all = compute_group_weighted_acc(test_dedup)
    grp_acc_seen = compute_group_weighted_acc(seen_df)
    grp_acc_unseen = compute_group_weighted_acc(unseen_df)

    out_data = {
        "analysis_type": "Historical Random-Split Within-Test Leakage Analysis",
        "model": "Model A (Historical MobileNetV2 Random Split)",
        "test_counts": {
            "total_rows_raw": len(test_df),
            "deduplicated_rows": n_total,
            "unique_base_families": len(total_families),
            "seen_base_families": len(seen_families),
            "unseen_base_families": len(unseen_families),
            "seen_images": n_seen,
            "unseen_images": n_unseen,
            "seen_image_ratio": float(n_seen / n_total),
            "unseen_image_ratio": float(n_unseen / n_total)
        },
        "metrics_all": m_all,
        "metrics_seen": m_seen,
        "metrics_unseen": m_unseen,
        "group_weighted_accuracy": {
            "all": grp_acc_all,
            "seen": grp_acc_seen,
            "unseen": grp_acc_unseen
        },
        "deltas": {
            "delta_accuracy": float(delta_acc),
            "delta_balanced_accuracy": float(delta_bal_acc),
            "delta_macro_f1": float(delta_f1)
        },
        "cluster_bootstrap_95ci": {
            "seen": ci_seen,
            "unseen": ci_unseen,
            "delta": ci_delta
        }
    }

    out_json = PROJECT_ROOT / "experiments" / "group_leakage_study" / "LEAKAGE_EFFECT_ANALYSIS_DATA.json"
    with open(out_json, "w") as f:
        json.dump(out_data, f, indent=2)
    print(f"\n✅ Saved analysis data to {out_json}")

if __name__ == "__main__":
    main()

