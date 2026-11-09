# Authoritative Research Reproducibility & Replication Guide (V3)

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Integrity Auditor:** Lead Scientific Integrity Engineer  
**Document ID:** `REPRODUCIBILITY_GUIDE_V3.md`  
**Execution Timestamp:** 2026-11-09  
**Git Branch:** `remediation/scientific-audit-repair`  
**Supersedes:** `archive/legacy_unverified/REPRODUCIBILITY_GUIDE_legacy.md`

---

## 1. Research Environment & Prerequisites

This reproducibility guide provides portable relative paths for Linux, macOS, and Windows environments. All commands assume execution from the repository root directory.

### 1.1 Python Environment Specification
- **Python:** 3.11.x
- **Deep Learning Framework:** TensorFlow 2.16.2 (or `tensorflow-macos` 2.16.2 / `tensorflow-metal` 1.1.0 on Apple Silicon)
- **Key Scientific Libraries:**
  - `numpy >= 1.26.0`
  - `scipy >= 1.12.0`
  - `pandas >= 2.2.0`
  - `scikit-learn >= 1.4.0`
  - `Pillow >= 10.2.0`
  - `imagehash >= 4.3.1`
  - `pytest >= 8.0.0`

### 1.2 Environment Installation
```bash
# Clone or navigate to the repository root
cd spoilage-predictor

# Create and activate conda environment
conda create -n agriroute_env python=3.11 -y
conda activate agriroute_env

# Install dependencies
pip install tensorflow scikit-learn scipy pandas pillow imagehash pytest
```

---

## 2. Experimental Classification & Architecture Clarifications

To prevent misleading claims, all experimental modules in this repository are categorized into five distinct tiers:

1. **Tier 1 — Group-Aware Model (Model B):**
   - **Weight Initialization:** Initialized with ImageNet-1k pretrained weights (`weights="imagenet"`), **not** trained from scratch.
   - **Partitioning:** Stratified group-aware partition (1,511 base-image families, zero group overlap).
   - **Status:** **AUTHORITATIVE SCIENTIFIC BASELINE**.
2. **Tier 2 — Historical Random-Split Model (Model A):**
   - **Partitioning:** Random filepath split with 77.8% base-image-family overlap.
   - **Status:** **BENCHMARK CONTAMINATED BASELINE** (maintained strictly for empirical comparison).
3. **Tier 3 — External Generalization Benchmarks:**
   - **Corpora:** FruitVision ($N=4,157$) and Sultana ($N=1,193$). Zero-shot cross-dataset evaluation.
   - **Status:** **VERIFIED OUT-OF-DISTRIBUTION BENCHMARK**.
4. **Tier 4 — Uncertainty Calibration & Selective Prediction:**
   - **Method:** Validation-fitted temperature scaling ($T^* = 0.6740$) and confidence thresholding ($\tau = 0.9000$).
   - **Status:** **VERIFIED DEPLOYMENT METHODOLOGY**.
5. **Tier 5 — Quarantined / Retracted Legacy Experiments:**
   - **Module:** Synthetic BiLSTM time-series sequence training ($AUC = 1.0000$).
   - **Status:** **RETRACTED AND QUARANTINED** in `archive/legacy_unverified/`. Must **not** be executed for scientific reporting.

---

## 3. Step-by-Step Reproduction Pipeline

All scripts execute reproducibly from the terminal using relative paths:

### Step 1: Base-Image-Family Grouping and Manifest Generation
Extracts prefix syntax, audits 1,511 base families, verifies zero group overlap across splits, and computes perceptual hash collisions:
```bash
python scripts/build_group_manifests.py
```
- **Outputs:**
  - `BASE_IMAGE_GROUP_AUDIT.csv`
  - `GROUP_SPLIT_MANIFEST.csv`
  - `GROUP_PHASH_COLLISION_REVIEW.csv`
  - `PHASH_COLLISION_CONTACT_SHEET/*.png`

### Step 2: Intra-Partition Leakage Impact Analysis
Quantifies the exact performance delta between seen and unseen base families within the historical random test set:
```bash
python scripts/analyze_leakage_effect.py
```
- **Outputs:**
  - `experiments/group_leakage_study/LEAKAGE_EFFECT_ANALYSIS_DATA.json`
  - Terminal output detailing the $+2.89\%$ accuracy and $+4.16\%$ macro F1 point inflation, class breakdowns, and cluster-bootstrap 95% CIs.

### Step 3: Authoritative Prediction Table Generation
Generates cryptographic MD5-traceable prediction CSVs and compresses the enhanced binary archive:
```bash
python scripts/generate_traceable_predictions.py
```
- **Outputs:**
  - `PREDICTIONS_RANDOM.csv` ($N=4,090$)
  - `PREDICTIONS_GROUP_TEST.csv` ($N=2,043$)
  - `PREDICTIONS_GROUP_TEST_RAW_ONLY.csv` ($N=227$)
  - `PREDICTIONS_FRUITVISION.csv` ($N=4,157$)
  - `PREDICTIONS_SULTANA.csv` ($N=1,193$)
  - `experiments/group_leakage_study/PREDICTIONS_TRACEABLE.npz`

### Step 4: Temperature Scaling Probability Calibration Audit
Resolves the optimizer discrepancy using Brent's bounded scalar search and audits ECE, MCE, NLL, and Brier score across 10 reliability bins:
```bash
python scripts/reproduce_calibration_details.py
```
- **Outputs:**
  - `experiments/group_leakage_study/AUTHORITATIVE_CALIBRATION_METRICS.json`

### Step 5: Master Experiment Registry & Citation Verification
Generates the authoritative registries:
```bash
python scripts/create_authoritative_registry.py
python scripts/generate_reference_verification_v3.py
```
- **Outputs:**
  - `AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`
  - `REFERENCE_VERIFICATION_V3.csv`
  - Verified `REFERENCES.bib`

---

## 4. Automated Reproduction Test Suite

To verify system integrity in a single command, execute the automated pytest suite:
```bash
pytest tests/test_reproducibility.py -v
```

This automated suite executes 6 critical integrity tests:
1. `test_manifest_integrity`: Verifies row counts, non-empty paths, and valid MD5 hashes.
2. `test_group_isolation`: Verifies zero group ID overlap across train, val, and test splits.
3. `test_prediction_alignment`: Asserts exact 1:1 ground-truth label alignment between manifests and prediction tables.
4. `test_metric_reconciliation`: Confirms that calculated metrics from raw predictions match `AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`.
5. `test_checkpoint_integrity`: Asserts that `.keras` model weights exist, load cleanly, and contain the expected 2.27M parameters.
6. `test_selective_prediction_constants`: Asserts exact coverage (25.11%) and accepted accuracy (95.69%) on FruitVision at $\tau=0.90$.

