#!/usr/bin/env python3
"""
train_all.py
============
Standalone training script — runs all three model training stages in sequence.

Stages
------
1. CNN  (MobileNetV2)        → models/cnn_freshness.h5
2. LSTM (Bidirectional LSTM) → models/lstm_spoilage.h5  +  models/lstm_scaler.pkl
3. XGBoost Fusion            → models/fusion_xgb.pkl

Faster than running notebooks interactively; same logic, reduced epochs.
"""

import os
import sys
import time

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
MODEL_DIR    = PROJECT_ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

CNN_PATH    = MODEL_DIR / "cnn_freshness.h5"
LSTM_PATH   = MODEL_DIR / "lstm_spoilage.h5"
SCALER_PATH = MODEL_DIR / "lstm_scaler.pkl"
FUSION_PATH = MODEL_DIR / "fusion_xgb.pkl"

# ── Hyperparameters (balanced speed vs quality) ───────────────────────────────
IMG_SIZE    = (224, 224)
BATCH_SIZE  = 32
EPOCHS_HEAD = 5          # Phase 1: frozen base (was 10)
EPOCHS_FINE = 5          # Phase 2: fine-tune   (was 10) — early stopping may end sooner
LR_HEAD     = 1e-3
LR_FINE     = 1e-4

LSTM_EPOCHS = 10
LSTM_BATCH  = 64

SEED = 42


# ══════════════════════════════════════════════════════════════════════════════
# Stage 1 — CNN Freshness Classifier
# ══════════════════════════════════════════════════════════════════════════════

def train_cnn():
    print("\n" + "═" * 60)
    print("  STAGE 1 — CNN Freshness Classifier (MobileNetV2)")
    print("═" * 60)
    t0 = time.time()

    if CNN_PATH.exists():
        print(f"  ✅  Already exists: {CNN_PATH} — skipping training.")
        return

    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    AUTOTUNE = tf.data.AUTOTUNE

    DATA_DIR  = PROJECT_ROOT / "data" / "images" / "dataset" / "dataset"
    TRAIN_DIR = DATA_DIR / "train"
    TEST_DIR  = DATA_DIR / "test"

    assert TRAIN_DIR.exists(), f"Train dir not found: {TRAIN_DIR}"
    assert TEST_DIR.exists(),  f"Test dir not found:  {TEST_DIR}"

    # ── Build file lists ──────────────────────────────────────────────────────
    def get_paths_labels(root: Path):
        paths, labels = [], []
        for cls_dir in sorted(root.iterdir()):
            if not cls_dir.is_dir():
                continue
            label = 1 if cls_dir.name.lower().startswith("rotten") else 0
            for p in cls_dir.glob("*"):
                if p.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                    paths.append(str(p))
                    labels.append(label)
        return paths, labels

    train_paths, train_labels = get_paths_labels(TRAIN_DIR)
    test_paths,  test_labels  = get_paths_labels(TEST_DIR)
    print(f"  Train: {len(train_paths)} images  |  Test: {len(test_paths)} images")

    # ── tf.data pipelines ─────────────────────────────────────────────────────
    @tf.function
    def load_img(path, label):
        raw = tf.io.read_file(path)
        img = tf.image.decode_png(raw, channels=3)
        img = tf.image.resize(img, IMG_SIZE)
        img = tf.cast(img, tf.float32) / 255.0
        return img, label

    augment = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.12),
        layers.RandomZoom(0.08),
    ], name="augmentation")

    @tf.function
    def augment_fn(img, label):
        return augment(img, training=True), label

    train_ds = (
        tf.data.Dataset.from_tensor_slices((train_paths, train_labels))
        .shuffle(len(train_paths), seed=SEED)
        .map(load_img,    num_parallel_calls=AUTOTUNE)
        .map(augment_fn,  num_parallel_calls=AUTOTUNE)
        .batch(BATCH_SIZE)
        .prefetch(AUTOTUNE)
    )
    test_ds = (
        tf.data.Dataset.from_tensor_slices((test_paths, test_labels))
        .map(load_img, num_parallel_calls=AUTOTUNE)
        .batch(BATCH_SIZE)
        .prefetch(AUTOTUNE)
    )

    # ── Model builder ─────────────────────────────────────────────────────────
    def build_model(trainable_base: bool = False):
        base = keras.applications.MobileNetV2(
            input_shape=(*IMG_SIZE, 3),
            include_top=False,
            weights="imagenet"
        )
        base.trainable = False
        if trainable_base:
            for layer in base.layers[-30:]:
                layer.trainable = True

        inputs  = keras.Input(shape=(*IMG_SIZE, 3))
        x       = base(inputs, training=trainable_base)
        x       = layers.GlobalAveragePooling2D()(x)
        x       = layers.Dense(256, activation="relu")(x)
        x       = layers.Dropout(0.4)(x)
        outputs = layers.Dense(1, activation="sigmoid")(x)
        return keras.Model(inputs, outputs)

    # ── Phase 1: frozen base ──────────────────────────────────────────────────
    print(f"\n  Phase 1: head-only training ({EPOCHS_HEAD} epochs max)…")
    model = build_model(trainable_base=False)
    model.compile(
        optimizer=keras.optimizers.Adam(LR_HEAD),
        loss="binary_crossentropy",
        metrics=["accuracy", keras.metrics.AUC(name="auc")]
    )
    model.fit(
        train_ds,
        validation_data=test_ds,
        epochs=EPOCHS_HEAD,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor="val_accuracy", patience=3,
                restore_best_weights=True, verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.5, patience=2,
                min_lr=1e-6, verbose=1
            ),
        ],
        verbose=1,
    )

    # ── Phase 2: fine-tune ────────────────────────────────────────────────────
    print(f"\n  Phase 2: fine-tuning last 30 layers ({EPOCHS_FINE} epochs max)…")
    model_ft = build_model(trainable_base=True)
    model_ft.set_weights(model.get_weights())
    model_ft.compile(
        optimizer=keras.optimizers.Adam(LR_FINE),
        loss="binary_crossentropy",
        metrics=["accuracy", keras.metrics.AUC(name="auc")]
    )
    model_ft.fit(
        train_ds,
        validation_data=test_ds,
        epochs=EPOCHS_FINE,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor="val_accuracy", patience=4,
                restore_best_weights=True, verbose=1
            ),
            keras.callbacks.ModelCheckpoint(
                filepath=str(CNN_PATH),
                monitor="val_accuracy",
                save_best_only=True, verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.3, patience=2,
                min_lr=1e-7, verbose=1
            ),
        ],
        verbose=1,
    )

    # Save best model explicitly if checkpoint didn't fire
    if not CNN_PATH.exists():
        model_ft.save(CNN_PATH)

    print(f"\n  ✅  CNN model saved → {CNN_PATH}")
    print(f"      File size: {CNN_PATH.stat().st_size / 1e6:.1f} MB")
    print(f"      Wall time: {(time.time() - t0) / 60:.1f} min")


# ══════════════════════════════════════════════════════════════════════════════
# Stage 2 — BiLSTM Sensor Spoilage Model
# ══════════════════════════════════════════════════════════════════════════════

def train_lstm():
    print("\n" + "═" * 60)
    print("  STAGE 2 — BiLSTM Sensor Spoilage Model")
    print("═" * 60)
    t0 = time.time()

    if LSTM_PATH.exists() and SCALER_PATH.exists():
        print(f"  ✅  Already exists — skipping LSTM training.")
        return

    import numpy as np
    import pandas as pd
    import joblib
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    SENSOR_CSV = PROJECT_ROOT / "data" / "sensors" / "sensor_logs.csv"
    assert SENSOR_CSV.exists(), f"Sensor CSV not found: {SENSOR_CSV}"

    df = pd.read_csv(SENSOR_CSV)
    print(f"  Sensor logs: {df.shape[0]} rows × {df.shape[1]} cols")

    # ── Wide-format CSV: each row has 24 hourly readings as columns ────────────
    # h00_ethylene … h23_ethylene, h00_co2 … h23_co2, etc.
    # Label column: 'label'  (1 = spoiled, 0 = fresh)
    TIMESTEPS   = 24
    SENSOR_KEYS = ["ethylene", "co2", "humidity", "temperature"]  # in feature order
    LABEL_COL   = "label"

    assert LABEL_COL in df.columns, f"Missing label column: {LABEL_COL}"
    for key in SENSOR_KEYS:
        for h in range(TIMESTEPS):
            col = f"h{h:02d}_{key}"
            assert col in df.columns, f"Missing column: {col}"

    # ── Build (N, 24, 4) tensor ────────────────────────────────────────────────
    # Stack each sensor key across hours → shape (N, 24) per key, then combine
    arrays = []
    for key in SENSOR_KEYS:
        cols = [f"h{h:02d}_{key}" for h in range(TIMESTEPS)]
        arrays.append(df[cols].values)          # (N, 24)
    X_raw = np.stack(arrays, axis=-1).astype(np.float32)  # (N, 24, 4)

    y = df[LABEL_COL].values.astype(np.float32)
    print(f"  Sequences: {X_raw.shape}  |  Labels: {y.shape}")
    print(f"  Spoilage rate: {y.mean():.1%}")

    # ── Fit scaler on flattened features, then reshape back ───────────────────
    scaler = StandardScaler()
    N = X_raw.shape[0]
    flat = X_raw.reshape(-1, len(SENSOR_KEYS))      # (N*24, 4)
    flat_scaled = scaler.fit_transform(flat)
    X = flat_scaled.reshape(N, TIMESTEPS, len(SENSOR_KEYS)).astype(np.float32)
    joblib.dump(scaler, SCALER_PATH)
    print(f"  Scaler saved → {SCALER_PATH}")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    # ── BiLSTM model ──────────────────────────────────────────────────────────
    inputs = keras.Input(shape=(TIMESTEPS, len(SENSOR_KEYS)))
    x      = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(inputs)
    x      = layers.Dropout(0.3)(x)
    x      = layers.Bidirectional(layers.LSTM(32))(x)
    x      = layers.Dropout(0.3)(x)
    x      = layers.Dense(32, activation="relu")(x)
    output = layers.Dense(1, activation="sigmoid")(x)
    lstm_model = keras.Model(inputs, output)

    lstm_model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy", keras.metrics.AUC(name="auc")]
    )
    lstm_model.summary()

    lstm_model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=LSTM_EPOCHS,
        batch_size=LSTM_BATCH,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor="val_auc", patience=4, mode="max",
                restore_best_weights=True, verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.5, patience=3,
                min_lr=1e-6, verbose=1
            ),
            keras.callbacks.ModelCheckpoint(
                filepath=str(LSTM_PATH),
                monitor="val_auc", mode="max",
                save_best_only=True, verbose=1
            ),
        ],
        verbose=1,
    )

    if not LSTM_PATH.exists():
        lstm_model.save(LSTM_PATH)

    print(f"\n  ✅  LSTM model saved → {LSTM_PATH}")
    print(f"      File size: {LSTM_PATH.stat().st_size / 1e6:.1f} MB")
    print(f"      Wall time: {(time.time() - t0) / 60:.1f} min")


# ══════════════════════════════════════════════════════════════════════════════
# Stage 3 — XGBoost Fusion Model
# ══════════════════════════════════════════════════════════════════════════════

def train_fusion():
    print("\n" + "═" * 60)
    print("  STAGE 3 — XGBoost Fusion Model")
    print("═" * 60)
    t0 = time.time()

    if FUSION_PATH.exists():
        print(f"  ✅  Already exists — skipping fusion training.")
        return

    import numpy as np
    import pandas as pd
    import joblib
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    from xgboost import XGBClassifier, XGBRegressor

    # ── Load or simulate fusion dataset ───────────────────────────────────────
    SENSOR_CSV = PROJECT_ROOT / "data" / "sensors" / "sensor_logs.csv"
    df = pd.read_csv(SENSOR_CSV)

    PRODUCE_ID = {"apple": 0, "banana": 1, "tomato": 2, "mango": 3}
    SHELF_LIFE = {"apple": 14, "banana": 7, "tomato": 10, "mango": 8}
    COLD_MULT  = 1.6

    # Actual CSV schema: produce_id (int 0-3), produce (str), label (0/1)
    # plus h00_ethylene … h23_temperature wide columns
    # We derive days_since_harvest from produce shelf life + label
    rng = np.random.default_rng(SEED)

    rows = []
    for _, row in df.iterrows():
        # Produce info
        produce_name = str(row.get("produce", "")).lower().strip()
        if produce_name not in PRODUCE_ID:
            produce_name = rng.choice(list(PRODUCE_ID.keys()))
        pid   = PRODUCE_ID[produce_name]
        shelf = SHELF_LIFE[produce_name]

        spoiled = int(row["label"])
        cold    = int(rng.integers(0, 2))   # simulate cold-chain flag
        eff_shelf = shelf * COLD_MULT if cold else shelf

        # Simulate days since harvest: spoiled items tend to be older
        if spoiled:
            days = int(rng.integers(max(1, shelf - 2), shelf + 5))
        else:
            days = int(rng.integers(1, max(2, shelf - 1)))

        age_frac  = min(days / eff_shelf, 1.0)

        # CNN score correlated with freshness
        cnn_base  = 1.0 - age_frac
        cnn_score = float(np.clip(cnn_base + rng.normal(0, 0.12), 0.0, 1.0))

        # LSTM risk correlated with spoilage label + age
        lstm_base = age_frac * 0.80 + spoiled * 0.15
        lstm_risk = float(np.clip(lstm_base + rng.normal(0, 0.10), 0.0, 1.0))

        days_left = max(0, int(eff_shelf - days + rng.normal(0, 1)))

        rows.append({
            "cnn_score":        cnn_score,
            "lstm_risk":        lstm_risk,
            "days":             days,
            "cold_chain":       float(cold),
            "produce_id":       float(pid),
            "is_spoiled":       spoiled,
            "days_to_spoilage": days_left,
        })

    fusion_df = pd.DataFrame(rows)
    print(f"  Fusion dataset: {fusion_df.shape[0]} rows")
    print(f"  Spoilage rate: {fusion_df['is_spoiled'].mean():.1%}")

    FEATURE_COLS = ["cnn_score", "lstm_risk", "days", "cold_chain", "produce_id"]
    X = fusion_df[FEATURE_COLS].values
    y_cls = fusion_df["is_spoiled"].values
    y_reg = fusion_df["days_to_spoilage"].values

    X_tr, X_val, yc_tr, yc_val, yr_tr, yr_val = train_test_split(
        X, y_cls, y_reg, test_size=0.2, random_state=SEED, stratify=y_cls
    )

    # ── Classifier ────────────────────────────────────────────────────────────
    print("\n  Training XGBoost classifier…")
    clf = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        early_stopping_rounds=20,
        random_state=SEED,
        verbosity=1,
    )
    clf.fit(X_tr, yc_tr, eval_set=[(X_val, yc_val)], verbose=50)
    print("\n  Classification report (val):")
    print(classification_report(yc_val, clf.predict(X_val)))

    # ── Regressor ─────────────────────────────────────────────────────────────
    print("\n  Training XGBoost regressor (days to spoilage)…")
    reg = XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="rmse",
        early_stopping_rounds=20,
        random_state=SEED,
        verbosity=1,
    )
    reg.fit(X_tr, yr_tr, eval_set=[(X_val, yr_val)], verbose=50)

    # ── Save bundle ───────────────────────────────────────────────────────────
    bundle = {
        "classifier":   clf,
        "regressor":    reg,
        "feature_cols": FEATURE_COLS,
        "produce_id":   PRODUCE_ID,
        "shelf_life":   SHELF_LIFE,
        "cold_mult":    COLD_MULT,
    }
    joblib.dump(bundle, FUSION_PATH)

    print(f"\n  ✅  Fusion bundle saved → {FUSION_PATH}")
    print(f"      File size: {FUSION_PATH.stat().st_size / 1e6:.2f} MB")
    print(f"      Wall time: {(time.time() - t0) / 60:.1f} min")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    total_start = time.time()
    print("\n🚀  Post-Harvest Spoilage Predictor — Training Pipeline")
    print(f"    Project root: {PROJECT_ROOT}")
    print(f"    Models dir  : {MODEL_DIR}")

    train_cnn()
    train_lstm()
    train_fusion()

    total_min = (time.time() - total_start) / 60
    print("\n" + "═" * 60)
    print(f"  🎉  All models trained in {total_min:.1f} min")
    print(f"      CNN   : {CNN_PATH}")
    print(f"      LSTM  : {LSTM_PATH}")
    print(f"      Fusion: {FUSION_PATH}")
    print("═" * 60)
