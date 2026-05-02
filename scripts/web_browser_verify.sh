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
  rm -f "${DB_FILE}" "${DB_FILE}-journal" "${API_LOG_FILE}" "${WEB_LOG_FILE}"
}

trap cleanup EXIT

rm -f "${API_LOG_FILE}" "${WEB_LOG_FILE}" "${DB_FILE}" "${DB_FILE}-journal"
mkdir -p "${ARTIFACT_DIR}"

export DATABASE_URL="sqlite:///${DB_FILE}"
export BILLING_ENABLED="${BILLING_ENABLED:-true}"
export ENVIRONMENT="web-browser-verify"

.venv/bin/uvicorn apps.api.app.main:app --host "${API_HOST}" --port "${API_PORT}" >"${API_LOG_FILE}" 2>&1 &
echo $! > "${API_PID_FILE}"

for _ in $(seq 1 30); do
  if curl -fsS "${API_BASE_URL}/health" >/tmp/cogniprint-web-browser-health.json 2>/dev/null; then
    break
  fi
  sleep 1
done

curl -fsS "${API_BASE_URL}/health" >/tmp/cogniprint-web-browser-health.json >/dev/null

(
  cd "${ROOT}/apps/web"
  npm ci >>"${WEB_LOG_FILE}" 2>&1
  VITE_API_BASE_URL="${API_BASE_URL}" npm run build >>"${WEB_LOG_FILE}" 2>&1
  npm run preview -- --host "${WEB_HOST}" --port "${WEB_PORT}" >>"${WEB_LOG_FILE}" 2>&1
) &
echo $! > "${WEB_PID_FILE}"

for _ in $(seq 1 30); do
  if curl -fsS "${WEB_BASE_URL}" >/tmp/cogniprint-web-browser-root.html 2>/dev/null; then
    break
  fi
  sleep 1
done

cd "${ROOT}/apps/web"
npx playwright install chromium >>"${WEB_LOG_FILE}" 2>&1
node "${ROOT}/apps/web/scripts/browser_verify.mjs" "${WEB_BASE_URL}" "${SCREENSHOT_PATH}"

echo "Web browser verification passed: ${WEB_BASE_URL} -> ${API_BASE_URL}"
echo "Screenshot: ${SCREENSHOT_PATH}"
