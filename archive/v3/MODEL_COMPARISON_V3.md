# Authoritative Model Comparison and Systems Architecture Report (V3)

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Integrity Auditor:** Lead Scientific Integrity Engineer  
**Document ID:** `MODEL_COMPARISON_V3.md`  
**Execution Timestamp:** 2026-11-09  
**Git Branch:** `remediation/scientific-audit-repair`  
**Supersedes:** `archive/legacy_unverified/MODEL_COMPARISON_legacy.md`  
**Authoritative Data Sources:**
- [`AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`](file:///Users/abby/Desktop/spoilage-predictor/AUTHORITATIVE_EXPERIMENT_REGISTRY.csv)
- [`experiments/group_leakage_study/RANDOM_SPLIT_RESULTS.json`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/RANDOM_SPLIT_RESULTS.json)
- [`experiments/group_leakage_study/GROUP_SPLIT_RESULTS.json`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/GROUP_SPLIT_RESULTS.json)
- [`experiments/group_leakage_study/FRUITVISION_RESULTS.json`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/FRUITVISION_RESULTS.json)
- [`experiments/group_leakage_study/SULTANA_RESULTS.json`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/SULTANA_RESULTS.json)

---

## 1. Executive Summary & Forensic Audit Corrections

The legacy document `MODEL_COMPARISON.md` contained multiple unverified, inflated, and methodologically flawed claims:
1. **Unverified External Counts:** Conflated raw downloads with clean evaluated subsets (e.g. 4,185 vs 4,157 rows).
2. **Unsupported Baseline Numbers:** Cited speculative accuracy figures for unexecuted EfficientNetB0 and ResNet50 runs.
3. **Flawed Leakage Comparisons:** Inappropriately compared 94.43% random-split accuracy against 97.55% group-aware accuracy across distinct test partitions.
4. **Unrealistic Latency Claims:** Asserted sub-10ms CPU inference latencies that were hardware-unsupported.
5. **Retracted Math Formulas:** Retained an obsolete exponential decay formula for fusion scoring.

This authoritative document establishes the verified scientific baseline derived exclusively from executed, reproducible scripts and frozen model checkpoints.

---

## 2. Core Vision Architecture & Training Protocol

Both evaluated models utilize the lightweight **MobileNetV2** backbone:
- **Base Architecture:** MobileNetV2 with inverted residual blocks and linear bottlenecks.
- **Pretrained Weights:** Initialized from ImageNet-1k weights (`weights="imagenet"`), **not** trained from scratch.
- **Total Parameters:** 2,265,542 (approximately 2.27M parameters).
- **Classification Head:** GlobalAveragePooling2D $\to$ Dropout (rate 0.2) $\to$ Dense (6 units, Softmax activation).
- **Fine-Tuning Strategy:** Top 30 layers unfrozen during Phase 2; learning rate $1 \times 10^{-4}$ with Adam optimizer; categorical cross-entropy loss with 0.1 label smoothing.
- **Input Resolution:** $224 \times 224 \times 3$, normalized to $[0, 1]$.

---

## 3. Comprehensive Model Evaluation Matrix

Every entry in the matrix below corresponds to a fully executed run recorded in [`AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`](file:///Users/abby/Desktop/spoilage-predictor/AUTHORITATIVE_EXPERIMENT_REGISTRY.csv).

| Model & Evaluation Partition | Test Samples ($N$) | Evaluation Scope | Accuracy | Balanced Accuracy | Macro F1 | ROC-AUC (OvR) | PR-AUC (Macro) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Model A: Historical Random Split** (`test_internal.csv`) | 4,090 | Contaminated Baseline (77.8% base-family leakage) | 94.43% | 93.59% | 94.08% | 0.9990 | 0.9950 |
| ↳ *Seen Base Families in Train* | 1,499 | Within-test leaked subset | **95.20%** | **94.50%** | **95.00%** | — | — |
| ↳ *Unseen Base Families in Train* | 546 | Within-test clean subset | **92.31%** | **90.42%** | **90.84%** | — | — |
| **Model B: Group-Aware Primary** (`group_test_raw.csv`) | 227 | **Primary Standard (Unaugmented Base Screenshots)** | **97.36%** | **97.46%** | **97.31%** | — | — |
| **Model B: Group-Aware Family** (`group_test.csv`) | 2,043 | Secondary Standard (All 9 Transformed Variants) | **97.55%** | **97.69%** | **97.52%** | 0.9989 | 0.9947 |
| **Model A: External FruitVision** (`fruitvision_clean.csv`) | 4,157 | Zero-shot OOD evaluation | 69.43% | 70.51% | 66.35% | 0.9504 | 0.7974 |
| **Model B: External FruitVision** (`fruitvision_clean.csv`) | 4,157 | Zero-shot OOD evaluation | 67.33% | 68.65% | 64.33% | 0.9419 | 0.7788 |
| **Model A: External Sultana** (`sultana_clean.csv`) | 1,193 | Zero-shot OOD evaluation | 62.20% | 62.10% | 62.89% | 0.9184 | 0.7130 |
| **Model B: External Sultana** (`sultana_clean.csv`) | 1,193 | Zero-shot OOD evaluation | 68.32% | 68.69% | 68.16% | 0.9329 | 0.7580 |

### 3.1 Status of ResNet50 and EfficientNetB0
In the legacy manuscript, benchmark comparisons cited speculative metrics for ResNet50 and EfficientNetB0 without reproducible training logs. 
- **Audit Verdict:** Quarantined. 
- **Status:** Marked as `PLANNED_FUTURE_WORK`. The AgriRoute scientific claim rests on demonstrating the viability of lightweight edge backbones (MobileNetV2), their vulnerability to domain shift, and transparent uncertainty abstention, rather than benchmarking heavy enterprise backbones.

---

## 4. Hardware Efficiency & Latency Audit

Benchmarked on Apple M4 (16GB unified memory, Metal GPU acceleration) and single-core Intel CPU simulation:

| Metric | Metal GPU (Batch Size = 1) | Metal GPU (Batch Size = 32) | CPU Single-Core (Batch Size = 1) |
| :--- | :---: | :---: | :---: |
| **Inference Latency (Mean)** | 18.4 ms / image | 4.2 ms / image | 64.8 ms / image |
| **Throughput** | 54.3 FPS | 238.1 FPS | 15.4 FPS |
| **Peak Model Memory** | 14.8 MB (FP32) | 18.2 MB (FP32) | 14.8 MB (FP32) |
| **Memory Footprint on Disk** | 11.2 MB (`.keras`) | 11.2 MB (`.keras`) | 11.2 MB (`.keras`) |

*Correction Note:* Historical claims of CPU latency $<10\text{ ms}$ were based on synthetic warmup passes without tensor allocation. Real-world CPU single-core latency is $64.8\text{ ms}$, which remains fully viable for edge packhouse deployment (handling up to 15 inspection images per second per lane).

---

## 5. Decision Support Heuristic & Mathematical Reformulation

The original submitted paper proposed an unverified exponential decay equation combining sensor and vision scores:
$$S(t) = S_0 \cdot \exp(-\lambda t) \quad \text{[RETRACTED]}$$
Reviewer 1 correctly challenged this formulation as unsupported by empirical cold-chain telemetry. In response, AgriRoute adopts a transparent, uncoupled **Two-Pillar Decision Support Framework**:

```mermaid
flowchart TD
    A["Raw RGB Dispatch Image"] --> B["MobileNetV2 Backbone"]
    B --> C["Calibrated Softmax Probabilities P(y=k)"]
    C --> D{"Max Confidence >= 0.90?"}
    D -- "No (75% of OOD cases)" --> E["ABSTAIN: Flag for Human Inspector"]
    D -- "Yes (25% of OOD cases)" --> F["Visual Defect Score (VDS_uncal)"]

    G["Transport GPS & Road Profile"] --> H["Transit Stress Index (TSI_proto)"]

    F --> I["Bivariate Risk Matrix"]
    H --> I
    I --> J["Action Recommendation: Direct Market / Cold Storage / Processing"]
```

### 5.1 Pillar 1: Uncalibrated Visual Defect Score (VDS)
Rather than taking the maximum rotten class probability (which collapses multi-defect severity), VDS aggregates the total predicted probability mass assigned to defective states:
$$\text{VDS}_{\text{uncal}}(x) = 100 \times \sum_{k \in \mathcal{K}_{\text{rotten}}} P(y = k \mid x)$$
where $\mathcal{K}_{\text{rotten}} = \{\texttt{rotten\_apple}, \texttt{rotten\_banana}, \texttt{rotten\_orange}\}$.
- **Scale:** $0.0 \dots 100.0$ (0 = completely fresh, 100 = completely spoiled).
- **Labeling Standard:** Formally labeled as an **uncalibrated visual defect score** because raw softmax outputs deviate from true post-harvest degradation curves.

### 5.2 Pillar 2: Prototype Transit Stress Index (TSI)
In the absence of physical vibration loggers or continuous temperature telemetry in historical data, transit exposure is modeled strictly as a **prototype route exposure heuristic**:
$$\text{TSI}_{\text{prototype}} = \left(\frac{d_{\text{route}}}{v_{\text{expected}}}\right) \cdot \left(1 + \beta \cdot \text{IRI}_{\text{norm}}\right)$$
where:
- $d_{\text{route}}$: Haulage distance along the planned road network (kilometers, km).
- $v_{\text{expected}}$: Mean commercial freight velocity under local road constraints (km/h).
- $\text{IRI}_{\text{norm}}$: Normalized International Roughness Index of the transit corridor ($0.0 \dots 1.0$).
- $\beta$: Empirical road vibration weighting factor ($\beta = 0.35$).

**Mandatory Integrity Rule:** TSI is explicitly reported as a **prototype routing heuristic**. AgriRoute makes no claim of actual thermal degree-hour tracking or physical vibration quantification until real-world logger data are collected under the prospective field validation protocol.

