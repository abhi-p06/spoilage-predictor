# STAGE 4.1.2.1.1 — FINAL CONFIDENCE INTERVAL AND CLAIMS RECONCILIATION LOG

**Document Type:** Formal Audit & Verification Change Log  
**Author:** Project Research Team  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** COMPLETE — CANONICAL STATISTICAL DELIVERABLES SEALED  

---

## 1. Overview of Stage 4.1.2.1.1 Corrections

This final reconciliation stage audited and synchronized all confidence intervals, ledger entries, and terminological specifications against the canonical file [`STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv). 

Zero model retraining, zero inference re-execution, and zero threshold modifications were performed. All underlying prediction records (`STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`) remain completely immutable.

---

## 2. Itemized Verification and Rectifications

### 2.1 Canonical Confidence Interval Reconciliation
All confidence interval bounds across the main report ([`STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md)) and claims ledger ([`STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv)) were updated to strictly match the canonical CSV:

- **Partition A:**
  - Top-1 Accuracy ($96.92\%$): **$[94.71\%, 98.68\%]$**
  - Macro-F1 ($96.87\%$): **$[94.65\%, 99.05\%]$**
  - Balanced Accuracy ($97.09\%$): **$[94.80\%, 98.98\%]$**
- **Partition B Pooled:**
  - Top-1 Accuracy ($68.36\%$): **$[67.20\%, 69.40\%]$**
  - Macro-F1 ($67.28\%$): **$[66.21\%, 68.32\%]$**
  - Balanced Accuracy ($68.66\%$): **$[67.55\%, 69.69\%]$**
- **FruitVision B:**
  - Top-1 Accuracy ($69.14\%$): **$[68.13\%, 70.17\%]$**
  - Macro-F1 ($66.75\%$): **$[65.62\%, 68.01\%]$**
  - Balanced Accuracy ($69.56\%$): **$[68.52\%, 70.58\%]$**
- **Sultana B:**
  - Top-1 Accuracy ($65.63\%$): **$[63.03\%, 68.15\%]$**
  - Macro-F1 ($65.77\%$): **$[63.32\%, 68.13\%]$**
  - Balanced Accuracy ($65.55\%$): **$[63.11\%, 67.99\%]$**

### 2.2 Representation of All Four Source-Matched Cohorts
Table 4 of the results report was expanded to include **Cohort C (Within-FruitVision Combined Shift: FruitVision B vs. FruitVision D2)**:
- Energy AUROC: **$84.72\%$** $[83.85\%, 85.58\%]$
- Dual-Gate AUROC (Proxy): **$84.16\%$** $[83.28\%, 85.05\%]$
- Energy Operational UFAR ($\tau_{95}$): **$6.86\%$** $[5.52\%, 8.28\%]$
- Dual-Gate Operational UFAR ($\tau_{95}$): **$9.54\%$** $[7.86\%, 11.30\%]$
- Dual-Gate Operational UFAR-Fresh ($\tau_{95}$): **$7.28\%$** $[5.94\%, 8.70\%]$
- Dual-Gate Operational KRR ($\tau_{95}$): **$41.98\%$** $[40.89\%, 43.20\%]$

### 2.3 Claims Ledger Adjustments
- Reconciled confidence intervals for CLM-002, CLM-003, CLM-005, CLM-006, CLM-007, CLM-008, CLM-011, CLM-012, CLM-013, and CLM-014.
- **Reclassified CLM-015:** Status changed from `VERIFIED` to:
  $$\text{HYPOTHESIS — NOT CAUSALLY VERIFIED}$$
- **Formal Claims Accounting:** The claims ledger and audit documents now accurately document:
  $$\mathbf{15\text{ verified quantitative claims and } 1\text{ qualitative observational hypothesis}}$$

### 2.4 Terminology Calibration
- Replaced unqualified statements claiming to eliminate macro-confounding with calibrated observational text:
  > *"reduces cross-repository confounding while leaving potential within-repository capture variation."*
- Maintained all existing observational guardrails regarding chemical fixative conditions and non-optical sensor integration.

---

## 3. Cryptographic Verification of Project Deliverables

To prevent circular self-referential checksum dependencies, individual byte sizes and SHA-256 cryptographic hashes are not embedded within this document. 

All definitive on-disk byte counts and SHA-256 checksums for the finalized Stage 4.1.2.1.1 deliverables and associated benchmark evidence files are recorded in the companion hash manifest:
- [`STAGE4_1_2_1_1_FILE_HASHES.txt`](file:///Users/abby/Desktop/spoilage-predictor/STAGE4_1_2_1_1_FILE_HASHES.txt)

This companion manifest provides the authoritative cryptographic verification registry across all reconciled reports, canonical confidence interval tables, pHash sensitivity tables, image predictions, locked thresholds, and the frozen model checkpoint.

---

## 4. Final Verdict

### **FINAL VERDICT: CONDITIONAL GO**

The AgriRoute empirical evidence, confidence intervals, failure counts, and claims register are fully reconciled and mathematically synchronized. This constitutes a **conditional go-ahead for manuscript drafting and internal research review**. 

*Operational Scope Boundary:* This verdict authorizes internal manuscript completion and revision preparation; it does not imply peer-reviewed journal endorsement, publication acceptance by Elsevier's *Procedia Computer Science*, or operational readiness for commercial field deployment in agricultural supply chains without non-optical multimodal sensor integration.
