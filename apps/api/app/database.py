"""SQLAlchemy persistence layer for CogniPrint Content Scanner.

Provides ORM models and a session factory. Falls back to SQLite when
DATABASE_URL is not set so local development requires no extra setup.
"""
from __future__ import annotations

import os
from datetime import date, datetime, timezone

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cogniprint_dev.db")

# SQLite doesn't support some Postgres-only kwargs; strip them on connect.
_connect_args: dict = {"check_same_thread": False} if _DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(_DATABASE_URL, connect_args=_connect_args, future=True)
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Account(Base):
    """One row per logical user (identified by an opaque user_id string)."""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(160), unique=True, nullable=False, index=True)
    email = Column(String(320), nullable=True)
    stripe_customer_id = Column(String(64), nullable=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Subscription(Base):
    """Active plan state for an account."""

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(160), ForeignKey("accounts.user_id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    plan = Column(String(32), nullable=False, default="free")  # free | pro | enterprise
    status = Column(String(32), nullable=False, default="active")  # active | trialing | cancelled | past_due | paused
    stripe_subscription_id = Column(String(64), nullable=True, index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class ScanUsage(Base):
    """Daily scan counter per user (free-tier quota enforcement)."""

    __tablename__ = "scan_usage"
    __table_args__ = (UniqueConstraint("user_id", "usage_date", name="uq_scan_usage_user_date"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(160), ForeignKey("accounts.user_id", ondelete="CASCADE"), nullable=False, index=True)
    usage_date = Column(Date, nullable=False)
    count = Column(Integer, nullable=False, default=0)


class ScanRecord(Base):
    """Immutable audit log of every scan request."""

    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String(160), ForeignKey("accounts.user_id", ondelete="SET NULL"), nullable=True, index=True)
    plan_at_scan = Column(String(32), nullable=False, default="free")
    content_hash = Column(String(64), nullable=False)
    char_count = Column(Integer, nullable=False, default=0)
    word_count = Column(Integer, nullable=False, default=0)
    scanned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def create_tables() -> None:
    """Create all tables if they do not yet exist."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:  # type: ignore[return]
    """Yield a database session, ensuring it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ──────────────────────────── Repository helpers ─────────────────────────────


def ensure_account(db: Session, user_id: str, email: str | None = None) -> Account:
    account = db.query(Account).filter(Account.user_id == user_id).first()
    if account is None:
        account = Account(user_id=user_id, email=email)
        db.add(account)
        db.flush()
    return account


def get_subscription(db: Session, user_id: str) -> Subscription | None:
    return db.query(Subscription).filter(Subscription.user_id == user_id).first()


def is_pro_account(db: Session, user_id: str) -> bool:
    sub = get_subscription(db, user_id)
    if sub is None:
        return False
    return sub.plan in {"pro", "enterprise"} and sub.status in {"active", "trialing", "enterprise"}


def get_daily_usage(db: Session, user_id: str, day: date) -> int:
    row = (
        db.query(ScanUsage)
        .filter(ScanUsage.user_id == user_id, ScanUsage.usage_date == day)
        .first()
    )
    return row.count if row else 0


def increment_daily_usage(db: Session, user_id: str, day: date) -> int:
    row = (
        db.query(ScanUsage)
        .filter(ScanUsage.user_id == user_id, ScanUsage.usage_date == day)
        .first()
    )
    if row is None:
        row = ScanUsage(user_id=user_id, usage_date=day, count=1)
        db.add(row)
    else:
        row.count = ScanUsage.count + 1  # type: ignore[assignment]
        db.add(row)
    db.flush()
    # Re-query for the committed value.
    db.refresh(row)
    return row.count


def activate_pro(db: Session, user_id: str, stripe_customer_id: str | None = None, stripe_subscription_id: str | None = None) -> None:
    ensure_account(db, user_id)
    sub = get_subscription(db, user_id)
    if sub is None:
        sub = Subscription(user_id=user_id, plan="pro", status="active", stripe_subscription_id=stripe_subscription_id)
        db.add(sub)
    else:
        sub.plan = "pro"
        sub.status = "active"
        if stripe_subscription_id:
            sub.stripe_subscription_id = stripe_subscription_id
    if stripe_customer_id:
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if account:
            account.stripe_customer_id = stripe_customer_id
    db.commit()


def downgrade_subscription(db: Session, stripe_subscription_id: str, new_status: str) -> None:
    """Downgrade or cancel a subscription by its Stripe subscription ID."""
    sub = db.query(Subscription).filter(Subscription.stripe_subscription_id == stripe_subscription_id).first()
    if sub:
        sub.status = new_status
        if new_status in {"cancelled", "past_due"}:
            sub.plan = "free"
        db.commit()


def downgrade_by_customer(db: Session, stripe_customer_id: str, new_status: str) -> None:
    """Downgrade subscriptions matching a Stripe customer ID."""
    account = db.query(Account).filter(Account.stripe_customer_id == stripe_customer_id).first()
    if account:
        sub = get_subscription(db, account.user_id)
        if sub:
            sub.status = new_status
            if new_status in {"cancelled", "past_due"}:
                sub.plan = "free"
            db.commit()
