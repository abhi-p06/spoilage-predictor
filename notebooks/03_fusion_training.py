import matplotlib
matplotlib.use("Agg")  # non-interactive backend — no display needed
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import xgboost as xgb

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve,
    mean_absolute_error, r2_score
)
from sklearn.preprocessing import label_binarize

print(f"XGBoost version : {xgb.__version__}")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR    = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

CNN_PATH     = MODEL_DIR / "cnn_freshness.keras"
LSTM_PATH    = MODEL_DIR / "lstm_spoilage.keras"
SCALER_PATH  = MODEL_DIR / "lstm_scaler.pkl"
FUSION_PATH  = MODEL_DIR / "fusion_xgb.pkl"

# Fusion dataset config
N_SAMPLES = 10_000
SEED      = 42
TEST_SIZE = 0.20

PRODUCE_ID   = {"apple": 0, "banana": 1, "tomato": 2, "mango": 3}
SHELF_LIFE   = {"apple": 14, "banana": 7, "tomato": 10, "mango": 8}
COLD_MULT    = 1.6   # cold chain extends shelf life 60%

rng = np.random.default_rng(SEED)
print(f"Fusion model output → {FUSION_PATH}")

cnn_available  = CNN_PATH.exists()
lstm_available = LSTM_PATH.exists()

print(f"CNN  model  : {'✅  found' if cnn_available  else '⚠️  not found — will simulate CNN outputs'}")
print(f"LSTM model  : {'✅  found' if lstm_available else '⚠️  not found — will simulate LSTM outputs'}")

if cnn_available:
    import os
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    import tensorflow as tf
    from tensorflow import keras
    cnn_model  = keras.models.load_model(CNN_PATH)
    lstm_model = keras.models.load_model(LSTM_PATH) if lstm_available else None
    scaler     = joblib.load(SCALER_PATH) if SCALER_PATH.exists() else None
    print("Models loaded.")
else:
    cnn_model  = None
    lstm_model = None
    scaler     = None

# Sensor feature names (must match generate_sensor_data.py)
TIMESTEPS  = 24
N_FEATURES = 4
FLAT_COLS  = [
    col
    for h in range(TIMESTEPS)
    for col in [f"h{h:02d}_ethylene", f"h{h:02d}_co2", f"h{h:02d}_humidity", f"h{h:02d}_temperature"]
]

ETHYLENE_RANGES = {
    "apple":  (1.2, 25.0),
    "banana": (8.5, 50.0),
    "tomato": (2.1, 20.0),
    "mango":  (3.4, 30.0),
}

def simulate_cnn_score(is_fresh: bool, rng_local) -> float:
    """
    Sample a CNN freshness score consistent with the known true label.
    Fresh:   Beta(7, 2) → concentrated near 1 (high freshness)
    Rotten:  Beta(2, 7) → concentrated near 0 (low freshness)
    """
    if is_fresh:
        return float(np.clip(rng_local.beta(7, 2), 0.01, 0.99))
    else:
        return float(np.clip(rng_local.beta(2, 7), 0.01, 0.99))


def simulate_lstm_risk(is_fresh: bool, age_fraction: float, rng_local) -> float:
    """
    Sample LSTM spoilage risk consistent with the true label and age.
    Fresh:   base risk proportional to age, Beta-distributed
    Spoiled: elevated risk Beta-distributed near 1
    """
    if is_fresh:
        base = age_fraction * 0.45
        alpha = max(1, (1 - base) * 5)
        beta  = max(1, base * 5 + 1)
        return float(np.clip(rng_local.beta(alpha, beta), 0.01, 0.99))
    else:
        base = 0.5 + age_fraction * 0.45
        alpha = max(1, base * 6)
        beta  = max(1, (1 - base) * 3 + 1)
        return float(np.clip(rng_local.beta(alpha, beta), 0.01, 0.99))


def run_real_models(produce: str, days: int, cold_chain: bool,
                    cnn_model, lstm_model, scaler) -> tuple:
    """
    Run actual CNN and LSTM models if available.
    Returns (cnn_score, lstm_risk).
    """
    import tensorflow as tf
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path().resolve().parent / "app"))
    from predict import _generate_sensor_sequence

    # CNN: use a placeholder white image (no image file in fusion training)
    dummy_img = tf.zeros((1, 224, 224, 3), dtype=tf.float32)
    raw = float(cnn_model.predict(dummy_img, verbose=0)[0][0])
    cnn_score = 1.0 - raw

    # LSTM
    seq = _generate_sensor_sequence(produce, days)   # (1, 24, 4)
    if scaler is not None:
        seq_flat = seq.reshape(-1, N_FEATURES)
        seq_flat = scaler.transform(seq_flat)
        seq = seq_flat.reshape(1, TIMESTEPS, N_FEATURES)
    lstm_risk = float(lstm_model.predict(seq, verbose=0)[0][0])
    return cnn_score, lstm_risk

print("Helper functions defined.")

records = []
produce_list = list(PRODUCE_ID.keys())

for i in range(N_SAMPLES):
    produce    = rng.choice(produce_list)
    shelf      = SHELF_LIFE[produce]
    cold_chain = bool(rng.integers(0, 2))
    eff_shelf  = int(shelf * COLD_MULT) if cold_chain else shelf

    # Days since harvest: 0 to eff_shelf + 3 (include slightly over-shelf)
    days       = int(rng.integers(0, eff_shelf + 4))
    age_frac   = min(days / eff_shelf, 1.0)

    # True label: spoiled if age > 70% of effective shelf life
    is_fresh   = age_frac < 0.70
    # Add some noise to mimic real-world uncertainty
    if 0.60 < age_frac < 0.80:
        is_fresh = bool(rng.random() > age_frac)  # probabilistic boundary

    label = 0 if is_fresh else 1
    days_to_spoilage = max(0, int(eff_shelf * 0.70) - days)

    # CNN and LSTM scores
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

fusion_df = pd.DataFrame(records)

print(f"Fusion dataset: {fusion_df.shape}")
print(f"Class balance  — fresh={( fusion_df.label==0).sum()}, spoiled={(fusion_df.label==1).sum()}")
print(f"\nDays-to-spoilage stats:")
print(fusion_df['days_to_spoilage'].describe().round(2).to_string())
fusion_df.head()

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
colors = {0: '#0F6E56', 1: '#D7263D'}
labels_map = {0: 'Fresh', 1: 'Spoiled'}

for label_val in [0, 1]:
    sub = fusion_df[fusion_df.label == label_val]
    c   = colors[label_val]
    name = labels_map[label_val]
    axes[0].hist(sub["cnn_score"],  bins=40, alpha=0.65, color=c, label=name, density=True)
    axes[1].hist(sub["lstm_risk"],  bins=40, alpha=0.65, color=c, label=name, density=True)
    axes[2].hist(sub["days"],       bins=30, alpha=0.65, color=c, label=name, density=True)

axes[0].set(title="CNN Freshness Score", xlabel="Score", ylabel="Density")
axes[1].set(title="LSTM Risk Score",     xlabel="Risk")
axes[2].set(title="Days Since Harvest",  xlabel="Days")
for ax in axes: ax.legend(); ax.grid(alpha=0.3)

plt.suptitle("Fusion Feature Distributions: Fresh vs Spoiled", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(PROJECT_ROOT / "notebooks" / "fusion_feature_dist.png", dpi=120, bbox_inches='tight')
plt.show()

FEATURE_COLS = ["cnn_score", "lstm_risk", "days", "cold_chain", "produce_id"]

X = fusion_df[FEATURE_COLS].values.astype(np.float32)
y = fusion_df["label"].values.astype(np.int32)
y_days = fusion_df["days_to_spoilage"].values.astype(np.float32)

X_train, X_test, y_train, y_test, y_days_train, y_days_test = train_test_split(
    X, y, y_days, test_size=TEST_SIZE, random_state=SEED, stratify=y
)

print(f"Train : {X_train.shape}")
print(f"Test  : {X_test.shape}")

xgb_clf = xgb.XGBClassifier(
    n_estimators      = 400,
    max_depth         = 5,
    learning_rate     = 0.08,
    subsample         = 0.85,
    colsample_bytree  = 0.85,
    min_child_weight  = 3,
    gamma             = 0.1,
    reg_alpha         = 0.05,
    reg_lambda        = 1.0,
    use_label_encoder = False,
    eval_metric       = "logloss",
    tree_method       = "hist",      # fast histogram algorithm
    random_state      = SEED,
    verbosity         = 0,
)

xgb_clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=50,
)

print("\n✅  XGBoost classifier trained.")

# 5-fold stratified cross-validation
cv_scores = cross_val_score(
    xgb_clf, X, y,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED),
    scoring="roc_auc",
    n_jobs=-1,
)
print(f"5-Fold CV AUC : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print(f"Per-fold      : {cv_scores.round(4)}")

y_pred      = xgb_clf.predict(X_test)
y_pred_prob = xgb_clf.predict_proba(X_test)[:, 1]

auc = roc_auc_score(y_test, y_pred_prob)
print(f"Test ROC-AUC : {auc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Fresh", "Spoiled"]))

# Feature importance
importance = pd.DataFrame({
    "feature":    FEATURE_COLS,
    "importance": xgb_clf.feature_importances_,
}).sort_values("importance", ascending=False)
print("\nFeature Importances:")
print(importance.to_string(index=False))

xgb_reg = xgb.XGBRegressor(
    n_estimators      = 400,
    max_depth         = 5,
    learning_rate     = 0.08,
    subsample         = 0.85,
    colsample_bytree  = 0.85,
    min_child_weight  = 3,
    gamma             = 0.1,
    reg_alpha         = 0.05,
    reg_lambda        = 1.0,
    tree_method       = "hist",
    random_state      = SEED,
    verbosity         = 0,
)

xgb_reg.fit(
    X_train, y_days_train,
    eval_set=[(X_test, y_days_test)],
    verbose=50,
)

y_days_pred = np.clip(xgb_reg.predict(X_test), 0, None)
mae  = mean_absolute_error(y_days_test, y_days_pred)
r2   = r2_score(y_days_test, y_days_pred)
print(f"\nDays-to-spoilage  MAE : {mae:.2f} days")
print(f"Days-to-spoilage  R²  : {r2:.4f}")

fig, axes = plt.subplots(1, 3, figsize=(17, 5))

# ── ROC Curve ────────────────────────────────────────────────────────────────
fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
axes[0].plot(fpr, tpr, lw=2, color='#0F6E56', label=f'AUC={auc:.3f}')
axes[0].plot([0,1],[0,1],'--', color='grey')
axes[0].set(title='ROC Curve — Fusion Classifier',
            xlabel='FPR', ylabel='TPR')
axes[0].legend(); axes[0].grid(alpha=0.3)

# ── Confusion matrix ─────────────────────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Fresh','Spoiled'],
            yticklabels=['Fresh','Spoiled'],
            ax=axes[1], linewidths=0.5)
axes[1].set(title='Confusion Matrix', xlabel='Predicted', ylabel='True')

# ── Feature importance ────────────────────────────────────────────────────────
axes[2].barh(importance["feature"], importance["importance"], color='#0F6E56', edgecolor='white')
axes[2].set(title='Feature Importances (XGBoost)', xlabel='Importance')
axes[2].grid(alpha=0.3, axis='x')
axes[2].invert_yaxis()

plt.suptitle("XGBoost Fusion Model — Evaluation", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(PROJECT_ROOT / "notebooks" / "fusion_evaluation.png", dpi=120, bbox_inches='tight')
plt.show()

# Days-to-spoilage: predicted vs actual
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(y_days_test, y_days_pred, alpha=0.25, s=10, color='#0F6E56')
lim = max(y_days_test.max(), y_days_pred.max()) + 1
ax.plot([0, lim], [0, lim], '--', color='red', lw=1, label='Perfect prediction')
ax.set(
    title=f"Days-to-Spoilage: Predicted vs Actual  (MAE={mae:.2f}d, R²={r2:.3f})",
    xlabel="Actual days", ylabel="Predicted days",
    xlim=(0, lim), ylim=(0, lim)
)
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(PROJECT_ROOT / "notebooks" / "fusion_days_scatter.png", dpi=120, bbox_inches='tight')
plt.show()

# Bundle both models and metadata into a single pickle
fusion_bundle = {
    "classifier":  xgb_clf,     # predict_proba → spoilage probability
    "regressor":   xgb_reg,     # predict       → days to spoilage
    "feature_cols": FEATURE_COLS,
    "produce_id":  PRODUCE_ID,
    "shelf_life":  SHELF_LIFE,
    "cold_mult":   COLD_MULT,
    "version":     "1.0",
}

joblib.dump(fusion_bundle, FUSION_PATH)
print(f"✅  Fusion bundle saved → {FUSION_PATH}")
print(f"    File size : {FUSION_PATH.stat().st_size / 1e6:.2f} MB")

# Verify round-trip
loaded = joblib.load(FUSION_PATH)
test_vec = np.array([[0.85, 0.12, 3, 0, 0]], dtype=np.float32)
test_prob = float(loaded["classifier"].predict_proba(test_vec)[0][1])
test_days = float(np.clip(loaded["regressor"].predict(test_vec)[0], 0, None))
print(f"\nRound-trip test (apple, day 3, no cold chain, cnn=0.85, lstm=0.12):")
print(f"  Spoilage probability : {test_prob*100:.1f}%")
print(f"  Days to spoilage     : {test_days:.1f} days")

# Simulate 4 representative scenarios
scenarios = [
    {"label": "Fresh apple (day 1, cold chain)",    "cnn": 0.92, "lstm": 0.08, "days": 1, "cc": 1, "prod": 0},
    {"label": "Border-line banana (day 5, ambient)","cnn": 0.55, "lstm": 0.45, "days": 5, "cc": 0, "prod": 1},
    {"label": "Old tomato (day 9, ambient)",        "cnn": 0.25, "lstm": 0.78, "days": 9, "cc": 0, "prod": 2},
    {"label": "Rotten mango (day 8, no cold)",     "cnn": 0.10, "lstm": 0.92, "days": 8, "cc": 0, "prod": 3},
]

clf  = loaded["classifier"]
reg  = loaded["regressor"]

print(f"{'Scenario':<45} {'Spoilage%':>10} {'Days Left':>10} {'Alert':>8}")
print("-" * 78)
for s in scenarios:
    vec  = np.array([[s["cnn"], s["lstm"], s["days"], s["cc"], s["prod"]]], dtype=np.float32)
    prob = float(clf.predict_proba(vec)[0][1])
    days = int(np.clip(reg.predict(vec)[0], 0, None))
    alert = "🔴 RED" if prob > 0.70 else ("🟡 YELLOW" if prob > 0.35 else "🟢 GREEN")
    print(f"{s['label']:<45} {prob*100:>9.1f}% {days:>9}d {alert:>8}")
