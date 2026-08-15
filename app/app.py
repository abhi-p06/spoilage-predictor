"""
app.py
======
Flask web application — Post-Harvest Spoilage Predictor / AgriRoute.

Routes
------
GET  /          → Input form with Leaflet map + dropdowns  (index.html)
POST /predict   → Runs prediction pipeline, live mandi price, SMS alert
GET  /report    → Plain-text .txt download of the last prediction

New in this version
-------------------
- Feature 1: live mandi price via mandi_prices.fetch_mandi_price()
- Feature 2: Twilio SMS alert via sms_alerts.send_risk_sms()
- Feature 3: accepts origin / destination / distance from the
             Leaflet map front-end (or falls back to dropdown values)
"""

import json
import logging
import os
from datetime import datetime, timedelta, date
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from werkzeug.utils import secure_filename

from predict       import run_prediction
from mandi_prices  import fetch_mandi_price
from sms_alerts    import send_risk_sms

load_dotenv()                                  # reads .env into os.environ

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger(__name__)

# ── Flask setup ────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "agriroute-dev-secret-2025")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024   # 16 MB


# ── City → state mapping for AGMARKNET queries ─────────────────────────────────
CITY_STATE: dict[str, str] = {
    "Mumbai":    "Maharashtra",
    "Nashik":    "Maharashtra",
    "Pune":      "Maharashtra",
    "Nagpur":    "Maharashtra",
    "Delhi":     "Delhi",
    "Bangalore": "Karnataka",
    "Bengaluru": "Karnataka",
    "Chennai":   "Tamil Nadu",
    "Hyderabad": "Telangana",
    "Kolkata":   "West Bengal",
    "Ahmedabad": "Gujarat",
    "Surat":     "Gujarat",
    "Jaipur":    "Rajasthan",
    "Lucknow":   "Uttar Pradesh",
    "Chandigarh":"Punjab",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def _sell_by_str(days_to_spoilage: int) -> str:
    """Return a human-readable sell-by date string, e.g. '25 Jul 2026'."""
    sell_date = date.today() + timedelta(days=max(days_to_spoilage, 0))
    return sell_date.strftime("%-d %b %Y")


def _build_estimated_mandi(produce: str, destination: str) -> dict:
    """
    Reproduce the original estimated price card so we always have something
    to render even without an API key.  Matches the shape returned by
    fetch_mandi_price() but with source='estimated'.
    """
    import hashlib, math
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
        forecast.append({
            "date":  fdate.strftime("%a %-d %b"),
            "price": int(fprice),
            "pct":   fpct,
        })

    if slope > 5:
        trend = "Rising"
    elif slope < -5:
        trend = "Falling"
    else:
        trend = "Stable"

    return {
        "modal_price":  current,
        "trend":        trend,
        "pct_change":   round(slope * 7 / current * 100, 1),
        "forecast":     forecast,
        "source":       "estimated",
        "market":       destination,
        "records_used": 0,
        "last_date":    today.strftime("%-d %b %Y"),
    }


def _sell_advice(trend: str) -> str:
    return {
        "Rising":  "Price is rising — consider holding 1–2 days if storage allows.",
        "Falling": "Price is falling — sell as soon as possible.",
        "Stable":  "Price is stable. Current window is good to sell.",
    }.get(trend, "Sell at your earliest convenience.")


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Render the input form (now includes Leaflet map for route selection)."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Accept form submission, run the three-model pipeline, fetch live mandi
    price, optionally send SMS, and render the result dashboard.

    New form fields (Feature 2 + 3)
    --------------------------------
    mobile      : str  — optional Indian mobile number (10 digits or with +91)
    origin      : str  — origin city / geocoded label from map
    destination : str  — destination mandi city / geocoded label from map
    distance_km : float (optional) — driving distance from OSRM
    origin_lat / origin_lng / dest_lat / dest_lng : hidden fields from map
    """
    # ── Validate image ─────────────────────────────────────────────────────────
    if "image" not in request.files:
        return redirect(url_for("index"))

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return redirect(url_for("index"))

    # ── Save uploaded image ────────────────────────────────────────────────────
    filename  = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_name = f"{timestamp}_{filename}"
    save_path = UPLOAD_DIR / save_name
    file.save(save_path)

    # ── Parse core form inputs ─────────────────────────────────────────────────
    produce    = request.form.get("produce",    "tomato").lower().strip()
    days       = int(request.form.get("days",   3))
    cold_chain = request.form.get("cold_chain", "no").lower() == "yes"

    # ── Feature 3: route inputs from Leaflet map or dropdown ──────────────────
    origin      = request.form.get("origin",      "").strip() or "Origin"
    destination = request.form.get("destination", "").strip() or "Destination"
    distance_km = None
    raw_dist    = request.form.get("distance_km", "").strip()
    if raw_dist:
        try:
            distance_km = float(raw_dist)
        except ValueError:
            pass

    # Map pins (passed through to result for re-rendering the route)
    origin_lat  = request.form.get("origin_lat",  "")
    origin_lng  = request.form.get("origin_lng",  "")
    dest_lat    = request.form.get("dest_lat",    "")
    dest_lng    = request.form.get("dest_lng",    "")

    # ── Feature 2: optional mobile number ─────────────────────────────────────
    mobile_raw = request.form.get("mobile", "").strip()

    # ── Run core prediction pipeline ──────────────────────────────────────────
    result = run_prediction(
        image_path  = save_path,
        produce     = produce,
        days        = days,
        cold_chain  = cold_chain,
    )

    # ── Feature 1: live mandi price ───────────────────────────────────────────
    dest_state  = CITY_STATE.get(destination, "Maharashtra")
    mandi_data  = None
    try:
        mandi_data = fetch_mandi_price(
            produce     = produce,
            destination = destination,
            state       = dest_state,
        )
    except Exception as exc:
        log.warning("mandi_prices error: %s", exc)

    if mandi_data is None:
        mandi_data = _build_estimated_mandi(produce, destination)

    mandi_data["sell_advice"] = _sell_advice(mandi_data["trend"])

    # ── Sell-by date string (used in SMS + result display) ────────────────────
    sell_by = _sell_by_str(result.get("days_to_spoilage", 0))

    # ── Feature 2: send SMS if risk is HIGH and mobile supplied ───────────────
    sms_status: dict = {"sent": None, "sid": None, "reason": "No mobile provided"}
    alert_level = result.get("alert", "green")

    if mobile_raw and alert_level == "red":
        try:
            sms_status = send_risk_sms(
                to_number    = mobile_raw,
                produce      = produce.capitalize(),
                risk_pct     = result.get("spoilage_pct", 0),
                origin       = origin,
                destination  = destination,
                sell_by_date = sell_by,
                blocking     = False,   # fire-and-forget thread
            ) or sms_status
        except Exception as exc:
            log.warning("SMS send error: %s", exc)
            sms_status = {"sent": False, "sid": None, "reason": str(exc)}

    # ── Assemble final result dict ─────────────────────────────────────────────
    result.update({
        "image_url":   f"uploads/{save_name}",
        "produce":     produce.capitalize(),
        "days":        days,
        "cold_chain":  "Yes" if cold_chain else "No",
        "timestamp":   datetime.now().strftime("%d %b %Y, %H:%M"),
        "sell_by":     sell_by,

        # Route
        "origin":      origin,
        "destination": destination,
        "distance_km": distance_km,
        "origin_lat":  origin_lat,
        "origin_lng":  origin_lng,
        "dest_lat":    dest_lat,
        "dest_lng":    dest_lng,

        # Mandi price
        "mandi":       mandi_data,

        # SMS
        "sms":         sms_status,
        "mobile_provided": bool(mobile_raw),
    })

    session["last_result"] = json.dumps(result, default=str)
    return render_template("result.html", r=result)


@app.route("/report")
def report():
    """Generate and download a plain-text summary of the last prediction."""
    raw = session.get("last_result")
    if not raw:
        return redirect(url_for("index"))

    r = json.loads(raw)
    mandi = r.get("mandi", {})

    lines = [
        "=" * 60,
        "  AGRIROUTE — POST-HARVEST SPOILAGE ANALYSIS REPORT",
        "=" * 60,
        f"  Generated   : {r.get('timestamp', 'N/A')}",
        f"  Produce     : {r.get('produce', 'N/A')}",
        f"  Route       : {r.get('origin','?')} → {r.get('destination','?')}",
        "",
        "  PREDICTION RESULTS",
        "  " + "-" * 40,
        f"  Alert Level          : {r.get('alert', 'N/A').upper()}",
        f"  Spoilage Probability : {r.get('spoilage_pct', 0):.1f}%",
        f"  Days to Spoilage     : {r.get('days_to_spoilage', 0)} days",
        f"  Sell By              : {r.get('sell_by', 'N/A')}",
        f"  CNN Freshness Score  : {r.get('cnn_score_pct', 0):.1f}%",
        f"  Sensor Risk Score    : {r.get('lstm_score_pct', 0):.1f}%",
        "",
        "  MANDI PRICE",
        "  " + "-" * 40,
        f"  Market     : {mandi.get('market', 'N/A')} ({mandi.get('source', 'N/A')})",
        f"  Modal Price: ₹{mandi.get('modal_price', 0):.0f} /quintal",
        f"  Trend      : {mandi.get('trend', 'N/A')} ({mandi.get('pct_change', 0):+.1f}%)",
        "",
        "  INPUT DETAILS",
        "  " + "-" * 40,
        f"  Days Since Harvest   : {r.get('days', 'N/A')}",
        f"  Cold Chain Storage   : {r.get('cold_chain', 'N/A')}",
        f"  Typical Shelf Life   : {r.get('shelf_life', 'N/A')} days",
        "",
        "  RECOMMENDATION",
        "  " + "-" * 40,
        f"  {r.get('recommendation', 'N/A')}",
        "",
        "=" * 60,
        "  AgriRoute AI — Post-Harvest Spoilage Predictor",
        "  Educational / Research use only.",
        "=" * 60,
    ]

    txt_content = "\n".join(lines)
    safe_ts     = r.get("timestamp", "report").replace(" ", "_").replace(",", "")
    report_path = UPLOAD_DIR / f"report_{safe_ts}.txt"
    report_path.write_text(txt_content, encoding="utf-8")

    return send_file(report_path, as_attachment=True, download_name="agriroute_report.txt")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
