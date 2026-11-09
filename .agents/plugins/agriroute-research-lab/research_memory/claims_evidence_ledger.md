# Claims and Evidence Ledger

Every quantitative assertion, performance metric, mathematical equation, and citation in the revised AgriRoute manuscript must be registered in this ledger. Any claim lacking an empirical output file or verified script must be marked `NOT VERIFIED`.

---

| Claim ID | Manuscript Location | Asserted Claim / Number | Source Type | Underlying Script / Command | Logged Output / Cell Reference | Verification Status |
|---|---|---|---|---|---|---|
| `CLM-01` | Abstract & Results | MobileNetV2 achieves $94.2 \pm 0.6\%$ accuracy on test partition | Experiment | `scripts/train_vision.py --backbone mobilenet_v2` | `mlruns/1/.../metrics/test_acc` | PENDING EXECUTION |
| `CLM-02` | Abstract & Results | EfficientNetB0 achieves $95.6 \pm 0.5\%$ accuracy | Experiment | `scripts/train_vision.py --backbone efficientnet_b0` | `mlruns/1/.../metrics/test_acc` | PENDING EXECUTION |
| `CLM-03` | Abstract & Results | Cross-dataset OOD test shows $\approx 14.8\%$ degradation | Experiment | `scripts/evaluate_ood.py` | `outputs/ood_metrics.json` | PENDING EXECUTION |
| `CLM-04` | Methodology | Fusion risk formula $R = \alpha R_{vision} + (1-\alpha) R_{sensor}$ | Mathematical Def. | `app/routing.py` | Line 45-52 | VERIFIED CODE |
| `CLM-05` | Results | Sensitivity curve shows cost minimum at $\alpha = 0.55 \pm 0.05$ | Experiment | `scripts/ablation_sensitivity.py` | `outputs/ablation_curve.csv` | PENDING EXECUTION |
| `CLM-06` | Results | Post-hoc temperature scaling reduces ECE from 0.078 to 0.021 | Experiment | `scripts/calibrate_probabilities.py` | `outputs/calibration_results.json` | PENDING EXECUTION |
| `CLM-07` | Intro & Scope | Prototype evaluation status ($N=0$ commercial fleet runs) | Author Statement | `manuscript.tex` | Section 1 & Section 6 | TRANSPARENTLY SCOPED |
| `CLM-08` | Sequence Model | BiLSTM sequence prediction on simulated cold chain | Experiment | `scripts/train_bilstm.py` | Replaces leaked AUC=1.000 script | UNDER REVISION |

---

## Verification Rules
1. No unverified claim may enter the final revision draft.
2. If an experiment cannot be run prior to submission deadline, the text must state `NOT EVALUATED` or describe the protocol under `Future Work`.
3. Disclose all simulation parameters explicitly.

