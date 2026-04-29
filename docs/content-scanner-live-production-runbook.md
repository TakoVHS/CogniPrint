# CogniPrint Content Scanner — Live Production Runbook

This runbook covers an optional production launch path for the application layer around the CogniPrint research engine.

## 1. Railway backend

Create a Railway service from this repository and point it to the FastAPI app under `apps/api`.

Start command:

`uvicorn apps.api.app.main:app --host 0.0.0.0 --port $PORT`

Healthcheck:

`/health`

Production gate:

- `/health` returns 200.
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

## 3. Stripe live mode

Create one product and one recurring monthly price:

- Product: CogniPrint Pro
- Price: USD 199 monthly recurring

Configure webhook endpoint:

`/webhooks/stripe`

Required events:

- checkout.session.completed
- customer.subscription.deleted
- customer.subscription.paused
- invoice.payment_failed

Production gate:

- Checkout session opens.
- Successful payment changes account state to Pro.
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
- Stripe Checkout is live.
- Stripe webhook is verified.
- Free quota is tested.
- Pro unlock is tested.
- Browser-local account restore is tested after returning from Checkout.
- Public copy includes the research disclaimer.
- Privacy Policy and Terms are linked.
