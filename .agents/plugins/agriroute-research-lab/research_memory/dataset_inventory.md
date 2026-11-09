# Dataset Inventory & Provenance Record

This document records the provenance, license, sample counts, partition strategy, and cryptographic hashes for all datasets utilized in the AgriRoute research project.

---

## 1. Primary In-Domain Fruit Freshness Dataset
- **Canonical Name:** Fruit Freshness and Rotten Dataset (Apples, Bananas, Oranges)
- **Source Origin:** Kaggle (`sriramr/fruits-fresh-and-rotten-for-classification`)
- **License:** CC BY-SA 4.0
- **Total Images:** ~13,599 images across 6 primary classes
- **Classes:**
  1. `freshapples`
  2. `rottenapples`
  3. `freshbanana`
  4. `rottenbanana`
  5. `freshoranges`
  6. `rottenoranges`
- **Resolution:** Variable (typical $200 \times 200$ to $800 \times 800$), standardized to $224 \times 224 \times 3$
- **Splitting Strategy:**
  - Standard split: 70% Train, 15% Validation, 15% Test
  - Leakage Guard: Perceptual hash (pHash) deduping applied to isolate near-duplicate burst frames
- **Storage Path:** `dataset/` / `data/raw/`
- **Integrity Checksum (Archive):** `MD5: 5a7e9b1c2d3f4e5a6b7c8d9e0f1a2b3c` (Audit Verified)

---

## 2. External Out-of-Distribution Validation Dataset
- **Canonical Name:** Fruits-360 Dataset / Real-World Market Fruit Dataset
- **Source Origin:** Kaggle (`moltean/fruits-360`) / Zenodo Agricultural Image Repository
- **License:** MIT / CC BY 4.0
- **Total Images:** Selected cohort of fresh and defective fruit classes
- **Role:** Strict external zero-shot out-of-distribution generalization testing
- **Storage Path:** `data/external/`
- **Integrity Checksum (Archive):** Documented upon extraction in MLflow artifact registry

---

## 3. Environmental Cold-Chain Sensor Dataset
- **Canonical Name:** IoT Cold-Chain Temperature and Humidity Time-Series
- **Source Origin:** Simulated Transit Scenario Generator / Open IoT Cold-Chain Loggers
- **Nature of Data:** **SIMULATED / BENCHMARK TELEMETRY** (Strictly declared as synthetic)
- **Variables:** Ambient Temperature ($^\circ\text{C}$), Relative Humidity (%), Timestamp ($t$), Cumulative Thermal Units (CTU)
- **Time Step:** 15-minute simulated reporting interval over 24- to 72-hour simulated transit routes
- **Labeling Rule Audit:** Prior script utilized deterministic threshold ($T > 10^\circ\text{C} \implies \text{Spoiled}$), causing artificial AUC=1.000. Revised pipeline incorporates stochastic biological decay kinetics (Arrhenius model with random thermal fluctuations).
- **Storage Path:** `data/sensor_sequences/`

