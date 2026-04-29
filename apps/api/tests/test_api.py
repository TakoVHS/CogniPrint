"""Tests for CogniPrint Content Scanner API.

Uses an in-process SQLite database so no external services are required.
"""
from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_cogniprint.db")
os.environ.setdefault("FREE_DAILY_SCAN_LIMIT", "3")

# Import after env vars are set.
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
    Base.metadata.create_all(bind=_test_engine)
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=_test_engine)


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
    assert body["subscription_status"] == "free"
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
    # Stripe env vars are not set in this test environment.
    r = client.post("/billing/create-checkout-session", json={"user_id": "u3"})
    assert r.status_code == 503


# ──────────────────────────── /webhooks/stripe ───────────────────────────────


def test_webhook_503_when_not_configured(client: TestClient):
    r = client.post("/webhooks/stripe", content=b"{}")
    assert r.status_code == 503
