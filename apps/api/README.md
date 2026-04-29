# CogniPrint Content Scanner API

FastAPI service for an optional application and deployment layer around the CogniPrint research engine.

This app wraps the existing deterministic CogniPrint research workflow and exposes an API for scanning text, enforcing usage quotas, and integrating subscription billing where that deployment path is needed.

The repository's public scientific framing remains research-first. Outputs remain statistical and heuristic signals only. They are not legal conclusions, source guarantees, authorship guarantees, or final judgments about text.

Current API surfaces used by the optional SaaS layer:

- `GET /health`
- `GET /account/status`
- `POST /scan`
- `POST /billing/create-checkout-session`
- `POST /webhooks/stripe`

The current frontend uses a browser-local `user_id` as the minimum viable account identifier for free quota tracking and Stripe Checkout activation.
