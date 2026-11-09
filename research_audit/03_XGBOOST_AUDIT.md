# Forensic Audit 03: Multi-Modal Fusion Engine & XGBoost Models

> **Audit Date:** 2026-11-09  
> **Auditor:** Independent Scientific Auditor  
> **Target System:** AgriRoute Multi-Modal Stacking Fusion Pipeline  
> **Primary Script:** `notebooks/03_fusion_training.py`  
> **Execution Log:** `logs/fusion_training.log` (2026-06-26)  
> **Reported Metric:** Test ROC-AUC = 0.9999, Accuracy = 99.0%, MAE = 0.07 days, $R^2 = 0.9980$.

---

## 1. Executive Summary & Verdict

| Parameter | Audit Finding | Classification |
|---|---|---|
| **Reported Metric** | Test AUC = 0.9999, Accuracy = 99.0%, $R^2 = 0.9980$ | `REPOSITORY-REPORTED` |
| **Dataset Source** | 100% Synthetic in-memory dataframe ($N = 10,000$ iterations) | `SYNTHETIC` |
| **CNN Score Input** | Simulated via `Beta(7,2)` / `Beta(2,7)` because CNN model was missing | `SYNTHETIC INPUT` |
| **LSTM Risk Input** | Simulated via `Beta` distribution parameterized by `is_fresh` | `SYNTHETIC INPUT` |
| **Target Construction** | `label = 0 if age_frac < 0.70 else 1` | `DETERMINISTIC RULE` |
| **Days-to-Spoilage Target** | `max(0, int(eff_shelf * 0.70) - days)` | `EXACT FORMULA` |
| **Source of >95% Accuracy** | **Direct algebraic target leakage**: features contain the exact formula inputs | `TARGET LEAKAGE` |
| **Model Persistence Status** | Bundle `models/fusion_xgb.pkl` deleted in commit `568fd604b6` | `DEFECTIVE` |

---

## 2. Dataset Synthesis & Feature Construction

### 2.1 Complete In-Memory Generation Loop
In `notebooks/03_fusion_training.py` lines 140–176, the entire fusion dataset is generated in an artificial loop:

```python
records = []
for i in range(10_000):
    produce    = rng.choice(["apple", "banana", "tomato", "mango"])
    shelf      = SHELF_LIFE[produce]
    cold_chain = bool(rng.integers(0, 2))
    eff_shelf  = int(shelf * 1.6) if cold_chain else shelf
    days       = int(rng.integers(0, eff_shelf + 4))
    age_frac   = min(days / eff_shelf, 1.0)

    # True label: spoiled if age > 70% of effective shelf life
    is_fresh   = age_frac < 0.70
    if 0.60 < age_frac < 0.80:
        is_fresh = bool(rng.random() > age_frac)  # slight probabilistic boundary

    label = 0 if is_fresh else 1
    days_to_spoilage = max(0, int(eff_shelf * 0.70) - days)

    # Simulated model scores
    cnn_score  = simulate_cnn_score(is_fresh, rng)
    lstm_risk  = simulate_lstm_risk(is_fresh, age_frac, rng)

    records.append({
        "cnn_score":        cnn_score,
        "lstm_risk":        lstm_risk,
        "days":             days,
        "cold_chain":       1 if cold_chain else 0,
        "produce_id":       PRODUCE_ID[produce],
        "label":            label,
        "days_to_spoilage": days_to_spoilage,
    })
```

### 2.2 Feature Vector Composition
The 5 input features used by XGBoost (`FEATURE_COLS`):
1. `cnn_score`: Freshness score $\in [0, 1]$
2. `lstm_risk`: Spoilage risk $\in [0, 1]$
3. `days`: Integer days since harvest $\in [0, 26]$
4. `cold_chain`: Binary indicator ($0 = \text{ambient}, 1 = \text{refrigerated}$)
5. `produce_id`: Categorical integer ($0=\text{apple}, 1=\text{banana}, 2=\text{tomato}, 3=\text{mango}$)

---

## 3. The Precise Mechanism of the >95% (99%) Accuracy

The extraordinary metrics reported in `logs/fusion_training.log` (ROC-AUC = 0.9999, Accuracy = 99.0%, $R^2 = 0.9980$) are the direct consequence of two forms of mathematical target leakage:

### 3.1 Feature Leakage in Classification
Look at how `cnn_score` is generated:
```python
def simulate_cnn_score(is_fresh: bool, rng_local) -> float:
    if is_fresh:
        return float(np.clip(rng_local.beta(7, 2), 0.01, 0.99))
    else:
        return float(np.clip(rng_local.beta(2, 7), 0.01, 0.99))
```
- For fresh samples, `cnn_score` has a mean of $\frac{7}{7+2} = 0.778$.
- For spoiled samples, `cnn_score` has a mean of $\frac{2}{2+7} = 0.222$.
- The input feature `cnn_score` was **synthesized by sampling from a distribution conditioned on the true target label `is_fresh`**!
- In the feature importance chart (`logs/fusion_training.log` lines 42–48), `cnn_score` accounts for **78.37%** of the model's total gain:
  ```text
  Feature Importances:
     feature    importance
   cnn_score      0.783662
        days      0.128479
  cold_chain      0.044199
  produce_id      0.027688
   lstm_risk      0.015972
  ```
- XGBoost simply inverted the Beta sampling function to achieve 99.0% accuracy.

### 3.2 Exact Arithmetic Leakage in Regression
Look at how `days_to_spoilage` is generated:
$$\text{days\_to\_spoilage} = \max\bigl(0,\ \lfloor \text{SHELF\_LIFE}[\text{produce}] \times (1.6^{\text{cold\_chain}}) \times 0.70 \rfloor - \text{days}\bigr)$$
- The inputs to this arithmetic formula are:
  - `produce` ($\implies \text{produce\_id}$)
  - `cold_chain`
  - `days`
- **All three variables are provided directly as features in the input vector.**
- The target is a deterministic, noise-free piecewise-linear arithmetic equation of the input features.
- Consequently, `XGBRegressor` fitted the exact formula with 400 trees, reaching $R^2 = 0.9980$ and an average error of MAE = 0.07 days ($\approx 1.6$ hours).

---

## 4. Hyperparameter Regimen & Partitioning

### 4.1 Partitioning
- **Total Dataset:** 10,000 synthetic rows
- **Train Split:** 8,000 rows (80%)
- **Test Split:** 2,000 rows (20%), stratified by `label`
- **Class Balance:** 5,268 fresh (52.7%) / 4,732 spoiled (47.3%)

### 4.2 Model Hyperparameters
Configured identically for both `XGBClassifier` and `XGBRegressor`:
- `n_estimators`: 400
- `max_depth`: 5
- `learning_rate`: 0.08
- `subsample`: 0.85
- `colsample_bytree`: 0.85
- `min_child_weight`: 3
- `gamma`: 0.1
- `reg_alpha`: 0.05
- `reg_lambda`: 1.0
- `tree_method`: `"hist"`

---

## 5. Discrepancy Between Code and Manuscript

| Dimension | Manuscript Claim (`main.tex`) | Code Implementation (`predict.py`) |
|---|---|---|
| **Fusion Mechanism** | Linear convex combination: $S = w_1 V + w_2 G$ with $w_1 + w_2 = 1$ | Stacking ensemble: `XGBClassifier` + `XGBRegressor` |
| **Route Features in Fusion** | Road distance $D$ and transport multiplier $\tau$ dictate $G$ | **Neither $D$ nor $\tau$ is an input to XGBoost** |
| **Fusion Parameters** | Asserts $w_1, w_2$ are "pending confirmation in Table V" | Handled non-linearly via 400 boosted decision trees |
| **Alert Thresholds** | Vaguely described as traffic-light alerts | Hardcoded: Green ($<0.35$), Yellow ($0.35\text{--}0.70$), Red ($\ge 0.70$) |
| **Fallback Formula** | Not mentioned in paper | $\text{spoilage} = 0.45(1 - \text{cnn}) + 0.40(\text{lstm}) + 0.15(\text{days}/\text{shelf})$ |

---

## 6. Audit Recommendations for Revision

1. **Reconcile Manuscript Theory with Code:**
   - Remove the fictional linear combination $S = w_1 V + w_2 G$ from `main.tex`.
   - Formally document the actual stacking ensemble: the 5-feature vector, XGBoost tree parameters, and decision boundary thresholds.
2. **Eliminate Synthetic Circularities:**
   - Clearly label the XGBoost evaluation table as an **architectural validation on a simulated metadata corpus**, not empirical validation on physical produce shipments.
3. **Conduct Sensitivity & Feature Ablation:**
   - Execute an ablation removing `cnn_score` to evaluate how well days and cold-chain alone predict spoilage.
   - Run SHAP (SHapley Additive exPlanations) to explain feature contributions honestly.
4. **Restore Model Persistence:**
   - Re-train the fusion bundle deterministically and commit `fusion_xgb.pkl` to the models directory.

