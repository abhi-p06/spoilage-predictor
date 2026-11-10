# STAGE 4.1.2 — REVISED COMPREHENSIVE BENCHMARK RESULTS REPORT

**Document Type:** Primary Scientific Benchmark Deliverable  
**Author:** Independent Research Methodologist & Scientific Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** RECONCILED WITH SOURCE-STRATIFIED ANALYSIS & CLAIMS AUDIT  

---

## 1. Executive Summary & Benchmark Image Census

This report establishes the verified, source-stratified empirical results of the frozen Model B V4.1 vision backbone across $N = 13,465$ local benchmark images evaluated under the Stage 4.0.3 external evaluation protocol.

Every numeric value reported in this document is derived by direct calculation from `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` and is fully synchronized with:
1. `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv` (64 rows)
2. `STAGE4_1_1_RECONCILED_CONFIDENCE_INTERVALS.csv` (40 rows)
3. `STAGE4_1_1_RECONCILED_SENSITIVITY_ANALYSIS.csv` (108 rows)

### Table 1: Final Benchmark Image Census and Upstream Provenance

| Partition Code | Partition Designation | Primary Upstream Source | Image Count ($N$) | Evaluation Function |
| :--- | :--- | :--- | :---: | :--- |
| **Partition A** | Primary In-Distribution (ID Test) | Primary Kaggle Archive | 227 | Benchmark closed-set baseline; Primary ID anchor |
| **Partition B** | External Known Shift | FruitVision ($N=4,157$) + Sultana ($N=1,193$) | 5,350 | External domain shift; Secondary ID anchor |
| **Partition C** | Treatment-Labelled Condition Shift | FruitVision (Preserved Knowns) | 1,917 | OOD Condition Shift (Chemical fixative treatment) |
| **Partition D1** | Unseen-Species External Cohort | FruitVision ($N=2,776$) + Sultana ($N=2,000$) | 4,776 | OOD Unseen Species (Natural ambient conditions) |
| **Partition D2** | Combined Shift Unknowns | FruitVision (Preserved Unseen Species) | 1,195 | OOD Combined Shift (Preserved unknown species) |
| **Total Cohort**| **Complete Evaluation Benchmark** | **All Local Partitions** | **13,465** | **Fully Audited Primary Test Suite** |

> [!NOTE]
> **Image Count vs. Specimen Count:** In accordance with rigorous scientific standards, records are designated as **Image Counts**. Image records cannot be assumed to represent statistically independent biological specimens.

**Model Checkpoint Integrity:**
- Checkpoint Path: `MODEL_B_V4_1_CHECKPOINT.keras`
- SHA-256: `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4` (Verified Frozen)
- Reproducibility Suite: 8 of 8 passed (`pytest tests/test_reproducibility_v4_1.py`)

---

## 2. Closed-Set Classification Performance (Partitions A & B)

Closed-set evaluation measures the model's accuracy on known classes (Apple, Banana, Orange $\times$ Fresh, Rotten) under laboratory conditions (Partition A) versus external retail conditions (Partition B).

### Table 2: Closed-Set Performance Comparison

| Metric | Partition A (ID Test, $N=227$) | Partition B (Pooled External, $N=5,350$) | Partition B (FruitVision-Only, $N=4,157$) | Partition B (Sultana-Only, $N=1,193$) |
| :--- | :---: | :---: | :---: | :---: |
| **Top-1 Accuracy** | **96.92%** | **68.36%** | **69.14%** | **65.63%** |
| **Macro-Averaged F1** | **96.87%** [94.11%, 98.81%] | **67.28%** [66.12%, 68.39%] | **66.75%** | **65.77%** |
| **Balanced Accuracy** | **96.43%** | **68.67%** | **69.31%** | **65.55%** |

### Table 3: Reconciled Class-Wise Performance on Partition B ($N = 5,350$)

| Class Name | Ground Truth ($N$) | Correct ($n$) | Class Accuracy (%) | Primary Misclassification Mode |
| :--- | :---: | :---: | :---: | :--- |
| **Fresh Apple** | 965 | 310 | **32.12%** | Rotten Apple ($40.73\%$), Rotten Orange ($26.42\%$) |
| **Rotten Apple** | 830 | 310 | **37.35%** | Rotten Orange ($43.49\%$), Fresh Apple ($18.92\%$) |
| **Fresh Banana** | 948 | 736 | **77.64%** | Rotten Banana ($21.84\%$) |
| **Rotten Banana** | 831 | 826 | **99.40%** | Fresh Banana ($0.36\%$) |
| **Fresh Orange** | 946 | 828 | **87.53%** | Rotten Orange ($9.83\%$), Fresh Apple ($0.95\%$) |
| **Rotten Orange** | 830 | 647 | **77.95%** | Fresh Orange ($12.77\%$), Rotten Apple ($8.43\%$) |
| **Species: Apple** | 1,795 | 620 | **34.54%** | Severe confusion between fresh/rotten and with orange |
| **Species: Banana** | 1,779 | 1,562 | **87.80%** | High fidelity; asymmetric bias toward rotten |
| **Species: Orange** | 1,776 | 1,475 | **83.05%** | Robust recognition; slight decay underestimation |
| **Total Cohort** | **5,350** | **3,657** | **68.36%** | **Overall Domain Degradation: $-28.56$ pp** |

---

## 3. Source-Stratified Open-Set Detection Benchmarks

To eliminate cross-repository confounding between FruitVision and Sultana, we evaluate within-source cohorts:

### 3.1 Cohort A: FruitVision B vs. FruitVision D1 (Within-FV Semantic Shift)
$N_{\text{id}} = 4,157$ (Known: Apple, Banana, Orange) vs. $N_{\text{ood}} = 2,776$ (Unseen: Grape, Mango)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 72.42% | 82.04% | 59.91% | 27.23% | 82.74% | 18.84% | 41.88% | 55.92% |
| **Energy Baseline** | **81.57%** | **88.36%** | **72.19%** | **13.18%** | **68.84%** | **7.64%** | 41.42% | **61.28%** |
| **ODIN Baseline** | 72.30% | 81.58% | 57.46% | 17.94% | 87.43% | 7.20% | 47.27% | 56.32% |
| **Mahalanobis** | 81.41% | 87.65% | 68.83% | 32.67% | 79.00% | 18.62% | 20.01% | 54.35% |
| **OpenMax** | 72.46% | 83.85% | 55.91% | 18.80% | 91.28% | 11.96% | 43.32% | 57.26% |
| **Dual-Gate Cascade** | **80.93%** | **87.98%** | **71.54%** | **16.07%** | **69.27%** | **10.48%** | 41.98% | **61.11%** |

---

### 3.2 Cohort B: FruitVision B vs. FruitVision C (Within-FV Treatment Condition Shift)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,917$ (Treatment-Labelled Knowns)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 58.77% | 78.59% | 36.73% | 50.29% | 92.85% | 37.09% | 41.88% | 47.62% |
| **Energy Baseline** | 53.13% | 71.25% | 33.41% | 53.94% | 94.42% | 44.03% | 41.42% | 43.45% |
| **ODIN Baseline** | 56.73% | 76.89% | 36.60% | 47.84% | 91.13% | 36.83% | 47.27% | 46.35% |
| **Mahalanobis** | 47.91% | 67.53% | 29.60% | 80.70% | 98.07% | 50.50% | 20.01% | 32.67% |
| **OpenMax** | 55.35% | 75.43% | 33.60% | 50.60% | 95.20% | 40.06% | 43.32% | 45.77% |
| **Dual-Gate Cascade** | 53.96% | 72.03% | 33.99% | 52.63% | 94.16% | 42.83% | 41.98% | 44.23% |

---

### 3.3 Cohort C: FruitVision B vs. FruitVision D2 (Within-FV Combined Shift)
$N_{\text{id}} = 4,157$ (Natural Knowns) vs. $N_{\text{ood}} = 1,195$ (Preserved Grape & Mango)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 76.47% | 92.18% | 47.85% | 22.26% | 76.40% | 19.16% | 41.88% | 58.01% |
| **Energy Baseline** | **84.72%** | **95.41%** | **56.71%** | **6.86%** | **64.94%** | **4.94%** | 41.42% | **62.92%** |
| **ODIN Baseline** | 78.11% | 93.17% | 43.32% | 10.46% | 83.85% | 7.28% | 47.27% | 59.69% |
| **Mahalanobis** | 80.08% | 93.82% | 47.10% | 41.26% | 78.49% | 27.70% | 20.01% | 53.42% |
| **OpenMax** | 77.22% | 93.25% | 39.71% | 10.38% | 88.12% | 7.95% | 43.32% | 59.62% |
| **Dual-Gate Cascade** | **84.16%** | **95.18%** | **57.63%** | **9.54%** | **63.18%** | **7.28%** | 41.98% | **62.74%** |

---

### 3.4 Cohort D: Sultana B vs. Sultana D1 (Within-Sultana Semantic Shift)
$N_{\text{id}} = 1,193$ (Known: Apple, Banana, Orange) vs. $N_{\text{ood}} = 2,000$ (Unseen: Grape, Guava, Jujube, Pomegranate, Strawberry)

| Detector | AUROC | AUPR-IN | AUPR-OUT | Operational UFAR ($\tau_{95}$) | Retrospective FPR@95 | UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) | OSCR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MSP Baseline** | 59.77% | 53.25% | 67.96% | 41.10% | 94.30% | 26.80% | 45.85% | 43.11% |
| **Energy Baseline** | **67.52%** | **57.10%** | **76.35%** | **34.15%** | **83.50%** | **21.45%** | 41.74% | **46.62%** |
| **ODIN Baseline** | 60.02% | 52.76% | 67.88% | 28.75% | 94.25% | 15.50% | 54.40% | 42.62% |
| **Mahalanobis** | **68.15%** | **59.17%** | **77.07%** | 65.65% | 81.20% | 37.35% | 16.18% | 42.01% |
| **OpenMax** | 64.38% | 57.23% | 70.56% | 35.50% | 94.75% | 22.30% | 43.76% | 45.59% |
| **Dual-Gate Cascade** | 66.68% | 56.54% | 75.47% | 34.90% | 84.60% | 22.65% | 44.01% | 46.54% |

---

## 4. Dual-Gate Cascade Methodology: Discrete Filter vs. Continuous Proxy

The manuscript must clearly separate the two roles of the Dual-Gate Cascade:

1. **Primary Operational Deployment Gate (Discrete Rule):**
   $$\text{Decision}(x) = \begin{cases} \text{Accept}, & \text{if } S_{\text{Energy}}(x) \ge 0.918451 \land S_{\text{MSP}}(x) \ge 0.582610 \\ \text{Reject}, & \text{otherwise} \end{cases}$$
   Evaluated strictly by fixed-threshold operational metrics:
   - Within-FruitVision Semantic UFAR: **$16.07\%$** (UFAR-Fresh: **$10.48\%$**)
   - Within-Sultana Semantic UFAR: **$34.90\%$** (UFAR-Fresh: **$22.65\%$**)
   - In-Distribution Abstention Rate (KRR): $\approx \mathbf{41.98\%}$ on external retail fruit.
2. **Exploratory Continuous Margin Proxy:**
   $$S_{\text{proxy}}(x) = (S_{\text{Energy}}(x) - 0.918451) + (S_{\text{MSP}}(x) - 0.582610)$$
   Used solely for tracing continuous ROC and PR curves. Because Energy variance ($\sigma \approx 2.15$) is $12\times$ larger than MSP variance ($\sigma \approx 0.18$), this proxy correlates with Energy at Spearman $\rho > 0.992$. It must not be presented as a novel standalone mathematical model.

---

## 5. Retrospective Selective Classification (Coverage-Risk Diagnostic)

Selecting the top-scoring $K\%$ test samples evaluates whether model confidence provides an effective selective ordering:

### Table 4: Retrospective Coverage-Risk on Partition B ($N = 5,350$)

| Target Coverage | MSP Risk | Energy Risk | ODIN Risk | Mahalanobis Risk | OpenMax Risk | Dual-Gate Risk (Proxy) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **10.0%** | **1.31%** | 3.18% | 2.43% | 28.04% | **1.50%** | 2.80% |
| **20.0%** | **4.86%** | 5.33% | 5.33% | 26.82% | **2.80%** | 4.67% |
| **30.0%** | 7.48% | 7.60% | 7.85% | 28.85% | **5.23%** | 6.92% |
| **50.0%** | 13.79% | 12.93% | 14.02% | 32.71% | **12.19%** | 12.37% |
| **70.0%** | 21.79% | 20.45% | 20.88% | 36.05% | **20.21%** | 20.13% |
| **100.0%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** | **31.64%** |

> [!IMPORTANT]
> **Diagnostic vs. Prospective Calibration:** This coverage-risk curve is a **retrospective diagnostic upper bound**. It demonstrates that confidence scores are monotonically well-ordered. In prospective real-world deployment, acceptance must be governed by pre-calibrated validation thresholds ($\tau_{95}^{\text{val}}$).

---

## 6. Supplementary Pooled Comparisons (Reference Benchmarks)

For completeness and historical traceability with Stage 4.1.1, the pooled benchmark metrics are retained:

| Benchmark Pair | Image Count ($N_{\text{id}}, N_{\text{ood}}$) | Energy AUROC | Dual-Gate AUROC | Energy UFAR ($\tau_{95}$) | Dual-Gate UFAR ($\tau_{95}$) | Dual-Gate UFAR-Fresh ($\tau_{95}$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **A vs C** (Primary ID vs Formalin) | 227 vs 1,917 | 84.09% | 85.35% | 53.94% | 52.63% | 42.83% |
| **A vs D1** (Primary ID vs Unseen External) | 227 vs 4,776 | 97.55% | 97.50% | 21.96% | 23.95% | 15.58% |
| **A vs D2** (Primary ID vs Combined) | 227 vs 1,195 | 99.46% | 99.38% | 6.86% | 9.54% | 7.28% |
| **B vs C** (Pooled Known vs Formalin) | 5,350 vs 1,917 | 52.57% | 53.31% | 53.94% | 52.63% | 42.83% |
| **B vs D1** (Pooled Known vs Unseen External)| 5,350 vs 4,776 | 76.04% | 75.43% | 21.96% | 23.95% | 15.58% |
| **B vs D2** (Pooled Known vs Combined) | 5,350 vs 1,195 | 84.97% | 84.23% | 6.86% | 9.54% | 7.28% |

---

*All reported metrics are verified against `STAGE4_1_2_SOURCE_STRATIFIED_METRICS.csv`.*

