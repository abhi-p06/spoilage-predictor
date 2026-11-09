# AgriRoute Research Lab Plugin (`agriroute-research-lab`)

A comprehensive academic research workflow plugin for Google Antigravity, engineered specifically to manage the peer-review revision, empirical auditing, and scientific rigor of the **AgriRoute** post-harvest logistics paper:

> **"AgriRoute: A Vision-Based Post-Harvest Risk System"**

---

## 1. Architectural Overview

```
agriroute-research-lab/
├── plugin.json                    # Plugin manifest (metadata, keywords, prompts)
├── assets/
│   └── logo.svg                   # Plugin vector icon
├── README.md                      # Comprehensive plugin documentation
├── INSTALL.md                     # CLI installation and verification guide
├── rules/
│   └── AGENTS.md                  # 13 permanent scientific integrity & ethics rules
├── agents/                        # 7 Specialized AI Research Agents
│   ├── research-director.md       # Principal investigator & workflow orchestrator
│   ├── literature-reviewer.md     # Scholarly search & SOTA matrix specialist
│   ├── data-integrity-auditor.md  # Leakage, provenance & synthetic artifact auditor
│   ├── computer-vision-researcher.md # Multi-backbone benchmark & Grad-CAM expert
│   ├── statistical-methodologist.md  # Calibration, ECE, CIs & ablation designer
│   ├── manuscript-editor.md       # Paper section rewrites & reviewer rebuttal drafting
│   └── adversarial-reviewer.md    # 3-persona critical peer reviewer simulation
├── skills/                        # 17 Reusable Specialized Skills
│   ├── audit-reviewer-comments/   # Deconstruct reviewer feedback into actionable registry
│   ├── systematic-literature-search/ # Multi-database queries (OpenAlex, Scholar, Scite)
│   ├── research-gap-identification/ # SOTA matrices & authentic novelty bounding
│   ├── citation-verification/     # Crossref / DOI / metadata verification
│   ├── dataset-provenance-audit/  # Checksums, licenses, and raw asset tracing
│   ├── image-leakage-detection/   # pHash & MD5 deduplication across train/test splits
│   ├── reproducible-experiment-design/ # Deterministic seeds, configs, and MLflow logging
│   ├── fruit-classification-benchmark/ # MobileNetV2 vs. EfficientNetB0 vs. ResNet50
│   ├── cross-dataset-validation/  # Out-of-distribution generalization testing
│   ├── calibration-analysis/      # ECE, Brier score, and post-hoc temperature scaling
│   ├── gradcam-analysis/          # Penultimate-layer convolutional attention maps
│   ├── ablation-study/            # Modular feature & fusion weight ablation
│   ├── statistical-reporting/     # 95% bootstrap CIs, McNemar & Wilcoxon tests
│   ├── scientific-figure-generation/ # Elsevier / Procedia-compliant vector figures
│   ├── manuscript-revision/       # Section-by-section academic paper revision
│   ├── response-to-reviewers/     # Point-by-point rebuttal letter with exact line numbers
│   └── publication-readiness-audit/ # Pre-submission sanity checks & ethics disclosures
└── research_memory/               # 9 Persistent Project Records
    ├── reviewer_objections.md     # Atomic reviewer feedback register
    ├── research_questions.md      # Formal research questions (RQ1-RQ4)
    ├── novelty_hypotheses.md      # Delineation of genuine contributions
    ├── dataset_inventory.md       # Checksums, licenses, and sample counts
    ├── experiment_registry.md     # MLflow run tracking manifest
    ├── model_comparison_matrix.md # Backbone benchmarks & literature SOTA table
    ├── claims_evidence_ledger.md  # Source script & output mapping for all paper numbers
    ├── reference_library_index.md # Verified BibTeX citations & DOIs
    └── manuscript_change_log.md   # Chronological paper edit history
```

---

## 2. Research Workflow & Lifecycle

The plugin operates across five interconnected revision phases:

```mermaid
flowchart TD
    subgraph Phase1["Phase 1: Ingestion & Forensic Audit"]
        P1A["Reviewer Feedback"] --> P1B["audit-reviewer-comments"]
        P1B --> P1C["reviewer_objections.md"]
        P1D["Repository & Data"] --> P1E["data-integrity-auditor"]
        P1E --> P1F["dataset_inventory.md & leakage check"]
    end

    subgraph Phase2["Phase 2: Scholarly Benchmarking"]
        P2A["systematic-literature-search"] --> P2B["literature-reviewer"]
        P2B --> P2C["model_comparison_matrix.md"]
        P2C --> P2D["research_questions.md & novelty_hypotheses.md"]
    end

    subgraph Phase3["Phase 3: Empirical Execution"]
        P3A["reproducible-experiment-design"] --> P3B["MLflow Tracking"]
        P3B --> P3C["fruit-classification-benchmark"]
        P3B --> P3D["cross-dataset-validation"]
        P3B --> P3E["calibration-analysis"]
        P3B --> P3F["ablation-study"]
        P3C & P3D & P3E & P3F --> P3G["experiment_registry.md"]
        P3G --> P3H["statistical-reporting (95% CI)"]
    end

    subgraph Phase4["Phase 4: Synthesis & Rebuttal"]
        P3H --> P4A["scientific-figure-generation"]
        P4A --> P4B["manuscript-revision"]
        P4B --> P4C["response-to-reviewers"]
        P4C --> P4D["manuscript_change_log.md"]
    end

    subgraph Phase5["Phase 5: Critical Peer Review & Certification"]
        P4B & P4C --> P5A["adversarial-reviewer (3 Personas)"]
        P5A --> P5B{"Vulnerabilities Found?"}
        P5B -- Yes --> P4B
        P5B -- No --> P5C["publication-readiness-audit"]
        P5C --> P5D["Submission Package Ready"]
    end

    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4
    Phase4 --> Phase5
```

---

## 3. Scientific Integrity Guarantees

All agents and skills are permanently bound by `rules/AGENTS.md`:
1. **Never fabricate a result:** No metric or p-value may be invented.
2. **Never invent a DOI:** Every citation must resolve to an authentic publication.
3. **Never report an unexecuted experiment as complete:** Unfinished runs must be marked `PENDING` or `PLANNED`.
4. **Never change the test set post-evaluation:** The test split remains sealed.
5. **Never claim synthetic data is real-world:** Simulated sensor logs must be explicitly marked `SIMULATED`.
6. **Never equate accuracy with field impact:** Benchmark scores on curated images do not prove supply-chain efficacy.
7. **Never call an uncalibrated score a probability:** Calibration error (ECE) must be reported.
8. **Never overwrite the original submitted paper:** Revisions occur in versioned paths.
9. **Preserve provenance:** Record hashes, licenses, and origins for all datasets.
10. **Maintain reproducible configs:** Random seeds, hardware, and libraries must be logged via MLflow.
11. **Link every number to code:** All quantitative claims must map to `claims_evidence_ledger.md`.

