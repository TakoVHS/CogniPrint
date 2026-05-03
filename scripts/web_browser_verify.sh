#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

API_HOST="127.0.0.1"
API_PORT="${WEB_BROWSER_VERIFY_API_PORT:-}"
WEB_HOST="127.0.0.1"
WEB_PORT="${WEB_BROWSER_VERIFY_PORT:-}"
ARTIFACT_DIR="${ROOT}/workspace/browser-verify"
SCREENSHOT_PATH="${ARTIFACT_DIR}/hosted-scanner-flow.png"
SUMMARY_PATH="${ARTIFACT_DIR}/verification-summary.json"
SKIP_NPM_CI="${WEB_BROWSER_VERIFY_SKIP_NPM_CI:-0}"
VERIFY_STAGE="init"
VERIFY_STATUS="failed"
START_TS="$(date +%s)"
API_READY_TS=""
WEB_READY_TS=""
VERIFY_DONE_TS=""

write_summary() {
  export SUMMARY_PATH SCREENSHOT_PATH API_BASE_URL WEB_BASE_URL VERIFY_STAGE VERIFY_STATUS START_TS API_READY_TS WEB_READY_TS VERIFY_DONE_TS
  python3 - <<'PY'
import json
import os
from pathlib import Path

def as_int(name: str):
    value = os.environ.get(name, "")
    return int(value) if value else None

start_ts = as_int("START_TS")
api_ready_ts = as_int("API_READY_TS")
web_ready_ts = as_int("WEB_READY_TS")
verify_done_ts = as_int("VERIFY_DONE_TS")

summary = {
    "status": os.environ.get("VERIFY_STATUS", "failed"),
    "stage": os.environ.get("VERIFY_STAGE", "unknown"),
    "api_base_url": os.environ.get("API_BASE_URL"),
    "web_base_url": os.environ.get("WEB_BASE_URL"),
    "screenshot_path": os.environ.get("SCREENSHOT_PATH"),
    "started_at_epoch": start_ts,
    "api_ready_at_epoch": api_ready_ts,
    "web_ready_at_epoch": web_ready_ts,
    "finished_at_epoch": verify_done_ts,
    "durations_seconds": {
        "api_ready": (api_ready_ts - start_ts) if start_ts and api_ready_ts else None,
        "web_ready": (web_ready_ts - start_ts) if start_ts and web_ready_ts else None,
        "total": (verify_done_ts - start_ts) if start_ts and verify_done_ts else None,
    },
}

Path(os.environ["SUMMARY_PATH"]).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
PY
}

reserve_port() {
  python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
}

if [[ -z "${API_PORT}" ]]; then
  API_PORT="$(reserve_port)"
fi

if [[ -z "${WEB_PORT}" ]]; then
  WEB_PORT="$(reserve_port)"
fi

API_BASE_URL="http://${API_HOST}:${API_PORT}"
WEB_BASE_URL="http://${WEB_HOST}:${WEB_PORT}"

API_PID_FILE="${ROOT}/.web-browser-verify-api.pid"
WEB_PID_FILE="${ROOT}/.web-browser-verify-web.pid"
API_LOG_FILE="${ROOT}/.web-browser-verify-api.log"
WEB_LOG_FILE="${ROOT}/.web-browser-verify-web.log"
DB_FILE="${ROOT}/.web-browser-verify.db"

cleanup() {
  local status="${1:-0}"

  if [[ -f "${WEB_PID_FILE}" ]]; then
    WEB_PID="$(cat "${WEB_PID_FILE}")"
    kill "${WEB_PID}" >/dev/null 2>&1 || true
    wait "${WEB_PID}" 2>/dev/null || true
    rm -f "${WEB_PID_FILE}"
  fi
  if [[ -f "${API_PID_FILE}" ]]; then
    API_PID="$(cat "${API_PID_FILE}")"
    kill "${API_PID}" >/dev/null 2>&1 || true
    wait "${API_PID}" 2>/dev/null || true
    rm -f "${API_PID_FILE}"
  fi
  rm -f "${DB_FILE}" "${DB_FILE}-journal"

  if [[ "${status}" -eq 0 ]]; then
    rm -f "${API_LOG_FILE}" "${WEB_LOG_FILE}"
  else
    VERIFY_STATUS="failed"
    VERIFY_DONE_TS="$(date +%s)"
    write_summary
    echo "Web browser verification failed. Logs preserved:"
    echo "  API: ${API_LOG_FILE}"
    echo "  WEB: ${WEB_LOG_FILE}"
  fi
}

trap 'status=$?; trap - EXIT; cleanup "$status"; exit "$status"' EXIT

rm -f "${API_LOG_FILE}" "${WEB_LOG_FILE}" "${DB_FILE}" "${DB_FILE}-journal"
mkdir -p "${ARTIFACT_DIR}"
rm -f "${SUMMARY_PATH}"

export DATABASE_URL="sqlite:///${DB_FILE}"
export BILLING_ENABLED="${BILLING_ENABLED:-true}"
export ENVIRONMENT="web-browser-verify"

VERIFY_STAGE="boot-api"
.venv/bin/uvicorn apps.api.app.main:app --host "${API_HOST}" --port "${API_PORT}" >"${API_LOG_FILE}" 2>&1 &
echo $! > "${API_PID_FILE}"

VERIFY_STAGE="wait-api-health"
for _ in $(seq 1 30); do
  if curl -fsS "${API_BASE_URL}/health" >/tmp/cogniprint-web-browser-health.json 2>/dev/null; then
    break
  fi
  sleep 1
done

curl -fsS "${API_BASE_URL}/health" >/tmp/cogniprint-web-browser-health.json >/dev/null
API_READY_TS="$(date +%s)"

VERIFY_STAGE="boot-web-preview"
(
  cd "${ROOT}/apps/web"
  if [[ "${SKIP_NPM_CI}" != "1" ]]; then
    npm ci >>"${WEB_LOG_FILE}" 2>&1
  fi
  VITE_API_BASE_URL="${API_BASE_URL}" npm run build >>"${WEB_LOG_FILE}" 2>&1
  npm run preview -- --host "${WEB_HOST}" --port "${WEB_PORT}" >>"${WEB_LOG_FILE}" 2>&1
) &
echo $! > "${WEB_PID_FILE}"

VERIFY_STAGE="wait-web-preview"
for _ in $(seq 1 30); do
  if curl -fsS "${WEB_BASE_URL}" >/tmp/cogniprint-web-browser-root.html 2>/dev/null; then
    break
  fi
  sleep 1
done

curl -fsS "${WEB_BASE_URL}" >/tmp/cogniprint-web-browser-root.html >/dev/null
WEB_READY_TS="$(date +%s)"

cd "${ROOT}/apps/web"
if [[ "${CI:-}" == "true" ]]; then
  VERIFY_STAGE="install-playwright-ci"
  npx playwright install --with-deps chromium >>"${WEB_LOG_FILE}" 2>&1
else
  VERIFY_STAGE="install-playwright-local"
  npx playwright install chromium >>"${WEB_LOG_FILE}" 2>&1
fi
VERIFY_STAGE="browser-verify"
node "${ROOT}/apps/web/scripts/browser_verify.mjs" "${WEB_BASE_URL}" "${SCREENSHOT_PATH}"
VERIFY_STATUS="passed"
VERIFY_DONE_TS="$(date +%s)"
write_summary

echo "Web browser verification passed: ${WEB_BASE_URL} -> ${API_BASE_URL}"
echo "Screenshot: ${SCREENSHOT_PATH}"
echo "Summary: ${SUMMARY_PATH}"
