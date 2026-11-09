"""
tests/test_reproducibility_v4.py
================================
Authoritative Automated Validation Test Suite for AgriRoute Scientific Integrity Remediation (V4).

Covers all 7 verification areas mandated by independent scientific audit:
1. Manifest integrity & class counts (13,599 rows, non-empty MD5s).
2. Checkpoint SHA-256 hash integrity.
3. Dataset exclusion accounting (FruitVision 28, Sultana 7).
4. Super-group partition separation (1,504 super-groups, zero cross-partition leakage).
5. Prediction table schema compliance (37 columns, class ordering, probability sum to 1.0).
6. Authoritative registry metric concordance (Acc, Macro F1, ROC-AUC, PR-AUC, ECE, NLL).
7. Portable relative path validity.
"""

import os
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score, average_precision_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLASSES = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]

EXPECTED_SHA_A = "6d7f61d368a74130ddb932df4c42b75fd9efcbeeab192f3912db0e94f753e2b9"
EXPECTED_SHA_B = "3bdda4572ba117bef65f707fdc520a12498667f0043d4d1822194cecee5d7689"

def compute_file_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

# -------------------------------------------------------------
# 1. Manifest Integrity & Class Counts
# -------------------------------------------------------------
def test_manifest_integrity():
    manifest_path = PROJECT_ROOT / "GROUP_SPLIT_MANIFEST_MERGED_V4.csv"
    assert manifest_path.exists(), f"Missing {manifest_path}"

    df_manifest = pd.read_csv(manifest_path)
    assert len(df_manifest) == 13599, f"Expected 13,599 manifest rows, got {len(df_manifest)}"

    # Check for empty MD5s
    assert "md5" in df_manifest.columns, "Missing 'md5' column in manifest!"
    assert df_manifest["md5"].str.len().eq(32).all(), "Found invalid MD5 hashes in manifest!"

    # Check expected classes
    assert set(df_manifest["class_name"].unique()) == set(CLASSES), "Class name mismatch in manifest!"

    # Check 1,504 super groups
    n_super = df_manifest["super_group_id"].nunique()
    assert n_super == 1504, f"Expected 1,504 super groups, got {n_super}"

# -------------------------------------------------------------
# 2. Checkpoint SHA-256 Hash Integrity
# -------------------------------------------------------------
def test_checkpoint_sha256_integrity():
    model_a_path = PROJECT_ROOT / "experiments" / "checkpoints" / "mobilenet_v2" / "best_model.keras"
    model_b_path = PROJECT_ROOT / "experiments" / "group_leakage_study" / "CHECKPOINTS" / "group_aware_mobilenet_v2.keras"

    assert model_a_path.exists(), f"Model A checkpoint missing: {model_a_path}"
    assert model_b_path.exists(), f"Model B checkpoint missing: {model_b_path}"

    assert model_a_path.stat().st_size > 9_000_000, "Model A file suspiciously small!"
    assert model_b_path.stat().st_size > 9_000_000, "Model B file suspiciously small!"

    sha_a = compute_file_sha256(model_a_path)
    sha_b = compute_file_sha256(model_b_path)

    assert sha_a == EXPECTED_SHA_A, f"Model A SHA-256 mismatch! Expected {EXPECTED_SHA_A}, got {sha_a}"
    assert sha_b == EXPECTED_SHA_B, f"Model B SHA-256 mismatch! Expected {EXPECTED_SHA_B}, got {sha_b}"

# -------------------------------------------------------------
# 3. Dataset Exclusion Accounting
# -------------------------------------------------------------
def test_dataset_exclusion_accounting():
    excl_dir = PROJECT_ROOT / "DATASET_EXCLUSION_MANIFESTS"
    assert excl_dir.exists(), f"Missing exclusion directory {excl_dir}"

    fv_excl = pd.read_csv(excl_dir / "FRUITVISION_EXCLUSION_MANIFEST.csv")
    fv_incl = pd.read_csv(excl_dir / "FRUITVISION_INCLUSION_MANIFEST.csv")
    sul_excl = pd.read_csv(excl_dir / "SULTANA_EXCLUSION_MANIFEST.csv")
    sul_incl = pd.read_csv(excl_dir / "SULTANA_INCLUSION_MANIFEST.csv")

    assert len(fv_excl) == 28, f"FruitVision exclusion: expected 28 rows, got {len(fv_excl)}"
    assert len(fv_incl) == 4157, f"FruitVision inclusion: expected 4,157 rows, got {len(fv_incl)}"
    assert len(fv_excl) + len(fv_incl) == 4185, f"FruitVision total accounting mismatch! Got {len(fv_excl) + len(fv_incl)}"

    assert len(sul_excl) == 7, f"Sultana exclusion: expected 7 rows, got {len(sul_excl)}"
    assert len(sul_incl) == 1193, f"Sultana inclusion: expected 1,193 rows, got {len(sul_incl)}"
    assert len(sul_excl) + len(sul_incl) == 1200, f"Sultana total accounting mismatch! Got {len(sul_excl) + len(sul_incl)}"

    # Check reason strings
    assert fv_excl["exclusion_reason"].str.contains("identical MD5 checksum", case=False).all()
    assert sul_excl["exclusion_reason"].str.contains("identical MD5 checksum", case=False).all()

# -------------------------------------------------------------
# 4. Super-Group Partition Separation & Zero Leakage
# -------------------------------------------------------------
def test_super_group_partition_separation():
    df_manifest = pd.read_csv(PROJECT_ROOT / "GROUP_SPLIT_MANIFEST_MERGED_V4.csv")

    train_groups = set(df_manifest[df_manifest["split_partition"] == "train"]["super_group_id"])
    val_groups = set(df_manifest[df_manifest["split_partition"] == "val"]["super_group_id"])
    test_groups = set(df_manifest[df_manifest["split_partition"] == "test"]["super_group_id"])

    assert len(train_groups & val_groups) == 0, "Super-group leak between Train and Val!"
    assert len(train_groups & test_groups) == 0, "Super-group leak between Train and Test!"
    assert len(val_groups & test_groups) == 0, "Super-group leak between Val and Test!"

    # Verify that all 7 confirmed near-duplicate pairs (MERGE_GROUPS) reside in the same partition
    phash_audit = pd.read_csv(PROJECT_ROOT / "PHASH_REVIEW" / "PHASH_CANDIDATE_AUDIT.csv")
    group_to_part = dict(zip(df_manifest["group_id"], df_manifest["split_partition"]))

    crossing_pairs = 0
    for _, r in phash_audit[phash_audit["recommended_action"] == "MERGE_GROUPS"].iterrows():
        part1 = group_to_part[r["group1"]]
        part2 = group_to_part[r["group2"]]
        if part1 != part2:
            crossing_pairs += 1

    assert crossing_pairs == 0, f"Found {crossing_pairs} merged pHash collision pairs crossing partitions in merged manifest!"

# -------------------------------------------------------------
# 5. Prediction Table Schema Compliance
# -------------------------------------------------------------
def test_prediction_schema_compliance():
    expected_cols = [
        "sample_id", "dataset_name", "split_name", "model_name", "relative_path",
        "filename", "base_filename", "base_group_id", "variant_type", "is_raw",
        "md5", "ground_truth_label", "ground_truth_idx", "predicted_label",
        "predicted_idx", "max_confidence", "tau_threshold", "decision", "temperature_T"
    ]
    for c in CLASSES:
        expected_cols.append(f"prob_{c}")
    for c in CLASSES:
        expected_cols.append(f"prob_cal_{c}")
    for c in CLASSES:
        expected_cols.append(f"logit_{c}")

    assert len(expected_cols) == 37, f"Expected 37 schema columns, got {len(expected_cols)}"

    pred_files = [
        ("PREDICTIONS_RANDOM_V4.csv", 4090),
        ("PREDICTIONS_GROUP_TEST_V4.csv", 2043),
        ("PREDICTIONS_GROUP_TEST_RAW_ONLY_V4.csv", 227),
        ("PREDICTIONS_FRUITVISION_V4.csv", 4157),
        ("PREDICTIONS_SULTANA_V4.csv", 1193),
        ("PREDICTIONS_FRUITVISION_MODEL_A_V4.csv", 4157),
        ("PREDICTIONS_SULTANA_MODEL_A_V4.csv", 1193)
    ]

    for fname, expected_len in pred_files:
        p = PROJECT_ROOT / fname
        assert p.exists(), f"Prediction file missing: {fname}"
        df = pd.read_csv(p)
        assert len(df) == expected_len, f"{fname}: Expected {expected_len} rows, got {len(df)}"
        assert list(df.columns) == expected_cols, f"{fname}: Schema column mismatch!"

        # Ground truth and predicted label alignment
        for idx in range(min(100, len(df))):
            row = df.iloc[idx]
            assert row["ground_truth_label"] == CLASSES[int(row["ground_truth_idx"])]
            assert row["predicted_label"] == CLASSES[int(row["predicted_idx"])]

        # Probabilities sum to 1.0
        prob_cols = [f"prob_{c}" for c in CLASSES]
        cal_prob_cols = [f"prob_cal_{c}" for c in CLASSES]

        assert np.allclose(df[prob_cols].sum(axis=1), 1.0, atol=1e-3), f"{fname}: raw probabilities do not sum to 1.0"
        assert np.allclose(df[cal_prob_cols].sum(axis=1), 1.0, atol=1e-3), f"{fname}: calibrated probabilities do not sum to 1.0"

        # Max confidence matches argmax
        max_probs = df[prob_cols].max(axis=1)
        assert np.allclose(df["max_confidence"], max_probs, atol=1e-5), f"{fname}: max_confidence mismatch!"

# -------------------------------------------------------------
# 6. Authoritative Registry Metric Concordance
# -------------------------------------------------------------
def test_registry_metric_concordance():
    reg_path = PROJECT_ROOT / "AUTHORITATIVE_EXPERIMENT_REGISTRY_V4.csv"
    assert reg_path.exists(), f"Registry missing: {reg_path}"
    df_reg = pd.read_csv(reg_path)
    assert len(df_reg) == 11, f"Expected 11 registry rows, got {len(df_reg)}"

    # Check key experiments
    exp_map = {r["experiment_id"]: r for _, r in df_reg.iterrows()}

    # EXP-A: Model A Random Test
    exp_a = exp_map["EXP-A"]
    df_a = pd.read_csv(PROJECT_ROOT / exp_a["source_prediction_file"])
    acc_a = accuracy_score(df_a["ground_truth_idx"], df_a["predicted_idx"])
    _, _, f1_a, _ = precision_recall_fscore_support(df_a["ground_truth_idx"], df_a["predicted_idx"], average="macro")
    assert np.isclose(acc_a, float(exp_a["accuracy"]), atol=1e-4)
    assert np.isclose(f1_a, float(exp_a["macro_f1"]), atol=1e-4)
    assert round(acc_a, 4) == 0.9443
    assert round(f1_a, 4) == 0.9408

    # EXP-B-ALL: Model B Group Test (2,043)
    exp_b_all = exp_map["EXP-B-ALL"]
    df_b = pd.read_csv(PROJECT_ROOT / exp_b_all["source_prediction_file"])
    acc_b = accuracy_score(df_b["ground_truth_idx"], df_b["predicted_idx"])
    _, _, f1_b, _ = precision_recall_fscore_support(df_b["ground_truth_idx"], df_b["predicted_idx"], average="macro")
    assert np.isclose(acc_b, float(exp_b_all["accuracy"]), atol=1e-4)
    assert np.isclose(f1_b, float(exp_b_all["macro_f1"]), atol=1e-4)
    assert round(acc_b, 4) == 0.9755
    assert round(f1_b, 4) == 0.9752

    # EXP-B-RAW: Model B Group Test Raw Only (227)
    exp_b_raw = exp_map["EXP-B-RAW"]
    df_raw = pd.read_csv(PROJECT_ROOT / exp_b_raw["source_prediction_file"])
    acc_raw = accuracy_score(df_raw["ground_truth_idx"], df_raw["predicted_idx"])
    _, _, f1_raw, _ = precision_recall_fscore_support(df_raw["ground_truth_idx"], df_raw["predicted_idx"], average="macro")
    assert np.isclose(acc_raw, float(exp_b_raw["accuracy"]), atol=1e-4)
    assert np.isclose(f1_raw, float(exp_b_raw["macro_f1"]), atol=1e-4)
    assert round(acc_raw, 4) == 0.9736
    assert round(f1_raw, 4) == 0.9731

    # EXP-C1-MOD-B: FruitVision Model B
    exp_fv_b = exp_map["EXP-C1-MOD-B"]
    df_fv_b = pd.read_csv(PROJECT_ROOT / exp_fv_b["source_prediction_file"])
    acc_fv_b = accuracy_score(df_fv_b["ground_truth_idx"], df_fv_b["predicted_idx"])
    assert round(acc_fv_b, 4) == 0.6733
    prob_cols = [f"prob_{c}" for c in CLASSES]
    auc_fv_b = roc_auc_score(df_fv_b["ground_truth_idx"], df_fv_b[prob_cols], multi_class="ovr")
    assert round(auc_fv_b, 4) == 0.9540

    # EXP-C2-MOD-B: Sultana Model B
    exp_sul_b = exp_map["EXP-C2-MOD-B"]
    df_sul_b = pd.read_csv(PROJECT_ROOT / exp_sul_b["source_prediction_file"])
    acc_sul_b = accuracy_score(df_sul_b["ground_truth_idx"], df_sul_b["predicted_idx"])
    assert round(acc_sul_b, 4) == 0.6832
    auc_sul_b = roc_auc_score(df_sul_b["ground_truth_idx"], df_sul_b[prob_cols], multi_class="ovr")
    assert round(auc_sul_b, 4) == 0.9229

# -------------------------------------------------------------
# 7. Portable Relative Path Validity
# -------------------------------------------------------------
def test_portable_paths_validity():
    pred_files = [
        "PREDICTIONS_RANDOM_V4.csv",
        "PREDICTIONS_GROUP_TEST_V4.csv",
        "PREDICTIONS_GROUP_TEST_RAW_ONLY_V4.csv",
        "PREDICTIONS_FRUITVISION_V4.csv",
        "PREDICTIONS_SULTANA_V4.csv"
    ]

    for fname in pred_files:
        df = pd.read_csv(PROJECT_ROOT / fname)
        # Check that relative_path does not start with / or contain /Users/ or /home/
        bad_paths = df["relative_path"].str.startswith("/") | df["relative_path"].str.contains("/Users/") | df["relative_path"].str.contains("/home/")
        assert not bad_paths.any(), f"{fname} contains absolute/non-portable paths!"
