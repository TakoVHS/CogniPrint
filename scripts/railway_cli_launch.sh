#!/usr/bin/env bash
# scripts/railway_cli_launch.sh
# CogniPrint — Railway CLI launch helper
# Usage: bash scripts/railway_cli_launch.sh [--browserless]
set -euo pipefail

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ────────────────────────────────────────────────────────────────────────────
# 1. Check railway CLI
# ────────────────────────────────────────────────────────────────────────────
info "Checking Railway CLI..."

if ! command -v railway &>/dev/null; then
  error "Railway CLI not found."
  echo ""
  echo "Install Railway CLI:"
  echo ""
  echo "  # Linux / WSL (recommended):"
  echo "  curl -fsSL https://railway.app/install.sh | sh"
  echo ""
  echo "  # npm (cross-platform):"
  echo "  npm install -g @railway/cli"
  echo ""
  echo "  # Homebrew (macOS):"
  echo "  brew install railway"
  echo ""
  echo "After installing, re-run this script."
  exit 1
fi

ok "Railway CLI found: $(railway --version 2>/dev/null || echo 'version unknown')"

# ────────────────────────────────────────────────────────────────────────────
# 2. Login
# ────────────────────────────────────────────────────────────────────────────
BROWSERLESS=${1:-""}

info "Logging in to Railway..."
if [[ "$BROWSERLESS" == "--browserless" ]]; then
  info "Using browserless login (token-based)."
  railway login --browserless
else
  railway login
fi

# ────────────────────────────────────────────────────────────────────────────
# 3. Verify authenticated identity
# ────────────────────────────────────────────────────────────────────────────
info "Verifying authentication..."
if ! railway whoami 2>/dev/null; then
  error "Not authenticated. Run 'railway login' and retry."
  exit 1
fi
ok "Authenticated."

# ────────────────────────────────────────────────────────────────────────────
# 4. Link or init project
# ────────────────────────────────────────────────────────────────────────────
info "Linking project to Railway..."
if railway status &>/dev/null; then
  ok "Project already linked."
else
  warn "No project linked. Running 'railway init'..."
  railway init
fi

# ────────────────────────────────────────────────────────────────────────────
# 5. Set safe (non-secret) environment variables
# ────────────────────────────────────────────────────────────────────────────
info "Setting non-secret environment variables..."

railway variables set \
  ENVIRONMENT=production \
  FREE_DAILY_SCAN_LIMIT=3 \
  MAX_TEXT_CHARS_FREE=12000 \
  MAX_TEXT_CHARS_PRO=120000

ok "Non-secret vars set."

# ────────────────────────────────────────────────────────────────────────────
# 6. Manual secret variables — print exact commands, never set them here
# ────────────────────────────────────────────────────────────────────────────
echo ""
warn "======================================================================"
warn " The following secrets MUST be set manually by the project owner."
warn " Copy-paste each command and replace the placeholder value."
warn "======================================================================"
echo ""
echo "  railway variables set DATABASE_URL=\"postgresql://user:pass@host:5432/dbname\""
echo ""
echo "  railway variables set FRONTEND_URL=\"https://your-vercel-app.vercel.app\""
echo ""
echo "  railway variables set STRIPE_SECRET_KEY=\"sk_live_...\""
echo ""
echo "  railway variables set STRIPE_WEBHOOK_SECRET=\"whsec_...\""
echo ""
echo "  railway variables set STRIPE_PRO_PRICE_ID=\"price_...\""
echo ""
warn "======================================================================"
echo ""

read -rp "Press ENTER once you have set the secrets above, or Ctrl-C to abort: "

# ────────────────────────────────────────────────────────────────────────────
# 7. Deploy
# ────────────────────────────────────────────────────────────────────────────
info "Deploying to Railway (railway up)..."
railway up

ok "Deploy triggered."

# ────────────────────────────────────────────────────────────────────────────
# 8. Show domain
# ────────────────────────────────────────────────────────────────────────────
info "Fetching deployment domain..."
DOMAIN=$(railway domain 2>/dev/null || echo "")
if [[ -n "$DOMAIN" ]]; then
  ok "Railway domain: ${DOMAIN}"
else
  warn "Could not retrieve domain automatically. Check Railway dashboard."
  DOMAIN="your-project.up.railway.app"
fi

# ────────────────────────────────────────────────────────────────────────────
# 9. Health check
# ────────────────────────────────────────────────────────────────────────────
HEALTH_URL="https://${DOMAIN}/health"
info "Running health check: ${HEALTH_URL}"

MAX_RETRIES=10
SLEEP_SECONDS=6
CURL_FAILURE_CODE='000'
for i in $(seq 1 $MAX_RETRIES); do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$HEALTH_URL" 2>/dev/null || echo "$CURL_FAILURE_CODE")
  if [[ "$HTTP_STATUS" == "200" ]]; then
    ok "Health check passed (HTTP 200)."
    curl -s "$HEALTH_URL" | python3 -m json.tool 2>/dev/null || true
    break
  fi
  warn "Attempt ${i}/${MAX_RETRIES}: got HTTP ${HTTP_STATUS}, waiting ${SLEEP_SECONDS}s..."
  sleep "$SLEEP_SECONDS"
  if [[ $i -eq $MAX_RETRIES ]]; then
    error "Health check failed after ${MAX_RETRIES} attempts. Check Railway logs:"
    echo "  railway logs"
    exit 1
  fi
done

echo ""
ok "======================================================================"
ok " CogniPrint API is live at: https://${DOMAIN}"
ok " Health endpoint:           https://${DOMAIN}/health"
ok " Scan endpoint:             https://${DOMAIN}/scan"
ok " Stripe webhook:            https://${DOMAIN}/webhooks/stripe"
ok "======================================================================"
echo ""
info "Next: set VITE_API_BASE_URL=https://${DOMAIN} in your Vercel project."
