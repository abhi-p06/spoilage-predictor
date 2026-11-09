#!/usr/bin/env python3
"""
scripts/build_remediation_v3_zip.py
===================================
Packages all authoritative remediation artifacts into AGRIRoute_REMEDIATION_V3.zip
and verifies archive integrity via testzip().
"""

import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ZIP_OUT = PROJECT_ROOT / "AGRIRoute_REMEDIATION_V3.zip"

FILES_TO_PACK = [
    # 12 Core Remediation Documents
    "REMEDIATION_V3_REPORT.md",
    "AUTHORITATIVE_EXPERIMENT_REGISTRY.csv",
    "MODEL_COMPARISON_V3.md",
    "EXTERNAL_GENERALIZATION_V3.md",
    "CALIBRATION_AUDIT_V3.md",
    "LEAKAGE_EFFECT_ANALYSIS.md",
    "GROUP_MANIFEST_REPRODUCIBILITY.md",
    "PREDICTION_TRACEABILITY_AUDIT.md",
    "REFERENCE_VERIFICATION_V3.csv",
    "FIELD_STUDY_PROTOCOL_V3.md",
    "UPDATED_REVIEWER_GAP_MATRIX_V3.md",
    "REPRODUCIBILITY_GUIDE_V3.md",

    # Authoritative Manifests & Reviews
    "BASE_IMAGE_GROUP_AUDIT.csv",
    "GROUP_SPLIT_MANIFEST.csv",
    "GROUP_PHASH_COLLISION_REVIEW.csv",

    # Authoritative Traceable Predictions
    "PREDICTIONS_RANDOM.csv",
    "PREDICTIONS_GROUP_TEST.csv",
    "PREDICTIONS_GROUP_TEST_RAW_ONLY.csv",
    "PREDICTIONS_FRUITVISION.csv",
    "PREDICTIONS_SULTANA.csv",

    # Bibliographic
    "REFERENCES.bib",

    # Testing & Verification
    "tests/test_reproducibility.py",

    # Core Scripts
    "scripts/build_group_manifests.py",
    "scripts/analyze_leakage_effect.py",
    "scripts/generate_traceable_predictions.py",
    "scripts/create_authoritative_registry.py",
    "scripts/generate_reference_verification_v3.py",
    "scripts/reproduce_calibration_details.py",

    # Raw Study JSONs
    "experiments/group_leakage_study/RANDOM_SPLIT_RESULTS.json",
    "experiments/group_leakage_study/GROUP_SPLIT_RESULTS.json",
    "experiments/group_leakage_study/FRUITVISION_RESULTS.json",
    "experiments/group_leakage_study/SULTANA_RESULTS.json",
    "experiments/group_leakage_study/LEAKAGE_EFFECT_ANALYSIS_DATA.json",
    "experiments/group_leakage_study/AUTHORITATIVE_CALIBRATION_METRICS.json",
]

def main():
    print(f"Creating {ZIP_OUT}...")
    if ZIP_OUT.exists():
        ZIP_OUT.unlink()

    with zipfile.ZipFile(ZIP_OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        # Add listed files
        for rel_path_str in FILES_TO_PACK:
            p = PROJECT_ROOT / rel_path_str
            if p.exists():
                arcname = f"AGRIRoute_REMEDIATION_V3/{rel_path_str}"
                zf.write(p, arcname=arcname)
                print(f"  + Added: {rel_path_str}")
            else:
                print(f"  ⚠️ Warning: File not found: {p}")

        # Add all contact sheets
        cs_dir = PROJECT_ROOT / "PHASH_COLLISION_CONTACT_SHEET"
        if cs_dir.exists():
            for f in sorted(cs_dir.glob("*.png")):
                arcname = f"AGRIRoute_REMEDIATION_V3/PHASH_COLLISION_CONTACT_SHEET/{f.name}"
                zf.write(f, arcname=arcname)
                print(f"  + Added Contact Sheet: {f.name}")

        # Add quarantined legacy files
        leg_dir = PROJECT_ROOT / "archive" / "legacy_unverified"
        if leg_dir.exists():
            for f in sorted(leg_dir.glob("*")):
                if f.is_file():
                    arcname = f"AGRIRoute_REMEDIATION_V3/archive/legacy_unverified/{f.name}"
                    zf.write(f, arcname=arcname)
                    print(f"  + Added Quarantined Legacy: {f.name}")

    print("\nVerifying archive integrity via testzip()...")
    with zipfile.ZipFile(ZIP_OUT, "r") as zf:
        first_bad = zf.testzip()
        if first_bad is not None:
            raise RuntimeError(f"Corrupt file in zip archive: {first_bad}")
        file_count = len(zf.namelist())
        size_mb = ZIP_OUT.stat().st_size / (1024 * 1024)
        print(f"✅ ZIP Archive Verified Clean! {file_count} files, {size_mb:.2f} MB")

if __name__ == "__main__":
    main()

