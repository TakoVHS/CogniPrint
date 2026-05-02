# Frontend Deploy

Platform: Vercel.

Project root:

`apps/web`

Build command:

`npm run build`

Output directory:

`dist`

Required environment variable:

`VITE_API_BASE_URL=https://<railway-api-domain>`

Expected backend integration surface:

- `GET /ready`
- `GET /account/status`
- `POST /scan`
