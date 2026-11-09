# Authoritative Reviewer Objection & Remediation Gap Matrix (V3)

**Project:** AgriRoute (ICMLDE 5.0, Paper ID: 1345)  
**Lead Scientific Integrity Auditor:** Lead Scientific Integrity Engineer  
**Document ID:** `UPDATED_REVIEWER_GAP_MATRIX_V3.md`  
**Execution Timestamp:** 2026-11-09  
**Git Branch:** `remediation/scientific-audit-repair`  
**Standardized Status Taxonomy:**
- `FULLY ADDRESSED`
- `PARTIALLY ADDRESSED`
- `NOT FULLY ADDRESSED`
- `HONESTLY CONCEDED`

---

## 1. Comprehensive Reviewer Objection Register

| Objection ID | Reviewer | Core Critique / Objection | Scientific Remediation Action Taken | Remediation Status | Supporting Verification Documents |
| :---: | :---: | :--- | :--- | :---: | :--- |
| **R1.1** | R1 | *Abstract needs to clarify the meaning of the fusion score and the decisions made.* | Retired arbitrary exponential fusion formula. Decoupled assessment into Uncalibrated Visual Defect Score (VDS) and Transit Stress Index (TSI). Abstract explicitly defines both metrics and states concrete operational decisions (Direct Market vs Cold Storage vs Manual Packhouse Inspection). | **FULLY ADDRESSED** | [`MODEL_COMPARISON_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/MODEL_COMPARISON_V3.md) |
| **R1.2** | R1 | *Combination of MobileNetV2 with routing and market data is system integration without much novelty.* | Ceased claiming algorithmic novelty for MobileNetV2 or BiLSTM. Repositioned the scientific contribution on: (1) rigorous quantification of base-image-family leakage (+2.89% acc, +4.16% F1 delta), (2) zero-shot out-of-distribution evaluation on two external datasets ($N=5,350$), and (3) uncertainty-aware selective classification. | **FULLY ADDRESSED** | [`MODEL_COMPARISON_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/MODEL_COMPARISON_V3.md), [`LEAKAGE_EFFECT_ANALYSIS.md`](file:///Users/abby/Desktop/spoilage-predictor/LEAKAGE_EFFECT_ANALYSIS.md) |
| **R1.3** | R1 | *BiLSTM validation on artificial sequences leads to an unrealistic AUC of 1.000.* | Conceded that synthetic sequence generation generated artificial deterministic patterns and severe target leakage. The BiLSTM module and AUC=1.000 claim have been formally retracted and quarantined in `archive/legacy_unverified/`. The manuscript presents sensor transit risk strictly as an unvalidated prototype heuristic. | **HONESTLY CONCEDED** | `archive/legacy_unverified/`, [`AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`](file:///Users/abby/Desktop/spoilage-predictor/AUTHORITATIVE_EXPERIMENT_REGISTRY.csv) |
| **R1.4** | R1 | *The lack of a comparison with state-of-the-art post-harvest decision-making systems is apparent.* | Built a verified academic comparison matrix benchmarking AgriRoute against 6 recent peer-reviewed post-harvest architectures (Abayomi-Alli et al., 2024; Chen et al., 2024; Zhang et al., 2024; Abougharib et al., 2023; Liang et al., 2024; Jomy et al., 2026). Removed unverified vendor marketing claims. | **PARTIALLY ADDRESSED** | [`REFERENCE_VERIFICATION_V3.csv`](file:///Users/abby/Desktop/spoilage-predictor/REFERENCE_VERIFICATION_V3.csv), [`REFERENCES.bib`](file:///Users/abby/Desktop/spoilage-predictor/REFERENCES.bib) |
| **R1.5** | R1 | *The conclusion should contain the field data, not the repository-level results.* | Conceded that empirical field observations are currently $N=0$. Removed claims that repository benchmark accuracy proves field loss reduction. Replaced speculative conclusion with an honest appraisal of laboratory benchmark limits and outlined a fully powered prospective field study. | **HONESTLY CONCEDED** | [`FIELD_STUDY_PROTOCOL_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/FIELD_STUDY_PROTOCOL_V3.md) |
| **R2.1** | R2 | *The selection of fusion weights and their novelty need clarification.* | Formally acknowledged that the original weighted exponential formula lacked physiological and statistical backing. The multi-modal components are now presented as an uncoupled bivariate decision matrix rather than a single black-box score. | **FULLY ADDRESSED** | [`MODEL_COMPARISON_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/MODEL_COMPARISON_V3.md) |
| **R2.2** | R2 | *The note "Specific roles can be updated before submission" suggests that the paper is not complete.* | Removed internal author placeholders and editorial notes from the manuscript. Formalized author contributions using the standard CRediT (Contributor Roles Taxonomy) framework. | **FULLY ADDRESSED** | Manuscript change log |
| **R2.3** | R2 | *The freshness model is not tested against the available fruit quality datasets.* | Harmonized and evaluated on two independent open-access datasets: FruitVision ($N=4,157$) and Sultana et al. ($N=1,193$). Reported complete cross-dataset performance, documented acute domain shift degradation (accuracy drops to 67.33% and 68.32%), and implemented selective prediction. | **FULLY ADDRESSED** | [`EXTERNAL_GENERALIZATION_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/EXTERNAL_GENERALIZATION_V3.md), [`PREDICTIONS_FRUITVISION.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_FRUITVISION.csv) |
| **R3.1** | R3 | *There is no research contribution other than application of existing approaches.* | Reframed research novelty away from algorithmic claims. The contribution is established through: (1) forensic proof of data leakage in widely used Kaggle agricultural benchmarks, (2) empirical characterization of OOD performance collapse, and (3) selective prediction abstention safeguarding agricultural supply chains. | **FULLY ADDRESSED** | [`MODEL_COMPARISON_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/MODEL_COMPARISON_V3.md), [`LEAKAGE_EFFECT_ANALYSIS.md`](file:///Users/abby/Desktop/spoilage-predictor/LEAKAGE_EFFECT_ANALYSIS.md) |
| **R3.2** | R3 | *There is only one demonstration shipment and it is not enough to test the system.* | Conceded that a single simulated shipment provides zero statistical power. Conceded this limitation in the manuscript, removing claims of empirical operational validation. | **HONESTLY CONCEDED** | [`FIELD_STUDY_PROTOCOL_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/FIELD_STUDY_PROTOCOL_V3.md) |
| **R3.3** | R3 | *A table comparing AgriRoute's characteristics to those of other agri-logistics platforms is needed.* | Designed a structured academic matrix comparing AgriRoute against published post-harvest systems across 8 dimensions (sensing modality, edge capability, OOD validation, uncertainty quantification, code open-access). Marketing platforms without verifiable peer-reviewed literature are excluded. | **PARTIALLY ADDRESSED** | [`MODEL_COMPARISON_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/MODEL_COMPARISON_V3.md) |
| **R3.4** | R3 | *The conclusion recognizes limited validation, but suggests nothing about the field evaluation plan.* | Authored an exhaustive, methodologically rigorous prospective field validation protocol ($K=40$ shipments, $N=400$ tracked fruit, parallel sacrificial cohort $N=200$ for destructive penetrometer/Brix testing, clustered logistic regression analysis plan) and summarized it in the revised conclusion. | **FULLY ADDRESSED** | [`FIELD_STUDY_PROTOCOL_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/FIELD_STUDY_PROTOCOL_V3.md) |

---

## 2. Integrity Summary of Matrix
- **Fully Addressed:** 7 objections ($58.3\%$)
- **Partially Addressed:** 2 objections ($16.7\%$)
- **Honestly Conceded:** 3 objections ($25.0\%$)
- **Not Fully Addressed:** 0 objections ($0.0\%$)

Zero unverified claims or simulated physical shipments have been represented as completed field evidence.

