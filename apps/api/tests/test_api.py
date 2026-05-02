"""Tests for CogniPrint Content Scanner API.

Uses an in-process SQLite database so no external services are required.
"""
from __future__ import annotations

import os
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_cogniprint.db")
os.environ.setdefault("FREE_DAILY_SCAN_LIMIT", "3")
os.environ.setdefault("BILLING_ENABLED", "true")

# Import after env vars are set.
from apps.api.app.billing import reset_billing_settings_cache  # noqa: E402
from apps.api.app.database import Base, SessionLocal, get_db  # noqa: E402
from apps.api.app.main import app  # noqa: E402

_TEST_DB_URL = "sqlite:///./test_cogniprint.db"
_test_engine = create_engine(_TEST_DB_URL, connect_args={"check_same_thread": False})
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


def _override_get_db():
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    reset_billing_settings_cache()
    Base.metadata.create_all(bind=_test_engine)
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=_test_engine)
    reset_billing_settings_cache()


@pytest.fixture()
def client():
    return TestClient(app)


# ──────────────────────────── /health ────────────────────────────────────────


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "cogniprint" in body["service"]
    assert "stripe_checkout_enabled" in body


# ──────────────────────────── /account/status ────────────────────────────────


def test_account_status_initializes_free_account(client: TestClient):
    r = client.get("/account/status", params={"user_id": "acct-user-1", "email": "acct@example.com"})
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "acct-user-1"
    assert body["email"] == "acct@example.com"
    assert body["plan"] == "free"
    assert body["subscription_status"] == "none"
    assert body["quota_remaining_today"] == 3
    assert body["checkout_enabled"] is False


# ──────────────────────────── /scan ──────────────────────────────────────────


SAMPLE_TEXT = "The quick brown fox jumps over the lazy dog. " * 10


def test_scan_returns_expected_keys(client: TestClient):
    r = client.post("/scan", json={"text": SAMPLE_TEXT, "user_id": "test-user-1"})
    assert r.status_code == 200
    body = r.json()
    assert "disclaimer" in body
    assert "metrics" in body
    assert "fingerprint" in body
    assert "fingerprint_vector" in body
    assert "content_hash" in body
    assert "insight_cards" in body
    assert body["plan"] == "free"
    assert body["quota_remaining_today"] == 2


def test_disclaimer_is_present(client: TestClient):
    r = client.post("/scan", json={"text": SAMPLE_TEXT, "user_id": "test-disclaimer"})
    body = r.json()
    assert "statistical" in body["disclaimer"].lower()
    assert "not legal" in body["disclaimer"].lower()


def test_free_quota_enforced(client: TestClient):
    uid = "quota-test-user"
    for i in range(3):
        r = client.post("/scan", json={"text": SAMPLE_TEXT, "user_id": uid})
        assert r.status_code == 200, f"scan {i+1} failed"
    # 4th scan should be blocked
    r = client.post("/scan", json={"text": SAMPLE_TEXT, "user_id": uid})
    assert r.status_code == 402
    assert "limit" in r.json()["detail"].lower()


def test_scan_quota_remaining_decrements(client: TestClient):
    uid = "decrement-user"
    r1 = client.post("/scan", json={"text": SAMPLE_TEXT, "user_id": uid})
    assert r1.json()["quota_remaining_today"] == 2
    r2 = client.post("/scan", json={"text": SAMPLE_TEXT, "user_id": uid})
    assert r2.json()["quota_remaining_today"] == 1
    r3 = client.post("/scan", json={"text": SAMPLE_TEXT, "user_id": uid})
    assert r3.json()["quota_remaining_today"] == 0


def test_scan_empty_text_rejected(client: TestClient):
    r = client.post("/scan", json={"text": "", "user_id": "u1"})
    assert r.status_code == 422


def test_scan_text_too_long_rejected(client: TestClient):
    big_text = "a" * 120001
    r = client.post("/scan", json={"text": big_text, "user_id": "u2"})
    assert r.status_code == 422


# ──────────────────────────── /billing/create-checkout-session ───────────────


def test_checkout_session_503_when_stripe_not_configured(client: TestClient):
    for key in (
        "STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET",
        "STRIPE_PRICE_STARTER",
        "STRIPE_PRICE_RESEARCH_PRO",
    ):
        os.environ.pop(key, None)
    reset_billing_settings_cache()
    r = client.post("/api/billing/create-checkout-session", json={"user_id": "u3", "plan": "starter"})
    assert r.status_code == 503


def test_billing_config_does_not_expose_secret(monkeypatch: pytest.MonkeyPatch, client: TestClient):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_hidden")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_hidden")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price_starter_test")
    monkeypatch.setenv("STRIPE_PRICE_RESEARCH_PRO", "price_research_pro_test")
    reset_billing_settings_cache()
    r = client.get("/api/billing/config")
    assert r.status_code == 200
    body = r.json()
    assert body["billing_enabled"] is True
    assert body["plans"]["starter"]["price_id"] == "price_starter_test"
    assert "sk_test_hidden" not in r.text
    assert "whsec_hidden" not in r.text


def test_checkout_session_uses_valid_plan_and_returns_url(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_hidden")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_hidden")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price_starter_test")
    monkeypatch.setenv("STRIPE_PRICE_RESEARCH_PRO", "price_research_pro_test")
    monkeypatch.setenv("STRIPE_SUCCESS_URL", "http://localhost:8000/billing/success")
    monkeypatch.setenv("STRIPE_CANCEL_URL", "http://localhost:8000/billing/cancel")
    monkeypatch.setenv("APP_PUBLIC_URL", "http://localhost:8000")
    reset_billing_settings_cache()

    create_mock = Mock(return_value=SimpleNamespace(url="https://checkout.stripe.test/session"))
    monkeypatch.setattr("apps.api.app.main.stripe.checkout.Session.create", create_mock)

    r = client.post(
        "/api/billing/create-checkout-session",
        json={"user_id": "u3", "email": "u3@example.com", "plan": "starter"},
    )
    assert r.status_code == 200
    assert r.json()["url"] == "https://checkout.stripe.test/session"
    kwargs = create_mock.call_args.kwargs
    assert kwargs["line_items"][0]["price"] == "price_starter_test"
    assert kwargs["mode"] == "subscription"


def test_checkout_session_rejects_unknown_plan(client: TestClient):
    r = client.post("/api/billing/create-checkout-session", json={"user_id": "u3", "plan": "enterprise"})
    assert r.status_code == 422


def test_portal_session_requires_customer(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_hidden")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_hidden")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price_starter_test")
    monkeypatch.setenv("STRIPE_PRICE_RESEARCH_PRO", "price_research_pro_test")
    reset_billing_settings_cache()
    r = client.post("/api/billing/create-portal-session", json={"user_id": "missing-customer"})
    assert r.status_code == 404


def test_portal_session_returns_url_for_known_customer(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_hidden")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_hidden")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price_starter_test")
    monkeypatch.setenv("STRIPE_PRICE_RESEARCH_PRO", "price_research_pro_test")
    reset_billing_settings_cache()
    create_mock = Mock(return_value=SimpleNamespace(url="https://billing.stripe.test/session"))
    monkeypatch.setattr("apps.api.app.main.stripe.billing_portal.Session.create", create_mock)
    r = client.post("/api/billing/create-portal-session", json={"customer_id": "cus_known"})
    assert r.status_code == 200
    assert r.json()["url"] == "https://billing.stripe.test/session"


# ──────────────────────────── /webhooks/stripe ───────────────────────────────


def test_webhook_503_when_not_configured(client: TestClient):
    for key in ("STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"):
        os.environ.pop(key, None)
    reset_billing_settings_cache()
    r = client.post("/api/billing/webhook", content=b"{}")
    assert r.status_code == 503


def test_webhook_invalid_signature_rejected(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_hidden")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_hidden")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price_starter_test")
    monkeypatch.setenv("STRIPE_PRICE_RESEARCH_PRO", "price_research_pro_test")
    reset_billing_settings_cache()

    def _raise(*args, **kwargs):
        raise ValueError("bad sig")

    monkeypatch.setattr("apps.api.app.main.stripe.Webhook.construct_event", _raise)
    r = client.post("/api/billing/webhook", content=b"{}", headers={"Stripe-Signature": "t=1,v1=bad"})
    assert r.status_code == 400


def test_webhook_idempotency(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_hidden")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_hidden")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price_starter_test")
    monkeypatch.setenv("STRIPE_PRICE_RESEARCH_PRO", "price_research_pro_test")
    reset_billing_settings_cache()

    event = {
        "id": "evt_duplicate",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "client_reference_id": "dup-user",
                "customer": "cus_123",
                "subscription": "sub_123",
                "metadata": {"user_id": "dup-user", "plan": "research_pro"},
            }
        },
    }
    monkeypatch.setattr("apps.api.app.main.stripe.Webhook.construct_event", lambda *args, **kwargs: event)
    first = client.post("/api/billing/webhook", content=b"{}", headers={"Stripe-Signature": "ok"})
    second = client.post("/api/billing/webhook", content=b"{}", headers={"Stripe-Signature": "ok"})
    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["duplicate"] is True


def test_subscription_status_schema(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_hidden")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_hidden")
    monkeypatch.setenv("STRIPE_PRICE_STARTER", "price_starter_test")
    monkeypatch.setenv("STRIPE_PRICE_RESEARCH_PRO", "price_research_pro_test")
    reset_billing_settings_cache()

    status = client.get("/api/billing/subscription-status", params={"user_id": "status-user"})
    assert status.status_code == 200
    body = status.json()
    assert set(body.keys()) == {"user_id", "plan", "subscription_status", "current_period_end"}
    assert body["subscription_status"] == "none"


def test_openapi_registers_response_contracts(client: TestClient):
    schema = client.get("/openapi.json")
    assert schema.status_code == 200
    openapi = schema.json()

    health_schema = openapi["paths"]["/health"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    account_schema = openapi["paths"]["/account/status"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    scan_schema = openapi["paths"]["/scan"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]
    billing_schema = openapi["paths"]["/api/billing/config"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    checkout_schema = openapi["paths"]["/api/billing/create-checkout-session"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]
    portal_schema = openapi["paths"]["/api/billing/create-portal-session"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]
    webhook_schema = openapi["paths"]["/api/billing/webhook"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]

    assert health_schema["$ref"].endswith("/HealthResponse")
    assert account_schema["$ref"].endswith("/AccountStatusResponse")
    assert scan_schema["$ref"].endswith("/ScanResponse")
    assert billing_schema["$ref"].endswith("/BillingConfigResponse")
    assert checkout_schema["$ref"].endswith("/UrlResponse")
    assert portal_schema["$ref"].endswith("/UrlResponse")
    assert webhook_schema["$ref"].endswith("/WebhookAckResponse")
