# CogniPrint Content Scanner — Enterprise Rollout Plan

## Status

This branch is reserved for the SaaS product layer around the existing CogniPrint research engine.

The implementation package is prepared externally as `cogniprint-content-scanner-enterprise.zip` and should be unpacked at repository root before opening the final PR.

## Product boundary

CogniPrint Content Scanner must remain a statistical content profiling and review product. It must not be marketed as legal proof, authorship proof, source guarantee, or final judgment system.

## Target architecture

- `apps/web`: React and Vite frontend deployed on Vercel.
- `apps/api`: FastAPI backend deployed on Railway.
- Stripe Checkout: subscription billing for Pro plan.
- Free tier: 3 scans per day.
- Pro tier: $199 per month.
- Enterprise tier: custom sales flow.
- Production database: managed Postgres.

## Required production secrets

Backend:

- `ENVIRONMENT=production`
- `FRONTEND_URL=https://<vercel-domain>`
- `DATABASE_URL=<railway-postgres-url>`
- `STRIPE_SECRET_KEY=<stripe-secret>`
- `STRIPE_WEBHOOK_SECRET=<stripe-webhook-secret>`
- `STRIPE_PRO_PRICE_ID=<stripe-price-id>`
- `FREE_DAILY_SCAN_LIMIT=3`
- `MAX_TEXT_CHARS_FREE=12000`
- `MAX_TEXT_CHARS_PRO=120000`

Frontend:

- `VITE_API_BASE_URL=https://<railway-api-domain>`

## Stripe setup

Create a Stripe Product named `CogniPrint Pro` with a recurring monthly USD price of 199. Copy the recurring Price ID into `STRIPE_PRO_PRICE_ID`.

Webhook endpoint:

`POST https://<railway-api-domain>/webhooks/stripe`

Webhook events:

- `checkout.session.completed`
- `customer.subscription.deleted`
- `customer.subscription.paused`
- `invoice.payment_failed`

## Validation gate

Before PR merge:

```bash
pip install -e .
pip install -r apps/api/requirements.txt
pytest apps/api/tests

cd apps/web
npm install
npm run build
```

## Launch gate

Do not call the product production-ready until all of these pass:

- Railway `/health` returns 200.
- Frontend can scan sample text against Railway API.
- Free quota blocks the fourth anonymous daily scan.
- Stripe Checkout creates a Pro subscription session.
- Stripe webhook upgrades account state to Pro.
- Pro account can scan beyond Free quota.
- Cancellation or failed payment downgrades or flags the account.
- Public copy includes the research disclaimer.
