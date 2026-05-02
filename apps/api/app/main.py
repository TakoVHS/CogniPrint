from __future__ import annotations

import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Literal

import stripe
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .billing import PLAN_LABELS, BillingSettings, get_billing_settings
from .database import (
    ScanRecord,
    activate_pro,
    create_tables,
    downgrade_by_customer,
    downgrade_subscription,
    ensure_account,
    get_account_by_user_id,
    get_daily_usage,
    get_db,
    get_subscription,
    increment_daily_usage,
    is_pro_account,
    mark_webhook_event_processed,
    set_subscription_by_customer,
    set_subscription_state,
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

STRIPE_API_VERSION = "2026-02-25.clover"


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


def _billing_public_config(settings: BillingSettings) -> dict[str, Any]:
    return settings.public_config()


def _stripe_checkout_enabled() -> bool:
    return get_billing_settings().public_config()["billing_enabled"] is True


def _require_billing_settings() -> BillingSettings:
    settings = get_billing_settings()
    if not settings.billing_enabled:
        raise HTTPException(status_code=503, detail="Billing is disabled.")
    missing = settings.missing_required()
    if missing:
        raise HTTPException(
            status_code=503,
            detail=f"Billing configuration incomplete: {', '.join(missing)}",
        )
    return settings


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
    plan: Literal["starter", "research_pro"] = "research_pro"


class PortalRequest(BaseModel):
    user_id: str = Field(default="anonymous", max_length=160)
    customer_id: str | None = Field(default=None, max_length=64)


class HealthResponse(BaseModel):
    ok: bool
    service: str
    version: str
    stripe_checkout_enabled: bool
    environment: str
    billing_mode: str


class PriceIdsResponse(BaseModel):
    starter: str | None = None
    research_pro: str | None = None


class AccountStatusResponse(BaseModel):
    user_id: str
    email: str | None = None
    plan: str
    subscription_status: str
    quota_remaining_today: int | None = None
    free_daily_scan_limit: int
    max_text_chars: int
    checkout_enabled: bool
    billing_mode: str
    price_ids: PriceIdsResponse


class BillingPlanPublic(BaseModel):
    label: str
    price_id: str | None = None
    free_tier: bool | None = None
    contact_only: bool | None = None


class BillingPlansResponse(BaseModel):
    starter: BillingPlanPublic
    research_pro: BillingPlanPublic
    institution: BillingPlanPublic


class BillingConfigResponse(BaseModel):
    billing_enabled: bool
    configured: bool
    mode: str
    app_public_url: str
    plans: BillingPlansResponse


class InsightCardResponse(BaseModel):
    title: str
    value: float | int
    severity: str


class ScanResponse(BaseModel):
    disclaimer: str
    plan: str
    quota_remaining_today: int | None = None
    metrics: dict[str, Any]
    fingerprint: dict[str, Any]
    fingerprint_vector: list[float | int]
    content_hash: str
    insight_cards: list[InsightCardResponse]


class UrlResponse(BaseModel):
    url: str


class SubscriptionStatusResponse(BaseModel):
    user_id: str
    plan: str
    subscription_status: str
    current_period_end: str | None = None


class WebhookAckResponse(BaseModel):
    received: bool
    duplicate: bool = False


def _account_status_payload(db: Session, user_id: str, email: str | None = None) -> AccountStatusResponse:
    settings = get_billing_settings()
    account = ensure_account(db, user_id, email)
    db.commit()
    pro = is_pro_account(db, user_id)
    sub = get_subscription(db, user_id)
    return AccountStatusResponse(
        user_id=account.user_id,
        email=account.email,
        plan=sub.plan if sub else ("research_pro" if pro else "free"),
        subscription_status=sub.status if sub else "none",
        quota_remaining_today=_quota_remaining_today(db, user_id),
        free_daily_scan_limit=_free_daily_limit(),
        max_text_chars=_max_text_chars(pro),
        checkout_enabled=_stripe_checkout_enabled(),
        billing_mode=settings.billing_mode,
        price_ids=PriceIdsResponse(
            starter=settings.stripe_price_starter if settings.is_configured() else None,
            research_pro=settings.stripe_price_research_pro if settings.is_configured() else None,
        ),
    )


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


def _quota_remaining_today(db: Session, user_id: str) -> int | None:
    if is_pro_account(db, user_id):
        return None
    limit = _free_daily_limit()
    used = get_daily_usage(db, user_id, _today())
    return max(limit - used, 0)


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


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_billing_settings()
    return HealthResponse(
        ok=True,
        service="cogniprint-content-scanner-api",
        version="0.1.0",
        stripe_checkout_enabled=_stripe_checkout_enabled(),
        environment=os.getenv("ENVIRONMENT", "development"),
        billing_mode=settings.billing_mode,
    )


@app.get("/account/status", response_model=AccountStatusResponse)
def account_status(
    user_id: str = Query(..., min_length=1, max_length=160),
    email: str | None = Query(default=None, max_length=320),
    db: Session = Depends(get_db),
) -> AccountStatusResponse:
    return _account_status_payload(db, user_id, email)


@app.get("/api/billing/config", response_model=BillingConfigResponse)
def billing_config() -> BillingConfigResponse:
    return BillingConfigResponse.model_validate(_billing_public_config(get_billing_settings()))


@app.post("/scan", response_model=ScanResponse)
def scan(payload: ScanRequest, db: Session = Depends(get_db)) -> ScanResponse:
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
    return ScanResponse(
        disclaimer=DISCLAIMER,
        plan="pro" if pro else "free",
        quota_remaining_today=remaining,
        metrics=profile["metrics"],
        fingerprint=profile["fingerprint"],
        fingerprint_vector=profile["fingerprint_vector"],
        content_hash=profile["content_hash"],
        insight_cards=[InsightCardResponse.model_validate(card) for card in _insights(profile)],
    )


@app.post("/billing/create-checkout-session")
@app.post("/api/billing/create-checkout-session")
def create_checkout_session(
    payload: CheckoutRequest, request: Request, db: Session = Depends(get_db)
) -> UrlResponse:
    del request
    settings = _require_billing_settings()
    price_id = settings.price_for_plan(payload.plan)
    if not price_id:
        raise HTTPException(status_code=400, detail="Unknown or unconfigured plan.")

    account = ensure_account(db, payload.user_id, payload.email)
    db.commit()

    stripe.api_key = settings.stripe_secret_key
    stripe.api_version = STRIPE_API_VERSION
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        customer_email=payload.email,
        customer=account.stripe_customer_id or None,
        client_reference_id=payload.user_id,
        metadata={"user_id": payload.user_id, "plan": payload.plan},
        success_url=settings.stripe_success_url,
        cancel_url=settings.stripe_cancel_url,
        allow_promotion_codes=True,
    )
    return UrlResponse(url=session.url)


@app.post("/billing/create-portal-session")
@app.post("/api/billing/create-portal-session")
def create_portal_session(payload: PortalRequest, db: Session = Depends(get_db)) -> UrlResponse:
    settings = _require_billing_settings()
    customer_id = payload.customer_id
    if not customer_id:
        account = get_account_by_user_id(db, payload.user_id)
        if account is None or not account.stripe_customer_id:
            raise HTTPException(status_code=404, detail="No Stripe customer exists for this account.")
        customer_id = account.stripe_customer_id

    stripe.api_key = settings.stripe_secret_key
    stripe.api_version = STRIPE_API_VERSION
    portal = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=settings.stripe_customer_portal_return_url,
    )
    return UrlResponse(url=portal.url)


@app.get("/api/billing/subscription-status", response_model=SubscriptionStatusResponse)
def billing_subscription_status(
    user_id: str = Query(..., min_length=1, max_length=160),
    db: Session = Depends(get_db),
) -> SubscriptionStatusResponse:
    status = _account_status_payload(db, user_id)
    return SubscriptionStatusResponse(
        user_id=user_id,
        plan=status.plan,
        subscription_status=status.subscription_status,
        current_period_end=None,
    )


def _normalize_subscription_status(raw_status: str | None) -> str:
    mapping = {
        "active": "active",
        "trialing": "trialing",
        "past_due": "past_due",
        "canceled": "canceled",
        "cancelled": "canceled",
        "unpaid": "past_due",
        "incomplete_expired": "canceled",
        "paused": "paused",
    }
    return mapping.get(raw_status or "", "active")


@app.post("/webhooks/stripe")
@app.post("/api/billing/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(default=""),
    db: Session = Depends(get_db),
) -> WebhookAckResponse:
    settings = _require_billing_settings()

    stripe.api_key = settings.stripe_secret_key
    stripe.api_version = STRIPE_API_VERSION
    body = await request.body()
    try:
        event = stripe.Webhook.construct_event(body, stripe_signature, settings.stripe_webhook_secret)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid webhook signature.") from exc

    event_id = event["id"]
    event_type = event["type"]
    data = event["data"]["object"]
    if not mark_webhook_event_processed(db, event_id, event_type):
        return WebhookAckResponse(received=True, duplicate=True)

    if event_type == "checkout.session.completed":
        user_id = data.get("client_reference_id") or data.get("metadata", {}).get("user_id")
        plan = data.get("metadata", {}).get("plan", "research_pro")
        if user_id:
            activate_pro(
                db,
                user_id=user_id,
                stripe_customer_id=data.get("customer"),
                stripe_subscription_id=data.get("subscription"),
                plan=plan,
                status="active",
            )

    elif event_type in {"customer.subscription.created", "customer.subscription.updated"}:
        customer_id = data.get("customer")
        if customer_id:
            set_subscription_by_customer(
                db,
                customer_id,
                plan=(data.get("metadata", {}) or {}).get("plan", "research_pro"),
                status=_normalize_subscription_status(data.get("status")),
                stripe_subscription_id=data.get("id"),
            )

    elif event_type == "customer.subscription.deleted":
        sub_id = data.get("id")
        customer_id = data.get("customer")
        if sub_id:
            downgrade_subscription(db, sub_id, "canceled")
        elif customer_id:
            downgrade_by_customer(db, customer_id, "canceled")

    elif event_type == "customer.subscription.paused":
        sub_id = data.get("id")
        customer_id = data.get("customer")
        if sub_id:
            downgrade_subscription(db, sub_id, "paused")
        elif customer_id:
            downgrade_by_customer(db, customer_id, "paused")

    elif event_type == "invoice.paid":
        customer_id = data.get("customer")
        sub_id = data.get("subscription")
        if customer_id:
            set_subscription_by_customer(
                db,
                customer_id,
                plan="research_pro",
                status="active",
                stripe_subscription_id=sub_id,
            )

    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer")
        sub_id = data.get("subscription")
        if sub_id:
            downgrade_subscription(db, sub_id, "past_due")
        elif customer_id:
            downgrade_by_customer(db, customer_id, "past_due")

    return WebhookAckResponse(received=True)
