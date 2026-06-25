# Post-Harvest Spoilage Predictor
## SY B.Tech AI & Data Science — College Project

A multimodal AI system that predicts produce spoilage from a fruit photo + basic farm details.

---

### 🏗️ Project Structure

```
spoilage-predictor/
├── data/
│   ├── images/        ← Kaggle "Fresh & Rotten Fruits" dataset
│   └── sensors/       ← generated sensor CSVs (auto-created)
├── models/            ← saved model files (.h5, .pkl)
├── notebooks/
│   ├── 01_cnn_training.ipynb
│   ├── 02_lstm_training.ipynb
│   └── 03_fusion_training.ipynb
├── app/
│   ├── app.py         ← Flask entry point
│   ├── predict.py     ← inference pipeline
│   ├── templates/     ← index.html, result.html
│   └── static/        ← style.css, uploads/
├── generate_sensor_data.py
├── download_dataset.py
└── requirements.txt
```

---

### ⚙️ Setup (Apple M4 MacBook, Anaconda)

```bash
# 1. Create environment
conda create -n spoilage python=3.11 -y
conda activate spoilage

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sensor data
python generate_sensor_data.py

# 4. Download Kaggle dataset (requires ~/.kaggle/kaggle.json)
python download_dataset.py
```

---

### 🤖 Training (Phase 2 — run notebooks in order)

```bash
jupyter notebook
```

Open and run:
1. `notebooks/01_cnn_training.ipynb`   → saves `models/cnn_freshness.h5`
2. `notebooks/02_lstm_training.ipynb`  → saves `models/lstm_spoilage.h5`
3. `notebooks/03_fusion_training.ipynb`→ saves `models/fusion_xgb.pkl`

---

### 🚀 Run the Web App

```bash
cd app/
python app.py
```

Open **http://localhost:5000** in your browser.

> The app runs in mock mode if model files are not yet trained — all UI features work.

---

### 🧠 Three Models

| Model | Architecture | Task | Target |
|-------|-------------|------|--------|
| CNN | MobileNetV2 (transfer learning) | Visual freshness from photo | val_acc > 85% |
| LSTM | 2-layer LSTM | Sensor risk from 24h gas/temp readings | val_AUC > 0.90 |
| Fusion | XGBoost | Final spoilage probability + days to spoilage | — |

---

### 📊 Sensor Data

Ethylene ranges (USDA-cited):

| Produce | Ethylene (ppm) | Shelf Life |
|---------|---------------|------------|
| Apple   | 1.2 – 25      | 14 days |
| Banana  | 8.5 – 50      | 7 days  |
| Tomato  | 2.1 – 20      | 10 days |
| Mango   | 3.4 – 30      | 8 days  |
