---
name: reproducible-experiment-design
description: Standardize experimental protocols, fix random seeds, enforce parameter isolation, and integrate MLflow tracking for fully reproducible machine learning runs.
---

# Objective
Establish an airtight, reproducible execution framework for all model training and evaluation experiments in AgriRoute. Guarantee that every figure, metric, and table can be regenerated deterministically from clean configurations.

# Workflow

1. **Seed and Determinism Control:**
   - Fix pseudo-random number generator (PRNG) seeds across all libraries:
     - `PYTHONHASHSEED = seed`
     - `numpy.random.seed(seed)`
     - `torch.manual_seed(seed)` / `tensorflow.random.set_seed(seed)`
     - Configure deterministic CUDA / cuDNN convolution algorithms where applicable.
2. **Environment & Dependency Pinning:**
   - Record exact package versions (`conda list --export` or `pip freeze`).
   - Log Python runtime, OS version, GPU hardware, and driver versions.
3. **MLflow Tracking Integration:**
   - Initialize an MLflow experiment run:
     - Log parameters: architecture, optimizer, initial learning rate, weight decay, batch size, epochs, loss function, image dimensions, data split seed.
     - Log data lineage: dataset version tag, data hash, split sizes.
     - Log metrics per epoch: train/val loss, train/val accuracy, train/val AUC, learning rate decay.
     - Save artifacts: model checkpoints, confusion matrix plots, ROC curves, PR curves, calibration diagrams.
4. **Configuration File Architecture:**
   - Store all experimental hyperparameters in version-controlled YAML or JSON configuration files.
   - Forbid hardcoded parameters inside training scripts.
5. **Register Run in Research Memory:**
   - Record MLflow Run ID, model artifact URI, and git commit hash in `research_memory/experiment_registry.md`.

