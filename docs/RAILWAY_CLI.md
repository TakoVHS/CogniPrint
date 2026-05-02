# Railway CLI — CogniPrint Deployment Guide

This document describes how to deploy the CogniPrint Content Scanner API to [Railway](https://railway.app) using the Railway CLI and the helper scripts in `scripts/`.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Railway CLI | latest |
| Python | ≥ 3.10 |
| A Railway account | — |

### Install Railway CLI

```bash
# Linux / WSL (recommended)
curl -fsSL https://railway.app/install.sh | sh

# npm (cross-platform)
npm install -g @railway/cli

# Homebrew (macOS)
brew install railway
```

Verify:

```bash
railway --version
```

---

## Quick Start

```bash
# 1. Clone the repo (if needed)
git clone https://github.com/TakoVHS/CogniPrint.git
cd CogniPrint

# 2. Run the launch script
bash scripts/railway_cli_launch.sh

# For headless / CI environments (no browser):
bash scripts/railway_cli_launch.sh --browserless
```

The script will:

1. Check for the Railway CLI and print install instructions if missing
2. Log you in via browser (`railway login`) or token (`--browserless`)
3. Confirm your identity with `railway whoami`
4. Link or initialise the project (`railway link` / `railway init`)
5. Set safe non-secret environment variables
6. Print exact commands for you to set the secrets manually
7. Run `railway up` to trigger the deployment
8. Print the Railway domain
9. Poll `GET /health` until it returns HTTP 200
10. Verify `GET /ready` before treating the deploy as ready

---

## Environment Variables

### Set Automatically by the Launch Script

| Variable | Value |
|---|---|
| `ENVIRONMENT` | `production` |
| `FREE_DAILY_SCAN_LIMIT` | `3` |
| `MAX_TEXT_CHARS_FREE` | `12000` |
| `MAX_TEXT_CHARS_PRO` | `120000` |

### Must Be Set Manually by the Project Owner

These contain secrets and must **never** be committed or scripted:

```bash
railway variables set DATABASE_URL="postgresql://user:pass@host:5432/dbname"
railway variables set FRONTEND_URL="https://your-vercel-app.vercel.app"
railway variables set STRIPE_SECRET_KEY="sk_live_..."
railway variables set STRIPE_WEBHOOK_SECRET="whsec_..."
railway variables set STRIPE_PRICE_RESEARCH_PRO="price_..."
railway variables set STRIPE_PRICE_STARTER="price_..."   # optional
```

`DATABASE_URL` is provisioned automatically when you add a **PostgreSQL** plugin inside the Railway project dashboard.

---

## Validate Environment Variables

Before deploying, or to audit a live deployment:

```bash
bash scripts/railway_env_check.sh
```

The script loads variables from Railway (if the CLI is linked) and reports any missing required vars with the exact `railway variables set` command needed to fix them.

---

## railway.json Reference

The `railway.json` at the repo root is already configured for production:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn apps.api.app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

| Setting | Value | Notes |
|---|---|---|
| `builder` | `NIXPACKS` | Auto-detects Python, installs `requirements.txt` |
| `startCommand` | `uvicorn ... --port $PORT` | Railway injects `$PORT` automatically |
| `healthcheckPath` | `/health` | Shallow liveness endpoint used by Railway |
| `healthcheckTimeout` | `300` | Seconds before Railway marks the deploy unhealthy |
| `restartPolicyType` | `ON_FAILURE` | Auto-restarts crashed containers |
| `restartPolicyMaxRetries` | `10` | |

---

## Useful Railway CLI Commands

```bash
# Check deployment status
railway status

# Tail live logs
railway logs

# Open the Railway dashboard in browser
railway open

# List all environment variables
railway variables

# Re-deploy from the current commit
railway up

# SSH into the running container
railway shell
```

---

## Adding a Database

1. In the Railway dashboard, open your project.
2. Click **+ New Service → Database → PostgreSQL**.
3. Railway will inject `DATABASE_URL` automatically into your API service.
4. The API will create all tables on startup via `create_tables()`.

---

## Healthcheck Endpoint

```
GET /health
```

Expected response:

```json
{
  "ok": true,
  "service": "cogniprint-content-scanner-api",
  "version": "0.1.0"
}
```

Railway polls this endpoint to determine deploy health. The deploy is marked **failed** if this returns a non-2xx status within `healthcheckTimeout` seconds.

## Readiness Endpoint

```
GET /ready
```

Expected response includes:

```json
{
  "ok": true,
  "database": "ok"
}
```

Use `/ready` for deploy-time verification and operational smoke checks after Railway reports the service healthy.
