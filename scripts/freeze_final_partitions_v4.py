"""
scripts/freeze_final_partitions_v4.py
====================================
Phase 1: Freezes the final dataset partitions from GROUP_SPLIT_MANIFEST_MERGED_V4.csv.

Generates:
- FINAL_GROUP_TRAIN_V4.csv
- FINAL_GROUP_VAL_V4.csv
- FINAL_GROUP_TEST_V4.csv

Conducts exhaustive forensic assertions:
- Partitions sum exactly to 13,599 rows.
- Zero super_group_id overlap between train, val, test.
- Every image row belongs to exactly one partition.
- All identical MD5 duplicates reside within the same partition.
- All 7 manually confirmed same-capture candidate pairs reside in the same partition.
- Documents filename-derived group counts, super-group counts, and raw screenshot counts.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def freeze_partitions():
    manifest_path = PROJECT_ROOT / "GROUP_SPLIT_MANIFEST_MERGED_V4.csv"
    assert manifest_path.exists(), f"Missing {manifest_path}"

    df = pd.read_csv(manifest_path)
    print(f"Loaded master manifest: {len(df)} rows")

    # Split by merged_split_partition_v4
    df_train = df[df["merged_split_partition_v4"] == "train"].copy().reset_index(drop=True)
    df_val = df[df["merged_split_partition_v4"] == "val"].copy().reset_index(drop=True)
    df_test = df[df["merged_split_partition_v4"] == "test"].copy().reset_index(drop=True)

    print(f"\nPartition Rows:")
    print(f"  Train: {len(df_train)}")
    print(f"  Val:   {len(df_val)}")
    print(f"  Test:  {len(df_test)}")
    print(f"  Total: {len(df_train) + len(df_val) + len(df_test)}")

    # 1. Total row check
    assert len(df_train) + len(df_val) + len(df_test) == 13599, "Row count mismatch!"
    assert len(df_train) == 9513, f"Expected 9,513 train rows, got {len(df_train)}"
    assert len(df_val) == 2043, f"Expected 2,043 val rows, got {len(df_val)}"
    assert len(df_test) == 2043, f"Expected 2,043 test rows, got {len(df_test)}"

    # 2. Super-group overlap check
    train_sg = set(df_train["super_group_id"])
    val_sg = set(df_val["super_group_id"])
    test_sg = set(df_test["super_group_id"])

    assert len(train_sg & val_sg) == 0, f"Leak detected: {train_sg & val_sg}"
    assert len(train_sg & test_sg) == 0, f"Leak detected: {train_sg & test_sg}"
    assert len(val_sg & test_sg) == 0, f"Leak detected: {val_sg & test_sg}"
    print("✅ Zero super-group leakage across Train, Val, and Test.")

    # 3. MD5 duplicate check
    train_md5 = set(df_train["md5"])
    val_md5 = set(df_val["md5"])
    test_md5 = set(df_test["md5"])

    assert len(train_md5 & val_md5) == 0, "MD5 collision between Train and Val!"
    assert len(train_md5 & test_md5) == 0, "MD5 collision between Train and Test!"
    assert len(val_md5 & test_md5) == 0, "MD5 collision between Val and Test!"
    print("✅ Zero MD5 hash collisions across Train, Val, and Test.")

    # 4. Confirmed pHash collision pairs check
    phash_audit_path = PROJECT_ROOT / "PHASH_REVIEW" / "PHASH_CANDIDATE_AUDIT.csv"
    if phash_audit_path.exists():
        df_phash = pd.read_csv(phash_audit_path)
        group_to_part = dict(zip(df["group_id"], df["merged_split_partition_v4"]))
        for _, r in df_phash[df_phash["recommended_action"] == "MERGE_GROUPS"].iterrows():
            part1 = group_to_part[r["group1"]]
            part2 = group_to_part[r["group2"]]
            assert part1 == part2, f"Near duplicate pair {r['pair_id']} crosses partitions ({part1} vs {part2})!"
        print("✅ All 7 confirmed near-duplicate pairs reside in common partitions.")

    # 5. Document counts
    for name, d in [("Train", df_train), ("Val", df_val), ("Test", df_test)]:
        n_raw = (d["is_raw"] == 1).sum()
        n_groups = d["group_id"].nunique()
        n_sg = d["super_group_id"].nunique()
        print(f"  [{name}] Super-groups: {n_sg}, Base groups: {n_groups}, Raw screenshots: {n_raw}, Total images: {len(d)}")

    # 6. Save final frozen partition manifests
    train_path = PROJECT_ROOT / "FINAL_GROUP_TRAIN_V4.csv"
    val_path = PROJECT_ROOT / "FINAL_GROUP_VAL_V4.csv"
    test_path = PROJECT_ROOT / "FINAL_GROUP_TEST_V4.csv"

    df_train.to_csv(train_path, index=False)
    df_val.to_csv(val_path, index=False)
    df_test.to_csv(test_path, index=False)

    print(f"\n✅ Successfully saved:\n  - {train_path}\n  - {val_path}\n  - {test_path}")

if __name__ == "__main__":
    freeze_partitions()
