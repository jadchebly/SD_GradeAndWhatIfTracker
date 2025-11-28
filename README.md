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

Deployment in CI

- On successful test + build, the workflow will build the Docker image. The deploy job runs only for pushes to the `main` branch (see `.github/workflows/ci.yml`).
- The current workflow has been updated to push the container image to Azure Container Registry (ACR). It will push:
	- `${ACR_NAME}.azurecr.io/<OWNER>/<REPO>:latest`
	- `${ACR_NAME}.azurecr.io/<OWNER>/<REPO>:<sha>`

Azure secrets / setup

The deploy job uses an Azure service principal to authenticate. You must add the following repository secrets (Repository -> Settings -> Secrets -> Actions):

- `AZURE_CREDENTIALS` — JSON string with the Azure service principal credentials. Create it with the Azure CLI like:

	```bash
	az ad sp create-for-rbac --name "github-actions-acr" --role acrpush --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RG>/providers/Microsoft.ContainerRegistry/registries/<ACR_NAME>
	```

	Take the JSON output from the command and paste it into the `AZURE_CREDENTIALS` secret. The JSON should contain `clientId`, `clientSecret`, `subscriptionId`, and `tenantId`.

- `ACR_NAME` — the short name of your Azure Container Registry (for example, `myregistry`); the workflow uses `${ACR_NAME}.azurecr.io` as the registry host.

Notes:

- The `azure/login` action uses the `AZURE_CREDENTIALS` secret to authenticate. The workflow then runs `az acr login --name $ACR_NAME` to log Docker into the registry before pushing.
- For tighter security you should protect the `main` branch in GitHub (Settings -> Branches -> Protect branch) so only reviewed PRs can be merged and trigger deploys.

Other providers

If you prefer a different Azure target (App Service, Azure Container Instances, AKS, or Web App for Containers) I can add the specific deployment steps — most will reuse the same `AZURE_CREDENTIALS` secret and require an additional resource name (e.g. `AZURE_WEBAPP_NAME`).
