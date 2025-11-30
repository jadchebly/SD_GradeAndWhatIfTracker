1. Code Quality and Testing
Multiple refactoring steps were performed to improve maintainability, readability, and alignment with software engineering best practices.

Refactoring improvements

- Separation of Concerns
	- Database logic was moved into `db.py`.
	- Business logic isolated in `services.py`.
	- Application configuration handled inside `app.py`.

- Removed duplication
	- Centralised shared CRUD logic and repeated error handling.

- SOLID improvements
	- SRP: Each module now has a single responsibility.
	- OCP: New assessment/stat calculation logic can now be added without modifying existing functions.

- No hard-coded values
	- Database URLs and settings now loaded through environment variables + `settings.py`.
	- Improved validation using Pydantic schemas (`schemas.py`).

- Testing improvements
	- Added unit tests for:
		- Calculation engine
		- Services layer
		- Stat/weight logic
	- Added integration tests for all API endpoints using FastAPI TestClient.
	- Achieved ≥ 70% test coverage (verified in CI).
	- Generated `coverage.xml` and `.coverage` reports.
	- Tests are automatically executed on every push via GitHub Actions.

These changes ensure correctness, maintainability, and stability of the codebase.

2. Continuous Integration (CI)

A complete CI pipeline was created using GitHub Actions (`.github/workflows/ci.yaml`).

CI pipeline tasks

- Install Python and project dependencies.
- Run full test suite (pytest).
- Enforce coverage ≥ 70% (pipeline fails otherwise).
- Build Docker image to ensure the container is valid.
- Upload test results + coverage report as workflow artifacts.
- On pushes to main, trigger deployment to Railway.

This ensures that code is always tested, verified, and ready for deployment.

3. Deployment Automation (CD)

Containerization

The application was fully containerized using the provided Dockerfile:

- Based on Python 3.11 slim image.
- Installs dependencies from `backend/requirements.txt`.
- Copies backend and frontend.
- Exposes port 8000.
- Runs FastAPI using Uvicorn.

Cloud Deployment

Deployment is fully automated via:

- GitHub Actions deploy job.
- Railway project linked to the GitHub repository.
- Only the main branch triggers deployment.

Secrets management

- `DATABASE_URL` stored in Railway environment variables.
- `RAILWAY_TOKEN` stored in GitHub Secrets for secure deployment.

This completes full CI/CD deployment automation.

4. Monitoring and Health Checks

Monitoring was added via two key endpoints:

1. `/health` endpoint
	 - Simple JSON response confirming application availability:
		 ```json
		 { "ok": true }
		 ```
2. `/metrics` endpoint
	 - Implemented using `prometheus_client`.
	 - Exposes full Prometheus-compatible metrics including:
		 - HTTP request count
		 - Handler-level statistics
		 - Error rate
		 - Response latency
		 - CPU and memory usage
		 - Python GC stats

