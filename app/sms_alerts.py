"""
sms_alerts.py
=============
Feature 2 — Twilio SMS alerts for HIGH-risk predictions.

Reads credentials from environment variables loaded via python-dotenv:
    TWILIO_ACCOUNT_SID   — from console.twilio.com
    TWILIO_AUTH_TOKEN    — from console.twilio.com
    TWILIO_FROM_NUMBER   — your Twilio phone number, e.g. +1415XXXXXXX

The send_risk_sms() function is intentionally non-blocking: it catches
all Twilio exceptions and returns a status dict so the caller (app.py)
can show an inline status on the result page without crashing.
"""

from __future__ import annotations

import logging
import os
import threading
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)


def _do_send(
    to_number: str,
    body: str,
    account_sid: str,
    auth_token: str,
    from_number: str,
) -> dict:
    """
    Internal: perform the Twilio API call.
    Always returns a status dict — never raises.
    """
    try:
        from twilio.rest import Client          # lazy import — avoids startup cost
        from twilio.base.exceptions import TwilioRestException

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number,
        )
        log.info("SMS sent: SID=%s to=%s", message.sid, to_number)
        return {"sent": True, "sid": message.sid, "reason": None}

    except ImportError:
        reason = "twilio package not installed"
        log.warning(reason)
        return {"sent": False, "sid": None, "reason": reason}

    except Exception as exc:                   # TwilioRestException or network err
        reason = str(exc)
        log.warning("SMS send failed: %s", reason)
        return {"sent": False, "sid": None, "reason": reason}


def send_risk_sms(
    to_number: str,
    produce: str,
    risk_pct: float,
    origin: str,
    destination: str,
    sell_by_date: str,
    blocking: bool = False,
) -> Optional[dict]:
    """
    Send an SMS alert for a HIGH-risk prediction.

    Parameters
    ----------
    to_number    : str   — recipient mobile number (with country code, e.g. +919876543210)
    produce      : str   — produce type capitalised ("Tomato")
    risk_pct     : float — combined risk percentage (0–100)
    origin       : str   — origin city
    destination  : str   — destination city
    sell_by_date : str   — recommended sell-by date string
    blocking     : bool  — if True, send synchronously (useful in tests)

    Returns
    -------
    dict with keys sent (bool), sid (str|None), reason (str|None)
    or None if Twilio credentials are missing.
    """
    account_sid  = os.environ.get("TWILIO_ACCOUNT_SID",  "")
    auth_token   = os.environ.get("TWILIO_AUTH_TOKEN",   "")
    from_number  = os.environ.get("TWILIO_FROM_NUMBER",  "")

    # Validate credentials present
    missing = [k for k, v in {
        "TWILIO_ACCOUNT_SID": account_sid,
        "TWILIO_AUTH_TOKEN":  auth_token,
        "TWILIO_FROM_NUMBER": from_number,
    }.items() if not v]

    if missing:
        log.info("SMS skipped — missing env vars: %s", missing)
        return {"sent": False, "sid": None, "reason": f"Missing: {', '.join(missing)}"}

    # Normalise phone: ensure +91 prefix for Indian numbers
    number = to_number.strip()
    if number.isdigit() and len(number) == 10:
        number = f"+91{number}"
    elif not number.startswith("+"):
        number = f"+{number}"

    body = (
        f"⚠️ AgriRoute HIGH RISK ALERT\n"
        f"Produce: {produce}\n"
        f"Route: {origin} → {destination}\n"
        f"Combined Risk: {risk_pct:.0f}%\n"
        f"Sell by: {sell_by_date}\n"
        f"Act now to avoid losses. — AgriRoute AI"
    )

    if blocking:
        return _do_send(number, body, account_sid, auth_token, from_number)

    # Fire-and-forget in a daemon thread so it doesn't block the response
    result_holder: dict[str, Optional[dict]] = {}

    def _thread_target():
        result_holder["r"] = _do_send(
            number, body, account_sid, auth_token, from_number
        )

    t = threading.Thread(target=_thread_target, daemon=True, name="sms-alert")
    t.start()

    # Return an optimistic status immediately; the thread logs the real outcome
    return {"sent": None, "sid": None, "reason": "sending in background"}
