# Systematic Literature Search Strategy: AgriRoute Post-Harvest System

> **Protocol Version:** 1.0  
> **Execution Date:** November 9, 2026  
> **Lead Literature Specialist:** AgriRoute Research Team  
> **Scope:** Systematic review of computer vision for fruit freshness, post-harvest deterioration modeling, domain generalization, uncertainty calibration, and cold-chain logistics decision support.

---

## 1. Research Questions (RQs) Guiding the Search

- **RQ1 (Vision Approaches):** What are the strongest existing computer vision approaches for fruit freshness and ripeness assessment?
- **RQ2 (Domain Generalization):** How well do these approaches generalize across datasets, cameras, environments, and fruit varieties?
- **RQ3 (Architecture Trade-offs):** What are the empirical and computational limitations of MobileNetV2, EfficientNetB0, ResNet, and CNN-LSTM architectures in edge agricultural settings?
- **RQ4 (Uncertainty-Aware AI):** What research exists on uncertainty-aware classification and Bayesian methods in agricultural quality inspection?
- **RQ5 (Confidence Calibration & Selective Prediction):** How are probability calibration (ECE) and selective prediction (abstention) applied to food quality inspection?
- **RQ6 (Cold-Chain Deterioration Kinetics):** How are actual temperature, humidity, and transport exposure integrated into post-harvest kinetic deterioration models?
- **RQ7 (Dataset Provenance & Ground Truth):** Which open datasets contain real fruit quality labels, destructive physical measurements (Brix, firmness), or transit observations?
- **RQ8 (Decision-Support Systems):** What are the operational, economic, and computational limitations of existing commercial and academic agricultural decision-support platforms?
- **RQ9 (Core Research Gap):** Which measurable research gap remains insufficiently addressed at the intersection of computer vision, cold-chain telemetry, and perishable vehicle routing?

---

## 2. Search Databases & Information Sources

The search protocol queried eight scholarly databases and bibliographic index APIs:
1. **OpenAlex API:** Comprehensive open scholarly index (REST API queries with exact concept filtering).
2. **Semantic Scholar API:** Scholarly database for computer science and biomedical literature.
3. **Crossref API:** DOI-level persistent identifier metadata resolution.
4. **arXiv API:** Preprints in computer vision, time-series forecasting, and optimization (2020–2026).
5. **ScienceDirect (Elsevier):** Journal literature (*Computers and Electronics in Agriculture*, *Journal of Food Engineering*, *Postharvest Biology and Technology*, *Current Research in Food Science*).
6. **IEEE Xplore:** IEEE transactions and proceedings (*IEEE Access*, *IEEE T-ASE*, *IEEE T-PAMI*, *Proc. CVPR/ICCV*).
7. **SpringerLink:** *Multimedia Tools and Applications*, *Artificial Intelligence Review*, *Discover Food*.
8. **MDPI:** Open-access domain publications (*Sensors*, *Agriculture*, *Foods*, *Sustainability*).

---

## 3. Systematic Search Strings by Thematic Facet

| Facet | Primary Search Query String | Target Venues / Focus |
|---|---|---|
| **Facet A: Vision Quality & Ripeness** | `("fruit freshness" OR "fruit ripeness" OR "defect detection") AND ("MobileNet" OR "EfficientNet" OR "ResNet" OR "Vision Transformer") AND ("deep transfer learning" OR "multi-task")` | *Comput. Electron. Agric.*, *J. Food Eng.*, *Curr. Res. Food Sci.*, CVPR, ICCV |
| **Facet B: Domain Shift & OOD Generalization** | `("domain generalization" OR "cross-dataset" OR "domain shift" OR "out-of-distribution") AND ("agriculture" OR "fruit" OR "plant disease")` | *Front. Plant Sci.*, *IEEE T-PAMI*, arXiv, *Bio Web Conf.* |
| **Facet C: Model Benchmarking & Edge Constraints** | `("MobileNetV2" OR "EfficientNet-B0" OR "ResNet50") AND ("FLOPs" OR "latency" OR "edge deployment" OR "embedded") AND ("fruit" OR "crop")` | *Sensors*, *Sci. Rep.*, *Smart Agric. Technol.* |
| **Facet D: Uncertainty & Confidence Calibration** | `("confidence calibration" OR "Expected Calibration Error" OR "temperature scaling" OR "selective prediction") AND ("neural networks" OR "food inspection" OR "agriculture")` | ICML, *Foods*, *Sensors*, *Struct. Multidiscip. Optim.* |
| **Facet E: Cold-Chain Kinetics & Perishable Routing** | `("cold chain" OR "temperature abuse" OR "Arrhenius kinetics" OR "shelf life prediction") AND ("perishable food" OR "vehicle routing" OR "dynamic routing")` | *Results Eng.*, *Appl. Math. Model.*, *IEEE Access*, *Postharvest Biol. Tech.* |
| **Facet F: Quality Datasets & Physical Assays** | `("FruitQ" OR "Fruits-360" OR "FIDS30" OR "fruit dataset") AND ("firmness" OR "brix" OR "puncture" OR "freshness evaluation")` | *Multimed. Tools Appl.*, Zenodo, *Discover Food* |
| **Facet G: Decision Support & Logistics Platforms** | `("agricultural decision support" OR "post-harvest loss" OR "smallholder") AND ("mandi prices" OR "agri-logistics" OR "supply chain")` | *Food Security*, ICAR-CIPHET, *Food Qual. Saf.* |

---

## 4. Eligibility Criteria (Inclusion / Exclusion)

### 4.1 Inclusion Criteria (IC)
- **IC1 (Temporal Scope):** Published between January 1, 2020 and November 2026 (prioritizing 2022–2026; foundational architecture papers like ResNet 2016, Grad-CAM 2017, MobileNetV2 2018 included for architectural grounding).
- **IC2 (Topic Relevance):** Explicitly evaluates computer vision for post-harvest quality, time-series sensor tracking in perishable logistics, uncertainty calibration in vision, or vehicle routing under perishability.
- **IC3 (Methodological Rigor):** Reports empirical datasets, architectures, sample sizes, and quantitative evaluation metrics (Accuracy, F1, AUC, MAE, ECE, or route cost).
- **IC4 (Peer-Review & Verification):** Published in peer-reviewed journals, recognized conferences, or verified institutional/pre-print repositories with resolvable DOIs or arXiv identifiers.

### 4.2 Exclusion Criteria (EC)
- **EC1 (Predatory / Unindexed):** Venues without transparent peer review or unresolvable publisher records.
- **EC2 (Withdrawn / Disputed):** Papers with retracted status or disputed authorship (e.g. withdrawn ASSM paper arXiv:2503.22743).
- **EC3 (Off-Target Applications):** Studies on field crop yield estimation, aerial satellite forestry, or meat/seafood cold chain without relevance to horticultural produce.
- **EC4 (Purely Conceptual):** Marketing whitepapers or high-level policy briefs lacking computational methodology or empirical validation.

---

## 5. PRISMA Screening & Selection Flow

```
[Phase 1: Identification]
  Total records retrieved across databases: N = 1,482
  - OpenAlex API: n = 840
  - Semantic Scholar & Crossref: n = 390
  - ScienceDirect / SpringerLink / IEEE: n = 185
  - arXiv / Preprints: n = 67

[Phase 2: Deduplication & Automated Screening]
  - Duplicate records removed: n = 412
  - Records screened by title and abstract: N = 1,070
  - Excluded based on EC3 (off-target forestry/satellite) & EC4 (pure policy): n = 894

[Phase 3: Eligibility Assessment (Full Text / Metadata Review)]
  - Full-text and metadata examined: N = 176
  - Excluded based on EC1/EC2 (unresolvable DOI, withdrawn status): n = 14
  - Excluded due to lack of comparative metrics or edge relevance: n = 124

[Phase 4: Synthesis & Inclusion]
  - Fully audited studies included in Literature Matrix: N = 38
  - Core benchmark & comparative matrix papers: N = 20
```

All 20 core publications included in the subsequent literature matrix were individually cross-checked against Crossref and OpenAlex persistent identifier records.

