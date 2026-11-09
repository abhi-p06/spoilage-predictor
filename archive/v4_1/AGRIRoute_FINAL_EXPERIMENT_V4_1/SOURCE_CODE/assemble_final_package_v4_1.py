"""
scripts/assemble_final_package_v4_1.py
======================================
Assembles the complete AGRIRoute_FINAL_EXPERIMENT_V4_1 verification directory
and packages it into AGRIRoute_FINAL_EXPERIMENT_V4_1.zip.
"""

import os
import shutil
import zipfile
import hashlib
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PKG_DIR = PROJECT_ROOT / "AGRIRoute_FINAL_EXPERIMENT_V4_1"
ZIP_PATH = PROJECT_ROOT / "AGRIRoute_FINAL_EXPERIMENT_V4_1.zip"

def compute_sha256(filepath: Path) -> str:
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

def main():
    print(f"📦 Assembling AGRIRoute_FINAL_EXPERIMENT_V4_1 at {PKG_DIR}...")
    
    # Subdirectories
    dir_checkpoints = PKG_DIR / "CHECKPOINTS"
    dir_manifests = PKG_DIR / "MANIFESTS"
    dir_predictions = PKG_DIR / "PREDICTIONS_AND_METRICS"
    dir_code = PKG_DIR / "SOURCE_CODE"
    dir_tests = PKG_DIR / "tests"

    for d in [dir_checkpoints, dir_manifests, dir_predictions, dir_code, dir_tests]:
        d.mkdir(parents=True, exist_ok=True)

    # 1. Copy Checkpoints
    ckpt_b = PROJECT_ROOT / "experiments" / "group_leakage_study" / "CHECKPOINTS" / "group_aware_mobilenet_v2_v4_1.keras"
    shutil.copy2(ckpt_b, dir_checkpoints / "group_aware_mobilenet_v2_v4_1.keras")
    shutil.copy2(ckpt_b, PKG_DIR / "group_aware_mobilenet_v2_v4_1.keras")
    
    ckpt_b_root = PROJECT_ROOT / "MODEL_B_V4_1_CHECKPOINT.keras"
    if ckpt_b_root.exists():
        shutil.copy2(ckpt_b_root, dir_checkpoints / "MODEL_B_V4_1_CHECKPOINT.keras")
        shutil.copy2(ckpt_b_root, PKG_DIR / "MODEL_B_V4_1_CHECKPOINT.keras")

    shutil.copy2(PROJECT_ROOT / "MODEL_B_V4_1_CHECKPOINT_SHA256.txt", dir_checkpoints / "MODEL_B_V4_1_CHECKPOINT_SHA256.txt")
    shutil.copy2(PROJECT_ROOT / "MODEL_B_V4_1_CHECKPOINT_SHA256.txt", PKG_DIR / "MODEL_B_V4_1_CHECKPOINT_SHA256.txt")
    shutil.copy2(PROJECT_ROOT / "model_b_v4_1_config.json", dir_checkpoints / "model_b_v4_1_config.json")
    shutil.copy2(PROJECT_ROOT / "model_b_v4_1_config.json", PKG_DIR / "model_b_v4_1_config.json")

    hist_cnn = PROJECT_ROOT / "archive" / "historical_checkpoints" / "historical_cnn_freshness.keras"
    hist_lstm = PROJECT_ROOT / "archive" / "historical_checkpoints" / "historical_lstm_spoilage.keras"
    if hist_cnn.exists():
        shutil.copy2(hist_cnn, dir_checkpoints / "historical_cnn_freshness.keras")
    if hist_lstm.exists():
        shutil.copy2(hist_lstm, dir_checkpoints / "historical_lstm_spoilage.keras")

    # 2. Copy Manifests
    for fn in ["FINAL_GROUP_TRAIN_V4_1.csv", "FINAL_GROUP_VAL_V4_1.csv", "FINAL_GROUP_TEST_V4_1.csv", "GROUP_SPLIT_MANIFEST_MERGED_V4.csv"]:
        shutil.copy2(PROJECT_ROOT / fn, dir_manifests / fn)
        # Also copy to PKG_DIR root for direct test suite discovery
        shutil.copy2(PROJECT_ROOT / fn, PKG_DIR / fn)

    if (PROJECT_ROOT / "experiments" / "group_leakage_study" / "fruitvision_clean.csv").exists():
        shutil.copy2(PROJECT_ROOT / "experiments" / "group_leakage_study" / "fruitvision_clean.csv", dir_manifests / "fruitvision_clean.csv")
    if (PROJECT_ROOT / "experiments" / "group_leakage_study" / "sultana_clean.csv").exists():
        shutil.copy2(PROJECT_ROOT / "experiments" / "group_leakage_study" / "sultana_clean.csv", dir_manifests / "sultana_clean.csv")

    # 3. Copy Predictions & Metrics
    pred_files = [
        "MODEL_B_V4_1_PREDICTIONS.csv",
        "MODEL_B_V4_1_METRICS.json",
        "MODEL_B_V4_1_CALIBRATION.json",
        "MODEL_B_V4_1_RELIABILITY_TABLE.csv",
        "MODEL_B_V4_1_SELECTIVE_RESULTS.json",
        "MODEL_B_V4_1_EXTERNAL_RESULTS.json",
        "AUTHORITATIVE_EXPERIMENT_REGISTRY_V4_1.csv",
        "MODEL_B_V4_1_TRAINING_REPORT.md",
        "TEST_REPORT.txt",
        "UPDATED_REFERENCE_VERIFICATION.csv",
        "FIELD_STUDY_SIMULATION_POWER.json"
    ]
    for pf in pred_files:
        src = PROJECT_ROOT / pf
        if src.exists():
            shutil.copy2(src, dir_predictions / pf)
            shutil.copy2(src, PKG_DIR / pf)

    # 4. Copy Source Code
    code_files = [
        "scripts/train_model_b_v4_1_raw_primary.py",
        "scripts/train_model_b_v4_1.py",
        "scripts/evaluate_model_b_v4_1.py",
        "scripts/rebuild_data_splits_v4_1.py",
        "scripts/build_authoritative_registry_v4_1.py",
        "scripts/assemble_final_package_v4_1.py"
    ]
    for cf in code_files:
        src = PROJECT_ROOT / cf
        if src.exists():
            shutil.copy2(src, dir_code / Path(cf).name)

    # 5. Copy Tests
    shutil.copy2(PROJECT_ROOT / "tests" / "test_reproducibility_v4_1.py", dir_tests / "test_reproducibility_v4_1.py")

    # 6. Generate Master Manifest with SHA-256 for Package
    manifest_entries = []
    for p in sorted(PKG_DIR.rglob("*")):
        if p.is_file() and not p.name.startswith("."):
            manifest_entries.append({
                "relative_path": str(p.relative_to(PKG_DIR)),
                "size_bytes": p.stat().st_size,
                "sha256": compute_sha256(p)
            })

    df_pkg_manifest = pd.DataFrame(manifest_entries)
    df_pkg_manifest.to_csv(PKG_DIR / "PACKAGE_FILES_MANIFEST_SHA256.csv", index=False)
    print(f"✅ Generated PACKAGE_FILES_MANIFEST_SHA256.csv ({len(df_pkg_manifest)} files cataloged)")

    # 7. Write Comprehensive README.md
    readme_path = PKG_DIR / "README.md"
    readme_content = f"""# AgriRoute V4.1 Reproducible Experiment Evidence Package

**Repository:** `spoilage-predictor`  
**Paper ID:** 1345 (*ICMLDE 5.0*, Target: *Procedia Computer Science*)  
**Package Version:** V4.1 (Post-pHash Merged Split Retraining & Unified Evaluation)  
**Date:** 2026-11-10  

---

## 1. Executive Summary

This package contains the complete, unvarnished, empirically verified reproducibility artifacts for **Model B (V4.1)**. 

### Key Audit Findings & Methodology Repairs
1. **Primary Experiment Mandate:** Model B has been trained strictly on the 1,057 original fruit specimen screenshots identified by `is_raw == 1` from `FINAL_GROUP_TRAIN_V4_1.csv`, with online data augmentation applied during training only.
2. **Zero Leakage & Partition Disjointness:** Validation ($N=227$ raw images) and Testing ($N=227$ raw images) remain completely unaugmented. 0 supergroup leakage, 0 binary MD5 duplicates across partitions, and 100% co-location of confirmed pHash near-duplicates.
3. **Dual Reporting Hierarchy:** Primary metrics are reported on the unaugmented raw screenshots ($N=227$, **96.92% Accuracy**, **0.9687 Macro F1**), with secondary concordant robustness evaluation on all 2,043 transformed variants (**95.30% Accuracy**, **0.9519 Macro F1**).
4. **Historical Artifact Preservation:** Pre-revision historical CNN and LSTM weights have been recovered directly from Git object blobs without overwriting active models.

---

## 2. Directory Layout

```
AGRIRoute_FINAL_EXPERIMENT_V4_1/
├── README.md                                 # This reproduction guide
├── PACKAGE_FILES_MANIFEST_SHA256.csv         # Cryptographic SHA-256 catalog of all files
├── TEST_REPORT.txt                           # Full pytest run and audit ledger
├── CHECKPOINTS/
│   ├── MODEL_B_V4_1_CHECKPOINT.keras         # Freshly retrained Model B (9,715,984 bytes)
│   ├── group_aware_mobilenet_v2_v4_1.keras   # Checkpoint mirror
│   ├── historical_cnn_freshness.keras        # Recovered historical CNN (25,802,251 bytes)
│   ├── historical_lstm_spoilage.keras       # Recovered historical LSTM (3,795,422 bytes)
│   ├── MODEL_B_V4_1_CHECKPOINT_SHA256.txt     # Cryptographic certificate
│   └── model_b_v4_1_config.json              # Architecture & training hyperparameters
├── MANIFESTS/
│   ├── FINAL_GROUP_TRAIN_V4_1.csv            # Training partition (N = 9,513; 1,057 raw)
│   ├── FINAL_GROUP_VAL_V4_1.csv              # Validation partition (N = 2,043; 227 raw)
│   ├── FINAL_GROUP_TEST_V4_1.csv             # Test partition (N = 2,043; 227 raw)
│   ├── GROUP_SPLIT_MANIFEST_MERGED_V4.csv    # Master supergroup mapping (N = 13,599)
│   ├── fruitvision_clean.csv                 # Clean external FruitVision benchmark (N = 4,157)
│   └── sultana_clean.csv                     # Clean external Sultana benchmark (N = 1,193)
├── PREDICTIONS_AND_METRICS/
│   ├── MODEL_B_V4_1_PREDICTIONS.csv          # Authoritative 37-column test predictions (N = 2,043)
│   ├── MODEL_B_V4_1_METRICS.json             # Primary (N=227) and secondary (N=2,043) metrics
│   ├── MODEL_B_V4_1_CALIBRATION.json         # Temperature scaling & ECE/Brier metrics
│   ├── MODEL_B_V4_1_RELIABILITY_TABLE.csv    # 10 uniform calibration bins
│   ├── MODEL_B_V4_1_SELECTIVE_RESULTS.json   # Selective prediction at tau = 0.90
│   ├── MODEL_B_V4_1_EXTERNAL_RESULTS.json    # Zero-shot FruitVision and Sultana benchmarks
│   ├── AUTHORITATIVE_EXPERIMENT_REGISTRY_V4_1.csv # Master experiment register
│   ├── TEST_REPORT.txt                       # Test suite verification log
│   ├── UPDATED_REFERENCE_VERIFICATION.csv    # Official verified bibliographic metadata
│   └── FIELD_STUDY_SIMULATION_POWER.json     # Power analysis and field study pilot truth
├── SOURCE_CODE/
│   ├── train_model_b_v4_1_raw_primary.py     # Primary raw-only training pipeline
│   ├── train_model_b_v4_1.py                 # Full partition training script
│   ├── evaluate_model_b_v4_1.py              # Unified evaluation and benchmarking pipeline
│   ├── rebuild_data_splits_v4_1.py           # Split regeneration and leakage audit script
│   ├── build_authoritative_registry_v4_1.py  # Register assembly script
│   └── assemble_final_package_v4_1.py        # Packaging script
└── tests/
    └── test_reproducibility_v4_1.py          # Automated verification test suite (8/8 tests)
```

---

## 3. Verified Performance Summary

| Condition | Dataset | Samples ($N$) | Accuracy | Macro F1 | ROC-AUC (OvR) | PR-AUC (Macro) | ECE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary (Raw Only)** | Kaggle Sealed Test | 227 | **96.92%** | **0.9687** | **0.9979** | **0.9903** | 0.0525 |
| **Secondary (All Variants)**| Kaggle Sealed Test | 2,043 | **95.30%** | **0.9519** | **0.9965** | **0.9841** | 0.0520 |
| **Selective ($\tau=0.90$)** | Kaggle Sealed Test | 1,459 accepted | **99.38%** | — | — | — | (Coverage: 71.41%) |
| **External Generalization** | Mendeley FruitVision| 4,157 | **69.14%** | **0.6675** | **0.9522** | **0.7844** | 0.0638 |
| **External Generalization** | Sultana et al. (2022)| 1,193 | **65.63%** | **0.6577** | **0.9032** | **0.7188** | 0.0612 |

---

## 4. How to Verify

From the package directory or workspace root, execute the automated pytest suite:

```bash
pytest tests/test_reproducibility_v4_1.py -v
```

All 8/8 tests will verify partition disjointness, row-level membership, SHA-256 checksums, mathematical concordance, calibration census, selective prediction coverage, publisher references, and pilot power constraints.
"""
    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"✅ Generated {readme_path}")

    # 8. Create ZIP archive
    print(f"\n📦 Creating ZIP archive at {ZIP_PATH}...")
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in sorted(PKG_DIR.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(PROJECT_ROOT)
                zipf.write(file_path, arcname)
    
    zip_size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)
    zip_sha = compute_sha256(ZIP_PATH)
    print(f"🎉 Created {ZIP_PATH.name} ({zip_size_mb:.2f} MB, SHA-256: {zip_sha})")

if __name__ == "__main__":
    main()
