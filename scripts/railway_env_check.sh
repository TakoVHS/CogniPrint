#!/usr/bin/env bash
# scripts/railway_env_check.sh
# CogniPrint — Validates that all required Railway environment variables are set.
# Usage: bash scripts/railway_env_check.sh
set -euo pipefail

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
error() { echo -e "${RED}[MISSING]${NC} $*"; }

# ────────────────────────────────────────────────────────────────────────────
# Required variables (must be present and non-empty)
# ────────────────────────────────────────────────────────────────────────────
REQUIRED_VARS=(
  DATABASE_URL
  FRONTEND_URL
  STRIPE_SECRET_KEY
  STRIPE_WEBHOOK_SECRET
  STRIPE_PRICE_RESEARCH_PRO
)

# ────────────────────────────────────────────────────────────────────────────
# Expected safe defaults (warn if absent but don't fail)
# ────────────────────────────────────────────────────────────────────────────
OPTIONAL_VARS=(
  ENVIRONMENT
  FREE_DAILY_SCAN_LIMIT
  MAX_TEXT_CHARS_FREE
  MAX_TEXT_CHARS_PRO
)

# ────────────────────────────────────────────────────────────────────────────
# Load from Railway if CLI is available; otherwise validate current environment
# ────────────────────────────────────────────────────────────────────────────
if command -v railway &>/dev/null && railway status &>/dev/null 2>&1; then
  info "Railway CLI detected. Loading variables from Railway..."
  # Export variables from Railway into the current shell for validation.
  eval "$(railway variables --json 2>/dev/null | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
for k, v in data.items():
    # Sanitise: skip values that look like they contain shell-unsafe chars
    safe_v = v.replace("'", "'\\''")
    print(f"export {k}='{safe_v}'")
" 2>/dev/null || true)"
  ok "Variables loaded from Railway."
else
  info "Railway CLI not linked; validating current shell environment."
fi

# ────────────────────────────────────────────────────────────────────────────
# Check required variables
# ────────────────────────────────────────────────────────────────────────────
echo ""
info "Checking required variables..."
MISSING=()
for var in "${REQUIRED_VARS[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    error "$var"
    MISSING+=("$var")
  else
    ok "$var is set"
  fi
done

# ────────────────────────────────────────────────────────────────────────────
# Check optional variables
# ────────────────────────────────────────────────────────────────────────────
echo ""
info "Checking optional variables..."
for var in "${OPTIONAL_VARS[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo -e "\033[1;33m[DEFAULT]\033[0m $var not set — Railway/app will use built-in default"
  else
    ok "$var = ${!var}"
  fi
done

# ────────────────────────────────────────────────────────────────────────────
# Result
# ────────────────────────────────────────────────────────────────────────────
echo ""
if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo -e "${RED}────────────────────────────────────────────────────${NC}"
  echo -e "${RED}FAIL: ${#MISSING[@]} required variable(s) are missing:${NC}"
  for var in "${MISSING[@]}"; do
    echo -e "  ${RED}• $var${NC}"
  done
  echo ""
  echo "Set them with:"
  for var in "${MISSING[@]}"; do
    echo "  railway variables set ${var}=\"<value>\""
  done
  echo -e "${RED}────────────────────────────────────────────────────${NC}"
  exit 1
else
  echo -e "${GREEN}────────────────────────────────────────────────────${NC}"
  echo -e "${GREEN}PASS: All required environment variables are set.${NC}"
  echo -e "${GREEN}────────────────────────────────────────────────────${NC}"
fi
