"""
scripts/evaluate_stage4_1_benchmark.py
======================================
Pre-specified and version-locked evaluation pipeline for the AgriRoute
Open-Set Fruit Quality Classification Benchmark.

Evaluates frozen Model B V4.1 across five empirical partitions:
- Partition A: Primary In-Distribution Test Set (Kaggle Fresh/Rotten, N=227)
- Partition B: External Known-Class Domain Shift (FruitVision + Sultana, N=5,350)
- Partition C: Condition-Shift Unknown (Labelled Formalin-mixed Known Species, N=1,917)
- Partition D1: Pure Semantic Shift (Unseen Species Fresh & Rotten, N=4,776)
- Partition D2: Combined Semantic & Treatment Shift (Unseen Species Formalin-mixed, N=1,195)

Strict Benchmarking Safeguards:
1. Reads ONLY STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv
2. Filters strictly inclusion_status == 'INCLUDED' (N=13,465 local images)
3. Zero ingestion of ToxiFruit records (which remain strictly PLANNED)
4. Loads calibrated operating thresholds from STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv
5. Uses joint cascade thresholds for Dual-Gate (NOT individual single-gate thresholds)
6. Implements all three pHash sensitivity tiers (Primary N=13,465; Tier 1 N=13,409; Tier 2 N=13,382)
7. Defaults to --dry-run (static validation of inputs and manifest without external inference)
"""

import os
import sys
import argparse
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# File Paths
MANIFEST_PATH = PROJECT_ROOT / "STAGE4_0_2_CORRECTED_IMAGE_MANIFEST.csv"
THRESHOLDS_PATH = PROJECT_ROOT / "STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv"
PHASH_REVIEW_PATH = PROJECT_ROOT / "STAGE4_0_3_PHASH_ROW_LEVEL_REVIEW.csv"
CENSUS_PATH = PROJECT_ROOT / "STAGE4_0_3_CORRECTED_PARTITION_CENSUS.csv"
CKPT_PATH = PROJECT_ROOT / "MODEL_B_V4_1_CHECKPOINT.keras"
EXPECTED_CKPT_SHA256 = "4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4"

EXPECTED_LOCAL_COUNTS = {
    "A_PRIMARY_IN_DISTRIBUTION": 227,
    "B_EXTERNAL_KNOWN_SHIFT": 5350,
    "C_CONDITION_SHIFT_UNKNOWN": 1917,
    "D1_PURE_SEMANTIC_SHIFT": 4776,
    "D2_COMBINED_SEMANTIC_TREATMENT_SHIFT": 1195
}
EXPECTED_TOTAL_INCLUDED = 13465
EXPECTED_TIER1_COUNT = 13409
EXPECTED_TIER2_COUNT = 13382

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def validate_environment_and_inputs():
    """Performs static pre-flight verification of all evaluation inputs."""
    print("=" * 80)
    print("STAGE 4.1: STATIC PRE-FLIGHT INPUT VERIFICATION")
    print("=" * 80)

    # 1. Verify Checkpoint SHA-256
    assert CKPT_PATH.exists(), f"Checkpoint not found: {CKPT_PATH}"
    actual_ckpt_sha = compute_sha256(CKPT_PATH)
    print(f"Checkpoint SHA-256: {actual_ckpt_sha}")
    assert actual_ckpt_sha == EXPECTED_CKPT_SHA256, (
        f"FATAL: Checkpoint SHA-256 mismatch! Expected {EXPECTED_CKPT_SHA256}, got {actual_ckpt_sha}"
    )
    print("✅ Checkpoint byte integrity confirmed.")

    # 2. Verify Manifest
    assert MANIFEST_PATH.exists(), f"Manifest not found: {MANIFEST_PATH}"
    df_manifest = pd.read_csv(MANIFEST_PATH)
    print(f"Loaded master manifest: {len(df_manifest)} rows")
    assert len(df_manifest) == 20781, f"Expected 20,781 rows in manifest, got {len(df_manifest)}"

    # 3. Filter inclusion_status == 'INCLUDED'
    df_included = df_manifest[df_manifest["inclusion_status"] == "INCLUDED"].copy().reset_index(drop=True)
    print(f"Filtered INCLUDED rows: {len(df_included)}")
    assert len(df_included) == EXPECTED_TOTAL_INCLUDED, (
        f"Expected {EXPECTED_TOTAL_INCLUDED} included rows, got {len(df_included)}"
    )

    # 4. Confirm zero ToxiFruit rows loaded
    toxi_rows = df_included[df_included["dataset"] == "ToxiFruit_2026"]
    print(f"ToxiFruit rows in INCLUDED subset: {len(toxi_rows)}")
    assert len(toxi_rows) == 0, "FATAL: ToxiFruit PLANNED rows must never enter active evaluation!"
    print("✅ Zero ToxiFruit PLANNED rows confirmed in evaluation set.")

    # 5. Confirm partition-level counts
    part_counts = df_included["partition_group"].value_counts().to_dict()
    for part, exp_cnt in EXPECTED_LOCAL_COUNTS.items():
        act_cnt = part_counts.get(part, 0)
        print(f"Partition {part}: {act_cnt} (Expected: {exp_cnt})")
        assert act_cnt == exp_cnt, f"Partition count mismatch for {part}: expected {exp_cnt}, got {act_cnt}"
    print("✅ All partition counts match expected census exactly.")

    # 6. Verify image loading columns (image_id and relative_path)
    assert "image_id" in df_included.columns, "image_id column missing from manifest"
    assert "relative_path" in df_included.columns, "relative_path column missing from manifest"
    assert df_included["image_id"].nunique() == len(df_included), "image_id contains collisions"
    print(f"✅ Verified {len(df_included)} unique image_id records with valid relative paths.")

    # 7. Verify Operating Thresholds & Dual-Gate Joint Setting
    assert THRESHOLDS_PATH.exists(), f"Thresholds table not found: {THRESHOLDS_PATH}"
    df_thresh = pd.read_csv(THRESHOLDS_PATH)
    print(f"Loaded threshold table: {len(df_thresh)} rows")
    assert len(df_thresh) == 12, f"Expected 12 threshold rows, got {len(df_thresh)}"

    # Check Dual-Gate joint thresholds
    dg_95 = df_thresh[df_thresh["configuration_id"] == "dual_gate_cascade_tau95"].iloc[0]
    dg_90 = df_thresh[df_thresh["configuration_id"] == "dual_gate_cascade_tau90"].iloc[0]
    
    tau_eng_95 = float(dg_95["energy_threshold"])
    tau_msp_95 = float(dg_95["msp_threshold"])
    tau_eng_90 = float(dg_90["energy_threshold"])
    tau_msp_90 = float(dg_90["msp_threshold"])

    print(f"Dual-Gate tau_95 joint thresholds: Energy={tau_eng_95:.6f}, MSP={tau_msp_95:.6f}")
    print(f"Dual-Gate tau_90 joint thresholds: Energy={tau_eng_90:.6f}, MSP={tau_msp_90:.6f}")

    # Assert joint thresholds are NOT single-gate thresholds
    single_eng_95 = float(df_thresh[df_thresh["configuration_id"] == "score_energy_id_tau95"]["primary_threshold_value"].iloc[0])
    single_msp_95 = float(df_thresh[df_thresh["configuration_id"] == "score_msp_tau95"]["primary_threshold_value"].iloc[0])
    assert tau_eng_95 != single_eng_95, "Dual-gate must use joint Energy threshold (s_(7)), not single-gate (s_(12))!"
    assert tau_msp_95 != single_msp_95, "Dual-gate must use joint MSP threshold (s_(7)), not single-gate (s_(12))!"
    print("✅ Dual-Gate correctly configured with calibrated joint thresholds.")

    # 8. Verify Three-Tier Sensitivity Analysis Subsets
    assert PHASH_REVIEW_PATH.exists(), f"pHash review file not found: {PHASH_REVIEW_PATH}"
    df_phash = pd.read_csv(PHASH_REVIEW_PATH)
    print(f"Loaded pHash review records: {len(df_phash)} rows")
    assert len(df_phash) == 170, f"Expected 170 pHash review rows, got {len(df_phash)}"

    cross_part_ids = set(df_phash[df_phash["phash_group_type"] == "CROSS_PARTITION"]["image_id"])
    multi_label_ids = set(df_phash[df_phash["phash_group_type"] == "INTRA_PARTITION_MULTI_LABEL"]["image_id"])

    print(f"Cross-partition collision images: {len(cross_part_ids)}")
    print(f"Multi-label intra-partition images: {len(multi_label_ids)}")
    assert len(cross_part_ids) == 56, f"Expected 56 cross-partition images, got {len(cross_part_ids)}"
    assert len(multi_label_ids) == 27, f"Expected 27 multi-label images, got {len(multi_label_ids)}"

    # Tier 1 subset (Primary excluding 56 cross-partition collisions)
    tier1_df = df_included[~df_included["image_id"].isin(cross_part_ids)]
    print(f"Sensitivity Tier 1 cohort: {len(tier1_df)} images (Expected: {EXPECTED_TIER1_COUNT})")
    assert len(tier1_df) == EXPECTED_TIER1_COUNT, f"Tier 1 count mismatch: {len(tier1_df)}"

    # Tier 2 subset (Primary excluding both cross-partition and multi-label collisions: 56 + 27 = 83 rows excluded)
    tier2_excluded_ids = cross_part_ids.union(multi_label_ids)
    tier2_df = df_included[~df_included["image_id"].isin(tier2_excluded_ids)]
    print(f"Sensitivity Tier 2 cohort: {len(tier2_df)} images (Expected: {EXPECTED_TIER2_COUNT})")
    assert len(tier2_df) == EXPECTED_TIER2_COUNT, f"Tier 2 count mismatch: {len(tier2_df)}"
    print("✅ All three pHash sensitivity tiers successfully verified and locked.")

    print("\n" + "=" * 80)
    print("PRE-FLIGHT STATIC VERIFICATION COMPLETE: ALL 8 CRITERIA PASSED [100%]")
    print("=" * 80)
    return True

def main():
    parser = argparse.ArgumentParser(description="Stage 4.1 Evaluation Pipeline")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Validate inputs and exit without inference")
    parser.add_argument("--execute", action="store_true", help="Execute inference on external partitions (Strictly Gated)")
    args = parser.parse_args()

    # Always perform input and environment verification
    validate_environment_and_inputs()

    if args.execute:
        print("\nFATAL: Stage 4.1 execution gate is LOCKED during pre-flight validation.")
        print("Run with --dry-run (default) until the preflight audit report is accepted.")
        sys.exit(1)
    else:
        print("\nDry-run mode active. No external inference was executed. Model weights remain uncalled.")

if __name__ == "__main__":
    main()

