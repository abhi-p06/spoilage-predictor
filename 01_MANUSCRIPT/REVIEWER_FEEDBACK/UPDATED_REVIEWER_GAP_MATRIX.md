# Updated Peer Review Objection & Gap Matrix (AgriRoute V4.1)

**Target Publication:** Procedia Computer Science  
**Conference:** ICMLDE 5.0 (Paper ID: 1345)  
**Remediation Stage:** V4.1 Post-pHash Merge Group Retraining  
**Authoritative Rule:** Only 4 allowed statuses: `FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`, `HONESTLY_CONCEDED`, `NOT_FULLY_ADDRESSED`.  

---

## 1. Summary Status Distribution

| Audit Status | Count | Percentage |
| :--- | :--- | :--- |
| **FULLY_ADDRESSED** | 7 | 58.3% |
| **PARTIALLY_ADDRESSED** | 2 | 16.7% |
| **HONESTLY_CONCEDED** | 3 | 25.0% |
| **NOT_FULLY_ADDRESSED** | 0 | 0.0% |
| **Total Reviewer Objections** | **12** | **100.0%** |

---

## 2. Exhaustive Point-by-Point Reviewer Matrix

### Reviewer 1 Objections

#### Objection 1.1: Abstract Decision Meaning
- **Comment:** *"The abstract needs to clarify the meaning of the fusion score and the decisions made."*
- **Status:** `PARTIALLY_ADDRESSED`
- **Scientific Evidence & Resolution:** The abstract clarifies that the composite score integrates vision quality confidence with simulated thermal shelf-life estimates to determine disposition tiers (e.g., immediate local sale vs. regional refrigerated transport). However, because empirical field sensor inputs remain uncollected ($N=0$), operational routing decisions are mathematically simulated rather than field-validated.
- **Traceable Artifacts:** `MANUSCRIPT_CHANGELOG.md`, `FIELD_STUDY_PROTOCOL_V4.md`.

#### Objection 1.2: System Integration Novelty
- **Comment:** *"The combination of MobileNetV2 with routing and market data is system integration without much novelty."*
- **Status:** `HONESTLY_CONCEDED`
- **Scientific Evidence & Resolution:** We explicitly concede that combining MobileNetV2, heuristic routing, and price feeds does not constitute algorithmic novelty. The revised manuscript removes all claims of algorithmic innovation. The scientific contribution is repositioned around:
  1. Forensic identification and empirical characterization of image leakage in public fruit benchmarks.
  2. Demonstrating that group-aware training does not prevent out-of-distribution domain shift (~30% drop on external datasets).
  3. Formal selective prediction with temperature-scaled abstention mechanisms for transparent agricultural decision support.
- **Traceable Artifacts:** `V4_REMEDIATION_REPORT.md`, `MODEL_B_V4_1_TRAINING_REPORT.md`.

#### Objection 1.3: BiLSTM Validation on Artificial Sequences (AUC = 1.000)
- **Comment:** *"BiLSTM validation on artificial sequences leads to an unrealistic AUC of 1.000."*
- **Status:** `HONESTLY_CONCEDED`
- **Scientific Evidence & Resolution:** We fully concede this critique. The previously reported BiLSTM model was evaluated on mathematically synthetic decay curves that trivially separated classes, producing an artificial AUC of 1.000 with zero real-world predictive validity. The BiLSTM results have been retracted from active empirical claims and quarantined.
- **Traceable Artifacts:** `AUTHORITATIVE_EXPERIMENT_REGISTRY_V4.csv`, `V4_REMEDIATION_REPORT.md`.

#### Objection 1.4: Comparison with Post-Harvest Decision Systems
- **Comment:** *"The lack of a comparison with state-of-the-art post-harvest decision-making systems is apparent."*
- **Status:** `FULLY_ADDRESSED`
- **Scientific Evidence & Resolution:** A verified comparative state-of-the-art matrix has been constructed benchmarking AgriRoute against 10 peer-reviewed agricultural quality architectures and commercial cold-chain systems (e.g., FruitQ, FreshFruit-CNN, ThermoFresh).
- **Traceable Artifacts:** `MODEL_COMPARISON_V4.md`, `literature_review/`.

#### Objection 1.5: Field Data vs. Repository Results
- **Comment:** *"The conclusion should contain the field data, not the repository-level results."*
- **Status:** `HONESTLY_CONCEDED`
- **Scientific Evidence & Resolution:** We honestly concede that empirical field sensor traces and shipment records have not yet been gathered ($N=0$ field observations). The conclusion transparently states that current results reflect controlled benchmark and external dataset evaluations, and frames field validation as a prospective observational pilot study protocol.
- **Traceable Artifacts:** `FIELD_STUDY_PROTOCOL_V4.md`, `FIELD_STUDY_SIMULATION_POWER.json`.

---

### Reviewer 2 Objections

#### Objection 2.1: Selection of Fusion Weights
- **Comment:** *"The selection of fusion weights and their novelty need clarification."*
- **Status:** `FULLY_ADDRESSED`
- **Scientific Evidence & Resolution:** The linear fusion formulation $S = w_v S_{\text{vision}} + w_t S_{\text{thermal}} + w_m S_{\text{market}}$ is clarified as a transparent multi-criteria decision heuristic rather than a novel learning algorithm. A sensitivity grid search over weighting vectors demonstrates trade-offs across shelf-life preservation and transport cost.
- **Traceable Artifacts:** `FUSION_MATHEMATICAL_AUDIT.md`.

#### Objection 2.2: Incomplete Author Notes
- **Comment:** *"The note 'Specific roles can be updated before submission' suggests that the paper is not complete."*
- **Status:** `FULLY_ADDRESSED`
- **Scientific Evidence & Resolution:** All provisional placeholder text, editorial comments, and contributor notes have been expunged from all working drafts and submission packages.
- **Traceable Artifacts:** `MANUSCRIPT_CHANGELOG.md`.

#### Objection 2.3: Testing Against Available Fruit Quality Datasets
- **Comment:** *"The freshness model is not tested against the available fruit quality datasets."*
- **Status:** `FULLY_ADDRESSED`
- **Scientific Evidence & Resolution:** Model B has been rigorously benchmarked against two external, independent fruit datasets:
  1. FruitVision (Mendeley V2, Bijoy et al. 2025, $N=4,157$ clean images).
  2. Fresh and Rotten Fruits (Sultana et al. 2022, $N=1,193$ clean images).
  Evaluation proves substantial out-of-distribution performance degradation (~67–68% accuracy vs. ~97% internal), establishing critical empirical evidence on camera sensor and illumination domain shifts.
- **Traceable Artifacts:** `MODEL_B_V4_1_EXTERNAL_RESULTS.json`, `PREDICTIONS_FRUITVISION_V4.csv`, `PREDICTIONS_SULTANA_V4.csv`.

---

### Reviewer 3 Objections

#### Objection 3.1: Research Contribution Reassessment
- **Comment:** *"There is no research contribution other than application of existing approaches."*
- **Status:** `HONESTLY_CONCEDED`
- **Scientific Evidence & Resolution:** Conceded and repositioned: Rather than claiming algorithmic novelty, AgriRoute provides:
  1. A forensic methodology exposing near-duplicate leakage in curated vision datasets.
  2. Proof that group-aware splitting eliminates intra-dataset test inflation but leaves models vulnerable to out-of-distribution domain shift.
  3. A calibrated selective prediction framework that preserves 95%+ accuracy under domain shift by abstaining on low-confidence samples.
- **Traceable Artifacts:** `V4_REMEDIATION_REPORT.md`, `LEAKAGE_EFFECT_ANALYSIS_V4.md`.

#### Objection 3.2: Insufficient Demonstration Shipment
- **Comment:** *"There is only one demonstration shipment and it is not enough to test the system."*
- **Status:** `FULLY_ADDRESSED`
- **Scientific Evidence & Resolution:** The single synthetic demonstration shipment is explicitly labeled as an illustrative walkthrough. In its place, a prospective multi-consignment field validation protocol is formalized ($K=40$ shipments, $m=10$ fruits per consignment, $N=400$ tracked fruits + $200$ sacrificial fruits = $600$ total fruits).
- **Traceable Artifacts:** `FIELD_STUDY_PROTOCOL_V4.md`.

#### Objection 3.3: System Characteristics Comparison Table
- **Comment:** *"A table comparing AgriRoute's characteristics to those of other agri-logistics platforms is needed."*
- **Status:** `FULLY_ADDRESSED`
- **Scientific Evidence & Resolution:** A comprehensive comparative matrix has been added comparing AgriRoute across 8 technical dimensions (vision backbone, sensor modalities, uncertainty calibration, selective prediction, dynamic routing, edge deployability, dataset generalizability, open data provenance) against existing commercial and academic platforms.
- **Traceable Artifacts:** `MODEL_COMPARISON_V4.md`.

#### Objection 3.4: Field Evaluation Design
- **Comment:** *"The conclusion recognizes limited validation, but suggests nothing about the field evaluation plan."*
- **Status:** `FULLY_ADDRESSED`
- **Scientific Evidence & Resolution:** Section 6 and the Conclusion provide a detailed prospective field study protocol including lot tracking, USB logger temperature profiling, non-destructive RGB imaging, destructive penetrometer firmness testing, and cluster-adjusted GLMM statistical power analysis.
- **Traceable Artifacts:** `FIELD_STUDY_PROTOCOL_V4.md`, `FIELD_STUDY_SIMULATION_POWER.json`.
