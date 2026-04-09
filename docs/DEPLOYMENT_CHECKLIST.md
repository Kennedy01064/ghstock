# Deployment Checklist

Follow these steps to deploy the `Stock` system to a production environment.

## 1. Prerequisites
- [ ] PostgreSQL Database instance.
- [ ] Redis instance (for rate limiting/cache).
- [ ] Node.js 20+ and Python 3.11+.
- [ ] Domain name and SSL certificates.

## 2. Infrastructure Setup
- [ ] Set up a persistent volume for static assets if needed.
- [ ] Configure PostgreSQL with a strong password.

## 3. Environment Variables
- [ ] Create a `.env` file in the root based on `.env.example`.
- [ ] **MANDATORY**: Set `ENVIRONMENT=production`.
- [ ] **MANDATORY**: Set `SECRET_KEY` (minimum 32 characters).
- [ ] Set `DATABASE_URL` (PostgreSQL).
- [ ] Set `BACKEND_CORS_ORIGINS` to the frontend production URL.

## 4. Backend Deployment
- [ ] Build your virtual environment or Docker image.
- [ ] Run migrations: `alembic upgrade head`.
- [ ] Start backend using Gunicorn:
  ```bash
  gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:8000
  ```

## 5. Frontend Deployment
- [ ] Configure `VITE_API_BASE_URL` in the frontend environment.
- [ ] Run build: `npm run build` inside `frontend-spa`.
- [ ] Serve the `dist/` folder using Nginx/Apache or a PaaS provider.
- [ ] Ensure the server redirects all routes to `index.html` (SPA fallback).

## 6. Post-Deploy Sanity Check
- [ ] Access `/health` on the API.
- [ ] Perform a login with a known user.
- [ ] Verify that images/uploads are correctly handled.
- [ ] Verify that the frontend can communicate with the backend.

## 7. Rollback Plan
- [ ] Keep a backup of the previous database state.
- [ ] Keep the previous build folder/container image tagged.
- [ ] In case of failure, revert environment variables and restart the previous version.
