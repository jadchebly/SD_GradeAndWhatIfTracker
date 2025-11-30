# Deployment & CI Report

## Summary
- CI: GitHub Actions runs tests, measures coverage (fail if <70%), and builds a Docker image.
- CD: GitHub Actions deploys to Railway on pushes to `main` using the Railway CLI and the `RAILWAY_TOKEN` secret.

## What I changed
- Added Prometheus metrics endpoint `/metrics` to `backend/app.py`.
- Added `prometheus-client` to `backend/requirements.txt`.
- Updated `.github/workflows/ci.yaml` deploy job to deploy to Railway using the Railway CLI and `RAILWAY_TOKEN`.
- Added documentation in `README.md` describing CI/CD, Railway setup, monitoring endpoints, and required secrets.

## How to verify
1. Add `RAILWAY_TOKEN` as a repository secret.
2. Push a commit to `main` or re-run the workflow from the Actions UI.
3. Watch the Actions run: tests -> build -> deploy. On successful deploy, check the Railway project dashboard.

## Notes & next steps
- Consider using GitHub's OIDC + Railway for tokenless auth if Railway supports it in the future.
- Consider adding health & uptime monitoring, alerting, and metrics scraping (Prometheus) for production.

*** End of report.
