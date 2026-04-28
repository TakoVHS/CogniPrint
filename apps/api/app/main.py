from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

import stripe
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from cogniprint.analysis import analyze_text
except Exception:  # pragma: no cover
    analyze_text = None

DISCLAIMER = (
    "CogniPrint outputs are statistical and heuristic profile signals. "
    "They are not legal conclusions, source guarantees, authorship guarantees, "
    "or final judgments about a text."
)

FREE_DAILY_LIMIT = 3
PRO_PRICE_USD_MONTHLY = 199

# MVP in-memory quota store. Replace with Postgres before production traffic.
USAGE: dict[str, dict[str, int]] = {}
SUBSCRIPTIONS: dict[str, dict[str, Any]] = {}

app = FastAPI(title="CogniPrint Content Scanner API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    text: str = Field(min_length=1, max_length=120000)
    user_id: str = Field(default="anonymous", max_length=160)


class CheckoutRequest(BaseModel):
    user_id: str = Field(default="anonymous", max_length=160)
    email: str | None = Field(default=None, max_length=320)


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _is_pro(user_id: str) -> bool:
    state = SUBSCRIPTIONS.get(user_id, {})
    return state.get("plan") in {"pro", "enterprise"} and state.get("status") in {"active", "trialing", "enterprise"}


def _quota_remaining(user_id: str) -> int | None:
    if _is_pro(user_id):
        return None
    day = _today()
    used = USAGE.get(user_id, {}).get(day, 0)
    return max(FREE_DAILY_LIMIT - used, 0)


def _consume_quota(user_id: str) -> int | None:
    if _is_pro(user_id):
        return None
    day = _today()
    USAGE.setdefault(user_id, {})
    used = USAGE[user_id].get(day, 0)
    if used >= FREE_DAILY_LIMIT:
        raise HTTPException(status_code=402, detail="Free daily scan limit reached. Upgrade to Pro.")
    USAGE[user_id][day] = used + 1
    return max(FREE_DAILY_LIMIT - USAGE[user_id][day], 0)


def _fallback_profile(text: str) -> dict[str, Any]:
    words = [word for word in text.replace("\n", " ").split(" ") if word.strip()]
    word_count = len(words)
    unique_count = len(set(word.lower() for word in words))
    char_count = len(text)
    fingerprint = {
        "log_char_count": float(char_count),
        "log_word_count": float(word_count),
        "type_token_ratio": round(unique_count / max(word_count, 1), 6),
        "avg_word_length": round(sum(len(word) for word in words) / max(word_count, 1), 6),
        "punctuation_ratio": round(sum(1 for char in text if char in ".,;:!?") / max(char_count, 1), 6),
    }
    return {
        "metrics": {"char_count": char_count, "word_count": word_count, "unique_word_count": unique_count},
        "fingerprint": fingerprint,
        "fingerprint_vector": list(fingerprint.values()),
        "content_hash": sha256(text.encode("utf-8")).hexdigest(),
    }


def _profile(text: str) -> dict[str, Any]:
    if analyze_text is None:
        return _fallback_profile(text)
    result = analyze_text(text)
    return {
        "metrics": result.metrics,
        "fingerprint": result.fingerprint,
        "fingerprint_vector": result.fingerprint_vector,
        "content_hash": result.content_hash,
    }


def _insights(profile: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = profile["metrics"]
    fingerprint = profile["fingerprint"]
    word_count = int(metrics.get("word_count", 0))
    ttr = float(fingerprint.get("type_token_ratio", 0.0))
    sentence_len = float(fingerprint.get("avg_sentence_length_words", 0.0))
    punctuation = float(fingerprint.get("punctuation_ratio", 0.0))
    return [
        {"title": "Lexical diversity", "value": round(ttr, 3), "severity": "high" if ttr > 0.72 else "medium"},
        {"title": "Text stability", "value": word_count, "severity": "low" if word_count >= 120 else "medium"},
        {"title": "Sentence cadence", "value": round(sentence_len, 2), "severity": "medium" if sentence_len > 32 else "low"},
        {"title": "Punctuation load", "value": round(punctuation, 3), "severity": "medium" if punctuation > 0.08 else "low"},
    ]


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "service": "cogniprint-content-scanner-api", "version": "0.1.0"}


@app.post("/scan")
def scan(payload: ScanRequest) -> dict[str, Any]:
    remaining = _consume_quota(payload.user_id)
    profile = _profile(payload.text)
    return {
        "disclaimer": DISCLAIMER,
        "plan": "pro" if _is_pro(payload.user_id) else "free",
        "quota_remaining_today": remaining,
        "metrics": profile["metrics"],
        "fingerprint": profile["fingerprint"],
        "fingerprint_vector": profile["fingerprint_vector"],
        "content_hash": profile["content_hash"],
        "insight_cards": _insights(profile),
    }


@app.post("/billing/create-checkout-session")
def create_checkout_session(payload: CheckoutRequest, request: Request) -> dict[str, str]:
    import os

    secret_key = os.getenv("STRIPE_SECRET_KEY")
    price_id = os.getenv("STRIPE_PRO_PRICE_ID")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    if not secret_key or not price_id:
        raise HTTPException(status_code=503, detail="Stripe is not configured.")

    stripe.api_key = secret_key
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        customer_email=payload.email,
        client_reference_id=payload.user_id,
        metadata={"user_id": payload.user_id, "plan": "pro"},
        success_url=f"{frontend_url}/app?checkout=success",
        cancel_url=f"{frontend_url}/pricing?checkout=cancelled",
        allow_promotion_codes=True,
    )
    return {"url": session.url}


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default="")) -> dict[str, bool]:
    import os

    secret_key = os.getenv("STRIPE_SECRET_KEY")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not secret_key or not webhook_secret:
        raise HTTPException(status_code=503, detail="Stripe webhook is not configured.")

    stripe.api_key = secret_key
    body = await request.body()
    try:
        event = stripe.Webhook.construct_event(body, stripe_signature, webhook_secret)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid webhook: {exc}") from exc

    event_type = event["type"]
    data = event["data"]["object"]
    if event_type == "checkout.session.completed":
        user_id = data.get("client_reference_id") or data.get("metadata", {}).get("user_id")
        if user_id:
            SUBSCRIPTIONS[user_id] = {"plan": "pro", "status": "active", "stripe_customer_id": data.get("customer")}
    elif event_type in {"customer.subscription.deleted", "customer.subscription.paused", "invoice.payment_failed"}:
        # MVP: real production implementation should map Stripe customer/subscription IDs to persisted users.
        pass

    return {"received": True}
