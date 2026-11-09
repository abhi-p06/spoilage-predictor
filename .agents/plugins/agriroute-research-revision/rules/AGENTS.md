# Research integrity and change-control rules

These rules apply to every task in this project.

- Never fabricate, infer, or alter experimental results, raw observations, shipment records, labels, dates, GPS tracks, sensor measurements, confidence intervals, citations, DOIs, participant counts, or reviewer actions.
- Never describe synthetic or simulated data as field data. Label every synthetic dataset, simulated route, generated sequence, or test fixture explicitly.
- Never claim a model was validated on an external dataset unless the exact data were downloaded under a compatible licence, inspected, evaluated with a reproducible script, and the resulting predictions and metrics are saved.
- Never treat AUC=1.000 on artificial or leaked sequences as evidence of real-world predictive validity. Audit the split, sequence construction, labels, duplication, and target leakage first.
- Preserve raw data, original manuscript files, existing model weights, and prior results. Do not delete or overwrite them. Work in a new revision branch or a clearly named copy.
- Before editing files, produce an audit and a proposed change list. Ask for approval before destructive or broad structural changes.
- Every numeric claim in the manuscript must map to a real source file, a calculation, and a reproducible command/notebook. Keep an evidence ledger with paths, dataset/version, split strategy, metric, and script/notebook that produced the value.
- Every literature claim must map to a retrievable source. Verify title, authors, venue, year, DOI and the specific claim in the source. Never invent a reference or use a search snippet as the sole source for a technical claim.
- Distinguish peer-reviewed research from vendor/platform marketing. Do not claim that a commercial platform has or lacks a feature without a reliable source.
- Use group-aware splits where images/records share fruit batches, shipment, capture session, source, or augmentation lineage. Check near-duplicates and prevent leakage across train/validation/test.
- Report class support, class-wise metrics, uncertainty, and failure cases. Do not report accuracy alone for imbalanced data.
- Do not tune weights, thresholds, or hyperparameters on the test set. Keep a validation set or nested/grouped cross-validation for model selection.
- Keep a change log and run logs. Record package versions, seeds, hardware, data versions, and exact commands.
- Do not paraphrase sources to evade similarity checking. Cite reused ideas, facts, figures, tables, data, and methods. Write original explanations based on the authors' own analysis.
- Use generative AI as an assistant only. Authors must verify and own the scientific claims and follow the venue's current AI disclosure policy.
- If evidence is missing, write `NOT AVAILABLE` or `NOT VERIFIED` and propose a valid way to obtain it. Never fill gaps with plausible-looking numbers.
