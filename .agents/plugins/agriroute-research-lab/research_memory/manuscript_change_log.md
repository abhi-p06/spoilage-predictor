# Manuscript Change Log & Versioning Record

This log tracks every substantive modification made to the AgriRoute manuscript throughout the academic revision process.

---

## Change Records

| Version Tag | Date | Target Section | Description of Change | Rationale / Linked Objection | Evidence Reference |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-10-15 | All Sections | Original conference/journal draft submitted. | Baseline submission | Archive `manuscript_v1.0.pdf` |
| `v1.1.0` | 2026-11-08 | Abstract & Intro | Replaced hyperbolic claims ("field-proven commercial savings") with bounded prototype framing ("prototype framework evaluated via laboratory benchmarks and simulated fleet logistics"). | Resolves `REV3-02`, `REV2-01` | `research_memory/reviewer_objections.md` |
| `v1.1.1` | 2026-11-08 | Related Work | Added comprehensive SOTA matrix comparing 5 modern post-harvest systems across modality, telemetry, and routing. | Resolves `REV2-01` | `research_memory/model_comparison_matrix.md` |
| `v1.1.2` | 2026-11-08 | Methodology | Formalized multi-modal risk equation $R_{transit}$; eliminated undefined variables. Added sensitivity parameter formulation $\alpha \in [0, 1]$. | Resolves `REV2-02` | `research_memory/research_questions.md` |
| `v1.1.3` | 2026-11-08 | Results | Added placeholder structure for MobileNetV2, EfficientNetB0, and ResNet50 comparative benchmark with 95% CIs. | Resolves `REV1-02`, `REV1-03` | `research_memory/experiment_registry.md` |
| `v1.1.4` | 2026-11-08 | Discussion | Added Section 6.2 "Threats to Validity & Biological Limitations" discussing surface RGB lag relative to internal enzymatic breakdown. | Resolves `REV2-03` | `research_memory/reviewer_objections.md` |
| `v1.1.5` | 2026-11-08 | Discussion | Disclosed $N=0$ physical fleet trials; outlined formal 4-phase field evaluation protocol for future trials. | Resolves `REV3-02` | `research_memory/novelty_hypotheses.md` |

---

## Archival Safeguard
- The original submitted LaTeX source and compiled PDF remain archived in `archive/manuscript_original/`.
- All revisions occur in `manuscript_revision/` under git version control.

