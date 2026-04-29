from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PlanName = Literal["starter", "research_pro"]

PLAN_LABELS: dict[PlanName, str] = {
    "starter": "Starter",
    "research_pro": "Research Pro",
}


class BillingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    billing_enabled: bool = Field(default=True, alias="BILLING_ENABLED")
    billing_mode: str = Field(default="test", alias="BILLING_MODE")
    app_public_url: str = Field(default="http://localhost:8000", alias="APP_PUBLIC_URL")
    stripe_secret_key: str | None = Field(default=None, alias="STRIPE_SECRET_KEY")
    stripe_webhook_secret: str | None = Field(default=None, alias="STRIPE_WEBHOOK_SECRET")
    stripe_price_starter: str | None = Field(default=None, alias="STRIPE_PRICE_STARTER")
    stripe_price_research_pro: str | None = Field(default=None, alias="STRIPE_PRICE_RESEARCH_PRO")
    stripe_success_url: str = Field(
        default="http://localhost:8000/billing/success",
        alias="STRIPE_SUCCESS_URL",
    )
    stripe_cancel_url: str = Field(
        default="http://localhost:8000/billing/cancel",
        alias="STRIPE_CANCEL_URL",
    )
    stripe_customer_portal_return_url: str = Field(
        default="http://localhost:8000/account/billing",
        alias="STRIPE_CUSTOMER_PORTAL_RETURN_URL",
    )

    def public_config(self) -> dict[str, object]:
        return {
            "billing_enabled": self.billing_enabled and self.is_configured(),
            "configured": self.is_configured(),
            "mode": self.billing_mode,
            "app_public_url": self.app_public_url,
            "plans": {
                "starter": {
                    "label": PLAN_LABELS["starter"],
                    "price_id": self.stripe_price_starter if self.is_configured() else None,
                },
                "research_pro": {
                    "label": PLAN_LABELS["research_pro"],
                    "price_id": self.stripe_price_research_pro if self.is_configured() else None,
                },
                "institution": {
                    "label": "Institution",
                    "contact_only": True,
                },
            },
        }

    def is_configured(self) -> bool:
        return not self.missing_required()

    def missing_required(self) -> list[str]:
        if not self.billing_enabled:
            return []
        missing: list[str] = []
        required = {
            "STRIPE_SECRET_KEY": self.stripe_secret_key,
            "STRIPE_WEBHOOK_SECRET": self.stripe_webhook_secret,
            "STRIPE_PRICE_STARTER": self.stripe_price_starter,
            "STRIPE_PRICE_RESEARCH_PRO": self.stripe_price_research_pro,
            "STRIPE_SUCCESS_URL": self.stripe_success_url,
            "STRIPE_CANCEL_URL": self.stripe_cancel_url,
            "APP_PUBLIC_URL": self.app_public_url,
        }
        for key, value in required.items():
            if not value:
                missing.append(key)
        return missing

    def price_for_plan(self, plan: PlanName) -> str:
        if plan == "starter":
            return self.stripe_price_starter or ""
        return self.stripe_price_research_pro or ""


@lru_cache(maxsize=1)
def get_billing_settings() -> BillingSettings:
    return BillingSettings()


def reset_billing_settings_cache() -> None:
    get_billing_settings.cache_clear()
