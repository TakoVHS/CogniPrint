# CogniPrint Content Scanner — Live Production Runbook

This runbook covers an optional hosted application layer around the CogniPrint research engine. Treat it as test-mode-first launch preparation, not as proof of production readiness.

## 1. Railway backend

Create a Railway service from this repository and point it to the FastAPI app under `apps/api`.

Start command:

`uvicorn apps.api.app.main:app --host 0.0.0.0 --port $PORT`

Healthcheck:

`/health`

Readiness:

`/ready`

Production gate:

- `/health` returns 200.
- `/ready` returns 200 and confirms database reachability.
- `/scan` accepts a text payload.
- Fourth Free scan returns upgrade/paywall response.

## 2. Vercel frontend

Create a Vercel project from this repository.

Project root:

`apps/web`

Build command:

`npm run build`

Output directory:

`dist`

Production gate:

- Landing page loads.
- Scanner can call the Railway API.
- Pricing section points to Pro checkout.
- Browser-local account state restores through `/account/status`.

## 3. Stripe billing

Use [`docs/stripe-billing-runbook.md`](docs/stripe-billing-runbook.md) for the current test-mode checklist.

Current integration surface:

- `GET /api/billing/config`
- `POST /api/billing/create-checkout-session`
- `POST /api/billing/create-portal-session`
- `POST /api/billing/webhook`
- `GET /api/billing/subscription-status`

Webhook endpoint:

`/api/billing/webhook`

Required Stripe events:

- checkout.session.completed
- customer.subscription.created
- customer.subscription.updated
- customer.subscription.deleted
- invoice.paid
- invoice.payment_failed

Hosted readiness gate:

- Billing env is configured in test mode.
- Checkout session opens.
- Webhook signature verification works.
- Customer portal session opens for a provisioned customer.
- Failed payment does not leave account as falsely active.

## 4. Domain

Recommended public topology:

- Frontend: `https://cogniprint.ai` or `https://scanner.cogniprint.ai`
- API: `https://api.cogniprint.ai`

Production gate:

- HTTPS active.
- CORS allows only the production frontend domain.
- No secret values are exposed in frontend bundles.

## 5. First paid customer flow

Minimum revenue path:

1. User lands on homepage.
2. User runs one scan.
3. User hits Free quota or sees Pro CTA.
4. User enters Stripe Checkout.
5. Webhook activates Pro state.
6. User returns to `/?checkout=success#pricing`.
7. User scans without Free quota block from the same browser account.

## 6. Sales page claims

Allowed language:

- statistical content fingerprinting
- style consistency review
- content QA
- editorial due diligence
- structural drift signals

Forbidden language:

- legal proof
- guaranteed authorship detection
- source proof
- definitive AI detector
- final judgment system

## 7. Revenue launch gate

Do not announce public paid launch until all are true:

- Railway backend is live.
- Vercel frontend is live.
- Stripe test-mode checkout is validated end to end.
- Stripe webhook is verified.
- Free quota is tested.
- Pro unlock is tested.
- Browser-local account restore is tested after returning from Checkout.
- Public copy includes the research disclaimer.
- Privacy Policy and Terms are linked.
