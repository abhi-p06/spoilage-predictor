# AgriRoute Research Revision — Antigravity Plugin

This workspace plugin adds evidence-first academic revision workflows for the AgriRoute manuscript. It is designed to help respond to the supplied reviewer reports while protecting research integrity.

## Important limits

- This plugin does not guarantee acceptance.
- It does not create or invent field observations, dataset labels, model metrics, citations, DOI values, baselines, shipment records, or reviewer responses.
- It starts with a read-only audit. Do not let an agent overwrite the original manuscript, raw data, or trained model artefacts. Work on a versioned copy and preserve reproducible outputs.
- The included workflows are instructions, not a substitute for the authors checking the underlying data, scientific interpretation, publisher requirements, and final submission.

## Install in the project workspace

1. Extract this folder into the root of the AgriRoute project.
2. The final location should be `<project-root>/.agents/plugins/agriroute-research-revision/`.
3. Restart or reload the Antigravity workspace if the plugin does not appear immediately.
4. Open the agent panel's Customizations area and confirm the plugin's skills and agents are loaded.
5. Start with `/audit-project-evidence`. Do not begin rewriting before reading its findings.

Optional CLI validation (if `agy` is installed and signed in):

```bash
agy plugin validate --strict .agents/plugins/agriroute-research-revision
```

## Skills

- `/audit-project-evidence` — inventory manuscript, code, datasets, checkpoints, results and evidence; read-only.
- `/design-validation-study` — build a defensible evaluation plan, including external fruit-quality datasets and field evaluation.
- `/literature-matrix` — construct a verified literature and platform-comparison matrix with real DOI/source checks.
- `/reviewer-response` — prepare a point-by-point response only after changes are actually implemented and verified.
- `/paper-readiness` — check scientific consistency, formatting, citations, figures, disclosures and submission files.

Two read-only specialist agents are included: `agriroute-methods-auditor` and `agriroute-systems-reviewer`.

## Suggested Antigravity MCP servers

Install only what you will use, through Antigravity's MCP Store:

- **Exa** — external source discovery and page retrieval. Treat results as leads; verify papers at the publisher or DOI record.
- **GitHub** — useful if this project is version-controlled on GitHub. Do not make the repo public just to use it.
- **Sequential Thinking** — optional structured planning for the revision.
- **Context7** — current documentation for PyTorch, torchvision, scikit-learn, pandas, and related code libraries. It is a developer-documentation tool, not a scholarly evidence database.

For references, use Zotero as the reference manager. An optional third-party Zotero MCP server that documents Antigravity compatibility is listed here: https://github.com/Jayaram-Nambiar/zotero-mcp . Review its code and permissions before installing it; do not put Zotero API keys in a public repository. You can also query OpenAlex and Crossref directly for bibliographic metadata, then verify every citation against the publisher/DOI page.

## Project-specific review priorities

1. Treat the reported BiLSTM AUC of 1.000 on artificial sequences as a validity issue. Do not present it as evidence of real-world predictive performance. Remove it from the main results unless it can be retrained and independently tested on genuine, correctly split shipment time-series data.
2. Test the freshness model on genuinely external, suitable fruit-quality data. AgriFreshNET and FruitVision are candidate datasets, not guaranteed matches. Inspect their label schemas, overlap in fruit categories, image provenance, licence, and any duplicate/augmented-image leakage before selecting them.
3. Demonstrate a research contribution beyond combining MobileNetV2, routing, and market inputs. The candidate direction to investigate is a clearly defined, reproducible post-harvest risk-aware routing/decision objective that uses calibrated freshness uncertainty and measured transport exposure. This is only a hypothesis until the related work and experiments support it.
4. Define what the fusion score means, how it is normalized, how weights are learned or justified, and how thresholds map to actual decisions. Do not call an arbitrary score a probability.
5. Report real field evidence separately from simulations and repository tests. If multi-shipment field evidence is unavailable, state that limit and frame the work as a prototype/feasibility evaluation rather than implying deployment validation.
