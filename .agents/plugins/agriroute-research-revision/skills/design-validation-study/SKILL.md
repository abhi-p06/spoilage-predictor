---
name: design-validation-study
description: Design and implement a reproducible, leakage-safe evaluation of AgriRoute's freshness model, fusion method and route decisions using real datasets and clearly labelled field observations or simulations.
---

# Objective

Turn the reviewers' validation criticisms into an honest experimental plan. Do not create synthetic data to stand in for field data, and do not report results until scripts have actually run on identified data.

# Stage 1 — data audit

1. Inspect all project datasets and label files. Report exact counts by fruit and quality class, source, licence, capture conditions, and any missing/corrupt files.
2. For candidate external datasets, verify the original landing page, DOI, licence, label definitions, image provenance, and download integrity before use.
3. Candidate sources to investigate (not assumed suitable):
   - AgriFreshNET Freshness and Shelf-Life Image Dataset, Mendeley Data DOI `10.17632/42m5tb7yv9.1`.
   - FruitVision: A benchmark dataset for fresh, rotten, and formalin-mixed fruit detection, Data in Brief (2025), DOI `10.1016/j.dib.2025.111752`.
4. Compare label definitions before mapping classes. Do not silently merge `Semi-Fresh`, `Formalin-mixed`, or fruit types that do not match AgriRoute's target task. Explain exclusions.
5. Detect exact and near-duplicate images. If a dataset includes augmented copies, group each original image with all of its transforms so they cannot cross splits.

# Stage 2 — model evaluation

1. Define the exact target: freshness class, quality class, remaining shelf life, or a decision proxy. Do not change targets mid-analysis.
2. Use a source-aware/grouped split. Group by original sample, batch, seller/farm, capture session, shipment, or dataset source when metadata permits. Keep an external dataset untouched until the final cross-dataset evaluation.
3. Establish simple reproducible baselines before tuning: a majority/class-frequency baseline; a conventional image baseline where appropriate; MobileNetV2; and one stronger compact CNN such as EfficientNet-B0 or ResNet50 if resources allow. Use the same split and comparable preprocessing.
4. Report macro-F1, balanced accuracy, per-class precision/recall/F1, confusion matrix, class support, and one-vs-rest ROC-AUC only where mathematically defined and class support permits. For calibrated probabilities, add Brier score and a reliability/calibration plot. If shelf-life regression is supported by reliable labels, report MAE and RMSE separately.
5. Give uncertainty estimates using repeated grouped splits or group bootstrap where feasible. Never imply that a single split establishes generalization.
6. Evaluate the model on the external dataset only for genuinely overlapping classes and compatible labels. State dataset shift and domain limitations. Do not combine in-domain and external test results into one headline score.

# Stage 3 — BiLSTM decision

- If the current BiLSTM is trained on artificial sequences, do not present its AUC as a real-world result.
- Preferred: remove it from the primary claimed system unless enough genuine temporally ordered shipment observations exist to train and test it with shipment-level separation.
- If retained for software simulation, clearly label it as a simulated proof-of-concept, report no field-performance claim, and segregate its outputs from measured results.
- If actual sequence data exist, define the time step, sensors/features, target horizon, missingness handling, leakage-safe temporal split, and naive baselines (persistence/mean or simple tree model) before using a BiLSTM.

# Stage 4 — fusion and routing experiments

1. Write down the exact fusion formula and units. State whether the output is a calibrated probability, a normalized risk index, or a decision score. Never call a weighted score a probability without calibration evidence.
2. Normalize each component using training/validation data only. Document missing-data handling and the direction of each component.
3. Justify weights using a stated, reproducible procedure: learn them on training/validation data against an observed outcome or decision objective; or, if only elicited by experts, state that they are expert-derived and not empirically learned. Do not invent an optimization result.
4. Freeze weights and decision thresholds before final test evaluation. Report sensitivity to plausible weight and threshold changes.
5. Use ablations: vision only; routing/transport only; market only; each pair; full model. Report the incremental effect of each modality.
6. Compare routes against at least: shortest-distance route, shortest-time route, and a suitable existing heuristic/baseline. State objective, constraints, time assumptions, and data source. Use repeated scenario tests only as simulation, clearly labelled.

# Stage 5 — field evaluation

1. Search for existing genuine shipment logs first. Do not claim a field trial based on a repository demo.
2. If new field observations can be collected with appropriate permission, create a protocol before data collection: shipment ID, commodity and batch, timestamps, origin/destination, measured temperature/humidity if available, route/time, image capture protocol, quality outcome at receiving, and missingness.
3. Report the actual count of independent shipments and the level at which each metric is calculated. Repeated images from one shipment are not independent shipments.
4. If the four-day revision window prevents a defensible multi-shipment study, report the limitation transparently, strengthen external dataset validation and simulation robustness, and give a concrete prospective field-evaluation plan. Never manufacture multiple shipments.

# Deliverables

Save a proposed protocol and analysis plan first. Only run experiments after data suitability and author approval are established. Keep code, environment, seeds, logs, predictions, and metrics together so every reported value is reproducible.
