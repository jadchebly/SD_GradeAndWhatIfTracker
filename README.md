# Grade & What-If Tracker

Simple app to track course assessments, compute current weighted grade, show remaining weight, and run what-if targets.

## Run backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
# Grade & What-If Tracker

Simple app to track course assessments, compute current weighted grade, show remaining weight, and run what-if targets.

## Run backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cd ..
uvicorn backend.app:app --reload

Open http://127.0.0.1:8000/
```

Testing:

```bash
pytest -q
```

## Continuous Integration (CI)

This repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` that:

- Installs dependencies from `backend/requirements.txt`.
- Runs the test suite with coverage. The job fails if coverage is below 70%.
- Builds a Docker image for the application and — on pushes to `main` — pushes the image to GitHub Container Registry (GHCR).

Run the CI steps locally (same commands used by the workflow):

```bash
# from repo root
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pytest --cov=backend --cov-report=term --cov-report=xml --cov-fail-under=70 -q

# build the Docker image (requires Docker installed)
docker build -t grade-tracker:local -f Dockerfile .
```

Deployment in CI

- On successful test + build, the workflow will build the Docker image and then run a deploy job when changes are pushed to the `main` branch.

Railway deployment

This repository deploys to Railway from the `main` branch using the Railway CLI. The `deploy` job in `.github/workflows/ci.yaml` will:

- Validate that the `RAILWAY_TOKEN` repository secret is present.
- Install the Railway CLI and log in using the token.
- Run `railway up --ci --detach` to deploy the current repository to the Railway project linked to this repo.

Required GitHub secret for Railway (Repository -> Settings -> Secrets -> Actions):

- `RAILWAY_TOKEN` — a Railway API token with deploy permissions. Create it in Railway (Account -> Settings -> API Keys) or via the Railway dashboard.

Railway setup

1. Create or sign in to your Railway account at https://railway.app.
2. Create a new project and connect your GitHub repository (the Railway UI will guide you through linking the repository to a project and environment).
3. In Railway, create any necessary environment variables (the UI provides a place to add them). Mirror these in GitHub Secrets as needed for the workflow.
4. Create a Railway API token (Account -> Settings -> API Keys) and add it to this repository as the `RAILWAY_TOKEN` secret.

Monitoring endpoints

- `/health` — quick health check; returns `{ "ok": true }`.
- `/metrics` — Prometheus metrics endpoint (provided by `prometheus-client`).

Secrets and branch protection

- Protect the `main` branch (Settings -> Branches -> Protect branch) to require reviews/checks before merging. The deploy job only runs on `main` and will not run for pull requests.

If you'd like help connecting the repository in Railway or configuring environment variables there, tell me and I can provide step-by-step guidance or add additional workflow steps to set environment variables using the Railway CLI.
