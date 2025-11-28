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

- On successful test + build, the workflow will push the Docker image to GHCR under `ghcr.io/<OWNER>/<REPO>:latest` and `ghcr.io/<OWNER>/<REPO>:<sha>`.
- The deploy job only runs for pushes to the `main` branch (see `.github/workflows/ci.yml`).

Secrets and extra providers

- Pushing to GHCR uses the built-in `GITHUB_TOKEN`. The workflow sets `packages: write` permission so the token can publish packages.
- If you want CI to also deploy to other cloud providers (Heroku, AWS ECR/ECS, GCR, DockerHub), tell me which provider you prefer and I will add the provider-specific steps. Those usually require adding repository secrets (e.g. `HEROKU_API_KEY` / `HEROKU_APP_NAME`, `DOCKERHUB_USERNAME`/`DOCKERHUB_TOKEN`, or cloud service credentials) in the repo `Settings -> Secrets`.

If you want a different deployment target or automatic releases (tags), I can add that next — tell me which cloud provider you want to deploy to and I will update the workflow and documentation.
