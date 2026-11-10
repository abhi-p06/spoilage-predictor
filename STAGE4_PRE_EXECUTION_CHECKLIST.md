# Stage 4.0 Pre-Execution Verification Checklist

**Document ID:** `STAGE4_PRE_EXECUTION_CHECKLIST.md`  
**Role:** Principal Investigator & Lead Methodologist  
**Execution Timestamp:** November 10, 2026  
**Status:** Audit Gate Prior to External Benchmark Execution  

---

## 1. Master Pre-Execution Checklist

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              PRE-EXECUTION AUDIT GATE                                  │
├────┬─────────────────────────────┬──────────────────────────────────┬──────────────────┤
│ ID │ Check Item                  │ Verification Standard            │ Verified Status  │
├────┼─────────────────────────────┼──────────────────────────────────┼──────────────────┤
│ 1  │ Frozen Checkpoint Integrity │ SHA-256 matches 4a12f354...      │ PASSED           │
│ 2  │ Architecture Stability      │ MobileNetV2 + Dropout + Dense    │ PASSED (4 layers)│
│ 3  │ Output Feature Dimension    │ Exactly 1,280 penultimate feats  │ PASSED           │
│ 4  │ Primary Test Set Isolation  │ FINAL_GROUP_TEST_V4_1.csv sealed │ PASSED (Unread)  │
│ 5  │ External Test Isolation     │ 0 external test samples executed │ PASSED (Sealed)  │
│ 6  │ Training Feature NPZ        │ train_features.npz (N=1057)      │ PASSED (3.5 MB)  │
│ 7  │ Validation Feature NPZ      │ validation_features.npz (N=227)  │ PASSED (770 KB)  │
│ 8  │ Validation Scores CSV       │ validation_scores.csv (227 rows) │ PASSED (28 KB)   │
│ 9  │ Mahalanobis Covariance      │ Ledoit-Wolf lambda=0.0978, kappa=526 PASSED (Full Rank)│
│ 10 │ ODIN Gradient Calibration   │ Positive gain (+1.833e-7)        │ PASSED (eps=0.0014)│
│ 11 │ OpenMax Weibull Fitting     │ 6 class Weibull models fitted    │ PASSED (eta=20)  │
│ 12 │ Probability Calibration     │ Scalar temperature T=1.0000      │ PASSED (ECE=6.02%)│
│ 13 │ Threshold Pre-Locking       │ tau_95 and tau_90 locked on Val  │ PASSED (Locked)  │
│ 14 │ Control Experiment Spec     │ Full, Fruit-only, Background-only│ PASSED (Documented)│
│ 15 │ Legal & Licence Compliance  │ FruitVision CC BY-NC-ND in-memory│ PASSED (Audited) │
│ 16 │ Pytest Reproducibility      │ 8/8 tests passing in test suite  │ PASSED (1.19s)   │
└────┴─────────────────────────────┴──────────────────────────────────┴──────────────────┘
```

---

## 2. Unresolved External Dataset Dependencies

While FruitVision and Sultana are fully extracted locally in `data/raw/`:
- **FruitVision Status:** Fully verified locally (`4,157` clean knowns, `1,950` condition shift, `4,019` semantic shift).
- **Sultana Status:** Fully verified locally (`1,193` clean knowns, `2,000` semantic shift).
- **ToxiFruit Status (Zenodo):** The 14.2 GB `Original Dataset.zip` resides on Zenodo (`10.5281/zenodo.21480141`) and is not yet fetched into local storage. 
  *Protocol Decision:* ToxiFruit evaluation will proceed once the raw archive is ingested under single-modality vision rules. Benchmarking on FruitVision and Sultana can proceed immediately without waiting for ToxiFruit.

---
*Audit Gate Certified by Lead Methodologist.*

