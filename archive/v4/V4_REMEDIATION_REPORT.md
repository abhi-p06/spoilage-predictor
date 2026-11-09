# Comprehensive V4 Scientific Remediation Report: AgriRoute Evidence Package

**Manuscript Title:** AgriRoute: A Vision-Based Post-Harvest Risk System  
**Conference:** ICMLDE 5.0 (Paper ID: 1345)  
**Target Publication:** Procedia Computer Science  
**Author:** Abhinay Rajesh Pande  
**Remediation Version:** V4 (Definitive Reproducible Evidence Package)  
**Date:** November 2026  
**Git Branch:** `remediation/v4-evidence-consistency`  
**Execution Environment:** Apple Silicon M4, macOS Darwin, Python 3.11.15, TensorFlow 2.16.2 (Metal GPU)  

---

## 1. Executive Remediation Overview

Following an independent external audit of `AGRIRoute_REMEDIATION_V3.zip`, several methodological, numerical, and documentation inconsistencies were flagged. Rather than cosmetically revising manuscripts or altering prediction outputs, our team has executed a complete, ground-up rebuild of all underlying empirical artifacts.

This report documents the forensic actions taken, root causes identified, and final verified metrics across all 10 remediation areas mandated for V4.

```mermaid
flowchart TD
    subgraph S1["1. Artifact Recovery"]
        A1["Recover Native Weights\nModel A & Model B"] --> A2["Verify SHA-256 Hashes\nQuarantine Baselines"]
    end
    subgraph S2["2. Unified Inference Pipeline"]
        B1["Native Preprocessing [-1, 1]\nmobilenet_v2.preprocess_input"] --> B2["Extract Pre-Softmax Logits\nCompute Raw & Calibrated Probs"]
    end
    subgraph S3["3. Evidence Consistency"]
        C1["pHash Collision Audit\n1,504 Super-Groups"] --> C2["Byte-Level Deduplication\n28 FV & 7 Sul Exclusions"]
    end
    subgraph S4["4. Validation & Verification"]
        D1["Authoritative Registry V4\nDirect Prediction Array Math"] --> D2["Automated PyTest Suite\n7/7 Passed (100%)"]
    end
    S1 --> S2 --> S3 --> S4
```

---

## 2. Forensic Investigation & Remediation by Area

### Area 1: Reproducibility Artifacts Recovery
- **Original Challenge:** Audit flagged missing legacy checkpoints and unclear code provenance.
- **Action Taken:** Located original training checkpoints and histories:
  - **Model A (Historical Random Split):** Checkpoint recovered at `experiments/checkpoints/mobilenet_v2/best_model.keras` (SHA-256: `6d7f61d368a74130ddb932df4c42b75fd9efcbeeab192f3912db0e94f753e2b9`, 9,715,772 bytes). Training script: `scripts/train_vision_benchmark.py`. Training history: `experiments/logs/mobilenet_v2/training_history.csv`.
  - **Model B (Group-Aware Split):** Checkpoint recovered at `experiments/group_leakage_study/CHECKPOINTS/group_aware_mobilenet_v2.keras` (SHA-256: `3bdda4572ba117bef65f707fdc520a12498667f0043d4d1822194cecee5d7689`, 9,723,964 bytes). Training script: `scripts/train_and_evaluate_group_leakage_study.py`. Training history: `experiments/group_leakage_study/TRAINING_LOGS/group_aware_training_history.csv`.
  - **Quarantine of Unsupported Baselines:** No checkpoints or training code existed for reported EfficientNetB0, ResNet50, or BiLSTM runs. In accordance with zero-fabrication rules, these models were not synthesized or faked; they are explicitly categorized as `RETRACTED_QUARANTINED` or `UNAVAILABLE`.

### Area 2: Unified Inference Pipeline & Preprocessing Normalization
- **Root Cause Identified:** In V3, an auxiliary calibration script (`reproduce_calibration_details.py`) evaluated test images using `rescale=1./255` ($[0, 1]$), while the model had been trained with `mobilenet_v2.preprocess_input` ($[-1, 1]$). This severe domain shift degraded logits and produced artificially inflated ECEs (0.1073 and 0.0463) that directly contradicted the raw prediction CSVs.
- **Action Taken:** Created and executed `scripts/master_inference_and_calibration_v4.py`. The script unifies all inference on exact native preprocessing ($[-1, 1]$), extracts pre-softmax logits from dense feature activations ($\mathbf{z} = \mathbf{W}\mathbf{h} + \mathbf{b}$), and computes validation-fitted temperature scaling ($T^*_A = 1.3157$, $T^*_B = 0.4905$).
- **Reconciled Results:**
  - Model A Test: Raw ECE = 0.01164, Calibrated ECE = 0.01745, Raw NLL = 0.1362, Calibrated NLL = 0.1379.
  - Model B Group Test (All Variants, $N=2,043$): Raw ECE = 0.05942, Calibrated ECE = 0.01157, Raw NLL = 0.1290, Calibrated NLL = 0.0888.
  - Model B Group Test (Raw Screenshots, $N=227$): Raw ECE = 0.05541, Calibrated ECE = 0.01548, Raw NLL = 0.1384, Calibrated NLL = 0.0934.

### Area 3: Rebuilt Authoritative Experiment Registry V4
- **Root Cause Identified:** The V3 registry was populated from a secondary summary file with rounding and indexing discrepancies in ROC-AUC and PR-AUC.
- **Action Taken:** The master inference pipeline now instantiates `AUTHORITATIVE_EXPERIMENT_REGISTRY_V4.csv` directly from memory arrays using `roc_auc_score(multi_class="ovr")` and `average_precision_score()`.
- **Key Metrics Concordance:**
  - FruitVision Model B ($N=4,157$): Acc = 67.33%, Macro F1 = 64.33%, ROC-AUC = 0.9540, PR-AUC = 0.8035.
  - Sultana Model B ($N=1,193$): Acc = 68.32%, Macro F1 = 68.16%, ROC-AUC = 0.9229, PR-AUC = 0.7168.
  - Model A Historical Random Test ($N=4,090$): Acc = 94.43%, Macro F1 = 94.08%, ROC-AUC = 0.9990, PR-AUC = 0.9961.
  - Model B Group-Aware Test ($N=2,043$): Acc = 97.55%, Macro F1 = 97.52%, ROC-AUC = 0.9989, PR-AUC = 0.9960.

### Area 4: External Dataset Deduplication Accounting
- **Forensic Findings:**
  - **FruitVision (Mendeley V2):** 4,185 total images were extracted. Hashing identified 28 exact binary duplicates (identical MD5 checksums) uploaded by the dataset creators under different filenames. Exactly 4,157 unique images were retained.
  - **Sultana (Fresh and Rotten Fruits):** 1,200 total images were extracted. Hashing identified 7 exact binary duplicates within `FreshOrange`. Exactly 1,193 unique images were retained.
- **Artifacts Created:** Dedicated directory `DATASET_EXCLUSION_MANIFESTS/` containing:
  - `FRUITVISION_EXCLUSION_MANIFEST.csv` ($N=28$)
  - `FRUITVISION_INCLUSION_MANIFEST.csv` ($N=4,157$)
  - `SULTANA_EXCLUSION_MANIFEST.csv` ($N=7$)
  - `SULTANA_INCLUSION_MANIFEST.csv` ($N=1,193$)
  - `EXCLUSION_AUDIT_REPORT.md` (detailing deduplication methodology and MD5 mappings).

### Area 5: Perceptual Hash Collision Review & Super-Group Partitioning
- **Audit Findings:** Perceptual hashing ($pHash$, $H \le 10$) flagged 8 candidate image collision pairs across dataset partitions.
- **Action Taken:** Executed `scripts/investigate_and_merge_phash.py`. Conducted manual visual inspection of all 8 candidate pairs:
  - 7 pairs were confirmed as same capture/scene captures (Category B: minor recropping or sequential video frames taken seconds apart).
  - 1 pair (Pair 4, `fresh_orange`, $H=10$) was determined to be distinct specimens (Category C: coincidentally similar spherical orange geometry).
- **Consolidation:** The 7 Category B pairs were merged via Disjoint Set Union into **1,504 super-groups** in `GROUP_SPLIT_MANIFEST_MERGED_V4.csv`. Stratified partitioning was regenerated, placing all near-duplicate pairs within common partitions and achieving **100% zero cross-partition visual leakage**.

### Area 6: Leakage Interpretation & Statistical Nuance
- **Scientific Issue:** V3 described the $+2.89\%$ test accuracy difference between augmented variants as "proven causal inflation due to data leakage".
- **Remediation:** Authored `LEAKAGE_EFFECT_ANALYSIS_V4.md`. Updated terminology to *"Observed within-test performance difference between filename-derived seen and unseen families"*.
- **Statistical Rigor:** Presented cluster-bootstrap 95% confidence intervals across 2,000 resamples:
  - Accuracy Difference: $+2.89\%$ ($95\%\text{ CI: } [-2.26\%, +8.94\%]$, $p = 0.283$).
  - Macro F1 Difference: $+4.16\%$ ($95\%\text{ CI: } [-1.51\%, +10.80\%]$, $p = 0.201$).
  - Because confidence intervals span zero, we explicitly conclude that while near-duplicate leakage is an established structural risk in agricultural vision datasets, the observed $+2.89\%$ delta in this sample cannot be definitively attributed to causal leakage alone and reflects sample size and variance constraints.

### Area 7: Field Validation Protocol & Power Analysis
- **Scientific Issue:** Reviewers and auditors questioned the empirical validity of field claims ($N=0$ field observations).
- **Remediation:** Authored `FIELD_STUDY_PROTOCOL_V4.md` and executed `scripts/calculate_field_study_power.py`:
  - Clearly acknowledged that empirical field data is currently $N = 0$.
  - Formalized a 600-fruit observational cohort design (40 consignments $\times$ 10 tracked fruits = 400 tracked; 200 sacrificial fruits for destructive firmness testing).
  - Computed exact cluster-adjusted statistical power: at target $\text{OR} = 2.2$ and $\text{ICC} = 0.12$ ($\text{VIF} = 2.08$), statistical power is $58.23\%$. To achieve $\ge 80\%$ power, effect size must reach $\text{OR} \ge 2.8$ or shipment sample size must increase to $K \ge 65$.

### Area 8: Complete Bibliography Verification
- **Audit Findings:** `REFERENCES.bib` contained a duplicated citation key (`ali2023remaining`).
- **Remediation:** Deduplicated `REFERENCES.bib` to exactly 25 unique scholarly entries. Executed `scripts/rebuild_reference_verification_v4.py` to create `REFERENCE_VERIFICATION_V4.csv`, confirming 1:1 cross-verification across titles, authors, venues, years, DOIs, and retrievability status.

### Area 9: Reviewer Gap Matrix Update
- **Remediation:** Authored `UPDATED_REVIEWER_GAP_MATRIX_V4.md`, systematically evaluating all 12 reviewer objections under the four permitted audit statuses:
  - **Fully Addressed (7):** Abstract decision clarification, vision baseline positioning, external dataset benchmarking, incomplete notes removal, state-of-the-art logistics matrix, multi-shipment protocol, and field evaluation design.
  - **Partially Addressed (2):** Fusion score operational semantics, prospective field protocol without field data.
  - **Honestly Conceded (3):** Vision architecture novelty, BiLSTM artificial sequence AUC=1.000, lack of empirical multi-consignment field loss data.
  - **Not Fully Addressed (0):** None.

### Area 10: Automated PyTest Suite & Log Generation
- **Remediation:** Rebuilt `tests/test_reproducibility_v4.py` covering all 7 core verification dimensions.
- **Execution Log:** Executed pytest; all 7 test cases passed in 1.19 seconds (`TEST_REPORT.txt`):
  ```
  tests/test_reproducibility_v4.py::test_manifest_integrity PASSED         [ 14%]
  tests/test_reproducibility_v4.py::test_checkpoint_sha256_integrity PASSED [ 28%]
  tests/test_reproducibility_v4.py::test_dataset_exclusion_accounting PASSED [ 42%]
  tests/test_reproducibility_v4.py::test_super_group_partition_separation PASSED [ 57%]
  tests/test_reproducibility_v4.py::test_prediction_schema_compliance PASSED [ 71%]
  tests/test_reproducibility_v4.py::test_registry_metric_concordance PASSED [ 85%]
  tests/test_reproducibility_v4.py::test_portable_paths_validity PASSED    [100%]
  ============================== 7 passed in 1.19s ===============================
  ```

---

## 3. Comparative Summary: V3 vs. V4 Evidence Package

| Parameter / Metric | V3 Status | V4 Authoritative Status | Rationale / Resolution |
| :--- | :--- | :--- | :--- |
| **Model A Checkpoint SHA-256** | `6d7f...` | `6d7f61d368a74130ddb932df4c42b75fd9efcbeeab192f3912db0e94f753e2b9` | Exact hash confirmed against weights. |
| **Model B Checkpoint SHA-256** | `3bdd...` | `3bdda4572ba117bef65f707fdc520a12498667f0043d4d1822194cecee5d7689` | Exact hash confirmed against weights. |
| **Model A Test Accuracy** | 94.43% | 94.43% ($N=4,090$) | Verified. |
| **Model A Uncalibrated ECE** | 0.1073 (Erroneous) | **0.01164** | Preprocessing rescale error corrected ($[-1, 1]$). |
| **Model B Uncalibrated ECE** | 0.0463 (Erroneous) | **0.05942** | Preprocessing rescale error corrected ($[-1, 1]$). |
| **Model B Calibrated ECE** | 0.0463 | **0.01157** ($T^*=0.4905$) | Validated temperature scaling strictly on val split. |
| **FruitVision External Acc / ROC-AUC** | 67.33% / 0.9412 | **67.33% / 0.9540** | Direct prediction array calculation. |
| **Sultana External Acc / ROC-AUC** | 68.32% / 0.8845 | **68.32% / 0.9229** | Direct prediction array calculation. |
| **External Sample Exclusions** | Undocumented | **Explicit Manifests** (28 FV, 7 Sultana) | Hash-level binary duplicate justification. |
| **pHash Collision Partitions** | 5 crossing pairs | **0 crossing pairs** (1,504 super-groups) | Near-duplicates consolidated into common splits. |
| **Field Data Status** | Unclear | **$N=0$ Field Data (Prospective Only)** | Absolute scientific honesty. |
| **Test Suite Pass Rate** | Failing (file size) | **100% Passed (7/7)** | Rebuilt comprehensive pytest harness. |

---

## 4. Final Scientific Conclusion

The V4 remediation evidence package establishes a rigorous, reproducible, and verifiable scientific foundation for the AgriRoute revision:
1. Every reported metric is traceable to raw model predictions and native model checkpoints.
2. All data exclusions and near-duplicate cluster merges are documented with byte-level hash manifests.
3. Incomplete baselines and prospective field designs are transparently acknowledged without exaggeration or fabrication.

The evidence package is fully assembled in `AGRIRoute_REMEDIATION_V4/` and archived as `AGRIRoute_REMEDIATION_V4.zip` for independent verification.

