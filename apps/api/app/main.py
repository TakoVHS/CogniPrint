from __future__ import annotations

import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

import stripe
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import (
    ScanRecord,
    activate_pro,
    create_tables,
    downgrade_by_customer,
    downgrade_subscription,
    ensure_account,
    get_daily_usage,
    get_db,
    increment_daily_usage,
    is_pro_account,
)

try:
    from cogniprint.analysis import analyze_text
except Exception:  # pragma: no cover
    analyze_text = None

DISCLAIMER = (
    "CogniPrint outputs are statistical and heuristic profile signals. "
    "They are not legal conclusions, source guarantees, authorship guarantees, "
    "or final judgments about a text."
)

PRO_PRICE_USD_MONTHLY = 199


def _free_daily_limit() -> int:
    return int(os.getenv("FREE_DAILY_SCAN_LIMIT", "3"))


def _max_text_chars(is_pro: bool) -> int:
    if is_pro:
        return int(os.getenv("MAX_TEXT_CHARS_PRO", "120000"))
    return int(os.getenv("MAX_TEXT_CHARS_FREE", "12000"))


def _cors_origins() -> list[str]:
    frontend = os.getenv("FRONTEND_URL", "")
    if frontend:
        return [frontend]
    return ["*"]


@asynccontextmanager
async def lifespan(application: FastAPI):  # type: ignore[type-arg]
    create_tables()
    yield


app = FastAPI(title="CogniPrint Content Scanner API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
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


def _today() -> datetime.date:  # type: ignore[return-value]
    return datetime.now(timezone.utc).date()


def _consume_quota(db: Session, user_id: str) -> int | None:
    """Check and increment daily scan quota. Returns remaining count or None for Pro."""
    if is_pro_account(db, user_id):
        return None
    limit = _free_daily_limit()
    day = _today()
    used = get_daily_usage(db, user_id, day)
    if used >= limit:
        raise HTTPException(status_code=402, detail="Free daily scan limit reached. Upgrade to Pro.")
    new_count = increment_daily_usage(db, user_id, day)
    return max(limit - new_count, 0)


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
def scan(payload: ScanRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    ensure_account(db, payload.user_id)
    pro = is_pro_account(db, payload.user_id)
    max_chars = _max_text_chars(pro)
    if len(payload.text) > max_chars:
        raise HTTPException(status_code=413, detail=f"Text exceeds {max_chars} character limit for your plan.")
    remaining = _consume_quota(db, payload.user_id)
    profile = _profile(payload.text)
    record = ScanRecord(
        user_id=payload.user_id,
        plan_at_scan="pro" if pro else "free",
        content_hash=profile["content_hash"],
        char_count=profile["metrics"].get("char_count", 0),
        word_count=profile["metrics"].get("word_count", 0),
    )
    db.add(record)
    db.commit()
    return {
        "disclaimer": DISCLAIMER,
        "plan": "pro" if pro else "free",
        "quota_remaining_today": remaining,
        "metrics": profile["metrics"],
        "fingerprint": profile["fingerprint"],
        "fingerprint_vector": profile["fingerprint_vector"],
        "content_hash": profile["content_hash"],
        "insight_cards": _insights(profile),
    }


@app.post("/billing/create-checkout-session")
def create_checkout_session(
    payload: CheckoutRequest, request: Request, db: Session = Depends(get_db)
) -> dict[str, str]:
    secret_key = os.getenv("STRIPE_SECRET_KEY")
    price_id = os.getenv("STRIPE_PRO_PRICE_ID")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    if not secret_key or not price_id:
        raise HTTPException(status_code=503, detail="Stripe is not configured.")

    ensure_account(db, payload.user_id, payload.email)
    db.commit()

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
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(default=""),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
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
            activate_pro(
                db,
                user_id=user_id,
                stripe_customer_id=data.get("customer"),
                stripe_subscription_id=data.get("subscription"),
            )

    elif event_type == "customer.subscription.deleted":
        sub_id = data.get("id")
        customer_id = data.get("customer")
        if sub_id:
            downgrade_subscription(db, sub_id, "cancelled")
        elif customer_id:
            downgrade_by_customer(db, customer_id, "cancelled")

    elif event_type == "customer.subscription.paused":
        sub_id = data.get("id")
        customer_id = data.get("customer")
        if sub_id:
            downgrade_subscription(db, sub_id, "paused")
        elif customer_id:
            downgrade_by_customer(db, customer_id, "paused")

    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer")
        sub_id = data.get("subscription")
        if sub_id:
            downgrade_subscription(db, sub_id, "past_due")
        elif customer_id:
            downgrade_by_customer(db, customer_id, "past_due")

    return {"received": True}
