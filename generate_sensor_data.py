"""
generate_sensor_data.py
=======================
Generates synthetic 24-hour sensor log CSVs for the LSTM training pipeline.

Each row represents one hourly reading per produce sample.
Ethylene ranges are drawn from USDA-cited literature:
  Apple:  1.2–25 ppm
  Banana: 8.5–50 ppm
  Tomato: 2.1–20 ppm
  Mango:  3.4–30 ppm

Output
------
data/sensors/sensor_logs.csv  — main training dataset
data/sensors/sample_input.csv — one 24-hour sequence for app inference

Usage
-----
  python generate_sensor_data.py
"""

from pathlib import Path
import numpy as np
import pandas as pd

# ── Config ────────────────────────────────────────────────────────────────────
SEED = 42
N_SAMPLES_PER_CLASS = 500   # fresh + spoiled per produce type
HOURS = 24
OUTPUT_DIR = Path(__file__).parent / "data" / "sensors"

PRODUCE_CONFIG = {
    "apple":  {"ethylene_range": (1.2, 25.0),  "shelf_life": 14},
    "banana": {"ethylene_range": (8.5, 50.0),  "shelf_life": 7},
    "tomato": {"ethylene_range": (2.1, 20.0),  "shelf_life": 10},
    "mango":  {"ethylene_range": (3.4, 30.0),  "shelf_life": 8},
}

PRODUCE_ID = {"apple": 0, "banana": 1, "tomato": 2, "mango": 3}

rng = np.random.default_rng(SEED)


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_sequence(produce: str, spoiled: bool) -> dict:
    """
    Simulate 24 hourly sensor readings for one produce sample.

    Spoiled samples have elevated ethylene, CO2, and temperature with
    higher variance to mimic real decay dynamics.

    Parameters
    ----------
    produce : str
        One of apple / banana / tomato / mango.
    spoiled : bool
        True → simulate a spoiling sample; False → fresh sample.

    Returns
    -------
    dict with keys: produce_id, label, hour_{0..23}_{ethylene|co2|humidity|temp}
    """
    cfg = PRODUCE_CONFIG[produce]
    eth_low, eth_high = cfg["ethylene_range"]

    if spoiled:
        # Ramp ethylene and CO2 upward; temperature slightly elevated
        ethylene   = rng.uniform(eth_high * 0.6, eth_high,  HOURS) + rng.normal(0, 1.5, HOURS)
        co2        = rng.uniform(1000, 3000,  HOURS) + np.linspace(0, 500, HOURS) + rng.normal(0, 80, HOURS)
        humidity   = rng.uniform(85, 98,      HOURS) + rng.normal(0, 1.5, HOURS)
        temperature= rng.uniform(20, 30,      HOURS) + rng.normal(0, 0.8, HOURS)
        label = 1
    else:
        ethylene   = rng.uniform(eth_low, eth_low * 4,  HOURS) + rng.normal(0, 0.5, HOURS)
        co2        = rng.uniform(400, 900,   HOURS) + rng.normal(0, 40, HOURS)
        humidity   = rng.uniform(65, 85,     HOURS) + rng.normal(0, 1.0, HOURS)
        temperature= rng.uniform(10, 22,     HOURS) + rng.normal(0, 0.5, HOURS)
        label = 0

    # Clip to physically plausible ranges
    ethylene    = np.clip(ethylene,    0,    60)
    co2         = np.clip(co2,         380, 4000)
    humidity    = np.clip(humidity,    40,  100)
    temperature = np.clip(temperature, 2,   40)

    row: dict = {
        "produce_id": PRODUCE_ID[produce],
        "produce":    produce,
        "label":      label,
    }

    for h in range(HOURS):
        row[f"h{h:02d}_ethylene"]    = round(float(ethylene[h]),    3)
        row[f"h{h:02d}_co2"]         = round(float(co2[h]),         1)
        row[f"h{h:02d}_humidity"]    = round(float(humidity[h]),    2)
        row[f"h{h:02d}_temperature"] = round(float(temperature[h]), 2)

    return row


def generate_dataset() -> pd.DataFrame:
    """
    Build the full training dataset: 500 fresh + 500 spoiled per produce type.
    Total rows = 4 produce × 1000 samples = 4000 rows.

    Returns
    -------
    pd.DataFrame
    """
    records = []
    for produce in PRODUCE_CONFIG:
        for _ in range(N_SAMPLES_PER_CLASS):
            records.append(make_sequence(produce, spoiled=False))
            records.append(make_sequence(produce, spoiled=True))

    df = pd.DataFrame(records)
    # Shuffle
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
    return df


def generate_sample_input(produce: str = "apple", spoiled: bool = False) -> pd.DataFrame:
    """
    Generate a single 24-row (one row per hour) sequence for app inference.

    The app's predict.py expects this long format:
      columns: hour, ethylene, co2, humidity, temperature

    Parameters
    ----------
    produce : str
        Produce type to simulate.
    spoiled : bool
        Whether to simulate a spoiling batch.

    Returns
    -------
    pd.DataFrame  shape (24, 5)
    """
    row = make_sequence(produce, spoiled)
    records = []
    for h in range(HOURS):
        records.append({
            "hour":        h,
            "ethylene":    row[f"h{h:02d}_ethylene"],
            "co2":         row[f"h{h:02d}_co2"],
            "humidity":    row[f"h{h:02d}_humidity"],
            "temperature": row[f"h{h:02d}_temperature"],
        })
    return pd.DataFrame(records)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("🌱  Generating training sensor dataset …")
    df_train = generate_dataset()
    train_path = OUTPUT_DIR / "sensor_logs.csv"
    df_train.to_csv(train_path, index=False)
    print(f"    ✔  {len(df_train):,} rows  →  {train_path}")

    print("🧪  Generating sample inference input …")
    df_sample = generate_sample_input(produce="apple", spoiled=False)
    sample_path = OUTPUT_DIR / "sample_input.csv"
    df_sample.to_csv(sample_path, index=False)
    print(f"    ✔  {len(df_sample)} rows  →  {sample_path}")

    # Quick stats
    print("\n📊  Class balance:")
    print(df_train.groupby(["produce", "label"]).size().rename("count").to_string())
    print("\n✅  Sensor data generation complete.")


if __name__ == "__main__":
    main()
