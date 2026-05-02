#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

API_HOST="127.0.0.1"
API_PORT="${WEB_RUNTIME_SMOKE_API_PORT:-}"
WEB_HOST="127.0.0.1"
WEB_PORT="${WEB_RUNTIME_SMOKE_PORT:-}"

if [[ -z "${API_PORT}" ]]; then
  API_PORT="$(python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)"
fi

if [[ -z "${WEB_PORT}" ]]; then
  WEB_PORT="$(python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)"
fi

API_BASE_URL="http://${API_HOST}:${API_PORT}"
WEB_BASE_URL="http://${WEB_HOST}:${WEB_PORT}"
export WEB_RUNTIME_SMOKE_PORT_INTERNAL="${WEB_PORT}"

API_PID_FILE="${ROOT}/.web-runtime-smoke-api.pid"
WEB_PID_FILE="${ROOT}/.web-runtime-smoke-web.pid"
API_LOG_FILE="${ROOT}/.web-runtime-smoke-api.log"
WEB_LOG_FILE="${ROOT}/.web-runtime-smoke-web.log"
DB_FILE="${ROOT}/.web-runtime-smoke.db"

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

export DATABASE_URL="sqlite:///${DB_FILE}"
export BILLING_ENABLED="${BILLING_ENABLED:-true}"
export ENVIRONMENT="web-runtime-smoke"

.venv/bin/uvicorn apps.api.app.main:app --host "${API_HOST}" --port "${API_PORT}" >"${API_LOG_FILE}" 2>&1 &
echo $! > "${API_PID_FILE}"

for _ in $(seq 1 30); do
  if curl -fsS "${API_BASE_URL}/health" >/tmp/cogniprint-web-runtime-health.json 2>/dev/null; then
    break
  fi
  sleep 1
done

curl -fsS "${API_BASE_URL}/ready" >/tmp/cogniprint-web-runtime-ready.json
curl -fsS "${API_BASE_URL}/account/status?user_id=web-runtime-smoke-user" >/tmp/cogniprint-web-runtime-account.json
curl -fsS \
  -H "Content-Type: application/json" \
  -d '{"text":"CogniPrint web runtime smoke request for hosted app verification.","user_id":"web-runtime-smoke-user"}' \
  "${API_BASE_URL}/scan" >/tmp/cogniprint-web-runtime-scan.json

python3 -m json.tool /tmp/cogniprint-web-runtime-ready.json >/dev/null
python3 -m json.tool /tmp/cogniprint-web-runtime-account.json >/dev/null
python3 -m json.tool /tmp/cogniprint-web-runtime-scan.json >/dev/null

(
  cd "${ROOT}/apps/web"
  VITE_API_BASE_URL="${API_BASE_URL}" npm run build >>"${WEB_LOG_FILE}" 2>&1
  npm run preview -- --host "${WEB_HOST}" --port "${WEB_PORT}" >>"${WEB_LOG_FILE}" 2>&1
) &
echo $! > "${WEB_PID_FILE}"

for _ in $(seq 1 30); do
  if curl -fsS "${WEB_BASE_URL}" >/tmp/cogniprint-web-runtime-root.html 2>/dev/null; then
    break
  fi
  sleep 1
done

curl -fsS "${WEB_BASE_URL}" >/tmp/cogniprint-web-runtime-root.html

python3 - <<'PY'
import pathlib
import re
import urllib.request

web_base = pathlib.Path("/tmp/cogniprint-web-runtime-root.html").read_text(encoding="utf-8")
assert 'id="root"' in web_base
assert '/assets/' in web_base

match = re.search(r'src="([^"]+\.js)"', web_base)
assert match, "No JS entry asset found in preview HTML"
asset_path = match.group(1)
if not asset_path.startswith("/"):
    asset_path = "/" + asset_path
asset_url = "http://127.0.0.1:" + str(__import__("os").environ["WEB_RUNTIME_SMOKE_PORT_INTERNAL"]) + asset_path
bundle = urllib.request.urlopen(asset_url, timeout=10).read().decode("utf-8")

for needle in ("/ready", "/scan", "/account/status", "/api/billing/create-checkout-session"):
    assert needle in bundle, f"Missing runtime surface marker: {needle}"
PY

echo "Web runtime smoke passed: ${WEB_BASE_URL} -> ${API_BASE_URL}"
