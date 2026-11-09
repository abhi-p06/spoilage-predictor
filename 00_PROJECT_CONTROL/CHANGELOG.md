# Repository Architecture Changelog

## [V2.0-CLEANUP] - 2026-11-09
- Cleaned and consolidated legacy V3, V4, and pre-V4 artifacts into structured `archive/` subdirectories.
- Pruned ephemeral `.pytest_cache`, `.DS_Store`, `__pycache__`, and temporary playwright files.
- Preserved all canonical datasets (`data/raw/kaggle`, `fruitvision`, `sultana`).
- Preserved authoritative V4.1 models, prediction arrays, and metrics.
- Initialized modular 10-tier project control architecture (`00_PROJECT_CONTROL` through `09_CODE`).
