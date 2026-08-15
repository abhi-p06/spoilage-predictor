"""
mandi_prices.py
===============
Feature 1 — Live Mandi Price Data via data.gov.in AGMARKNET API.

Fetches the last 7–14 days of modal_price for a given commodity +
market from the AGMARKNET dataset (resource ID:
9ef84268-d588-465a-a308-a864a43d0070).

Fallback chain
--------------
1. Try exact commodity + market.
2. Try commodity + other markets in the same state (first hit).
3. Return None → caller falls back to the existing estimated calculation.

Cache
-----
Responses are cached in-process (dict keyed by commodity+market+date)
for CACHE_TTL_SECONDS (4 hours). The dataset updates once daily.
"""

from __future__ import annotations

import logging
import os
import time
from datetime import date, datetime, timedelta
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
AGMARKNET_API_URL = (
    "https://api.data.gov.in/resource/"
    "9ef84268-d588-465a-a308-a864a43d0070"
)
AGMARKNET_API_KEY = os.environ.get("DATA_GOV_API_KEY", "")

CACHE_TTL_SECONDS = 4 * 60 * 60   # 4 hours
REQUEST_TIMEOUT   = 8              # seconds

# In-process response cache: key → (timestamp, payload)
_cache: dict[str, tuple[float, list[dict]]] = {}

# Map produce names used in the app to AGMARKNET commodity strings
PRODUCE_TO_COMMODITY: dict[str, str] = {
    "apple":  "Apple",
    "banana": "Banana",
    "tomato": "Tomato",
    "mango":  "Mango",
}


# ── Internal helpers ───────────────────────────────────────────────────────────

def _cache_key(commodity: str, state: str, market: str) -> str:
    today = date.today().isoformat()
    return f"{commodity}|{state}|{market}|{today}"


def _is_fresh(key: str) -> bool:
    if key not in _cache:
        return False
    cached_at, _ = _cache[key]
    return (time.time() - cached_at) < CACHE_TTL_SECONDS


def _fetch_records(
    commodity: str,
    state: str,
    market: Optional[str] = None,
    limit: int = 50,
) -> list[dict]:
    """
    Fire one API request. Returns a list of record dicts or [] on any error.
    Caches the result.
    """
    if not AGMARKNET_API_KEY:
        log.debug("DATA_GOV_API_KEY not set — skipping live mandi fetch")
        return []

    cache_key = _cache_key(commodity, state, market or "__any__")
    if _is_fresh(cache_key):
        _, records = _cache[cache_key]
        return records

    # Build query params
    params: dict[str, str] = {
        "api-key": AGMARKNET_API_KEY,
        "format":  "json",
        "limit":   str(limit),
        "filters[commodity]": commodity,
        "filters[state]":     state,
    }
    if market:
        params["filters[market]"] = market

    try:
        resp = requests.get(
            AGMARKNET_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data    = resp.json()
        records = data.get("records", [])
    except Exception as exc:
        log.warning("AGMARKNET fetch error: %s", exc)
        records = []

    _cache[cache_key] = (time.time(), records)
    return records


def _parse_records(records: list[dict]) -> list[dict]:
    """
    Clean and sort records. Keep only rows with a valid modal_price and
    arrival_date in the last 14 days. Returns list sorted by date asc.
    """
    cutoff = date.today() - timedelta(days=14)
    cleaned = []
    for row in records:
        try:
            price = float(row.get("modal_price", 0) or 0)
            if price <= 0:
                continue
            raw_date = row.get("arrival_date", "")
            # AGMARKNET dates arrive as DD/MM/YYYY
            parsed_date = datetime.strptime(raw_date, "%d/%m/%Y").date()
            if parsed_date < cutoff:
                continue
            cleaned.append({
                "date":        parsed_date,
                "modal_price": price,
                "market":      row.get("market", ""),
                "variety":     row.get("variety", ""),
            })
        except (ValueError, TypeError):
            continue

    cleaned.sort(key=lambda r: r["date"])
    return cleaned


# ── Public API ─────────────────────────────────────────────────────────────────

def fetch_mandi_price(
    produce: str,
    destination: str,
    state: str = "Maharashtra",
) -> Optional[dict]:
    """
    Fetch live mandi price data for a produce + destination market.

    Parameters
    ----------
    produce     : str  — produce name used in the app (apple / banana / tomato / mango)
    destination : str  — destination city / market name (e.g. "Mumbai")
    state       : str  — state name for AGMARKNET filter (default: Maharashtra)

    Returns
    -------
    dict with keys:
        modal_price     float  — most recent modal price (₹/quintal)
        trend           str    — "Rising" | "Falling" | "Stable"
        pct_change      float  — % change over the window
        forecast        list   — 3-element list of {date, price, pct} dicts
        source          str    — "live" | "estimated"
        market          str    — actual market name used
        records_used    int    — number of records in the window
    or None if the fallback should be used.
    """
    commodity = PRODUCE_TO_COMMODITY.get(produce.lower())
    if not commodity:
        return None

    # 1. Try exact market
    records = _fetch_records(commodity, state, market=destination)
    parsed  = _parse_records(records)

    # 2. Fuzzy fallback: try state-wide search for any market
    if not parsed:
        log.info(
            "No exact records for %s @ %s — trying state-wide %s",
            commodity, destination, state,
        )
        records = _fetch_records(commodity, state)
        parsed  = _parse_records(records)

    if not parsed:
        return None    # caller uses estimated fallback

    # Build result from last N records
    prices = [r["modal_price"] for r in parsed]
    dates  = [r["date"]        for r in parsed]
    current_price = prices[-1]
    market_used   = parsed[-1]["market"] or destination

    # Trend: compare last third vs first third of the window
    n = len(prices)
    if n >= 4:
        first_half  = sum(prices[: n // 2]) / (n // 2)
        second_half = sum(prices[n // 2 :]) / (n - n // 2)
        pct_change  = (second_half - first_half) / first_half * 100
        if pct_change > 2.5:
            trend = "Rising"
        elif pct_change < -2.5:
            trend = "Falling"
        else:
            trend = "Stable"
    else:
        pct_change = 0.0
        trend = "Stable"

    # 3-day linear forecast
    forecast = []
    # Simple linear extrapolation from last 3 data points
    if n >= 3:
        slope = (prices[-1] - prices[-3]) / 2
    elif n == 2:
        slope = prices[-1] - prices[-2]
    else:
        slope = 0.0

    today = date.today()
    for i in range(1, 4):
        fdate  = today + timedelta(days=i)
        fprice = round(current_price + slope * i, 0)
        fpct   = round(slope * i / current_price * 100, 1) if current_price else 0
        forecast.append({
            "date":  fdate.strftime("%a %-d %b"),
            "price": int(fprice),
            "pct":   fpct,
        })

    return {
        "modal_price":   current_price,
        "trend":         trend,
        "pct_change":    round(pct_change, 1),
        "forecast":      forecast,
        "source":        "live",
        "market":        market_used,
        "records_used":  n,
        "last_date":     dates[-1].strftime("%-d %b %Y"),
    }
