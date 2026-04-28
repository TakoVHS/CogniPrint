#!/usr/bin/env bash
# scripts/railway_recover.sh
# CogniPrint — Railway Recovery Helper
#
# Interactive script that diagnoses the current Railway state, offers to clean
# up the accidental "grateful-beauty" service, and guides the operator through
# creating the canonical "cogniprint-api" service.
#
# Usage: bash scripts/railway_recover.sh
#
# Nothing destructive runs without an explicit yes/no prompt.
set -euo pipefail

# ────────────────────────────────────────────────────────────────────────────
# Colour helpers
# ────────────────────────────────────────────────────────────────────────────
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
ok()      { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; }
section() { echo -e "\n${BOLD}══════════════════════════════════════════════${NC}"; \
            echo -e "${BOLD}  $*${NC}"; \
            echo -e "${BOLD}══════════════════════════════════════════════${NC}"; }

ask_yes_no() {
  local prompt="$1"
  local answer
  while true; do
    read -rp "$(echo -e "${YELLOW}${prompt} [yes/no]: ${NC}")" answer
    case "$answer" in
      yes|YES|y|Y) return 0 ;;
      no|NO|n|N)   return 1 ;;
      *) echo "Please answer yes or no." ;;
    esac
  done
}

# ────────────────────────────────────────────────────────────────────────────
# 1. Railway CLI check
# ────────────────────────────────────────────────────────────────────────────
section "1. Railway CLI"

if ! command -v railway &>/dev/null; then
  error "Railway CLI not found. Install it first:"
  echo ""
  echo "  # Linux / WSL:"
  echo "  curl -fsSL https://railway.app/install.sh | sh"
  echo ""
  echo "  # npm (cross-platform):"
  echo "  npm install -g @railway/cli"
  echo ""
  echo "  # macOS Homebrew:"
  echo "  brew install railway"
  echo ""
  exit 1
fi

ok "Railway CLI found: $(railway --version 2>/dev/null || echo 'version unknown')"

# ────────────────────────────────────────────────────────────────────────────
# 2. Login check
# ────────────────────────────────────────────────────────────────────────────
section "2. Authentication"

WHOAMI=$(railway whoami 2>/dev/null || true)
if [[ -z "$WHOAMI" ]]; then
  warn "Not logged in. Attempting login..."
  railway login
  WHOAMI=$(railway whoami 2>/dev/null || true)
  if [[ -z "$WHOAMI" ]]; then
    error "Login failed. Run 'railway login' manually and retry."
    exit 1
  fi
fi
ok "Logged in as: ${WHOAMI}"

# ────────────────────────────────────────────────────────────────────────────
# 3. Linked project
# ────────────────────────────────────────────────────────────────────────────
section "3. Linked Project"

STATUS_OUTPUT=$(railway status 2>/dev/null || true)
if [[ -z "$STATUS_OUTPUT" ]]; then
  warn "No project is currently linked to this directory."
  info "To link to an existing project, run:"
  echo ""
  echo "  railway link"
  echo ""
  info "To create a new project, run:"
  echo ""
  echo "  railway init"
  echo ""
else
  echo "$STATUS_OUTPUT"
fi

# ────────────────────────────────────────────────────────────────────────────
# 4. Services — detect grateful-beauty
# ────────────────────────────────────────────────────────────────────────────
section "4. Service Inspection"

info "Current service context:"
CURRENT_SERVICE=$(railway service 2>/dev/null || echo "")
if [[ -n "$CURRENT_SERVICE" ]]; then
  echo "$CURRENT_SERVICE"
else
  warn "Could not retrieve service context (no project linked or CLI error)."
fi

echo ""
info "Check the Railway dashboard for the full list of services:"
echo "  railway open"
echo ""

# Detect grateful-beauty in status output
FOUND_GRATEFUL=false
if echo "${STATUS_OUTPUT}${CURRENT_SERVICE}" | grep -qi "grateful-beauty"; then
  FOUND_GRATEFUL=true
  warn "Accidental service 'grateful-beauty' detected in the current context."
fi

# ────────────────────────────────────────────────────────────────────────────
# 5. Offer to guide grateful-beauty deletion
# ────────────────────────────────────────────────────────────────────────────
section "5. Remove 'grateful-beauty' (if needed)"

if $FOUND_GRATEFUL; then
  warn "'grateful-beauty' appears to be the currently linked service."
  echo ""
  if ask_yes_no "Would you like guidance on deleting 'grateful-beauty'?"; then
    echo ""
    info "Deletion must be done through the Railway dashboard (CLI has no delete command)."
    echo ""
    echo "  1. Open the dashboard:  railway open"
    echo "  2. Click on service:    grateful-beauty"
    echo "  3. Go to:               Settings → Danger Zone → Delete Service"
    echo "  4. Type 'grateful-beauty' to confirm."
    echo ""
    info "After deleting, unlink this directory from the old service:"
    echo ""
    echo "  railway unlink"
    echo ""
  else
    info "Skipping 'grateful-beauty' deletion guidance."
  fi
else
  info "'grateful-beauty' not detected in the current CLI context."
  echo ""
  warn "If it still exists in your project, check the dashboard: railway open"
  echo ""
  if ask_yes_no "Would you still like to see the deletion steps for 'grateful-beauty'?"; then
    echo ""
    echo "  1. railway open"
    echo "  2. Click on service: grateful-beauty"
    echo "  3. Settings → Danger Zone → Delete Service"
    echo "  4. Type 'grateful-beauty' to confirm."
    echo ""
    echo "  Then unlink this directory if it was linked to it:"
    echo ""
    echo "  railway unlink"
    echo ""
  fi
fi

# ────────────────────────────────────────────────────────────────────────────
# 6. Offer to create cogniprint-api
# ────────────────────────────────────────────────────────────────────────────
section "6. Create Canonical Service 'cogniprint-api'"

echo ""
if ask_yes_no "Would you like guidance on creating the canonical 'cogniprint-api' service?"; then
  echo ""
  info "Creating 'cogniprint-api' in the Railway dashboard:"
  echo ""
  echo "  1. Open:  railway open"
  echo "  2. In project 'CogniPrint Production':"
  echo "     + New Service → Empty Service"
  echo "  3. Rename to: cogniprint-api"
  echo "  4. Service Settings → Source → Connect Repo → TakoVHS/CogniPrint"
  echo "  5. Railway will auto-detect railway.json (NIXPACKS builder)."
  echo "  6. Set required secrets (see Step 7)."
  echo "  7. Click Deploy."
  echo ""
  info "Adding a managed PostgreSQL database:"
  echo ""
  echo "  1. + New Service → Database → PostgreSQL"
  echo "  2. Rename to: cogniprint-db"
  echo "  3. DATABASE_URL will be injected into cogniprint-api automatically."
  echo ""
fi

# ────────────────────────────────────────────────────────────────────────────
# 7. Relink this directory
# ────────────────────────────────────────────────────────────────────────────
section "7. Relink Repository Directory"

echo ""
if ask_yes_no "Would you like to relink this directory to 'cogniprint-api' now?"; then
  echo ""
  info "Unlinking current project (if any)..."
  railway unlink 2>/dev/null || true
  echo ""
  info "Linking to project interactively..."
  echo "(Select 'CogniPrint Production' → 'cogniprint-api' from the list)"
  echo ""
  railway link
  echo ""
  ok "Relink complete. Verify with:"
  echo "  railway status"
else
  echo ""
  info "To relink manually:"
  echo ""
  echo "  railway unlink"
  echo "  railway link"
  echo ""
fi

# ────────────────────────────────────────────────────────────────────────────
# 8. Final command reference
# ────────────────────────────────────────────────────────────────────────────
section "8. Useful Commands"

echo ""
echo -e "  ${BOLD}railway service${NC}        — show / switch service context"
echo -e "  ${BOLD}railway unlink${NC}         — unlink this directory from current project"
echo -e "  ${BOLD}railway link${NC}           — link this directory to a project/service"
echo -e "  ${BOLD}railway up${NC}             — deploy current commit"
echo -e "  ${BOLD}railway status${NC}         — show linked project/service/environment"
echo -e "  ${BOLD}railway open${NC}           — open Railway dashboard in browser"
echo -e "  ${BOLD}railway logs${NC}           — tail live deployment logs"
echo -e "  ${BOLD}railway variables${NC}      — list environment variables"
echo ""
echo -e "  ${BOLD}bash scripts/railway_smoke.sh${NC}   — post-deploy smoke test"
echo ""
ok "Recovery script complete."
