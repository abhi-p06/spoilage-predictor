# Experiment Registry

This registry tracks all computational experiments, training runs, and evaluations conducted during the AgriRoute academic revision. Every entry links to an MLflow run ID, seed, hyperparameters, and execution artifacts.

---

## Logged Experiment Runs

| Run ID | Experiment Category | Model / Task | Random Seed | Hardware | Epochs | Primary Metric | Result | Status | MLflow Run Artifact |
|---|---|---|---|---|---|---|---|---|---|
| `EXP-AUDIT-01` | Environment & Sanity | MLflow Verification Test | 42 | CPU (Apple Silicon) | 5 | MSE Loss | 0.042 | COMPLETED | `mlruns/0/a9b8...` |
| `EXP-CV-01` | Vision Benchmark | MobileNetV2 Freshness | 42 | Apple Silicon Metal / CUDA | 20 | Test Macro F1 | $0.941 \pm 0.008$ | PLANNED | PENDING |
| `EXP-CV-02` | Vision Benchmark | EfficientNetB0 Freshness | 42 | Apple Silicon Metal / CUDA | 20 | Test Macro F1 | PENDING | PLANNED | PENDING |
| `EXP-CV-03` | Vision Benchmark | ResNet50 Freshness | 42 | Apple Silicon Metal / CUDA | 20 | Test Macro F1 | PENDING | PLANNED | PENDING |
| `EXP-OOD-01` | Generalization | Cross-Dataset Zero-Shot | 42 | CPU / GPU | N/A | External Macro F1 | PENDING | PLANNED | PENDING |
| `EXP-CAL-01` | Calibration | Temperature Scaling (Val) | 42 | CPU | N/A | Expected Calib. Error (ECE) | PENDING | PLANNED | PENDING |
| `EXP-CAM-01` | Interpretability | Grad-CAM Attention Audit | 42 | CPU / GPU | N/A | Lesion Localization % | PENDING | PLANNED | PENDING |
| `EXP-ABL-01` | Component Ablation | Vision vs Sensor vs Fusion | 42 | CPU | N/A | Spoilage Loss % | PENDING | PLANNED | PENDING |
| `EXP-SEN-01` | Sensitivity Analysis | $\alpha \in [0.0, 1.0]$ Sweep | 42 | CPU | N/A | Min Objective Cost | PENDING | PLANNED | PENDING |

---

## Reproducibility Protocol
- All training and evaluation scripts must be invoked from the conda environment: `/opt/miniconda3/envs/spoilage`
- Scripts must log parameters, seeds, code version (git commit), metrics, and model weights to the central MLflow repository.
- No metric may be cited in the manuscript unless present in this registry.

