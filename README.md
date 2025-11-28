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
- Builds a Docker image for the application (tagged `grade-tracker:ci`) after tests pass.

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

If you want to tweak the coverage threshold, edit `.github/workflows/ci.yml` (the pytest `--cov-fail-under` value).
# SD_Assignment1
Grades Tracker App

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

Open 
http://127.0.0.1:8000/

Testing:
run pytest -q
