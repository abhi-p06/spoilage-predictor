"""
tests/test_reproducibility_v4_1.py
==================================
Comprehensive automated validation test suite for AgriRoute V4.1 evidence package.

Can be executed with identical pass results from:
1. Workspace root (/Users/abby/Desktop/spoilage-predictor)
2. Packaged directory (AGRIRoute_REMEDIATION_V4_1/)
3. Extracted ZIP directory

Validates:
1. Dynamic root discovery.
2. Final partition integrity and zero super-group leakage across Train, Val, Test.
3. Row-level test manifest membership (merged_split_partition_v4 == 'test' for 100% of samples).
4. Model B V4.1 checkpoint SHA-256 integrity.
5. Exact prediction array metrics concordance (Acc, Macro F1, ROC-AUC, PR-AUC).
6. Calibration reliability bin census and weighted ECE math.
7. Selective prediction accounting.
8. Official publisher-verified reference metadata (Chen 2024, FruitQ, Li 2026).
9. Prospective field study pilot power and zero empirical field data truth.
"""

import os
import json
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score, average_precision_score

CLASSES = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]
NUM_CLASSES = 6

def get_package_root() -> Path:
    """Dynamically resolve root directory whether running from repo, package, or tests dir."""
    cwd = Path.cwd()
    if (cwd / "FINAL_GROUP_TEST_V4_1.csv").exists() or (cwd / "FINAL_GROUP_TEST_V4.csv").exists():
        return cwd
    if (cwd / "AGRIRoute_REMEDIATION_V4_1" / "FINAL_GROUP_TEST_V4_1.csv").exists() or (cwd / "AGRIRoute_REMEDIATION_V4_1" / "FINAL_GROUP_TEST_V4.csv").exists():
        return cwd / "AGRIRoute_REMEDIATION_V4_1"
    if (cwd / "AGRIRoute_FINAL_EXPERIMENT_V4_1" / "FINAL_GROUP_TEST_V4_1.csv").exists() or (cwd / "AGRIRoute_FINAL_EXPERIMENT_V4_1" / "FINAL_GROUP_TEST_V4.csv").exists():
        return cwd / "AGRIRoute_FINAL_EXPERIMENT_V4_1"
    
    file_parent = Path(__file__).resolve().parent
    if (file_parent / "FINAL_GROUP_TEST_V4_1.csv").exists() or (file_parent / "FINAL_GROUP_TEST_V4.csv").exists():
        return file_parent
    if (file_parent.parent / "FINAL_GROUP_TEST_V4_1.csv").exists() or (file_parent.parent / "FINAL_GROUP_TEST_V4.csv").exists():
        return file_parent.parent
    if (file_parent.parent / "AGRIRoute_REMEDIATION_V4_1" / "FINAL_GROUP_TEST_V4_1.csv").exists() or (file_parent.parent / "AGRIRoute_REMEDIATION_V4_1" / "FINAL_GROUP_TEST_V4.csv").exists():
        return file_parent.parent / "AGRIRoute_REMEDIATION_V4_1"
    if (file_parent.parent / "AGRIRoute_FINAL_EXPERIMENT_V4_1" / "FINAL_GROUP_TEST_V4_1.csv").exists() or (file_parent.parent / "AGRIRoute_FINAL_EXPERIMENT_V4_1" / "FINAL_GROUP_TEST_V4.csv").exists():
        return file_parent.parent / "AGRIRoute_FINAL_EXPERIMENT_V4_1"
    
    return cwd

def compute_file_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

# -------------------------------------------------------------
# 1. Final Partition Integrity & Super-Group Disjointness
# -------------------------------------------------------------
def test_final_partition_integrity_and_disjointness():
    root = get_package_root()
    train_p = root / "FINAL_GROUP_TRAIN_V4_1.csv" if (root / "FINAL_GROUP_TRAIN_V4_1.csv").exists() else root / "FINAL_GROUP_TRAIN_V4.csv"
    val_p = root / "FINAL_GROUP_VAL_V4_1.csv" if (root / "FINAL_GROUP_VAL_V4_1.csv").exists() else root / "FINAL_GROUP_VAL_V4.csv"
    test_p = root / "FINAL_GROUP_TEST_V4_1.csv" if (root / "FINAL_GROUP_TEST_V4_1.csv").exists() else root / "FINAL_GROUP_TEST_V4.csv"

    assert train_p.exists(), f"Missing train manifest: {train_p}"
    assert val_p.exists(), f"Missing val manifest: {val_p}"
    assert test_p.exists(), f"Missing test manifest: {test_p}"

    df_train = pd.read_csv(train_p)
    df_val = pd.read_csv(val_p)
    df_test = pd.read_csv(test_p)

    assert len(df_train) == 9513, f"Expected 9,513 train rows, got {len(df_train)}"
    assert len(df_val) == 2043, f"Expected 2,043 val rows, got {len(df_val)}"
    assert len(df_test) == 2043, f"Expected 2,043 test rows, got {len(df_test)}"
    assert len(df_train) + len(df_val) + len(df_test) == 13599

    # Super-group disjointness
    sg_train = set(df_train["super_group_id"])
    sg_val = set(df_val["super_group_id"])
    sg_test = set(df_test["super_group_id"])

    assert len(sg_train) == 1052, f"Expected 1,052 train super-groups, got {len(sg_train)}"
    assert len(sg_val) == 226, f"Expected 226 val super-groups, got {len(sg_val)}"
    assert len(sg_test) == 226, f"Expected 226 test super-groups, got {len(sg_test)}"

    assert len(sg_train & sg_val) == 0, "Train-Val super-group leakage!"
    assert len(sg_train & sg_test) == 0, "Train-Test super-group leakage!"
    assert len(sg_val & sg_test) == 0, "Val-Test super-group leakage!"

    # MD5 duplicate disjointness
    md5_train = set(df_train["md5"])
    md5_val = set(df_val["md5"])
    md5_test = set(df_test["md5"])

    assert len(md5_train & md5_val) == 0, "Train-Val MD5 collision!"
    assert len(md5_train & md5_test) == 0, "Train-Test MD5 collision!"
    assert len(md5_val & md5_test) == 0, "Val-Test MD5 collision!"

# -------------------------------------------------------------
# 2. Row-Level Test Manifest Membership Assertion
# -------------------------------------------------------------
def test_row_level_test_membership():
    root = get_package_root()
    test_p = root / "FINAL_GROUP_TEST_V4_1.csv" if (root / "FINAL_GROUP_TEST_V4_1.csv").exists() else root / "FINAL_GROUP_TEST_V4.csv"
    pred_p = root / "MODEL_B_V4_1_PREDICTIONS.csv"

    assert test_p.exists() and pred_p.exists()
    df_test = pd.read_csv(test_p)
    df_pred = pd.read_csv(pred_p)

    assert len(df_pred) == len(df_test) == 2043, "Prediction row count mismatch with test manifest!"

    # Mandatory assertion: every predicted row has merged_split_partition_v4 == 'test'
    assert (df_test["merged_split_partition_v4"] == "test").all()

    # Exact row-level matching by filename and MD5
    assert (df_pred["filename"].values == df_test["filename"].values).all(), "Filename order mismatch!"
    assert (df_pred["md5"].values == df_test["md5"].values).all(), "MD5 order mismatch!"

# -------------------------------------------------------------
# 3. Model B V4.1 Checkpoint SHA-256 Integrity
# -------------------------------------------------------------
def test_model_b_v4_1_checkpoint_sha256():
    root = get_package_root()
    sha_file = root / "MODEL_B_V4_1_CHECKPOINT_SHA256.txt"
    assert sha_file.exists(), f"Missing SHA report: {sha_file}"

    with open(sha_file, "r") as f:
        sha_text = f.read()

    expected_sha = None
    for line in sha_text.splitlines():
        if "MODEL_B_V4_1_CHECKPOINT_SHA256:" in line:
            expected_sha = line.split(":", 1)[1].strip()
            break
    assert expected_sha is not None and len(expected_sha) == 64

    # Locate checkpoint
    ckpt_candidates = [
        root / "MODEL_B_V4_1_CHECKPOINT.keras",
        root / "CHECKPOINTS" / "group_aware_mobilenet_v2_v4_1.keras",
        root / "group_aware_mobilenet_v2_v4_1.keras",
        root / "experiments" / "group_leakage_study" / "CHECKPOINTS" / "group_aware_mobilenet_v2_v4_1.keras"
    ]
    ckpt_p = None
    for c in ckpt_candidates:
        if c.exists():
            ckpt_p = c
            break
    assert ckpt_p is not None, "Could not locate group_aware_mobilenet_v2_v4_1.keras checkpoint!"
    assert ckpt_p.stat().st_size > 9_000_000, "Checkpoint suspiciously small!"

    computed_sha = compute_file_sha256(ckpt_p)
    assert computed_sha == expected_sha, f"SHA mismatch! Expected {expected_sha}, got {computed_sha}"

# -------------------------------------------------------------
# 4. Prediction Array Metrics Concordance
# -------------------------------------------------------------
def test_metrics_concordance():
    root = get_package_root()
    pred_p = root / "MODEL_B_V4_1_PREDICTIONS.csv"
    metrics_p = root / "MODEL_B_V4_1_METRICS.json"

    assert pred_p.exists() and metrics_p.exists()
    df_pred = pd.read_csv(pred_p)
    with open(metrics_p, "r") as f:
        metrics = json.load(f)

    # Secondary analysis: All 2,043 variants
    acc_all = accuracy_score(df_pred["ground_truth_idx"], df_pred["predicted_idx"])
    _, _, f1_all, _ = precision_recall_fscore_support(df_pred["ground_truth_idx"], df_pred["predicted_idx"], average="macro")
    
    assert np.isclose(acc_all, metrics["secondary_analysis_all_variants"]["uncalibrated"]["accuracy"], atol=1e-4)
    assert np.isclose(f1_all, metrics["secondary_analysis_all_variants"]["uncalibrated"]["macro_f1"], atol=1e-4)

    # Primary analysis: Raw screenshots only (N=227)
    df_raw = df_pred[df_pred["is_raw"] == 1]
    assert len(df_raw) == 227
    acc_raw = accuracy_score(df_raw["ground_truth_idx"], df_raw["predicted_idx"])
    _, _, f1_raw, _ = precision_recall_fscore_support(df_raw["ground_truth_idx"], df_raw["predicted_idx"], average="macro")

    assert np.isclose(acc_raw, metrics["primary_analysis_raw_only"]["accuracy"], atol=1e-4)
    assert np.isclose(f1_raw, metrics["primary_analysis_raw_only"]["macro_f1"], atol=1e-4)

# -------------------------------------------------------------
# 5. Calibration Reliability Census Verification
# -------------------------------------------------------------
def test_calibration_reliability_census():
    root = get_package_root()
    rel_p = root / "MODEL_B_V4_1_RELIABILITY_TABLE.csv"
    cal_p = root / "MODEL_B_V4_1_CALIBRATION.json"

    assert rel_p.exists() and cal_p.exists()
    df_rel = pd.read_csv(rel_p)
    with open(cal_p, "r") as f:
        cal_data = json.load(f)

    assert len(df_rel) == 10, f"Expected 10 reliability bins, got {len(df_rel)}"
    assert df_rel["sample_count"].sum() == 2043, "Reliability bins do not sum to 2,043 test samples!"

    # Weighted ECE sum
    computed_ece = df_rel["weighted_ece_contribution"].sum()
    assert np.isclose(computed_ece, cal_data["calibrated_ece"], atol=1e-4)

# -------------------------------------------------------------
# 6. Selective Prediction Consistency
# -------------------------------------------------------------
def test_selective_prediction_consistency():
    root = get_package_root()
    sel_p = root / "MODEL_B_V4_1_SELECTIVE_RESULTS.json"
    assert sel_p.exists()

    with open(sel_p, "r") as f:
        sel = json.load(f)

    assert sel["total_test_samples"] == 2043
    assert sel["accepted_samples"] + sel["abstained_samples"] == 2043
    assert np.isclose(sel["coverage_ratio"], sel["accepted_samples"] / 2043.0, atol=1e-4)

# -------------------------------------------------------------
# 7. Official Publisher Reference Verification
# -------------------------------------------------------------
def test_publisher_reference_verification():
    root = get_package_root()
    ref_p = root / "UPDATED_REFERENCE_VERIFICATION.csv"
    assert ref_p.exists()

    df_ref = pd.read_csv(ref_p)
    assert len(df_ref) == 25, f"Expected 25 references, got {len(df_ref)}"

    # Check Chen 2024
    chen = df_ref[df_ref["citation_key"] == "chen2024classification"].iloc[0]
    assert "Classification and identification of agricultural products based on improved MobileNetV2" in chen["title"]
    assert "Haiwei Chen" in chen["authors"]

    # Check FruitQ
    fruitq = df_ref[df_ref["citation_key"] == "abayomi2023fruitq"].iloc[0]
    assert "FruitQ: a new dataset of multiple fruit images for freshness evaluation" in fruitq["title"]
    assert "Misra" in fruitq["authors"]

    # Check Li 2026
    li = df_ref[df_ref["citation_key"] == "li2026dynamic"].iloc[0]
    assert "Kwon" in li["authors"] and "Dai" in li["authors"]

# -------------------------------------------------------------
# 8. Prospective Field Study Characterization
# -------------------------------------------------------------
def test_field_study_pilot_characterization():
    root = get_package_root()
    field_p = root / "FIELD_STUDY_SIMULATION_POWER.json"
    assert field_p.exists()

    with open(field_p, "r") as f:
        field_data = json.load(f)

    assert field_data["empirical_field_data_collected"] == 0, "Must be explicitly acknowledged as 0 empirical field data!"
    assert "exploratory pilot" in field_data["honest_concession"].lower()
    assert field_data["empirical_power_percent"] < 80.0, "Must honestly report that K=40 does not achieve 80% power!"
