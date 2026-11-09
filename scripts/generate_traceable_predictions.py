#!/usr/bin/env python3
"""
scripts/generate_traceable_predictions.py
=========================================
Generates fully traceable prediction tables aligning every prediction to its
exact manifest entry, MD5 hash, relative filepath, and base group ID.

Creates:
1. PREDICTIONS_RANDOM.csv (4,090 rows)
2. PREDICTIONS_GROUP_TEST.csv (2,043 rows)
3. PREDICTIONS_GROUP_TEST_RAW_ONLY.csv (227 rows)
4. PREDICTIONS_FRUITVISION.csv (4,157 rows)
5. PREDICTIONS_SULTANA.csv (1,193 rows)

Also saves an updated PREDICTIONS_TRACEABLE.npz with explicit string identifiers.
"""

import os
import re
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXP_DIR = PROJECT_ROOT / "experiments" / "group_leakage_study"

CLASSES = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]
TAU_THRESHOLD = 0.90

PREFIX_REGEX = re.compile(r"^(rotated_by_\d+_|translation_|saltandpepper_|vertical_flip_)")

def parse_base_filename(filename: str):
    m = PREFIX_REGEX.match(filename)
    return filename[len(m.group(1)):] if m else filename

def main():
    print("Loading manifests and raw predictions...")
    preds_npz = np.load(EXP_DIR / "PREDICTIONS.npz")

    # Load group audit for group_id mapping
    df_audit = pd.read_csv(PROJECT_ROOT / "BASE_IMAGE_GROUP_AUDIT.csv")
    group_map = {(r["class_name"], r["base_filename"]): r["group_id"] for _, r in df_audit.iterrows()}

    # 1. PREDICTIONS_RANDOM.csv (Model A on historical random test)
    print("Generating PREDICTIONS_RANDOM.csv...")
    df_rand_manifest = pd.read_csv(PROJECT_ROOT / "experiments" / "split_manifests" / "test_internal.csv")
    assert len(df_rand_manifest) == 4090
    assert (df_rand_manifest["label_idx"].values == preds_npz["true_a_rand_test"]).all()

    prob_rand = preds_npz["prob_a_rand_test"]
    pred_rand = preds_npz["pred_a_rand_test"]
    conf_rand = np.max(prob_rand, axis=1)

    rand_rows = []
    for idx, row in df_rand_manifest.iterrows():
        base_fn = parse_base_filename(row["filename"])
        gid = group_map.get((row["class_name"], base_fn), "UNKNOWN")
        rel_path = str(Path(row["filepath"]).relative_to(PROJECT_ROOT)) if Path(row["filepath"]).is_absolute() else str(row["filepath"])
        max_p = conf_rand[idx]
        is_accepted = bool(max_p >= TAU_THRESHOLD)

        row_dict = {
            "sample_id": f"RAND_TEST_{idx:04d}",
            "dataset_name": "Kaggle_FreshRotten",
            "split_name": "historical_random_test",
            "model_name": "Model_A_Historical_Random",
            "relative_path": rel_path,
            "filename": row["filename"],
            "base_filename": base_fn,
            "base_group_id": gid,
            "md5": row["md5"],
            "ground_truth_label": row["class_name"],
            "ground_truth_idx": int(row["label_idx"]),
            "predicted_label": CLASSES[pred_rand[idx]],
            "predicted_idx": int(pred_rand[idx]),
            "max_confidence": float(max_p),
            "tau_threshold": TAU_THRESHOLD,
            "decision": "ACCEPTED" if is_accepted else "ABSTAINED",
        }
        for c_idx, c_name in enumerate(CLASSES):
            row_dict[f"prob_{c_name}"] = float(prob_rand[idx, c_idx])
        rand_rows.append(row_dict)

    df_preds_rand = pd.DataFrame(rand_rows)
    df_preds_rand.to_csv(PROJECT_ROOT / "PREDICTIONS_RANDOM.csv", index=False)
    print(f"✅ Saved PREDICTIONS_RANDOM.csv ({len(df_preds_rand)} rows)")

    # 2. PREDICTIONS_GROUP_TEST.csv (Model B on group-aware test)
    print("Generating PREDICTIONS_GROUP_TEST.csv...")
    df_grp_manifest = pd.read_csv(EXP_DIR / "group_test.csv")
    assert len(df_grp_manifest) == 2043
    assert (df_grp_manifest["label_idx"].values == preds_npz["true_b_grp_test"]).all()

    prob_grp = preds_npz["prob_b_grp_test"]
    pred_grp = preds_npz["pred_b_grp_test"]
    conf_grp = np.max(prob_grp, axis=1)

    grp_rows = []
    for idx, row in df_grp_manifest.iterrows():
        max_p = conf_grp[idx]
        is_accepted = bool(max_p >= TAU_THRESHOLD)
        rel_path = str(row["relative_path"])

        row_dict = {
            "sample_id": f"GRP_TEST_{idx:04d}",
            "dataset_name": "Kaggle_FreshRotten",
            "split_name": "group_aware_test",
            "model_name": "Model_B_Group_Aware",
            "relative_path": rel_path,
            "filename": row["filename"],
            "base_filename": row["base_filename"],
            "base_group_id": row["group_id"],
            "variant_type": row["variant_type"],
            "is_raw": int(row["is_raw"]),
            "md5": row["md5"],
            "ground_truth_label": row["class_name"],
            "ground_truth_idx": int(row["label_idx"]),
            "predicted_label": CLASSES[pred_grp[idx]],
            "predicted_idx": int(pred_grp[idx]),
            "max_confidence": float(max_p),
            "tau_threshold": TAU_THRESHOLD,
            "decision": "ACCEPTED" if is_accepted else "ABSTAINED",
        }
        for c_idx, c_name in enumerate(CLASSES):
            row_dict[f"prob_{c_name}"] = float(prob_grp[idx, c_idx])
        grp_rows.append(row_dict)

    df_preds_grp = pd.DataFrame(grp_rows)
    df_preds_grp.to_csv(PROJECT_ROOT / "PREDICTIONS_GROUP_TEST.csv", index=False)
    print(f"✅ Saved PREDICTIONS_GROUP_TEST.csv ({len(df_preds_grp)} rows)")

    # 3. PREDICTIONS_GROUP_TEST_RAW_ONLY.csv (227 raw screenshot rows)
    print("Generating PREDICTIONS_GROUP_TEST_RAW_ONLY.csv...")
    df_preds_grp_raw = df_preds_grp[df_preds_grp["is_raw"] == 1].copy().reset_index(drop=True)
    assert len(df_preds_grp_raw) == 227
    df_preds_grp_raw.to_csv(PROJECT_ROOT / "PREDICTIONS_GROUP_TEST_RAW_ONLY.csv", index=False)
    print(f"✅ Saved PREDICTIONS_GROUP_TEST_RAW_ONLY.csv ({len(df_preds_grp_raw)} rows)")

    # 4. PREDICTIONS_FRUITVISION.csv (Model B on FruitVision clean external test)
    print("Generating PREDICTIONS_FRUITVISION.csv...")
    df_fv_manifest = pd.read_csv(EXP_DIR / "fruitvision_clean.csv")
    assert len(df_fv_manifest) == 4157
    assert (df_fv_manifest["label_idx"].values == preds_npz["true_b_fv"]).all()

    prob_fv = preds_npz["prob_b_fv"]
    pred_fv = preds_npz["pred_b_fv"]
    conf_fv = np.max(prob_fv, axis=1)

    fv_rows = []
    for idx, row in df_fv_manifest.iterrows():
        rel_path = str(Path(row["filepath"]).relative_to(PROJECT_ROOT)) if Path(row["filepath"]).is_absolute() else str(row["filepath"])
        max_p = conf_fv[idx]
        is_accepted = bool(max_p >= TAU_THRESHOLD)

        row_dict = {
            "sample_id": f"FV_{idx:04d}",
            "dataset_name": "FruitVision",
            "split_name": "external_test",
            "model_name": "Model_B_Group_Aware",
            "relative_path": rel_path,
            "filename": row["filename"],
            "base_filename": "N/A_EXTERNAL",
            "base_group_id": "N/A_EXTERNAL",
            "md5": row["md5"],
            "ground_truth_label": row["class_name"],
            "ground_truth_idx": int(row["label_idx"]),
            "predicted_label": CLASSES[pred_fv[idx]],
            "predicted_idx": int(pred_fv[idx]),
            "max_confidence": float(max_p),
            "tau_threshold": TAU_THRESHOLD,
            "decision": "ACCEPTED" if is_accepted else "ABSTAINED",
        }
        for c_idx, c_name in enumerate(CLASSES):
            row_dict[f"prob_{c_name}"] = float(prob_fv[idx, c_idx])
        fv_rows.append(row_dict)

    df_preds_fv = pd.DataFrame(fv_rows)
    df_preds_fv.to_csv(PROJECT_ROOT / "PREDICTIONS_FRUITVISION.csv", index=False)
    print(f"✅ Saved PREDICTIONS_FRUITVISION.csv ({len(df_preds_fv)} rows)")

    # Verify selective prediction metrics for FruitVision at tau=0.90
    accepted_fv = df_preds_fv[df_preds_fv["decision"] == "ACCEPTED"]
    abstained_fv = df_preds_fv[df_preds_fv["decision"] == "ABSTAINED"]
    cov_fv = len(accepted_fv) / len(df_preds_fv)
    acc_accepted_fv = (accepted_fv["ground_truth_idx"] == accepted_fv["predicted_idx"]).mean() if len(accepted_fv) > 0 else 0.0
    err_accepted_fv = 1.0 - acc_accepted_fv
    print(f"  FruitVision Selective Prediction (tau=0.90):")
    print(f"    Total: {len(df_preds_fv)}")
    print(f"    Accepted: {len(accepted_fv)} ({cov_fv*100:.2f}%)")
    print(f"    Abstained: {len(abstained_fv)} ({(1-cov_fv)*100:.2f}%)")
    print(f"    Accepted Accuracy: {acc_accepted_fv*100:.2f}% (Error: {err_accepted_fv*100:.2f}%)")

    # 5. PREDICTIONS_SULTANA.csv (Model B on Sultana clean external test)
    print("Generating PREDICTIONS_SULTANA.csv...")
    df_sul_manifest = pd.read_csv(EXP_DIR / "sultana_clean.csv")
    assert len(df_sul_manifest) == 1193
    assert (df_sul_manifest["label_idx"].values == preds_npz["true_b_sul"]).all()

    prob_sul = preds_npz["prob_b_sul"]
    pred_sul = preds_npz["pred_b_sul"]
    conf_sul = np.max(prob_sul, axis=1)

    sul_rows = []
    for idx, row in df_sul_manifest.iterrows():
        rel_path = str(Path(row["filepath"]).relative_to(PROJECT_ROOT)) if Path(row["filepath"]).is_absolute() else str(row["filepath"])
        max_p = conf_sul[idx]
        is_accepted = bool(max_p >= TAU_THRESHOLD)

        row_dict = {
            "sample_id": f"SULTANA_{idx:04d}",
            "dataset_name": "Sultana",
            "split_name": "external_test",
            "model_name": "Model_B_Group_Aware",
            "relative_path": rel_path,
            "filename": row["filename"],
            "base_filename": "N/A_EXTERNAL",
            "base_group_id": "N/A_EXTERNAL",
            "md5": row["md5"],
            "ground_truth_label": row["class_name"],
            "ground_truth_idx": int(row["label_idx"]),
            "predicted_label": CLASSES[pred_sul[idx]],
            "predicted_idx": int(pred_sul[idx]),
            "max_confidence": float(max_p),
            "tau_threshold": TAU_THRESHOLD,
            "decision": "ACCEPTED" if is_accepted else "ABSTAINED",
        }
        for c_idx, c_name in enumerate(CLASSES):
            row_dict[f"prob_{c_name}"] = float(prob_sul[idx, c_idx])
        sul_rows.append(row_dict)

    df_preds_sul = pd.DataFrame(sul_rows)
    df_preds_sul.to_csv(PROJECT_ROOT / "PREDICTIONS_SULTANA.csv", index=False)
    print(f"✅ Saved PREDICTIONS_SULTANA.csv ({len(df_preds_sul)} rows)")

    # Save traceable NPZ with explicit sample identifiers
    npz_out = EXP_DIR / "PREDICTIONS_TRACEABLE.npz"
    np.savez_compressed(
        npz_out,
        # Probabilities and predictions
        prob_a_rand_test=preds_npz["prob_a_rand_test"],
        pred_a_rand_test=preds_npz["pred_a_rand_test"],
        true_a_rand_test=preds_npz["true_a_rand_test"],
        ids_a_rand_test=np.array(df_preds_rand["sample_id"].tolist()),
        md5_a_rand_test=np.array(df_preds_rand["md5"].tolist()),
        paths_a_rand_test=np.array(df_preds_rand["relative_path"].tolist()),

        prob_b_grp_test=preds_npz["prob_b_grp_test"],
        pred_b_grp_test=preds_npz["pred_b_grp_test"],
        true_b_grp_test=preds_npz["true_b_grp_test"],
        ids_b_grp_test=np.array(df_preds_grp["sample_id"].tolist()),
        md5_b_grp_test=np.array(df_preds_grp["md5"].tolist()),
        paths_b_grp_test=np.array(df_preds_grp["relative_path"].tolist()),

        prob_b_fv=preds_npz["prob_b_fv"],
        pred_b_fv=preds_npz["pred_b_fv"],
        true_b_fv=preds_npz["true_b_fv"],
        ids_b_fv=np.array(df_preds_fv["sample_id"].tolist()),
        md5_b_fv=np.array(df_preds_fv["md5"].tolist()),
        paths_b_fv=np.array(df_preds_fv["relative_path"].tolist()),

        prob_b_sul=preds_npz["prob_b_sul"],
        pred_b_sul=preds_npz["pred_b_sul"],
        true_b_sul=preds_npz["true_b_sul"],
        ids_b_sul=np.array(df_preds_sul["sample_id"].tolist()),
        md5_b_sul=np.array(df_preds_sul["md5"].tolist()),
        paths_b_sul=np.array(df_preds_sul["relative_path"].tolist())
    )
    print(f"✅ Saved PREDICTIONS_TRACEABLE.npz to {npz_out}")

if __name__ == "__main__":
    main()

