# Algo Novo — Backend

FastAPI + SQLite. Serves auth, product catalog, orders and admin management.

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env (set SECRET_KEY at minimum)
python -m app.seed         # creates admin user + seeds products
python run.py              # starts server on http://127.0.0.1:8000
```

Admin default: `admin@algonovo.pt` / `1234567` (change via `.env` before `python -m app.seed`).

## Endpoints (summary)

Auth
- `POST /api/auth/register` — email/password + captcha
- `POST /api/auth/login`    — email/password + captcha (client)
- `POST /api/auth/admin/login` — email/password (admin, no captcha)
- `POST /api/auth/logout`
- `GET  /api/auth/me`
- `GET  /api/auth/captcha` — returns `{ token, question }`
- `GET  /api/auth/oauth/{provider}` — start OAuth (google | facebook)
- `GET  /api/auth/oauth/{provider}/callback` — handled by backend

Products
- `GET  /api/products` — active products only (public)

Orders
- `POST   /api/orders` — create order (auth required). multipart/form-data if art file.
- `GET    /api/orders` — my orders (client) or all (admin)
- `GET    /api/orders/{id}` — one order (owner or admin)

Admin
- `GET    /api/admin/products` — all products (including inactive)
- `PATCH  /api/admin/products/{id}` — update (price/active/etc.)
- `PATCH  /api/admin/orders/{id}` — update status

Uploads served under `/uploads/…`.

## OAuth

Fill `GOOGLE_CLIENT_ID`, `FACEBOOK_CLIENT_ID`, etc. in `.env`. Providers with empty creds are disabled and the button won't do anything. Register the callback URLs at each provider:

- `http://127.0.0.1:8000/api/auth/oauth/google/callback`
- `http://127.0.0.1:8000/api/auth/oauth/facebook/callback`
