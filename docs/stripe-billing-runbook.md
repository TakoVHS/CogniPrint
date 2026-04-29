# Stripe Billing Runbook

This runbook covers the optional CogniPrint billing layer in Stripe test mode. It does not change the research framing of the repository.

## Environment

Required variables:

```bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_STARTER=price_...
STRIPE_PRICE_RESEARCH_PRO=price_...
STRIPE_SUCCESS_URL=http://localhost:5173/billing-success.html
STRIPE_CANCEL_URL=http://localhost:5173/billing-cancel.html
APP_PUBLIC_URL=http://localhost:8000
BILLING_MODE=test
BILLING_ENABLED=true
```

Optional:

```bash
STRIPE_CUSTOMER_PORTAL_RETURN_URL=http://localhost:5173/account.html
```

## Dashboard setup

In Stripe test mode:

1. Create product `CogniPrint Starter`.
2. Create recurring monthly price and copy the test `price_...` to `STRIPE_PRICE_STARTER`.
3. Create product `CogniPrint Research Pro`.
4. Create recurring monthly price and copy the test `price_...` to `STRIPE_PRICE_RESEARCH_PRO`.
5. Configure Customer Portal.
6. Keep all work in test mode first.

Only switch to live mode after end-to-end test mode validation.

## Local steps

1. Install Stripe CLI manually if needed.
2. Login:

```bash
stripe login
```

3. Forward webhooks:

```bash
stripe listen --forward-to localhost:8000/api/billing/webhook
```

4. Copy the reported `whsec_...` value into `STRIPE_WEBHOOK_SECRET`.
5. Start the API:

```bash
cd /home/vietcash/projects/CogniPrint
source .venv/bin/activate
uvicorn apps.api.app.main:app --reload --port 8000
```

6. Start the frontend:

```bash
cd /home/vietcash/projects/CogniPrint/apps/web
npm install
npm run dev
```

7. Open the pricing section or call the API endpoint directly.
8. Trigger a test webhook:

```bash
stripe trigger checkout.session.completed
```

9. Verify local subscription state:

```bash
curl 'http://localhost:8000/api/billing/subscription-status?user_id=<your-browser-user-id>'
```

10. Open the customer portal test flow from the account section.

## Notes

- Billing fails closed if required Stripe env is missing.
- `/api/billing/config` never exposes secret keys.
- Webhook signature verification is mandatory.
- Webhook processing is idempotent by Stripe event ID.
- No real Stripe network access is required for automated tests.
