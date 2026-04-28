# Vercel Launch Guide — CogniPrint Frontend

This document describes how to deploy the CogniPrint frontend (`apps/web`) to [Vercel](https://vercel.com).

---

## Project Settings

When importing the repository into Vercel, configure the following:

| Setting | Value |
|---|---|
| **Root Directory** | `apps/web` |
| **Framework Preset** | Vite |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |
| **Install Command** | `npm install` |

Vercel auto-detects Vite when the root directory is set correctly. If it doesn't, select **Vite** from the framework dropdown manually.

---

## Environment Variables

### Required

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Full URL of the deployed Railway API, e.g. `https://your-project.up.railway.app` |

Set this in **Vercel → Project → Settings → Environment Variables** for the `Production` environment (and `Preview` if you want preview deployments to hit a staging API).

> **Note:** `VITE_` prefix is required by Vite to expose the variable to the browser bundle. Variables without this prefix are not embedded into the build.

### Setting via Vercel CLI

```bash
vercel env add VITE_API_BASE_URL production
# Enter value when prompted: https://your-project.up.railway.app
```

---

## Deploying

### Via Vercel Dashboard (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new).
2. Import the `TakoVHS/CogniPrint` repository.
3. Set **Root Directory** to `apps/web`.
4. Add the `VITE_API_BASE_URL` environment variable.
5. Click **Deploy**.

### Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# From repo root
cd apps/web

# First deploy (interactive — sets project settings)
vercel

# Subsequent production deploys
vercel --prod
```

---

## vercel.json Reference

`apps/web/vercel.json` is already configured:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite"
}
```

---

## Custom Domain

1. In Vercel dashboard, go to **Project → Settings → Domains**.
2. Add your domain (e.g. `app.cogniprint.org`).
3. Follow the DNS instructions to add a CNAME record.
4. Update `FRONTEND_URL` in Railway to match the custom domain:
   ```bash
   railway variables set FRONTEND_URL="https://app.cogniprint.org"
   ```

---

## CORS Configuration

The backend reads `FRONTEND_URL` from the environment and restricts CORS to that origin in production. If `FRONTEND_URL` is not set, it defaults to `*` (permissive, for local dev only).

Always set `FRONTEND_URL` in Railway before going live.

---

## Preview Deployments

Vercel creates a unique URL for every pull request. To point preview builds at a separate staging API:

1. Create a staging Railway environment.
2. Set `VITE_API_BASE_URL` for the `Preview` scope in Vercel to the staging Railway URL.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Blank page after deploy | Check browser console for `VITE_API_BASE_URL` being `undefined`; re-add the env var |
| CORS error in browser | Ensure `FRONTEND_URL` in Railway exactly matches the Vercel deployment URL (no trailing slash) |
| Build fails with TS errors | Run `npm run build` locally to reproduce; check `tsconfig.json` |
| 502 on `/scan` | The API is not running; check Railway logs with `railway logs` |
