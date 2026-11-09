"""
scripts/package_v4.py
=====================
Assembles AGRIRoute_REMEDIATION_V4 directory and builds AGRIRoute_REMEDIATION_V4.zip.
Verifies all files exist, checks sizes, and validates zip archive integrity.
"""

import os
import shutil
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = PROJECT_ROOT / "AGRIRoute_REMEDIATION_V4"
ZIP_PATH = PROJECT_ROOT / "AGRIRoute_REMEDIATION_V4.zip"

def assemble_v4():
    print(f"Creating clean target directory: {TARGET_DIR}")
    if TARGET_DIR.exists():
        shutil.rmtree(TARGET_DIR)
    TARGET_DIR.mkdir(parents=True)

    # Subdirectories
    subdirs = ["SOURCE_CODE", "CHECKPOINTS", "TRAINING_LOGS", "PREDICTIONS", "DATASET_EXCLUSION_MANIFESTS", "PHASH_REVIEW"]
    for sd in subdirs:
        (TARGET_DIR / sd).mkdir(parents=True)

    # 1. Root documents
    root_files = [
        "README_FOR_CHATGPT.md",
        "REPRODUCIBILITY_GUIDE_V4.md",
        "V4_REMEDIATION_REPORT.md",
        "AUTHORITATIVE_EXPERIMENT_REGISTRY_V4.csv",
        "GROUP_SPLIT_MANIFEST_MERGED_V4.csv",
        "BASE_IMAGE_GROUP_AUDIT.csv",
        "CALIBRATION_AUDIT_V4.md",
        "PREDICTION_TRACEABILITY_V4.md",
        "LEAKAGE_EFFECT_ANALYSIS_V4.md",
        "FIELD_STUDY_PROTOCOL_V4.md",
        "UPDATED_REVIEWER_GAP_MATRIX_V4.md",
        "REFERENCE_VERIFICATION_V4.csv",
        "REFERENCES.bib",
        "TEST_REPORT.txt"
    ]
    for rf in root_files:
        src = PROJECT_ROOT / rf
        assert src.exists(), f"Missing root file: {rf}"
        shutil.copy2(src, TARGET_DIR / rf)
        print(f"  [ROOT] Copied {rf}")

    # 2. SOURCE_CODE
    code_files = [
        ("scripts/master_inference_and_calibration_v4.py", "master_inference_and_calibration_v4.py"),
        ("scripts/investigate_and_merge_phash.py", "investigate_and_merge_phash.py"),
        ("scripts/calculate_field_study_power.py", "calculate_field_study_power.py"),
        ("scripts/build_dataset_exclusion_manifests.py", "build_dataset_exclusion_manifests.py"),
        ("scripts/rebuild_reference_verification_v4.py", "rebuild_reference_verification_v4.py"),
        ("scripts/train_vision_benchmark.py", "train_vision_benchmark.py"),
        ("scripts/train_and_evaluate_group_leakage_study.py", "train_and_evaluate_group_leakage_study.py"),
        ("tests/test_reproducibility_v4.py", "test_reproducibility_v4.py")
    ]
    for src_rel, dst_name in code_files:
        src = PROJECT_ROOT / src_rel
        assert src.exists(), f"Missing code file: {src_rel}"
        shutil.copy2(src, TARGET_DIR / "SOURCE_CODE" / dst_name)
        print(f"  [SOURCE_CODE] Copied {dst_name}")

    # 3. CHECKPOINTS
    ckpt_files = [
        ("experiments/checkpoints/mobilenet_v2/best_model.keras", "best_model.keras"),
        ("experiments/group_leakage_study/CHECKPOINTS/group_aware_mobilenet_v2.keras", "group_aware_mobilenet_v2.keras")
    ]
    for src_rel, dst_name in ckpt_files:
        src = PROJECT_ROOT / src_rel
        assert src.exists(), f"Missing checkpoint: {src_rel}"
        shutil.copy2(src, TARGET_DIR / "CHECKPOINTS" / dst_name)
        print(f"  [CHECKPOINTS] Copied {dst_name} ({src.stat().st_size:,} bytes)")

    # 4. TRAINING_LOGS
    log_files = [
        ("experiments/logs/mobilenet_v2/training_history.csv", "historical_random_training_history.csv"),
        ("experiments/group_leakage_study/TRAINING_LOGS/group_aware_training_history.csv", "group_aware_training_history.csv")
    ]
    for src_rel, dst_name in log_files:
        src = PROJECT_ROOT / src_rel
        assert src.exists(), f"Missing log file: {src_rel}"
        shutil.copy2(src, TARGET_DIR / "TRAINING_LOGS" / dst_name)
        print(f"  [TRAINING_LOGS] Copied {dst_name}")

    # 5. PREDICTIONS
    pred_files = [
        "PREDICTIONS_RANDOM_V4.csv",
        "PREDICTIONS_GROUP_TEST_V4.csv",
        "PREDICTIONS_GROUP_TEST_RAW_ONLY_V4.csv",
        "PREDICTIONS_FRUITVISION_V4.csv",
        "PREDICTIONS_FRUITVISION_MODEL_A_V4.csv",
        "PREDICTIONS_SULTANA_V4.csv",
        "PREDICTIONS_SULTANA_MODEL_A_V4.csv"
    ]
    for pf in pred_files:
        src = PROJECT_ROOT / pf
        assert src.exists(), f"Missing prediction file: {pf}"
        shutil.copy2(src, TARGET_DIR / "PREDICTIONS" / pf)
        print(f"  [PREDICTIONS] Copied {pf} ({src.stat().st_size:,} bytes)")

    # 6. DATASET_EXCLUSION_MANIFESTS
    excl_dir = PROJECT_ROOT / "DATASET_EXCLUSION_MANIFESTS"
    for f in excl_dir.glob("*"):
        if f.is_file():
            shutil.copy2(f, TARGET_DIR / "DATASET_EXCLUSION_MANIFESTS" / f.name)
            print(f"  [DATASET_EXCLUSION_MANIFESTS] Copied {f.name}")

    # 7. PHASH_REVIEW
    phash_dir = PROJECT_ROOT / "PHASH_REVIEW"
    for f in phash_dir.glob("*"):
        if f.is_file():
            shutil.copy2(f, TARGET_DIR / "PHASH_REVIEW" / f.name)
            print(f"  [PHASH_REVIEW] Copied {f.name}")

    print("\nVerifying directory contents...")
    total_files = list(TARGET_DIR.rglob("*"))
    print(f"Total files in AGRIRoute_REMEDIATION_V4: {len([f for f in total_files if f.is_file()])}")

    # 8. Create ZIP archive
    print(f"\nBuilding ZIP archive: {ZIP_PATH} ...")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in TARGET_DIR.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(PROJECT_ROOT)
                zf.write(file_path, arcname)

    print(f"✅ Created {ZIP_PATH} ({ZIP_PATH.stat().st_size:,} bytes)")

    # Test ZIP integrity
    print("Testing ZIP archive integrity...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        bad_file = zf.testzip()
        if bad_file:
            raise RuntimeError(f"Corrupt file in zip: {bad_file}")
        print("✅ ZIP testzip() passed with zero errors!")

if __name__ == "__main__":
    assemble_v4()

