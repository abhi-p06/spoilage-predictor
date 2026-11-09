# Forensic Audit 04: Transport Routing & AGMARKNET Market Price Module

> **Audit Date:** 2026-11-09  
> **Auditor:** Independent Scientific Auditor  
> **Target Systems:** Route Risk Estimator & AGMARKNET Price Trend Forecaster  
> **Primary Scripts:** `app/app.py`, `app/predict.py`, `app/mandi_prices.py`, `app/templates/index.html`  
> **Manuscript Claims:** 
> 1. Road distance and inter-state transit multipliers compute route risk $G = \text{clip}(\alpha \tau D - \beta c, 0, 100)$.
> 2. AGMARKNET daily prices are pulled live at request time and short-horizon forecasts guide farmer market decisions.

---

## 1. Executive Summary & Verdict

| Component | Manuscript Claim | Code Implementation Reality | Classification |
|---|---|---|---|
| **Route Distance ($D$)** | Computed via mapping backend | Fetched client-side via public OSRM in JavaScript (`index.html` line 672) | `CALCULATED (CLIENT)` |
| **Route Impact on Spoilage Risk** | Asserts distance $D$ drives route risk $G$ in Eq. (2) | **Distance $D$ is completely ignored by the prediction pipeline!** | `UNSUPPORTED (GHOST CODE)` |
| **Transport Multiplier ($\tau$)** | Inter-state multiplier $\tau$ increases risk | **Does not exist in the codebase**; never parsed or computed | `UNSUPPORTED (GHOST VARIABLE)` |
| **Cold-Chain Multiplier** | Refrigeration parameter $\beta$ reduces risk | Hardcoded heuristic: extends shelf life by 60% (`COLD_CHAIN_MULT = 1.6`) | `ASSUMED` |
| **AGMARKNET Live API** | Live government portal queries at request time | Implemented in `app/mandi_prices.py`, but requires uncommitted API key | `FETCHED (OPTIONAL)` |
| **Mandi Price Default / Fallback** | Not disclosed in paper | **MD5 hash of produce + destination name** (`app/app.py` line 91) | `SIMULATED (HASH ARTIFACT)` |
| **Price Forecasting** | Described as short-horizon price forecasting | 2-point linear slope extrapolation; no ML model (no ARIMA/LSTM) | `HEURISTIC CALCULATION` |
| **Case Study (Guntur $\to$ Rajkot)** | Live system demonstration of a banana shipment | Run on local mock server with $N=0$ physical produce or transport | `SOFTWARE SIMULATION` |

---

## 2. Forensic Breakdown of Route Risk & Discrepancies

### 2.1 The Client-Side Distance Fetching
In `app/templates/index.html` (lines 671–685):
```javascript
const url = `https://router.project-osrm.org/route/v1/driving/${oLng},${oLat};${dLng},${dLat}?overview=full&geometries=geojson`;
const resp = await fetch(url);
const data = await resp.json();
const route = data.routes[0];
const distKm = (route.distance / 1000).toFixed(1);
document.getElementById('distance_km').value = distKm;
```
- The road network route and distance are computed purely in the client's browser via the public Project-OSRM demo server (`router.project-osrm.org`).
- The coordinates and `distKm` are posted to `/predict` in `app/app.py`.

### 2.2 Ghost Equation 2: The Severed Route Connection
In `main.tex` Section VI-B:
$$\text{Eq. (2): } G = \operatorname{clip}\bigl(\alpha \tau D - \beta c,\ 0,\ 100\bigr)$$
$$\text{Eq. (3): } S = w_1 V + w_2 G$$

Now look at `app/app.py` lines 180–205:
```python
# app.py line 183
raw_dist = request.form.get("distance_km", "").strip()
if raw_dist:
    distance_km = float(raw_dist)

# app.py line 200
result = run_prediction(
    image_path  = save_path,
    produce     = produce,
    days        = days,
    cold_chain  = cold_chain,
)
```
- **The Severed Link:** `distance_km` is parsed from the form on line 186, but line 200 calls `run_prediction(save_path, produce, days, cold_chain)`.
- **`distance_km` is NEVER passed into the prediction function!**
- Inside `predict.py`, neither `predict_cnn`, `predict_lstm`, nor `predict_fusion` accepts a distance parameter.
- On line 258 of `app/app.py`, `distance_km` is merely attached to the result dictionary so it can be echoed back into the HTML template!
- **Audit Finding:** A shipment traveling 15 km has the **exact same calculated spoilage risk and days-to-spoilage** as a shipment traveling 3,000 km. The route-risk formulation in the paper is completely fictitious relative to the codebase.

---

## 3. Forensic Breakdown of AGMARKNET Market Prices

### 3.1 The Live API Integration (`app/mandi_prices.py`)
- **API Endpoint:** `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070`
- **Query Filter:** `filters[commodity]`, `filters[state]`, `filters[market]`
- **Authentication:** Requires `DATA_GOV_API_KEY` in environment variables.
- **Record Parsing:** Filters records within the last 14 days and extracts `modal_price` (₹/quintal).

### 3.2 The Offline MD5 Fallback Mechanism
If `DATA_GOV_API_KEY` is not set or the network request fails, `app/app.py` falls back to `_build_estimated_mandi(produce, destination)` (lines 84–126):

```python
def _build_estimated_mandi(produce: str, destination: str) -> dict:
    import hashlib
    seed = int(hashlib.md5(f"{produce}{destination}".encode()).hexdigest(), 16)
    base_prices = {"tomato": 1650, "apple": 4200, "banana": 1800, "mango": 3500}
    base = base_prices.get(produce.lower(), 2000)
    rng  = (seed % 300) - 150
    current = base + rng
    slope   = (seed % 30) - 15

    today = date.today()
    forecast = []
    for i in range(1, 4):
        fdate  = today + timedelta(days=i)
        fprice = current + slope * i
        fpct   = round(slope * i / current * 100, 1)
        forecast.append({"date": fdate.strftime("%a %-d %b"), "price": int(fprice), "pct": fpct})

    trend = "Rising" if slope > 5 else ("Falling" if slope < -5 else "Stable")
    return {"modal_price": current, "trend": trend, "forecast": forecast, "source": "estimated", ...}
```
- **Audit Finding:** Without an API key, the mandi prices, trend direction, and 3-day forecast are generated entirely deterministically from the **MD5 hash of the string combination (e.g. `"bananarajkot"`)**!
- In the manuscript's case study (Section VII-A), the reported price trend for Rajkot was generated by this MD5 fallback function, not by a live government data transaction.

### 3.3 The "Price Forecaster" Implementation
Even when live AGMARKNET records are successfully returned:
```python
# mandi_prices.py lines 223-228
if n >= 3:
    slope = (prices[-1] - prices[-3]) / 2
elif n == 2:
    slope = prices[-1] - prices[-2]
else:
    slope = 0.0

for i in range(1, 4):
    fprice = round(current_price + slope * i, 0)
```
- **Audit Finding:** The "forecasting model" is a rudimentary 2-point linear finite difference ($\Delta y / \Delta t$). It contains no autoregressive modeling, no seasonal decomposition, no moving averages, and no machine learning.

---

## 4. Signal Classification Matrix: Truth Ledger

Every output displayed in the AgriRoute system is categorized below according to its true source:

| Pipeline Signal / Output | App Variable | True Operational Origin | Integrity Classification |
|---|---|---|---|
| Visual Freshness Score | `cnn_score_pct` | MobileNetV2 inference if weights present; otherwise MD5 uniform random `[0.45, 0.90]` | `CALCULATED / SIMULATED` |
| Sensor Spoilage Risk | `lstm_score_pct` | BiLSTM on simulated sequence if weights present; otherwise linear age heuristic | `SIMULATED` |
| Route Road Distance | `distance_km` | OSRM routing API query based on Leaflet map markers | `CALCULATED` |
| Route Spoilage Impact | N/A | **Zero impact on risk calculation**; omitted from pipeline | `UNSUPPORTED` |
| Inter-State Multiplier $\tau$ | N/A | **Does not exist in codebase** | `UNSUPPORTED` |
| Cold-Chain Multiplier | `COLD_CHAIN_MULT` | Constant $1.6$ (assumes 60% shelf life extension) | `ASSUMED` |
| Destination Mandi Price | `modal_price` | Live AGMARKNET query (if key exists) OR MD5 hash of city name | `FETCHED / SIMULATED` |
| Mandi Price Trend | `trend` | Difference between window halves OR MD5 slope | `CALCULATED / SIMULATED` |
| 3-Day Price Forecast | `forecast` | 2-point linear slope extrapolation OR MD5 slope | `HEURISTIC CALCULATION` |
| Final Spoilage Probability | `spoilage_pct` | XGBoost probability (if bundle exists) OR weighted fallback | `CALCULATED / ASSUMED` |
| Days to Spoilage | `days_to_spoilage` | XGBoost regressor (if bundle exists) OR shelf-life formula | `CALCULATED / ASSUMED` |
| Traffic Light Alert | `alert` | Threshold rules: $<35\%$ Green, $35\text{--}70\%$ Yellow, $\ge 70\%$ Red | `CALCULATED` |
| Case Study Validation | Section VII-A | 1 simulated run on a laptop with zero physical cargo or fleet | `SIMULATED` |

---

## 5. Audit Recommendations for Revision

1. **Actually Implement Route Risk in Code OR Acknowledge Prototype Separation:**
   - Either pass `distance_km` and transit hours into `predict_fusion` and train a genuine route-aware risk model, OR:
   - Transparently acknowledge in the paper that the current prototype displays route distance as an informational overlay for the driver while the spoilage engine calculates cargo state independently.
2. **Remove Fictional Equations:**
   - Remove Eq. (2) and Eq. (3) from `main.tex`. Disclose the real XGBoost feature set and fallback formula.
3. **Transparent Mandi Pricing Disclosure:**
   - Document the AGMARKNET REST API architecture clearly, but honestly state that the price trend module performs short-term linear extrapolation rather than claiming a deep time-series forecaster.
4. **Relabel Case Study as Software Demonstration:**
   - Rewrite Section VII-A to explicitly describe the Guntur $\to$ Rajkot walkthrough as an **"End-to-End Software Architecture Demonstration"**, removing all language implying it validated real-world freight savings.

