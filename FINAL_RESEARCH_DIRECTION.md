# Strategic Research Direction & PI Recommendation

**Role:** Principal Investigator & Academic Research Director  
**Target Venue:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0)  
**Publication:** *Procedia Computer Science* (Elsevier)  
**Date:** November 10, 2026  
**Status:** Executive Strategic Recommendation

---

## 1. Synthesis of the Strategic Audit

Over the past four remediation iterations (V1 to V4.1), AgriRoute has evolved through an intense forensic cycle:
1. We uncovered and eliminated critical target leakage and near-duplicate image splits in the public fruit benchmarks.
2. We proved that group-aware training restores internal split integrity (96.92% accuracy, 0.9687 Macro-F1), but exposes acute vulnerability to external domain shifts (~30% performance drop on FruitVision and Sultana).
3. We retracted unverified BiLSTM models ($\text{AUC} = 1.000$ on synthetic decay curves) and eliminated uncalibrated probability claims.

However, the central vulnerability identified by Reviewers 1, 2, and 3 remains: **What is the original research contribution of this paper, and why should it be published as an academic paper rather than dismissed as a trivial application of off-the-shelf software?**

The proposed new research question:
> *"Can a risk-aware open-set fruit quality classifier recognize known fresh/rotten fruit conditions while rejecting unfamiliar or potentially unsafe fruit conditions under cross-dataset shift?"*

directly attacks the root cause of the previous rejections.

---

## 2. Evaluation of Strategic Options

We evaluate three potential strategic paths:

### Option A: Retain the Original "AgriRoute Logistics & Vehicle Routing" Premise
- **Concept:** Keep the narrative of an end-to-end refrigerated truck re-routing system using MobileNetV2 + simulated decay + heuristic routing.
- **Feasibility:** High (code already exists).
- **Academic Viability:** **FATAL (Certain Rejection).**
- **Rationale:** Reviewers 1.5 and 3.2 demanded real empirical field data ($N > 0$ refrigerated trucks, physical sensor traces, real highway transit records). We have zero real trucks. Attempting to disguise simulated routing as "field validation" will guarantee an immediate second rejection for scientific misrepresentation.

### Option B: Pursue the Proposed "Open-Set Risk-Aware Screening" Direction Unmodified
- **Concept:** Train on Kaggle fresh/rotten fruits; test open-set rejection on FruitVision/ToxiFruit formalin-mixed fruits; claim detection of chemical adulteration via a dual-gate architecture.
- **Feasibility:** High (datasets and code structures are accessible).
- **Academic Viability:** **HIGH RISK (Chemical Reviewer Trap).**
- **Rationale:** If the manuscript claims or implies that RGB cameras perform *chemical verification of formalin*, reviewers with food-science or optical spectroscopy backgrounds will reject the paper with prejudice. Formaldehyde is transparent and colorless; RGB cameras cannot detect chemical bonds.

### Option C: The Modified, Hardened Scientific Pivot (RECOMMENDED)
- **Concept:** Reposition the paper as **"Risk-Aware Open-Set Fruit Quality Screening: Rejecting Unseen Cultivars and Adulterated Batches Under Cross-Dataset Shift"**.
- **The Core Scientific Framing:**
  1. We frame the task as **Intake Quality Screening & Cost-Sensitive Anomaly Rejection** in post-harvest packing sheds and cold storage hubs.
  2. We explicitly disclaim optical chemical spectroscopy: we demonstrate that chemical immersion produces *morphological, desiccation, and reflective surface deviations* that can be detected as statistical Out-of-Distribution anomalies.
  3. We formalize the **Asymmetric Food-Safety Cost Matrix**, proving that cascading an energy-based OOD filter with calibrated selective prediction bounds consumer hazard risk to near-zero while maintaining high operational throughput on benign produce.
  4. We benchmark 5 established SOTA baselines (MSP, ODIN, Energy, Mahalanobis, OpenMax) across 3 external independent datasets ($N > 20,000$ images).
- **Academic Viability:** **EXCEPTIONAL (High Probability of Acceptance).**
- **Rationale:** Fully resolves R1 novelty, R1 SOTA baselines, R1 external evaluation, R2 fusion methodology, and R3 contribution. It eliminates the truck field-data trap entirely.

---

## 3. The Brutally Honest PI Recommendation

```
================================================================================
                    BRUTALLY HONEST PI RECOMMENDATION
================================================================================

WE SHOULD PURSUE THIS DIRECTION WITH THE MANDATORY MODIFICATIONS SPECIFIED IN OPTION C.

DO NOT ABANDON THIS WORK.
DO NOT ATTEMPT TO RESCUE THE REFRIGERATED TRUCK DISPATCH NARRATIVE.

1. ABANDON THE TRUCK ROUTING APPLICATION NARRATIVE:
   We do not have real trucks, real highway GPS logs, or real transit telematics.
   Continuing to sell this as a "fleet routing platform" will kill the paper on
   Reviewer 1.5's desk.

2. EMBRACE INTAKE PACKHOUSE OPEN-SET SCREENING:
   Pivoting to risk-aware open-set recognition on multi-source fruit benchmarks
   is a legitimate, publishable, and highly relevant pattern-recognition contribution
   for Procedia Computer Science / ICMLDE 5.0.

3. REMOVE ALL PSEUDOSCIENTIFIC CHEMICAL CLAIMS:
   Never claim RGB vision "detects formalin." Frame it strictly as detecting
   unseen physical anomalies and preservative-induced morphological deviations
   as Out-of-Distribution conditions.

4. BENCHMARK THE 5 SOTA OSR/OOD BASELINES:
   By benchmarking MSP, ODIN, Energy, Mahalanobis, and OpenMax across FruitVision,
   ToxiFruit, and Sultana, the paper transitions from a weak application paper
   into a rigorous, authoritative benchmark study.

================================================================================
```

---

## 4. Execution Roadmap for ICMLDE 5.0 / Procedia Computer Science

```
PHASE 1: BENCHMARK SUITE IMPLEMENTATION (Zero training modification)
├── Reuse frozen Model B V4.1 backbone weights (MODEL_B_V4_1_CHECKPOINT.keras)
├── Implement baseline score extractors:
│   ├── scripts/benchmark_msp_ood.py
│   ├── scripts/benchmark_odin_ood.py
│   ├── scripts/benchmark_energy_ood.py
│   ├── scripts/benchmark_mahalanobis_ood.py
│   ├── scripts/benchmark_openmax_ood.py
│   └── scripts/benchmark_dualgate_selective.py
└── Compute unified metrics table across:
    ├── Kaggle Primary Test (In-Distribution Knowns, N=227)
    ├── FruitVision Knowns (Covariate Shift, N=4,185)
    ├── Sultana Knowns (Covariate Shift, N=1,200)
    ├── FruitVision Formalin (Condition OOD, N=1,950)
    ├── ToxiFruit Formalin (Condition OOD, N=2,700)
    └── FruitVision & Sultana Unseen Species (Semantic OOD, N=6,019)

PHASE 2: MANUSCRIPT RESTRUCTURING (Target: Procedia Computer Science)
├── Retitle: "Risk-Aware Open-Set Fruit Quality Screening: Rejecting Unseen Cultivars 
│             and Adulterated Batches Under Cross-Dataset Shift"
├── Rewrite Abstract & Introduction: Focus on open-set vulnerability and food safety.
├── Section 3: Asymmetric Food-Safety Loss Matrix & Dual-Gate Theory.
├── Section 4: Multi-Source Experimental Setup & Leakage-Safe Splits.
├── Section 5: Comparative Evaluation & OSCR / Coverage-Risk Curves.
└── Section 6: Discussion on Optical Limits of Non-Destructive Screening.

PHASE 3: SUBMISSION READINESS & ARTIFACT COMPLIANCE
├── Verify 100% DOI resolution in References (using verified LITERATURE_COMPARISON.csv).
├── Run reproducibility test suite verifying table concordance.
└── Build final sealed archive for camera-ready submission.
```

