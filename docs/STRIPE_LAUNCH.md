# Stripe Launch Guide — CogniPrint Pro

This document describes how to set up Stripe for CogniPrint's Pro subscription billing.

---

## Product & Pricing

| Field | Value |
|---|---|
| **Product name** | CogniPrint Pro |
| **Billing interval** | Monthly recurring |
| **Price** | $199.00 USD / month |
| **Currency** | USD |

### Create in Stripe Dashboard

1. Go to [dashboard.stripe.com/products](https://dashboard.stripe.com/products).
2. Click **+ Add product**.
3. **Name:** `CogniPrint Pro`
4. **Description:** Unlimited text scans, 120k character limit, priority support.
5. Under **Pricing**, select **Recurring** → **Monthly** → `$199.00`.
6. Click **Save product**.
7. Copy the **Price ID** (starts with `price_`).

### Set the Price ID in Railway

```bash
railway variables set STRIPE_PRO_PRICE_ID="price_..."
```

---

## Stripe API Keys

### Obtain Keys

| Key | Location |
|---|---|
| Secret key | Stripe Dashboard → Developers → API keys → Secret key |
| Publishable key | Stripe Dashboard → Developers → API keys → Publishable key (frontend use only, currently unused) |

### Set in Railway

```bash
railway variables set STRIPE_SECRET_KEY="sk_live_..."
```

> Use `sk_test_...` during development and `sk_live_...` in production.

---

## Webhook Configuration

### Endpoint

```
POST /webhooks/stripe
```

Full URL after Railway deployment:

```
https://your-project.up.railway.app/webhooks/stripe
```

### Register in Stripe Dashboard

1. Go to [dashboard.stripe.com/webhooks](https://dashboard.stripe.com/webhooks).
2. Click **+ Add endpoint**.
3. **Endpoint URL:** `https://your-project.up.railway.app/webhooks/stripe`
4. **Listen to:** Select the following events:

| Event | Effect in CogniPrint |
|---|---|
| `checkout.session.completed` | Activates Pro plan for the user |
| `invoice.payment_failed` | Marks subscription as `past_due`, revokes Pro access |
| `customer.subscription.deleted` | Marks subscription as `cancelled`, revokes Pro access |
| `customer.subscription.paused` | Marks subscription as `paused`, revokes Pro access |

5. Click **Add endpoint**.
6. Copy the **Signing secret** (starts with `whsec_`).

### Set the Signing Secret in Railway

```bash
railway variables set STRIPE_WEBHOOK_SECRET="whsec_..."
```

The API verifies every incoming webhook request using this secret via `stripe.Webhook.construct_event`. Invalid or missing signatures return HTTP 400.

---

## Test Mode Checklist

Before switching to live keys, test end-to-end with Stripe's test mode:

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Log in
stripe login

# Forward webhooks to local dev server
stripe listen --forward-to localhost:8000/webhooks/stripe

# Trigger a test checkout completion
stripe trigger checkout.session.completed
```

### Test Card Numbers

| Scenario | Card number |
|---|---|
| Successful payment | `4242 4242 4242 4242` |
| Payment declined | `4000 0000 0000 0002` |
| Requires authentication | `4000 0025 0000 3155` |

---

## Billing Flow

```
User clicks "Upgrade to Pro"
    └─▶ POST /billing/create-checkout-session
            └─▶ Stripe Checkout (hosted page)
                    ├─▶ Payment success
                    │       └─▶ Stripe sends checkout.session.completed
                    │               └─▶ POST /webhooks/stripe → activate_pro()
                    └─▶ Payment failure / cancellation
                            └─▶ User redirected to /?checkout=cancelled#pricing
                                (no state change; account remains free)
```

### Subscription Lifecycle

```
Active Pro
    ├─▶ invoice.payment_failed          → status: past_due  → plan: free
    ├─▶ customer.subscription.deleted  → status: cancelled  → plan: free
    └─▶ customer.subscription.paused   → status: paused     → plan: free (access revoked)
```

Failed or paused payments immediately revoke Pro access. No grace period is implemented by default.

---

## Environment Variables Summary

| Variable | Description |
|---|---|
| `STRIPE_SECRET_KEY` | `sk_live_...` — Stripe API secret key |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` — Webhook signing secret |
| `STRIPE_PRO_PRICE_ID` | `price_...` — Monthly Pro price ID |

Set all three in Railway:

```bash
railway variables set STRIPE_SECRET_KEY="sk_live_..."
railway variables set STRIPE_WEBHOOK_SECRET="whsec_..."
railway variables set STRIPE_PRO_PRICE_ID="price_..."
```

---

## Going Live Checklist

- [ ] Stripe account fully verified (business details, bank account)
- [ ] Product created with correct $199/month price
- [ ] `STRIPE_PRO_PRICE_ID` set in Railway
- [ ] `STRIPE_SECRET_KEY` (live key) set in Railway
- [ ] Webhook endpoint registered for all four events
- [ ] `STRIPE_WEBHOOK_SECRET` set in Railway
- [ ] End-to-end test with a real card in live mode
- [ ] `FRONTEND_URL` set in Railway (required for Stripe redirect URLs)
- [ ] `FRONTEND_URL` points to the root frontend origin, because success/cancel return URLs use `/?checkout=...#pricing`

## Browser-account note

The current frontend stores a browser-local `user_id` and uses it for `/scan`, `/account/status`, and Stripe checkout creation. This is the minimum viable identity layer for the current optional SaaS surface.

Implications:

- the same browser returns to the same free/pro account state;
- checkout completion activates Pro for that browser-linked account id;
- this is not a full authentication system;
- before broader paid launch, decide whether browser-local identity is sufficient or whether a stronger account system is required.
