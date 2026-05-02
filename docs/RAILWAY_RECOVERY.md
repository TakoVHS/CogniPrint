# Railway Recovery Guide — CogniPrint

This guide walks through recovering and standardising a Railway deployment
for CogniPrint after an accidental service was created.

---

## Canonical Layout

| Item | Value |
|---|---|
| **Project** | `CogniPrint Production` |
| **API service** | `cogniprint-api` |
| **DB service** | `cogniprint-db` |
| **Frontend** | Not on Railway (deployed to Vercel) |

---

## Step 1 — Verify Railway Login

```bash
# Check that the CLI is installed
railway --version

# Log in (opens browser)
railway login

# Confirm your identity
railway whoami
```

Expected output of `railway whoami`:

```
Logged in as <your-email>@example.com
```

If `railway whoami` returns nothing or an error, run `railway login` again.
For headless / CI environments:

```bash
railway login --browserless
```

---

## Step 2 — Check the Linked Project

```bash
# From inside the repo directory:
railway status
```

Expected output contains something like:

```
Project:     CogniPrint Production
Environment: production
Service:     cogniprint-api
```

If the wrong project is linked (or nothing is linked), see **Step 6 — Relink**.

---

## Step 3 — List All Services

Railway CLI does not have a `railway services list` command.
Use the dashboard or the following:

```bash
# Opens the Railway project in your browser
railway open
```

From the dashboard you can see every service in the project and their names.

Alternatively, inspect the linked service directly:

```bash
railway status
```

---

## Step 4 — Delete the Accidental Service `grateful-beauty`

> ⚠️ **This is destructive and irreversible. Confirm the service name before
> proceeding.**

1. Open the Railway dashboard:

   ```bash
   railway open
   ```

2. In the project view, locate the service named **`grateful-beauty`**.
3. Click on it → **Settings** → scroll to the bottom → **Delete Service**.
4. Type the service name to confirm deletion.

**CLI alternative** (Railway CLI ≥ 3.x):

```bash
# Switch the CLI context to the accidental service first
railway service

# Then delete it via the dashboard URL that the command prints,
# or use the interactive Railway dashboard.
```

> Railway CLI does not expose a `railway service delete` command.
> Deletion must be done through the dashboard.

---

## Step 5 — Create the Canonical Service `cogniprint-api`

1. Open the Railway dashboard (`railway open`).
2. Inside **CogniPrint Production**, click **+ New Service → Empty Service**.
3. Rename the service to **`cogniprint-api`**.
4. Connect the GitHub repo `TakoVHS/CogniPrint` to this service:
   - Service Settings → Source → Connect Repo → select `TakoVHS/CogniPrint`.
5. Railway will detect `railway.json` and use the NIXPACKS builder automatically.
6. Set environment variables (see **Environment Variables** below).
7. Click **Deploy**.

For the database, add a managed Postgres service:

1. **+ New Service → Database → PostgreSQL**.
2. Rename it to **`cogniprint-db`**.
3. Railway will inject `DATABASE_URL` into `cogniprint-api` automatically once
   both services are in the same project.

---

## Step 6 — Relink the Local Repo Directory

If your local working copy is linked to the wrong project or service:

```bash
# From the repo root — unlink current project
railway unlink

# Re-link to the correct project and service interactively
railway link
```

`railway link` will present a list of your projects and services to choose from.
Select **CogniPrint Production** → **cogniprint-api**.

Verify the result:

```bash
railway status
```

---

## Step 7 — Validate the Deployment

After linking and deploying, run the smoke-test script:

```bash
bash scripts/railway_smoke.sh
```

It will check `railway status`, retrieve the domain, verify `GET /health`,
and then verify `GET /ready` before treating the deploy as operational.

For a local runtime check of the optional API layer, also run:

```bash
make api-runtime-smoke
```

---

## Environment Variables

### Required Secrets (set manually — never commit)

```bash
railway variables set DATABASE_URL="postgresql://user:pass@host:5432/dbname"
railway variables set FRONTEND_URL="https://your-vercel-app.vercel.app"
railway variables set STRIPE_SECRET_KEY="sk_live_..."
railway variables set STRIPE_WEBHOOK_SECRET="whsec_..."
railway variables set STRIPE_PRICE_RESEARCH_PRO="price_..."
railway variables set STRIPE_PRICE_STARTER="price_..."   # optional
```

### Safe Defaults (can be scripted)

```bash
railway variables set \
  ENVIRONMENT=production \
  FREE_DAILY_SCAN_LIMIT=3 \
  MAX_TEXT_CHARS_FREE=12000 \
  MAX_TEXT_CHARS_PRO=120000
```

---

## Quick-Reference Commands

```bash
# Check status / linked service
railway status

# Tail live logs
railway logs

# Open dashboard in browser
railway open

# List / switch service context
railway service

# Unlink current project
railway unlink

# Link to a project interactively
railway link

# Deploy current commit
railway up

# List environment variables
railway variables
```

---

## See Also

- [`docs/RAILWAY_CLI.md`](RAILWAY_CLI.md) — Full deployment guide
- [`scripts/railway_recover.sh`](../scripts/railway_recover.sh) — Interactive recovery helper
- [`scripts/railway_smoke.sh`](../scripts/railway_smoke.sh) — Post-deploy health + readiness test
- [`scripts/api_runtime_smoke.sh`](../scripts/api_runtime_smoke.sh) — Local runtime smoke for the optional API layer
