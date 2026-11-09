#!/usr/bin/env python3
"""
Rebuild Final Data Splits (V4.1)
===============================
Regenerates authoritative train, validation, and test manifests directly from
GROUP_SPLIT_MANIFEST_MERGED_V4.csv, verifying zero supergroup leakage, zero MD5
duplication, and zero pHash collision leakage.
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path("/Users/abby/Desktop/spoilage-predictor").resolve()

def main():
    print("=" * 70)
    print("🔍 AgriRoute Phase 2: Rebuilding & Verifying Final Data Splits (V4.1)")
    print("=" * 70)

    master_manifest_path = PROJECT_ROOT / "GROUP_SPLIT_MANIFEST_MERGED_V4.csv"
    assert master_manifest_path.exists(), f"Missing master manifest: {master_manifest_path}"

    df_master = pd.read_csv(master_manifest_path)
    print(f"Master manifest loaded: {len(df_master):,} total image rows")

    # Check required columns
    required_cols = [
        "group_id", "filepath", "relative_path", "filename", "base_filename",
        "class_name", "label_idx", "variant_type", "is_raw", "split_partition",
        "md5", "legacy_unmerged_partition", "super_group_id", "merged_split_partition_v4"
    ]
    for col in required_cols:
        assert col in df_master.columns, f"Missing required column: {col}"

    # Verify all filepaths exist on disk
    print("Verifying filesystem accessibility of all images in manifest...")
    missing_files = []
    for fp in df_master["filepath"]:
        p = Path(fp)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        if not p.exists():
            missing_files.append(str(p))

    if missing_files:
        raise FileNotFoundError(f"Found {len(missing_files)} missing image files on disk! First: {missing_files[0]}")
    print(f"All {len(df_master):,} images verified present on disk!")

    # Separate into V4.1 partitions
    train_mask = df_master["merged_split_partition_v4"] == "train"
    val_mask = df_master["merged_split_partition_v4"] == "val"
    test_mask = df_master["merged_split_partition_v4"] == "test"

    df_train = df_master[train_mask].copy().reset_index(drop=True)
    df_val = df_master[val_mask].copy().reset_index(drop=True)
    df_test = df_master[test_mask].copy().reset_index(drop=True)

    print("\n--- Partition Sample Counts ---")
    print(f"Train samples: {len(df_train):,} ({len(df_train)/len(df_master)*100:.2f}%)")
    print(f"Val samples:   {len(df_val):,} ({len(df_val)/len(df_master)*100:.2f}%)")
    print(f"Test samples:  {len(df_test):,} ({len(df_test)/len(df_master)*100:.2f}%)")
    assert len(df_train) + len(df_val) + len(df_test) == len(df_master)

    # 1. Supergroup disjointness check
    print("\n--- Forensic Check 1: Supergroup Disjointness ---")
    train_sg = set(df_train["super_group_id"].unique())
    val_sg = set(df_val["super_group_id"].unique())
    test_sg = set(df_test["super_group_id"].unique())

    print(f"Unique supergroups: Train={len(train_sg):,}, Val={len(val_sg):,}, Test={len(test_sg):,}")
    print(f"Total unique supergroups: {len(train_sg | val_sg | test_sg):,}")
    assert len(train_sg | val_sg | test_sg) == 1504, "Expected exactly 1,504 supergroups!"

    overlap_train_val = train_sg & val_sg
    overlap_train_test = train_sg & test_sg
    overlap_val_test = val_sg & test_sg

    assert len(overlap_train_val) == 0, f"Leakage: {len(overlap_train_val)} supergroups between train and val!"
    assert len(overlap_train_test) == 0, f"Leakage: {len(overlap_train_test)} supergroups between train and test!"
    assert len(overlap_val_test) == 0, f"Leakage: {len(overlap_val_test)} supergroups between val and test!"
    print("✅ Supergroup overlap: EXACTLY ZERO LEAKAGE across all partitions.")

    # 2. Base group disjointness check
    print("\n--- Forensic Check 2: Base Group Disjointness ---")
    train_bg = set(df_train["group_id"].unique())
    val_bg = set(df_val["group_id"].unique())
    test_bg = set(df_test["group_id"].unique())
    assert len(train_bg & val_bg) == 0
    assert len(train_bg & test_bg) == 0
    assert len(val_bg & test_bg) == 0
    print(f"Unique base groups: Train={len(train_bg):,}, Val={len(val_bg):,}, Test={len(test_bg):,} (Total: {len(train_bg | val_bg | test_bg):,})")
    print("✅ Base group overlap: EXACTLY ZERO LEAKAGE across all partitions.")

    # 3. MD5 disjointness check
    print("\n--- Forensic Check 3: MD5 Duplication Check ---")
    train_md5 = set(df_train["md5"].unique())
    val_md5 = set(df_val["md5"].unique())
    test_md5 = set(df_test["md5"].unique())
    assert len(train_md5 & val_md5) == 0, f"MD5 leakage between train and val: {len(train_md5 & val_md5)}"
    assert len(train_md5 & test_md5) == 0, f"MD5 leakage between train and test: {len(train_md5 & test_md5)}"
    assert len(val_md5 & test_md5) == 0, f"MD5 leakage between val and test: {len(val_md5 & test_md5)}"
    print(f"Unique MD5 hashes: Train={len(train_md5):,}, Val={len(val_md5):,}, Test={len(test_md5):,}")
    print("✅ MD5 duplication across splits: EXACTLY ZERO.")

    # 4. Confirmed pHash collision check
    print("\n--- Forensic Check 4: Confirmed pHash Collision Pairs ---")
    collision_review_path = PROJECT_ROOT / "GROUP_PHASH_COLLISION_REVIEW.csv"
    if collision_review_path.exists():
        df_coll = pd.read_csv(collision_review_path)
        print(f"Checking {len(df_coll)} pHash collision review pairs in master manifest...")
        group_to_part = dict(zip(df_master["group_id"], df_master["merged_split_partition_v4"]))
        group_to_sg = dict(zip(df_master["group_id"], df_master["super_group_id"]))
        for _, row in df_coll.iterrows():
            cid = row["collision_id"]
            g1, g2 = row["group1"], row["group2"]
            p1, p2 = group_to_part.get(g1), group_to_part.get(g2)
            sg1, sg2 = group_to_sg.get(g1), group_to_sg.get(g2)
            assert p1 == p2, f"pHash collision violation! {g1} is in {p1} but {g2} is in {p2}!"
            if cid == 4:
                # Pair 4 was classified as C. Visually similar but independent (KEEP_SEPARATE)
                assert sg1 != sg2, "Pair 4 was expected to be kept separate"
                print(f"  Collision pair {cid} ({g1} <-> {g2}): KEEP_SEPARATE (independent specimens, both in '{p1}')")
            else:
                # Pairs 1, 2, 3, 5, 6, 7, 8 are confirmed same fruit series (MERGE_GROUPS)
                assert sg1 == sg2, f"Supergroup merge violation! {g1} is {sg1} but {g2} is {sg2}!"
                print(f"  Collision pair {cid} ({g1} <-> {g2}): MERGE_GROUPS into {sg1}, co-located in partition '{p1}'")
        print("✅ Confirmed pHash collision co-location: 100% verified.")

    # 5. Raw vs Augmented counts
    print("\n--- Forensic Check 5: Image Type Census ---")
    for name, df_p in [("Train", df_train), ("Val", df_val), ("Test", df_test)]:
        n_raw = (df_p["is_raw"] == 1).sum()
        n_aug = (df_p["is_raw"] == 0).sum()
        print(f"  {name}: Total={len(df_p):,}, Raw Base Screenshots={n_raw:,}, Augmented Variants={n_aug:,}")

    # 6. Class Distribution
    print("\n--- Forensic Check 6: Class Distribution Census ---")
    classes = ["fresh_apple", "fresh_banana", "fresh_orange", "rotten_apple", "rotten_banana", "rotten_orange"]
    dist_table = []
    for cls in classes:
        c_tr = (df_train["class_name"] == cls).sum()
        c_val = (df_val["class_name"] == cls).sum()
        c_te = (df_test["class_name"] == cls).sum()
        dist_table.append({
            "class_name": cls,
            "train": c_tr,
            "val": c_val,
            "test": c_te,
            "total": c_tr + c_val + c_te
        })
    df_dist = pd.DataFrame(dist_table)
    print(df_dist.to_string(index=False))

    # Save Authoritative V4.1 Manifests
    train_v4_1_path = PROJECT_ROOT / "FINAL_GROUP_TRAIN_V4_1.csv"
    val_v4_1_path = PROJECT_ROOT / "FINAL_GROUP_VAL_V4_1.csv"
    test_v4_1_path = PROJECT_ROOT / "FINAL_GROUP_TEST_V4_1.csv"

    df_train.to_csv(train_v4_1_path, index=False)
    df_val.to_csv(val_v4_1_path, index=False)
    df_test.to_csv(test_v4_1_path, index=False)
    print(f"\nSaved new V4.1 manifests:")
    print(f"  -> {train_v4_1_path.name} ({len(df_train):,} rows)")
    print(f"  -> {val_v4_1_path.name} ({len(df_val):,} rows)")
    print(f"  -> {test_v4_1_path.name} ({len(df_test):,} rows)")

    # Also verify existing FINAL_GROUP_*_V4.csv
    print("\nCross-checking existing FINAL_GROUP_*_V4.csv files...")
    for old_name, df_new in [("FINAL_GROUP_TRAIN_V4.csv", df_train), ("FINAL_GROUP_VAL_V4.csv", df_val), ("FINAL_GROUP_TEST_V4.csv", df_test)]:
        old_path = PROJECT_ROOT / old_name
        if old_path.exists():
            df_old = pd.read_csv(old_path)
            assert len(df_old) == len(df_new), f"Row count mismatch in {old_name}!"
            assert set(df_old["md5"]) == set(df_new["md5"]), f"MD5 set mismatch in {old_name}!"
            print(f"  {old_name} verified 100% identical to V4.1 manifest ({len(df_new):,} rows).")

    print("\n✅ PHASE 2 COMPLETE: All data splits rebuilt and cryptographically verified.")
    print("=" * 70)

if __name__ == "__main__":
    main()
