#!/usr/bin/env bash
set -euo pipefail

# CogniPrint Railway CLI launch helper.
# This script intentionally does not contain secrets.
# Run it locally after `railway login`.

PROJECT_NAME="${PROJECT_NAME:-CogniPrint Production}"
SERVICE_NAME="${SERVICE_NAME:-cogniprint-api}"

command -v railway >/dev/null 2>&1 || {
  echo "Railway CLI is not installed. Install it first: npm i -g @railway/cli"
  exit 1
}

if ! railway whoami >/dev/null 2>&1; then
  echo "Railway CLI is not authenticated. Run: railway login"
  exit 1
fi

echo "Using Railway project name: ${PROJECT_NAME}"
echo "Using Railway service name: ${SERVICE_NAME}"

echo "Step 1: create or select a Railway project manually if prompted."
echo "Recommended project name: ${PROJECT_NAME}"
railway init --name "${PROJECT_NAME}" || true

# Link the current directory to the Railway project selected/created above.
railway link

# These non-secret values are safe to set from CLI.
railway variables --set "ENVIRONMENT=production"
railway variables --set "FREE_DAILY_SCAN_LIMIT=3"
railway variables --set "MAX_TEXT_CHARS_FREE=12000"
railway variables --set "MAX_TEXT_CHARS_PRO=120000"

cat <<'EOF'

Manual secret variables still required in Railway UI or Railway CLI:

  DATABASE_URL            Railway Postgres connection string
  FRONTEND_URL            Vercel/frontend URL, e.g. https://app.cogniprint.org
  STRIPE_SECRET_KEY       Stripe live secret key
  STRIPE_WEBHOOK_SECRET   Stripe webhook signing secret
  STRIPE_PRO_PRICE_ID     Stripe recurring price id for CogniPrint Pro $199/mo

Recommended CLI pattern, entered locally by the owner only:

  railway variables --set "DATABASE_URL=<railway-postgres-url>"
  railway variables --set "FRONTEND_URL=<vercel-or-domain-url>"
  railway variables --set "STRIPE_SECRET_KEY=<stripe-live-secret>"
  railway variables --set "STRIPE_WEBHOOK_SECRET=<stripe-webhook-secret>"
  railway variables --set "STRIPE_PRO_PRICE_ID=<stripe-price-id>"

Deploy:

  railway up

Verify:

  railway domain
  curl https://<railway-domain>/health

Expected health response:

  {"ok":true}

EOF
