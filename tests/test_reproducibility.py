"""
tests/test_reproducibility.py
=============================
Authoritative automated validation test suite for AgriRoute scientific integrity remediation.
Tests:
1. Manifest integrity and class counts
2. Group separation (zero leakage across train/val/test)
3. Prediction alignment and schema compliance
4. Metric reconciliation against raw predictions
5. Model checkpoint integrity
6. Authoritative registry validity
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_manifest_integrity():
    manifest_path = PROJECT_ROOT / "GROUP_SPLIT_MANIFEST.csv"
    audit_path = PROJECT_ROOT / "BASE_IMAGE_GROUP_AUDIT.csv"

    assert manifest_path.exists(), f"Missing {manifest_path}"
    assert audit_path.exists(), f"Missing {audit_path}"

    df_manifest = pd.read_csv(manifest_path)
    df_audit = pd.read_csv(audit_path)

    assert len(df_manifest) == 13599, f"Expected 13,599 manifest rows, got {len(df_manifest)}"
    assert len(df_audit) == 1511, f"Expected 1,511 base groups, got {len(df_audit)}"

    # Check for empty MD5s
    assert df_manifest["md5"].str.len().eq(32).all(), "Found invalid MD5 hashes in manifest!"
    assert (df_audit["group_integrity_status"] == "VERIFIED_9_VARIANTS").all(), "Found anomalous groups!"

def test_class_counts():
    df_manifest = pd.read_csv(PROJECT_ROOT / "GROUP_SPLIT_MANIFEST.csv")
    expected_classes = {"fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"}
    assert set(df_manifest["class_name"].unique()) == expected_classes

    # Check group distribution by partition
    part_counts = df_manifest.groupby("split_partition")["group_id"].nunique()
    assert part_counts["train"] == 1057, f"Expected 1,057 train groups, got {part_counts['train']}"
    assert part_counts["val"] == 227, f"Expected 227 val groups, got {part_counts['val']}"
    assert part_counts["test"] == 227, f"Expected 227 test groups, got {part_counts['test']}"

def test_group_separation():
    df_manifest = pd.read_csv(PROJECT_ROOT / "GROUP_SPLIT_MANIFEST.csv")

    train_groups = set(df_manifest[df_manifest["split_partition"] == "train"]["group_id"])
    val_groups = set(df_manifest[df_manifest["split_partition"] == "val"]["group_id"])
    test_groups = set(df_manifest[df_manifest["split_partition"] == "test"]["group_id"])

    assert len(train_groups & val_groups) == 0, "Train & Val group overlap detected!"
    assert len(train_groups & test_groups) == 0, "Train & Test group overlap detected!"
    assert len(val_groups & test_groups) == 0, "Val & Test group overlap detected!"

def test_prediction_alignment_and_probabilities():
    pred_files = [
        ("PREDICTIONS_RANDOM.csv", 4090),
        ("PREDICTIONS_GROUP_TEST.csv", 2043),
        ("PREDICTIONS_GROUP_TEST_RAW_ONLY.csv", 227),
        ("PREDICTIONS_FRUITVISION.csv", 4157),
        ("PREDICTIONS_SULTANA.csv", 1193),
    ]
    classes = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]

    for fname, expected_len in pred_files:
        csv_path = PROJECT_ROOT / fname
        assert csv_path.exists(), f"Missing {fname}"
        df = pd.read_csv(csv_path)
        assert len(df) == expected_len, f"{fname}: Expected {expected_len} rows, got {len(df)}"

        # Verify ground truth matches label idx
        for idx, row in df.iterrows():
            assert row["ground_truth_label"] == classes[row["ground_truth_idx"]], f"Mismatch in {fname} row {idx}"
            assert row["predicted_label"] == classes[row["predicted_idx"]], f"Pred mismatch in {fname} row {idx}"

        # Probabilities sum to 1.0
        prob_cols = [f"prob_{c}" for c in classes]
        prob_sums = df[prob_cols].sum(axis=1)
        assert np.allclose(prob_sums, 1.0, atol=1e-3), f"Probabilities do not sum to 1 in {fname}"

        # Max confidence matches argmax
        max_probs = df[prob_cols].max(axis=1)
        assert np.allclose(df["max_confidence"], max_probs, atol=1e-5), f"Max confidence mismatch in {fname}"

def test_metric_reconciliation():
    # Model A historical test
    df_rand = pd.read_csv(PROJECT_ROOT / "PREDICTIONS_RANDOM.csv")
    acc_rand = accuracy_score(df_rand["ground_truth_idx"], df_rand["predicted_idx"])
    _, _, f1_rand, _ = precision_recall_fscore_support(df_rand["ground_truth_idx"], df_rand["predicted_idx"], average="macro")
    assert round(acc_rand, 4) == 0.9443, f"Model A Acc: expected 0.9443, got {acc_rand:.4f}"
    assert round(f1_rand, 4) == 0.9408, f"Model A F1: expected 0.9408, got {f1_rand:.4f}"

    # Model B group test (all variants)
    df_grp = pd.read_csv(PROJECT_ROOT / "PREDICTIONS_GROUP_TEST.csv")
    acc_grp = accuracy_score(df_grp["ground_truth_idx"], df_grp["predicted_idx"])
    _, _, f1_grp, _ = precision_recall_fscore_support(df_grp["ground_truth_idx"], df_grp["predicted_idx"], average="macro")
    assert round(acc_grp, 4) == 0.9755, f"Model B Acc: expected 0.9755, got {acc_grp:.4f}"
    assert round(f1_grp, 4) == 0.9752, f"Model B F1: expected 0.9752, got {f1_grp:.4f}"

    # Model B raw only (227)
    df_raw = pd.read_csv(PROJECT_ROOT / "PREDICTIONS_GROUP_TEST_RAW_ONLY.csv")
    acc_raw = accuracy_score(df_raw["ground_truth_idx"], df_raw["predicted_idx"])
    _, _, f1_raw, _ = precision_recall_fscore_support(df_raw["ground_truth_idx"], df_raw["predicted_idx"], average="macro")
    assert round(acc_raw, 4) == 0.9736, f"Model B Raw Acc: expected 0.9736, got {acc_raw:.4f}"
    assert round(f1_raw, 4) == 0.9731, f"Model B Raw F1: expected 0.9731, got {f1_raw:.4f}"

    # FruitVision selective prediction at tau=0.90
    df_fv = pd.read_csv(PROJECT_ROOT / "PREDICTIONS_FRUITVISION.csv")
    accepted_fv = df_fv[df_fv["decision"] == "ACCEPTED"]
    cov_fv = len(accepted_fv) / len(df_fv)
    acc_acc_fv = accuracy_score(accepted_fv["ground_truth_idx"], accepted_fv["predicted_idx"])
    assert round(cov_fv, 4) == 0.2511, f"FruitVision Coverage: expected 0.2511, got {cov_fv:.4f}"
    assert round(acc_acc_fv, 4) == 0.9569, f"FruitVision Accepted Acc: expected 0.9569, got {acc_acc_fv:.4f}"

def test_checkpoint_integrity():
    model_a_path = PROJECT_ROOT / "experiments" / "checkpoints" / "mobilenet_v2" / "best_model.keras"
    model_b_path = PROJECT_ROOT / "experiments" / "group_leakage_study" / "CHECKPOINTS" / "group_aware_mobilenet_v2.keras"

    assert model_a_path.exists(), f"Model A checkpoint missing: {model_a_path}"
    assert model_b_path.exists(), f"Model B checkpoint missing: {model_b_path}"
    assert model_a_path.stat().st_size > 9_000_000, "Model A file suspiciously small!"
    assert model_b_path.stat().st_size > 9_000_000, "Model B file suspiciously small!"

def test_authoritative_registry():
    reg_path = PROJECT_ROOT / "AUTHORITATIVE_EXPERIMENT_REGISTRY.csv"
    assert reg_path.exists(), f"Missing {reg_path}"
    df_reg = pd.read_csv(reg_path)
    assert len(df_reg) == 11, f"Expected 11 authoritative registry rows, got {len(df_reg)}"
    assert not df_reg["experiment_id"].isnull().any()
    assert (df_reg["execution_status"] == "EXECUTED_AND_VERIFIED").all()
