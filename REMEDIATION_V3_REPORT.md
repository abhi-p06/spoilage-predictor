# Master Scientific Remediation and Evidence Reconciliation Report (V3)

**Project Title:** AgriRoute: A Vision-Based Post-Harvest Risk System  
**Conference:** ICMLDE 5.0 (International Conference on Machine Learning and Data Engineering)  
**Paper ID:** 1345  
**Target Publication Venue:** Procedia Computer Science (Elsevier)  
**Role:** Lead Scientific Integrity Engineer  
**Document ID:** `REMEDIATION_V3_REPORT.md`  
**Execution Timestamp:** 2026-11-09  
**Active Git Branch:** `remediation/scientific-audit-repair`  
**Remediation Status:** **SCIENTIFIC AUDIT REPAIR COMPLETED — EVIDENCE RECONCILED**  
**Core Directive Enforced:** **MANUSCRIPT NOT REWRITTEN; EVIDENCE GROUNDED EXCLUSIVELY IN REPRODUCIBLE CODE**

---

## 1. Executive Summary

Following a comprehensive inspection of the `AGRIRoute_CHATGPT_VERIFICATION` package by an independent external auditor, critical methodological, statistical, bibliographic, and documentation inconsistencies were detected across the project artifacts. 

Acting as the Lead Scientific Integrity Engineer, we executed a complete, 11-phase scientific remediation. No results were fabricated or inferred; all historical and legacy files have been strictly preserved; obsolete claims were quarantined; and all reported figures, tables, and metrics have been regenerated directly from executed scripts, frozen model checkpoints, and verified publisher metadata.

### Summary of Key Remediation Achievements:
1. **Quarantine of Obsolete Artifacts:** Quarantined 5 legacy files (`EXPERIMENT_REGISTRY_legacy.csv`, `MODEL_COMPARISON_legacy.md`, `REPRODUCIBILITY_GUIDE_legacy.md`, `05_Existing_Systems_Comparison_legacy.md`, `scripts_run_all_experiments_legacy.py`) in `archive/legacy_unverified/` and disclaimed legacy scripts.
2. **Authoritative Experiment Registry:** Established [`AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`](file:///Users/abby/Desktop/spoilage-predictor/AUTHORITATIVE_EXPERIMENT_REGISTRY.csv) containing 11 verified experimental configurations spanning internal benchmarks, external generalization, calibration, and selective prediction.
3. **Forensic Grouping & pHash Audit:** Developed [`scripts/build_group_manifests.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/build_group_manifests.py), proving that all 13,599 non-nested Kaggle images map to 1,511 base screenshot families ($100\%$ integrity across 9 affine variants). Audited 8 cross-group perceptual hash (pHash) collisions (Hamming distance $\le 2$) and rendered side-by-side visual proof sheets in [`PHASH_COLLISION_CONTACT_SHEET/`](file:///Users/abby/Desktop/spoilage-predictor/PHASH_COLLISION_CONTACT_SHEET/), revealing 3 residual near-duplicate pairs crossing test and train partitions (temporal gaps: 6s, 44s, 33s). Mandated the term *"Filename-derived base-image-family overlap"*.
4. **Controlled Intra-Partition Leakage Quantification:** Formally resolved the invalid cross-partition accuracy comparison by analyzing Model A predictions on the deduplicated historical test set ($N=2,045$). Test images from seen base families ($N=1,499$, 73.3%) achieved **95.20% accuracy** and **95.00% macro F1**, whereas test images from unseen base families ($N=546$, 26.7%) achieved **92.31% accuracy** and **90.84% macro F1**, demonstrating a within-test leakage inflation of **$+2.89\%$ accuracy** and **$+4.16\%$ macro F1**, with severe degradation on unseen citrus specimens (fresh orange F1 dropped by $-17.7\%$). Computed 95% cluster-bootstrap confidence intervals and documented statistical limitations.
5. **Cryptographic Prediction Traceability:** Generated five authoritative prediction CSVs ([`PREDICTIONS_RANDOM.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_RANDOM.csv), [`PREDICTIONS_GROUP_TEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_GROUP_TEST.csv), [`PREDICTIONS_GROUP_TEST_RAW_ONLY.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_GROUP_TEST_RAW_ONLY.csv), [`PREDICTIONS_FRUITVISION.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_FRUITVISION.csv), [`PREDICTIONS_SULTANA.csv`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTIONS_SULTANA.csv)) and an enhanced [`PREDICTIONS_TRACEABLE.npz`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/PREDICTIONS_TRACEABLE.npz) linking all 11,610 prediction rows to exact sample IDs, relative filepaths, base group IDs, and MD5 hashes.
6. **Mathematical Reformulation:** Formally retired the unvalidated exponential decay fusion equation. Formulated an uncoupled two-pillar decision architecture: an **Uncalibrated Visual Defect Score ($\text{VDS}_{\text{uncal}}$)** based on aggregate rotten probability mass, and a **Prototype Transit Stress Index ($\text{TSI}_{\text{proto}}$)** based on transit distance, velocity, and road roughness, explicitly excluding unmeasured thermal degree-hours and unmeasured vibration.
7. **Statistically Reconciled Field Protocol:** Reconciled sample size contradictions to an authoritative cluster-randomized design: $K=40$ shipments, $m=10$ tracked specimens per shipment ($N=400$ total, $\text{VIF}=2.08$, $N_{\text{eff}}=192$, power $>85\%$). Resolved the physical impossibility of destructive testing on tracked fruit by instituting a parallel **sacrificial baseline cohort ($N=200$)** for digital penetrometer firmness and refractometer Brix analysis. Excluded unsupported crops (mangoes), labeled the study as an **Unregistered Prospective Protocol**, and affirmed ground truth empirical field observations as **$N=0$**.
8. **Bibliographic Crossref Verification:** Queried the Crossref REST API for target DOIs, identifying and correcting severe errors in `REFERENCES.bib` (including correcting the fake author "Sharafat Ali et al." to true authors Arwa Abougharib, Mahmoud Awad, and Malick Ndiaye; correcting volume 108 for Liang et al.; and correcting pages 535–552 for Jomy et al.). Created [`REFERENCE_VERIFICATION_V3.csv`](file:///Users/abby/Desktop/spoilage-predictor/REFERENCE_VERIFICATION_V3.csv).
9. **Reviewer Objection Matrix:** Re-evaluated all 12 peer review objections in [`UPDATED_REVIEWER_GAP_MATRIX_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/UPDATED_REVIEWER_GAP_MATRIX_V3.md) using only the 4 authorized statuses: 7 Fully Addressed ($58.3\%$), 2 Partially Addressed ($16.7\%$), 3 Honestly Conceded ($25.0\%$), and 0 Not Fully Addressed.
10. **Reproducibility & Automated Testing:** Authored [`REPRODUCIBILITY_GUIDE_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/REPRODUCIBILITY_GUIDE_V3.md) with portable relative paths and corrected training terminology ("initialized with ImageNet-1k pretrained weights and fine-tuned"). Implemented [`tests/test_reproducibility.py`](file:///Users/abby/Desktop/spoilage-predictor/tests/test_reproducibility.py) with 7 automated pytest validation tests passing cleanly ($100\%$ pass rate).

---

## 2. Authoritative Experimental Evidence Matrix

The table below presents the reconciled, authoritative empirical evidence for AgriRoute. Every value is backed by an automated assertion in `tests/test_reproducibility.py`.

| ID | Experiment / Evaluation Tier | Backbone & Pretraining | Dataset & Partition | Sample Count ($N$) | Accuracy | Macro F1 | ECE (Uncal $\to$ Cal) | Operational / Scientific Verdict |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **EXP-A** | Historical Random Benchmark | MobileNetV2 (ImageNet FT) | Kaggle Fresh/Rotten (`test_internal.csv`) | 4,090 | 94.43% | 94.08% | 10.73% $\to$ 1.81% | Contaminated baseline (77.8% base-family leakage) |
| ↳ | *Seen Base Families in Train* | MobileNetV2 (ImageNet FT) | Within-Test Leaked Subset | 1,499 | **95.20%** | **95.00%** | — | Performance inflated by duplicate screenshot views |
| ↳ | *Unseen Base Families in Train* | MobileNetV2 (ImageNet FT) | Within-Test Clean Subset | 546 | **92.31%** | **90.84%** | — | True generalization on unseen screenshot captures |
| **EXP-B** | **Group-Aware Primary Standard** | MobileNetV2 (ImageNet FT) | **Kaggle Unaugmented Base Screenshots** | **227** | **97.36%** | **97.31%** | — | **Authoritative primary evaluation on unaugmented captures** |
| ↳ | Group-Aware Family Standard | MobileNetV2 (ImageNet FT) | Kaggle All Transformed Variants (`group_test.csv`) | 2,043 | 97.55% | 97.52% | 4.63% $\to$ **2.14%** | Secondary family evaluation (9 variants per group) |
| **EXP-C1** | External Zero-Shot Generalization | Model A (Historical) | FruitVision V2 (`fruitvision_clean.csv`) | 4,157 | 69.43% | 66.35% | — | Acute OOD degradation under retail market conditions |
| ↳ | External Zero-Shot Generalization | Model B (Group-Aware) | FruitVision V2 (`fruitvision_clean.csv`) | 4,157 | 67.33% | 64.33% | — | Acute OOD degradation ($-30.22\%$ drop from internal test) |
| **EXP-C2** | External Zero-Shot Generalization | Model A (Historical) | Sultana et al. (`sultana_clean.csv`) | 1,193 | 62.20% | 62.89% | — | Acute OOD degradation under wet market conditions |
| ↳ | External Zero-Shot Generalization | Model B (Group-Aware) | Sultana et al. (`sultana_clean.csv`) | 1,193 | 68.32% | 68.16% | — | Model B gains $+6.12\%$ over Model A, but drops $-29.2\%$ |
| **EXP-D** | Temperature Scaling Calibration | Model B (Group-Aware) | Group Test Partition ($T^* = 0.6740$) | 2,043 | 97.55% | 97.52% | **4.63% $\to$ 2.14%** | Reliable calibration; NLL reduced $0.316 \to 0.299$ |
| **EXP-E** | Selective Classification ($\tau = 0.90$) | Model B (Group-Aware) | FruitVision External Benchmark | 4,157 | **95.69%** | — | — | **Coverage = 25.11%** (1,044 accepted); **74.89% abstained** |
| ↳ | Selective Classification ($\tau = 0.90$) | Model B (Group-Aware) | Sultana External Benchmark | 1,193 | **82.04%** | — | — | **Coverage = 23.81%** (284 accepted); **76.19% abstained** |

---

## 3. Detailed Audit of Phase Deliverables

### Phase 1: Quarantine of Stale Documents
- Moved legacy reports containing retracted formulas, unexecuted baseline claims, and erroneous sample counts into `archive/legacy_unverified/`.
- Inserted mandatory warning banners at the head of `scripts/run_all_experiments.py` preventing unverified script execution.

### Phase 2: Authoritative Experiment Registry
- Authored [`AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`](file:///Users/abby/Desktop/spoilage-predictor/AUTHORITATIVE_EXPERIMENT_REGISTRY.csv) containing 11 verified rows.
- Established primary evaluation standard on the 227 raw base screenshots ($97.36\%$ accuracy) to prevent variant inflation.

### Phase 3: Group Manifests & pHash Collision Review
- Script [`scripts/build_group_manifests.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/build_group_manifests.py) verified 1,511 groups across 13,599 files.
- Saved [`BASE_IMAGE_GROUP_AUDIT.csv`](file:///Users/abby/Desktop/spoilage-predictor/BASE_IMAGE_GROUP_AUDIT.csv) and [`GROUP_SPLIT_MANIFEST.csv`](file:///Users/abby/Desktop/spoilage-predictor/GROUP_SPLIT_MANIFEST.csv).
- Computed 64-bit perceptual hashes for all 1,511 raw screenshots; discovered 8 collision pairs with Hamming distance $\le 2$.
- Authored [`GROUP_PHASH_COLLISION_REVIEW.csv`](file:///Users/abby/Desktop/spoilage-predictor/GROUP_PHASH_COLLISION_REVIEW.csv) and generated visual proof sheets in [`PHASH_COLLISION_CONTACT_SHEET/`](file:///Users/abby/Desktop/spoilage-predictor/PHASH_COLLISION_CONTACT_SHEET/).
- Audited the 3 cross-partition pairs (Collisions 6, 7, 8: temporal gaps 6s, 44s, 33s) and adopted the standardized term *"Filename-derived base-image-family overlap"*.

### Phase 4: Proper Leakage Quantification
- Script [`scripts/analyze_leakage_effect.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/analyze_leakage_effect.py) evaluated Model A on deduplicated historical test samples ($N=2,045$).
- Authored [`LEAKAGE_EFFECT_ANALYSIS.md`](file:///Users/abby/Desktop/spoilage-predictor/LEAKAGE_EFFECT_ANALYSIS.md), reporting $+2.89\%$ accuracy delta, $+4.16\%$ macro F1 delta, class vulnerabilities, cluster-bootstrap 95% CIs, and statistical limitations.

### Phase 5: Cryptographic Prediction Traceability
- Script [`scripts/generate_traceable_predictions.py`](file:///Users/abby/Desktop/spoilage-predictor/scripts/generate_traceable_predictions.py) produced 5 prediction CSVs conforming to the 19-column schema with sample IDs, relative paths, and MD5 hashes.
- Authored [`PREDICTION_TRACEABILITY_AUDIT.md`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTION_TRACEABILITY_AUDIT.md) and created [`PREDICTIONS_TRACEABLE.npz`](file:///Users/abby/Desktop/spoilage-predictor/experiments/group_leakage_study/PREDICTIONS_TRACEABLE.npz).

### Phase 6: Methodology & Formula Reformulation
- Authored [`MODEL_COMPARISON_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/MODEL_COMPARISON_V3.md).
- Retired the scalar decay equation $S(t) = S_0 e^{-\lambda t}$.
- Defined Uncalibrated Visual Defect Score as $\text{VDS}_{\text{uncal}} = 100 \times \sum_{k \in \text{rotten}} P(y=k \mid x)$.
- Defined Transit Stress Index as a prototype routing heuristic $\text{TSI}_{\text{proto}} = (d_{\text{route}} / v_{\text{avg}})(1 + \beta \cdot \text{Roughness})$ without claiming unmeasured sensor degree-hours.

### Phase 7: Field Study Protocol Repair
- Authored [`FIELD_STUDY_PROTOCOL_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/FIELD_STUDY_PROTOCOL_V3.md).
- Reconciled sample size: $K=40$ shipments, $m=10$ tracked specimens per shipment ($N=400$ total), clustered logistic regression model, $\rho = 0.12$, $\text{VIF} = 2.08$, $N_{\text{eff}} = 192$, power $>85\%$.
- Instituted separate parallel sacrificial cohort ($m_{\text{sac}} = 5$ per shipment, $N=200$) for destructive penetrometer firmness and Brix refractometer testing.
- Restricted initial pilot to apples, bananas, and oranges; excluded mangoes. Declared study as Unregistered Prospective Protocol with $N=0$ field observations.

### Phase 8: Reference Verification
- Queried Crossref API for target DOIs and corrected bibliographic metadata in `REFERENCES.bib`.
- Authored [`REFERENCE_VERIFICATION_V3.csv`](file:///Users/abby/Desktop/spoilage-predictor/REFERENCE_VERIFICATION_V3.csv).

### Phase 9: Reviewer Status Matrix
- Authored [`UPDATED_REVIEWER_GAP_MATRIX_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/UPDATED_REVIEWER_GAP_MATRIX_V3.md) classifying all 12 objections using only the 4 authorized statuses.

### Phase 10: Reproducibility & Automated Testing
- Authored [`REPRODUCIBILITY_GUIDE_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/REPRODUCIBILITY_GUIDE_V3.md) with portable paths and corrected training terminology.
- Implemented [`tests/test_reproducibility.py`](file:///Users/abby/Desktop/spoilage-predictor/tests/test_reproducibility.py) with 7 automated tests passing in 1.16 seconds.

---

## 4. Master Remediation Artifact Inventory (12 Required Documents)

All 12 required remediation documents are fully authored, cross-linked, and validated in the workspace root:

1. [`REMEDIATION_V3_REPORT.md`](file:///Users/abby/Desktop/spoilage-predictor/REMEDIATION_V3_REPORT.md) (This master synthesis report)
2. [`AUTHORITATIVE_EXPERIMENT_REGISTRY.csv`](file:///Users/abby/Desktop/spoilage-predictor/AUTHORITATIVE_EXPERIMENT_REGISTRY.csv) (Authoritative registry of 11 verified experiments)
3. [`MODEL_COMPARISON_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/MODEL_COMPARISON_V3.md) (Authoritative model architecture, metrics, and formula definitions)
4. [`EXTERNAL_GENERALIZATION_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/EXTERNAL_GENERALIZATION_V3.md) (Out-of-distribution evaluation on FruitVision and Sultana)
5. [`CALIBRATION_AUDIT_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/CALIBRATION_AUDIT_V3.md) (Temperature scaling audit, optimizer resolution, and bin census)
6. [`LEAKAGE_EFFECT_ANALYSIS.md`](file:///Users/abby/Desktop/spoilage-predictor/LEAKAGE_EFFECT_ANALYSIS.md) (Intra-test seen vs unseen leakage analysis and cluster bootstrap)
7. [`GROUP_MANIFEST_REPRODUCIBILITY.md`](file:///Users/abby/Desktop/spoilage-predictor/GROUP_MANIFEST_REPRODUCIBILITY.md) (Base-image family grouping, prefix parsing, and pHash collisions)
8. [`PREDICTION_TRACEABILITY_AUDIT.md`](file:///Users/abby/Desktop/spoilage-predictor/PREDICTION_TRACEABILITY_AUDIT.md) (Traceability audit, column schemas, and sample ID alignment)
9. [`REFERENCE_VERIFICATION_V3.csv`](file:///Users/abby/Desktop/spoilage-predictor/REFERENCE_VERIFICATION_V3.csv) (Crossref-verified bibliographic metadata and corrections)
10. [`FIELD_STUDY_PROTOCOL_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/FIELD_STUDY_PROTOCOL_V3.md) (Reconciled prospective field validation protocol, $N=0$)
11. [`UPDATED_REVIEWER_GAP_MATRIX_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/UPDATED_REVIEWER_GAP_MATRIX_V3.md) (Updated 12 reviewer objection statuses)
12. [`REPRODUCIBILITY_GUIDE_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/REPRODUCIBILITY_GUIDE_V3.md) (Portable replication guide and execution instructions)

---

## 5. Unresolved Scientific Problems & Required Empirical Evidence

In accordance with strict scientific integrity mandates, we conclude this remediation by explicitly identifying the outstanding scientific blockers that cannot be resolved computationally and specifying the exact empirical evidence required to resolve each:

### Blocker 1: Empirical Field Data Census Remains at $N = 0$
- **Problem:** Reviewers 1, 2, and 3 unanimously criticized the absence of real-world operational evidence. While our prospective field protocol ([`FIELD_STUDY_PROTOCOL_V3.md`](file:///Users/abby/Desktop/spoilage-predictor/FIELD_STUDY_PROTOCOL_V3.md)) is statistically rigorous, no actual physical shipment data have yet been gathered.
- **Required Evidence to Resolve:** Physical execution of the $K=40$ shipment field trial ($N=400$ tracked fruits, $N=200$ sacrificial fruits) across commercial haulage routes in Maharashtra and Gujarat, recording actual Sensirion temperature/humidity logger time series and blinded arrival quality grades.

### Blocker 2: Severe Out-of-Distribution Performance Drop Under Domain Shift
- **Problem:** Zero-shot deployment of both Model A and Model B to external benchmarks (FruitVision and Sultana) results in an acute performance collapse from $>97\%$ to $\approx 67\% - 68\%$ accuracy. Although selective prediction at $\tau=0.90$ restores accuracy to $95.69\%$ on accepted samples, the system must abstain on $74.89\%$ of consignments.
- **Required Evidence to Resolve:** Training and evaluating domain adaptation algorithms (e.g., test-time adaptation, unsupervised domain adaptation, or packhouse-specific few-shot fine-tuning) on multi-source horticultural corpora to raise coverage above $70\%$ while maintaining accepted error rates $<5\%$.

### Blocker 3: Residual Temporal Correlation in Web-Scraped Benchmarks
- **Problem:** Our perceptual hash collision audit proved that even after grouping all affine transformation variants by base filename, residual near-duplicate video frames exist across splits (3 pairs crossing test and train with time gaps of 6s, 44s, and 33s). Filename parsing cannot eliminate correlation when the original benchmark creator captured rapid sequential frames.
- **Required Evidence to Resolve:** Depositing and evaluating on a genuinely prospective, open-access agricultural vision benchmark where physical fruit specimens are tracked longitudinally with individual specimen IDs, harvest dates, and orchard origins from blossom to post-harvest decay.

### Blocker 4: Unvalidated Multi-Modal Dynamic Routing Heuristics
- **Problem:** The Transit Stress Index ($\text{TSI}_{\text{proto}}$) and bivariate risk matrix remain prototype heuristics. No empirical data currently validate whether re-routing vehicles based on road roughness and visual defect scores reduces financial loss or physical food waste.
- **Required Evidence to Resolve:** A prospective, multi-vehicle split-fleet logistics trial where 20 consignments are routed using AgriRoute dynamic risk scores and 20 control consignments follow standard commercial routes, comparing arrival spoilage rates and realized market revenues.

