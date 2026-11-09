# AgriRoute Scientific Integrity and Research Ethics Rules

These mandatory rules apply to every agent, subagent, and human contributor in this project. They take absolute precedence over any conflicting goal or shortcut.

## 1. Absolute Scientific Honesty
- **Never fabricate a result:** Every number, metric, p-value, confidence interval, and curve must originate from an executed, logged, and reproducible script.
- **Never invent a DOI or reference:** Every citation must resolve to an authentic, retrievable scholarly document with verified authors, title, venue, and year.
- **Never report an unexecuted experiment as complete:** If an experiment is running, planned, or unexecuted, mark it unambiguously as `PLANNED`, `IN-PROGRESS`, or `NOT EXECUTED`.
- **Never create artificial evidence:** Never generate mock traces, fake GPS logs, or fabricated participant statements to satisfy a reviewer comment.

## 2. Experimental & Data Integrity
- **Never claim synthetic data is real-world data:** Clearly and prominently label all simulated sensor sequences, synthetic images, mathematical decay curves, or generated fixtures as `SYNTHETIC` or `SIMULATED`.
- **Never change the external test set after evaluation:** The test partition must remain sealed until final evaluation. Test-set snooping, hyperparameter tuning on test splits, and post-hoc pruning of test samples are strictly prohibited.
- **Preserve dataset provenance:** Document the exact license, acquisition timestamp, raw checksum, preprocessing transformations, and lineage for every image and tabular row.
- **Enforce group-aware splits:** Never split images or time-series randomly if they share underlying fruit lots, collection batches, harvest dates, background environments, or video capture sequences. Near-duplicate leakage between train, validation, and test must be audited and prevented.

## 3. Methodological and Metric Rigor
- **Never equate model accuracy with field impact:** High benchmark accuracy on curated photos does not prove operational efficacy in agricultural supply chains. Distinguish classification metrics from field loss reduction.
- **Never call an uncalibrated score a probability:** Raw sigmoid or softmax logits are confidence scores, not true probabilities. If claiming a value is a calibrated spoilage probability, report the calibration method (Platt scaling, Isotonic regression) and calibration error (Brier Score, Expected Calibration Error).
- **Never silently change research methodology:** Every shift in loss function, feature set, architecture, or evaluation protocol must be recorded in the project change log with an explicit rationale.
- **Link every numerical claim to its source:** Every quantitative assertion in the manuscript, tables, and reviewer responses must cite its exact output file, cell ID, and reproducing command in the Claims and Evidence Ledger.

## 4. Preservation of Historical Records
- **Never overwrite the original submitted paper:** Preserve all historical manuscript versions, raw data archives, and legacy model checkpoints. Work exclusively in new revision branches or versioned document paths.
- **Maintain reproducible experiment configurations:** Every training run must log its random seed, hardware environment, package versions, hyperparameter manifest, and data hash via MLflow or versioned run logs.

