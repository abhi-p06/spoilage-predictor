<div align="center">

# 🌾 AgriRoute — Post-Harvest Spoilage Predictor

**AI-powered spoilage risk forecasting for Indian farmers, before the damage is visible.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-Fusion-189AB4?style=flat-square)](https://xgboost.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

</div>

---

## 🚨 The Problem

India loses **₹92,000 crore (~$11B) worth of fruits and vegetables every year** to post-harvest spoilage — **30–40% of total produce**. Small farmers have no early-warning system. By the time spoilage is visible, it's too late to sell.

**AgriRoute changes that.** A farmer uploads a photo of their produce, enters three simple details, and gets a real-time RED/YELLOW/GREEN risk alert — *before* visible rot begins.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📸 **Visual Freshness Analysis** | MobileNetV2 CNN scores produce freshness from a photo |
| 📡 **Sensor Risk Modeling** | BiLSTM reads 24-hour atmospheric sensor patterns (ethylene, CO₂, humidity, temperature) |
| 🧠 **Fusion Prediction** | XGBoost combines CNN + LSTM outputs with farm metadata for a final spoilage % |
| 🗺️ **Route-Aware Alerts** | Leaflet map + OSRM routing — predicts risk given actual transport distance |
| 💰 **Live Mandi Prices** | Fetches real wholesale market prices from data.gov.in (AGMARKNET API) with 3-day forecast |
| 📱 **SMS Alerts** | Sends Twilio SMS to the farmer's mobile when risk is HIGH |
| 📄 **Downloadable Reports** | One-click `.txt` report of every prediction |
| 🔄 **Graceful Fallbacks** | App runs fully without trained models, using calibrated heuristics |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FARMER INPUT                                 │
│   📸 Photo  +  🌾 Produce Type  +  📅 Days Since Harvest  +  ❄️ Cold Chain │
└──────────────────────┬──────────────────────────────────────────────┘
                       │
           ┌───────────▼───────────┐
           │                       │
    ┌──────▼──────┐       ┌────────▼────────┐
    │  CNN Stage  │       │   LSTM Stage    │
    │ MobileNetV2 │       │   BiLSTM(64,32) │
    │ (ImageNet + │       │ 24h × 4 sensors │
    │  fine-tune) │       │   (simulated)   │
    └──────┬──────┘       └────────┬────────┘
           │  freshness_score      │  lstm_risk
           │     ∈ [0,1]          │   ∈ [0,1]
           └──────────┬───────────┘
                      │
             ┌────────▼────────┐
             │  XGBoost Fusion │
             │  Classifier +   │
             │  Regressor      │
             │  (5 features)   │
             └────────┬────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
    Spoilage %   Days to Sell  Alert Level
                               🟢/🟡/🔴
```

### Three-Model Pipeline

| Stage | Model | Input | Output |
|---|---|---|---|
| **1 — Vision** | MobileNetV2 (CNN) | 224×224 produce photo | `freshness_score` ∈ [0,1] |
| **2 — Sensors** | Bidirectional LSTM | (24, 4) hourly sensor sequence | `lstm_risk` ∈ [0,1] |
| **3 — Fusion** | XGBoost (×2) | CNN score + LSTM risk + days + cold chain + produce ID | `spoilage_probability` % + `days_to_spoilage` |

---

## 📊 Model Performance

| Model | Metric | Score |
|---|---|---|
| CNN (MobileNetV2) | Validation Accuracy | **97.22%** |
| BiLSTM | Validation AUC | **1.000** |
| XGBoost Fusion | Classifier accuracy on held-out set | **>95%** |

> **Note:** LSTM was trained on synthetic sensor data generated using USDA Handbook 66 ethylene ranges. Real IoT sensor deployment would be the next production step.

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/abhi-p06/spoilage-predictor.git
cd spoilage-predictor
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your API keys (see Configuration section below)
```

### 3. Train the models

```bash
# Download the Kaggle dataset first
python download_dataset.py

# Generate synthetic sensor data
python generate_sensor_data.py

# Run the full training pipeline (CNN → LSTM → XGBoost)
python train_all.py
```

> ⏱️ **Training time:** ~10–20 min on Apple Silicon (M-series) with `tensorflow-metal`. CPU-only will take longer.

### 4. Launch the app

```bash
cd app
python app.py
# Open http://localhost:5000
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and fill in:

| Variable | Description | Required |
|---|---|---|
| `FLASK_SECRET_KEY` | Random secret for Flask sessions | ✅ Yes |
| `DATA_GOV_API_KEY` | [data.gov.in](https://data.gov.in) API key for live mandi prices | ✅ For live prices |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | ✅ For SMS alerts |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | ✅ For SMS alerts |
| `TWILIO_FROM_NUMBER` | Your Twilio phone number (e.g. `+1415XXXXXXX`) | ✅ For SMS alerts |

> **Without API keys:** The app runs fully — mandi prices fall back to deterministic estimates, and SMS alerts are silently skipped.

---

## 📁 Project Structure

```
spoilage-predictor/
├── app/
│   ├── app.py                  # Flask routes (/, /predict, /report)
│   ├── predict.py              # Inference pipeline (CNN → LSTM → XGBoost)
│   ├── mandi_prices.py         # AGMARKNET live price fetcher + cache
│   ├── sms_alerts.py           # Twilio SMS module
│   ├── templates/
│   │   ├── index.html          # Input form (Leaflet map, route selector)
│   │   └── result.html         # Result dashboard (gauge, timeline, mandi card)
│   └── static/
│       └── style.css           # Full custom CSS (Inter font, green theme)
│
├── data/
│   ├── images/                 # Kaggle fruit images (gitignored)
│   └── sensors/
│       └── sample_input.csv    # 24-row sample sensor sequence
│
├── models/                     # Trained model files (gitignored, generated by training)
│   └── lstm_scaler.pkl         # StandardScaler (committed)
│
├── notebooks/                  # Training notebooks & EDA plots
├── reports/
│   ├── pitch_preparation.md    # Viva prep guide (for college presentation)
│   └── research_brief.md       # Academic literature survey
│
├── download_dataset.py         # Kaggle dataset downloader
├── generate_sensor_data.py     # Synthetic IoT sensor data generator
├── train_all.py                # Full training pipeline
└── requirements.txt
```

---

## 🌾 Supported Produce

| Produce | Shelf Life (no cold) | Cold Chain Multiplier |
|---|---|---|
| 🍎 Apple | 14 days | ×1.6 |
| 🍌 Banana | 7 days | ×1.6 |
| 🍅 Tomato | 10 days | ×1.6 |
| 🥭 Mango | 8 days | ×1.6 |

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

**Good first issues:**
- Add more produce types (potato, onion, grapes)
- Real IoT sensor integration (MQTT / LoRaWAN)
- Multi-language UI (Hindi, Marathi, Tamil)
- Mobile PWA version

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- **Dataset:** [Fresh and Rotten Fruits](https://www.kaggle.com/datasets/sriramr/fruits-fresh-and-rotten-for-classification) by Sriram R on Kaggle
- **Sensor parameters:** [USDA Handbook 66](https://www.ams.usda.gov/sites/default/files/media/USDA_Handbook_66.pdf) — Commercial Storage of Fruits, Vegetables, and Florist and Nursery Stocks
- **Market prices:** [data.gov.in AGMARKNET](https://data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070) — Government of India Open Data
- **MobileNetV2:** Howard et al., 2018 — *Inverted Residuals and Linear Bottlenecks*

---

<div align="center">
  Built with ❤️ for SY B.Tech AI & Data Science · AgriRoute 2026
</div>
