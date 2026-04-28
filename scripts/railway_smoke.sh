#!/usr/bin/env bash
# scripts/railway_smoke.sh
# CogniPrint — Post-deploy smoke test
#
# Usage: bash scripts/railway_smoke.sh [DOMAIN]
#
# If DOMAIN is not provided, the script tries to retrieve it via `railway domain`.
# Pass a domain explicitly when running in CI / outside a linked repo directory:
#
#   bash scripts/railway_smoke.sh my-project.up.railway.app
set -euo pipefail

# ────────────────────────────────────────────────────────────────────────────
# Colour helpers
# ────────────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; }

PASS=0
FAIL=0

check_pass() { ok    "$1"; ((PASS++)) || true; }
check_fail() { fail  "$1"; ((FAIL++)) || true; }

# ────────────────────────────────────────────────────────────────────────────
# 1. railway status
# ────────────────────────────────────────────────────────────────────────────
echo -e "\n${BOLD}── 1. railway status ──${NC}"

if command -v railway &>/dev/null; then
  STATUS=$(railway status 2>/dev/null || true)
  if [[ -n "$STATUS" ]]; then
    echo "$STATUS"
    check_pass "railway status returned output"
  else
    warn "railway status returned no output (project may not be linked)"
    ((FAIL++)) || true
  fi
else
  warn "Railway CLI not installed — skipping CLI checks"
  ((FAIL++)) || true
fi

# ────────────────────────────────────────────────────────────────────────────
# 2. Resolve domain
# ────────────────────────────────────────────────────────────────────────────
echo -e "\n${BOLD}── 2. railway domain ──${NC}"

DOMAIN="${1:-}"

if [[ -z "$DOMAIN" ]]; then
  if command -v railway &>/dev/null; then
    DOMAIN=$(railway domain 2>/dev/null | grep -Eo '[a-zA-Z0-9.-]+\.up\.railway\.app' | head -1 || true)
  fi
fi

if [[ -n "$DOMAIN" ]]; then
  # Strip protocol prefix if the caller accidentally included it
  DOMAIN="${DOMAIN#https://}"
  DOMAIN="${DOMAIN#http://}"
  ok "Domain: ${DOMAIN}"
  check_pass "Domain resolved: ${DOMAIN}"
else
  warn "Could not resolve Railway domain automatically."
  warn "Provide it as an argument: bash scripts/railway_smoke.sh <domain>"
  check_fail "Domain not resolved"
fi

# ────────────────────────────────────────────────────────────────────────────
# 3. curl /health
# ────────────────────────────────────────────────────────────────────────────
echo -e "\n${BOLD}── 3. GET /health ──${NC}"

if [[ -z "$DOMAIN" ]]; then
  warn "No domain available — skipping health check"
  check_fail "Health check skipped (no domain)"
else
  HEALTH_URL="https://${DOMAIN}/health"
  info "Checking: ${HEALTH_URL}"

  MAX_RETRIES=5
  SLEEP_SECS=6

  for i in $(seq 1 "$MAX_RETRIES"); do
    HTTP_STATUS=$(curl -s -o /tmp/cogniprint_health_response.json \
      -w "%{http_code}" --max-time 15 "$HEALTH_URL" 2>/dev/null || echo "000")

    if [[ "$HTTP_STATUS" == "200" ]]; then
      check_pass "GET /health → HTTP 200"
      echo -e "  Response body:"
      python3 -m json.tool /tmp/cogniprint_health_response.json 2>/dev/null \
        || cat /tmp/cogniprint_health_response.json
      break
    fi

    if [[ $i -lt $MAX_RETRIES ]]; then
      warn "Attempt ${i}/${MAX_RETRIES}: HTTP ${HTTP_STATUS} — retrying in ${SLEEP_SECS}s..."
      sleep "$SLEEP_SECS"
    else
      check_fail "GET /health → HTTP ${HTTP_STATUS} (after ${MAX_RETRIES} attempts)"
      echo -e "  Raw response:"
      cat /tmp/cogniprint_health_response.json 2>/dev/null || true
    fi
  done
fi

# ────────────────────────────────────────────────────────────────────────────
# 4. Summary
# ────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}══════════════════════════════════════${NC}"
if [[ $FAIL -eq 0 ]]; then
  echo -e "${GREEN}${BOLD}  SMOKE TEST PASSED  (${PASS} checks)${NC}"
  if [[ -n "$DOMAIN" ]]; then
    echo ""
    ok "API base URL:      https://${DOMAIN}"
    ok "Health endpoint:   https://${DOMAIN}/health"
    ok "Scan endpoint:     https://${DOMAIN}/scan"
    ok "Stripe webhook:    https://${DOMAIN}/webhooks/stripe"
  fi
else
  echo -e "${RED}${BOLD}  SMOKE TEST FAILED  (${PASS} passed, ${FAIL} failed)${NC}"
  echo ""
  echo "  Investigate with:"
  echo "    railway logs"
  echo "    railway status"
  exit 1
fi
echo -e "${BOLD}══════════════════════════════════════${NC}"
