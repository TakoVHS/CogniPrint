# CogniPrint Content Scanner API

FastAPI service for an optional application and deployment layer around the CogniPrint research engine.

This app wraps the existing deterministic CogniPrint research workflow and exposes an API for scanning text, enforcing usage quotas, and integrating subscription billing where that deployment path is needed.

The repository's public scientific framing remains research-first. Outputs remain statistical and heuristic signals only. They are not legal conclusions, source guarantees, authorship guarantees, or final judgments about text.

Current API surfaces used by the optional SaaS layer:

- `GET /health`
- `GET /account/status`
- `POST /scan`
- `GET /api/billing/config`
- `POST /api/billing/create-checkout-session`
- `POST /api/billing/create-portal-session`
- `POST /api/billing/webhook`
- `GET /api/billing/subscription-status`

The current API now also exposes explicit JSON response contracts through FastAPI and Pydantic response models. The intended contract surface is visible in `/openapi.json` and is covered by API tests for:

- `HealthResponse`
- `AccountStatusResponse`
- `ScanResponse`
- `BillingConfigResponse`
- `UrlResponse`
- `WebhookAckResponse`

The current frontend uses a browser-local `user_id` as the minimum viable account identifier for free quota tracking, Stripe Checkout activation, and customer portal lookup.
