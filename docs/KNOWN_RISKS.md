# Known Risks

This document outlines potential risks and mitigation strategies for the `Stock` system.

## 1. Local Database Persistence
- **Risk**: The system uses SQLite by default for local development. If pushed to production without changing to PostgreSQL, data may be lost on container restarts (if using non-persistent volumes).
- **Mitigation**: The backend will refuse to start if `ENVIRONMENT=production` and `DATABASE_URL` contains `sqlite`.

## 2. CORS Misconfiguration
- **Risk**: Incorrect `BACKEND_CORS_ORIGINS` will block the SPA from performing API calls.
- **Mitigation**: Test the connection immediately after deploy; keep the `.env` value updated.

## 3. Rate Limiting Backend
- **Risk**: The authentication endpoint has a hard rate limit. Excessive failed setups or bot attacks could lock out legitimate users.
- **Mitigation**: Monitor logs and ensure `storageState` is used for automated testing.

## 4. Frontend SPA Routing
- **Risk**: Direct access to nested routes (e.g., `/dashboard/admin`) might return 404 if the web server is not configured for SPA fallbacks.
- **Mitigation**: Nginx or similar must be configured to serve `index.html` for all unknown routes.

## 5. Secret Key Exposure
- **Risk**: If the `SECRET_KEY` is leaked, JWTs can be forged.
- **Mitigation**: Generate a long, random string in production. Never share the `.env` file.
