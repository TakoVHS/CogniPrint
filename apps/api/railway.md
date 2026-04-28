# Railway Deploy

Service root can use repository root with app path `apps/api`.

Healthcheck path:

`/health`

Start command:

`uvicorn apps.api.app.main:app --host 0.0.0.0 --port $PORT`
