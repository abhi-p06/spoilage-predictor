# Forensic Audit 02: Time-Series Sensor Generator & BiLSTM Sequence Model

> **Audit Date:** 2026-11-09  
> **Auditor:** Independent Scientific Auditor  
> **Target System:** AgriRoute Environmental Sensor & Spoilage Sequence Model  
> **Primary Scripts:** `generate_sensor_data.py`, `notebooks/02_lstm_training.py`  
> **Execution Log:** `logs/lstm_training.log` (2026-06-26)  
> **Manuscript Claim:** Bidirectional LSTM achieves AUC-ROC = 1.000 across 24-hour multivariate sensor sequences.

---

## 1. Executive Summary & Verdict

| Parameter | Audit Finding | Classification |
|---|---|---|
| **Reported Metric** | AUC-ROC = 1.000, Accuracy = 1.000, F1 = 1.000 | `REPOSITORY-REPORTED` |
| **Data Nature** | 100% Synthetic / Numerically Simulated | `SYNTHETIC` |
| **Realism of Sensor Traces** | Synthetic Gaussian ramps with non-physical boundaries | `UNREALISTIC` |
| **Label Generation Mechanism** | Deterministic if-else conditional branch in generator script | `SYNTHETIC TARGET LEAKAGE` |
| **Distribution Overlap** | **ZERO overlap** in CO₂ and Humidity between Fresh and Spoiled | `FATAL ARTIFACT` |
| **Why AUC = 1.000** | Problem is linearly separable on single features ($CO_2 > 950$ ppm) | `TRIVIAL CLASSIFICATION` |
| **Global Preprocessing Leakage** | `StandardScaler` fitted on combined data before train/val/test split | `METHODOLOGICAL FLAW` |
| **External Real-World Validity** | **Zero predictive validity** on real cold-chain transport IoT | `UNSUPPORTED` |

---

## 2. Forensic Analysis of Data Generation (`generate_sensor_data.py`)

### 2.1 The Label Generation Mechanism
In `generate_sensor_data.py` (lines 47–81), the function `make_sequence(produce: str, spoiled: bool)` generates a 24-hour hourly sequence of 4 variables (`ethylene`, `co2`, `humidity`, `temperature`):

```python
if spoiled:
    ethylene    = rng.uniform(eth_high * 0.6, eth_high, HOURS) + rng.normal(0, 1.5, HOURS)
    co2         = rng.uniform(1000, 3000, HOURS) + np.linspace(0, 500, HOURS) + rng.normal(0, 80, HOURS)
    humidity    = rng.uniform(85, 98, HOURS) + rng.normal(0, 1.5, HOURS)
    temperature = rng.uniform(20, 30, HOURS) + rng.normal(0, 0.8, HOURS)
    label = 1
else:
    ethylene    = rng.uniform(eth_low, eth_low * 4, HOURS) + rng.normal(0, 0.5, HOURS)
    co2         = rng.uniform(400, 900, HOURS) + rng.normal(0, 40, HOURS)
    humidity    = rng.uniform(65, 85, HOURS) + rng.normal(0, 1.0, HOURS)
    temperature = rng.uniform(10, 22, HOURS) + rng.normal(0, 0.5, HOURS)
    label = 0
```

### 2.2 Proof of Disjoint Distribution & Trivial Separation

Let us compare the mathematical intervals generated for each channel:

1. **Carbon Dioxide ($CO_2$):**
   - **Fresh ($\text{label} = 0$):** Drawn from $\mathcal{U}(400, 900) + \mathcal{N}(0, 40)$. With $99.7\%$ probability, $CO_2 \le 900 + 3(40) = 1,020$ ppm. The mean fresh $CO_2 \approx 650$ ppm.
   - **Spoiled ($\text{label} = 1$):** Drawn from $\mathcal{U}(1000, 3000) + [0, 500] + \mathcal{N}(0, 80)$. The minimum baseline is $1,000$ ppm, and with upward drift reaches up to $3,500$ ppm. The mean spoiled $CO_2 \approx 2,250$ ppm.
   - **Distribution Overlap:** Near zero. A single static rule:
     $$\text{If } CO_2 > 950 \text{ ppm} \implies \text{Spoiled}$$
     achieves $\approx 99.9\%$ classification accuracy on its own.

2. **Relative Humidity (%):**
   - **Fresh ($\text{label} = 0$):** $\mathcal{U}(65, 85) + \mathcal{N}(0, 1.0) \implies \text{Interval } [62\%, 88\%]$.
   - **Spoiled ($\text{label} = 1$):** $\mathcal{U}(85, 98) + \mathcal{N}(0, 1.5) \implies \text{Interval } [82\%, 100\%]$.

3. **Temperature ($^\circ\text{C}$):**
   - **Fresh ($\text{label} = 0$):** $\mathcal{U}(10, 22) + \mathcal{N}(0, 0.5) \implies \text{Interval } [8.5^\circ\text{C}, 23.5^\circ\text{C}]$.
   - **Spoiled ($\text{label} = 1$):** $\mathcal{U}(20, 30) + \mathcal{N}(0, 0.8) \implies \text{Interval } [17.6^\circ\text{C}, 32.4^\circ\text{C}]$.

**Audit Verdict:** The labels are not probabilistic outcomes of a complex biochemical decay process; they are **direct reflections of the generator's binary conditional branch**. The data features are separated by a massive hyperplane gap.

---

## 3. Training Dynamics & The Emergence of AUC = 1.000

### 3.1 Model Architecture
In `notebooks/02_lstm_training.py` lines 118–154:
- **Input Shape:** $(24 \text{ timesteps}, 4 \text{ channels})$
- **Layer 1:** `Bidirectional(LSTM(128, return_sequences=True))` (256 hidden units) + `LayerNormalization` + `Dropout(0.3)`
- **Layer 2:** `Bidirectional(LSTM(64, return_sequences=False))` (128 hidden units) + `LayerNormalization` + `Dropout(0.3)`
- **Dense Layer:** `Dense(64, activation="relu")` + `Dropout(0.2)`
- **Output:** `Dense(1, activation="sigmoid")`
- **Total Parameters:** 309,633 parameters.

### 3.2 Preprocessing Leakage
In lines 92–108:
```python
N = X_raw.shape[0]
X_flat = X_raw.reshape(N * TIMESTEPS, N_FEATURES)

scaler = StandardScaler()
X_scaled_flat = scaler.fit_transform(X_flat)      # FITTED ON THE ENTIRE DATASET!
X_scaled = X_scaled_flat.reshape(N, TIMESTEPS, N_FEATURES)

# Split performed AFTER scaler fitting:
X_tv, X_test, y_tv, y_test = train_test_split(X_scaled, y, ...)
```
Fitting `StandardScaler` across all 4,000 samples prior to splitting leaks the global mean and variance of test samples into the training pipeline.

### 3.3 Epoch 1 Convergence Log
From `logs/lstm_training.log` (lines 55–65):
```text
Epoch 1/40:
41/41 [==============================] - 8s 192ms/step - 
  loss: 0.0542 - accuracy: 0.9846 - auc: 0.9991 - 
  val_loss: 1.8779e-06 - val_accuracy: 1.0000 - val_auc: 1.0000
```
- By **Epoch 1**, the validation AUC reached **1.0000** and validation loss collapsed to $1.87 \times 10^{-6}$.
- At Epoch 9, early stopping triggered with:
  ```text
  Epoch 9: early stopping
  Restoring model weights from the end of the best epoch: 1.
  ── Test Set Results ─────────────────────────────────
    loss        : 0.0000
    compile_metrics: 1.0000
  ROC-AUC : 1.0000
  ```
- **Finding:** A 309,633-parameter deep recurrent network was trained to solve a problem that required only a single decision threshold on synthetic data.

---

## 4. Assessment of Realism & Biological Validity

In post-harvest physiology (USDA Handbook 66; Kader, 2002):
1. **Ethylene Release:** Ethylene production during climacteric ripening is governed by non-linear enzymatic reactions ($S$-adenosylmethionine $\to$ ACC $\to$ ethylene) dependent on cellular temperature and respiration rates. The simple static uniform distribution with random normal noise used in `generate_sensor_data.py` ignores true biological kinetics.
2. **Sensor Response Latency:** Electrochemical gas sensors (e.g. MQ-136) experience significant baseline drift, thermal sensitivity, cross-sensitivity to relative humidity, and 15–30 minute response latencies. None of these physical distortions exist in the generated dataset.
3. **Container Microclimates:** In refrigerated transport, temperature gradients across pallets can exceed $8^\circ\text{C}$ between outer walls and pallet cores. Treating a single 4-channel sequence as representative of whole-shipment quality is non-viable.

---

## 5. Explicit Recommendation: Retention vs. Removal

### Recommendation: **REPOSITION SOLELY AS A SIMULATION EXTENSION / FUTURE FRAMEWORK**

1. **Immediate Retraction:**
   - **Retract all claims that AgriRoute achieved a valid empirical AUC of 1.000.** In peer-reviewed machine learning venues, claiming AUC=1.000 on synthetic data is universally recognized as a hallmark of target leakage.
2. **Manuscript Reframing:**
   - Follow the honest framing already begun in `main.tex` Section IV-D and Table II: clearly classify the sensor track as **"Designed & Proposed Simulation Extension"** rather than an empirically validated deployment.
   - Explicitly label all sensor data as **"Synthetic Benchmark Simulation"**.
3. **If Retained in Empirical Results:**
   - Re-generate the synthetic dataset using an **Arrhenius-based biological decay simulator** with substantial noise, realistic cross-channel correlation, sensor drift, and **heavily overlapping distributions** between fresh and borderline-spoiled produce.
   - Re-train the model and report realistic metrics with 95% bootstrap confidence intervals (e.g., AUC $\approx 0.82\text{--}0.88$).

