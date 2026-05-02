#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

HOST="${API_RUNTIME_SMOKE_HOST:-127.0.0.1}"
PORT="${API_RUNTIME_SMOKE_PORT:-}"

if [[ -z "${PORT}" ]]; then
  PORT="$(python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)"
fi

BASE_URL="http://${HOST}:${PORT}"
PID_FILE="${ROOT}/.api-runtime-smoke.pid"
LOG_FILE="${ROOT}/.api-runtime-smoke.log"
DB_FILE="${ROOT}/.api-runtime-smoke.db"

cleanup() {
  if [[ -f "${PID_FILE}" ]]; then
    PID="$(cat "${PID_FILE}")"
    kill "${PID}" >/dev/null 2>&1 || true
    wait "${PID}" 2>/dev/null || true
    rm -f "${PID_FILE}"
  fi
  rm -f "${DB_FILE}" "${DB_FILE}-journal" "${LOG_FILE}"
}

trap cleanup EXIT

rm -f "${LOG_FILE}" "${DB_FILE}" "${DB_FILE}-journal"

export DATABASE_URL="sqlite:///${DB_FILE}"
export BILLING_ENABLED="${BILLING_ENABLED:-true}"
export ENVIRONMENT="runtime-smoke"

.venv/bin/uvicorn apps.api.app.main:app --host "${HOST}" --port "${PORT}" >"${LOG_FILE}" 2>&1 &
echo $! > "${PID_FILE}"

for _ in $(seq 1 30); do
  if curl -fsS "${BASE_URL}/health" >/tmp/cogniprint-runtime-health.json 2>/dev/null; then
    break
  fi
  sleep 1
done

curl -fsS "${BASE_URL}/health" >/tmp/cogniprint-runtime-health.json
curl -fsS "${BASE_URL}/ready" >/tmp/cogniprint-runtime-ready.json
curl -fsS "${BASE_URL}/api/billing/config" >/tmp/cogniprint-runtime-billing.json
curl -fsS \
  -H "Content-Type: application/json" \
  -d '{"text":"CogniPrint runtime smoke request for optional API layer.","user_id":"runtime-smoke-user"}' \
  "${BASE_URL}/scan" >/tmp/cogniprint-runtime-scan.json

python3 -m json.tool /tmp/cogniprint-runtime-health.json >/dev/null
python3 -m json.tool /tmp/cogniprint-runtime-ready.json >/dev/null
python3 -m json.tool /tmp/cogniprint-runtime-billing.json >/dev/null
python3 -m json.tool /tmp/cogniprint-runtime-scan.json >/dev/null

python3 - <<'PY'
import json

with open("/tmp/cogniprint-runtime-health.json", "r", encoding="utf-8") as fh:
    health = json.load(fh)
with open("/tmp/cogniprint-runtime-ready.json", "r", encoding="utf-8") as fh:
    ready = json.load(fh)
with open("/tmp/cogniprint-runtime-billing.json", "r", encoding="utf-8") as fh:
    billing = json.load(fh)
with open("/tmp/cogniprint-runtime-scan.json", "r", encoding="utf-8") as fh:
    scan = json.load(fh)

assert health["ok"] is True
assert ready["ok"] is True
assert ready["database"] == "ok"
assert "plans" in billing
assert "content_hash" in scan
assert "metrics" in scan
assert "fingerprint_vector" in scan
PY

echo "API runtime smoke passed: ${BASE_URL}"
