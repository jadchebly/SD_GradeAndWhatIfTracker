Grade & What-If Tracker

A FastAPI application for managing course assessments, computing weighted grades, validating assessment weights, and running what-if scenarios. The project includes:
- FastAPI backend (Python)
- Static frontend served automatically
- CI/CD with GitHub Actions
- Docker-based deployment on Railway
- Monitoring endpoints (/health, /metrics)
- Automated tests with coverage enforcement

🚀 Run the Backend Locally:
Create & activate a virtual environment:
cd backend
python -m venv .venv
Windows:
.venv\Scripts\activate
macOS/Linux:
source .venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Start the server (from project root):
uvicorn backend.app:app --reload

Visit the app in the browser:
http://127.0.0.1:8000/

🧪 Run Tests
Run the full test suite with coverage:
pytest --cov=backend --cov-report=term --cov-report=xml --cov-fail-under=70
This will:
- Run unit + API tests
- Enforce minimum 70% coverage
- Produce coverage.xml

🐳 Run with Docker
Build the image:
docker build -t grade-tracker .

Run the container:
docker run -p 8000:8000 grade-tracker

Then open:
http://localhost:8000/

🔄 CI/CD (GitHub Actions)
The workflow file is located at:
.github/workflows/ci.yaml
The pipeline performs:
- Installs Python
- Installs dependencies
- Runs tests with coverage
- Builds Docker image
- Deploys automatically to Railway when code is pushed to main
- No manual deployment steps required.

🌐 Deployment (Railway)
Railway automatically builds the Dockerfile and deploys the app.
Required Railway variables:
- DATABASE_URL (provided by Railway PostgreSQL)

Required GitHub Secret:
- RAILWAY_TOKEN — enables GitHub Actions to trigger deployments

My app becomes publicly available at the URL:

https://sdgradeandwhatiftracker-production.up.railway.app

❤️ Monitoring & Health

Health check:
GET /health → { "ok": true }

Prometheus metrics:
GET /metrics

Provides:
- Request counters
- Latency histograms
- Error counts
- CPU/memory metrics
- Python runtime & GC metrics
- Per-endpoint stats
