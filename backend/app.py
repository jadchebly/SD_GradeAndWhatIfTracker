from typing import NoReturn
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import calculations, models, schemas, services
from .db import SessionLocal, engine
from .settings import Settings, settings

NOT_FOUND_DETAIL = "Assessment not found"


# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_assessment_service(
    session: Session = Depends(get_db),
) -> services.AssessmentService:
    repository = services.AssessmentRepository(session)
    return services.AssessmentService(repository)


def get_settings() -> Settings:
    return settings


def _raise_not_found(err: Exception) -> NoReturn:
    raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL) from err


# -----------------------------
# Application Factory
# -----------------------------
def create_app(app_settings: Settings = settings) -> FastAPI:
    app = FastAPI(
        title=app_settings.app_title,
        version=app_settings.app_version,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(app_settings.allowed_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Auto-create tables (SQLite or Postgres)
    if app_settings.auto_create_tables:

        @app.on_event("startup")
        def _create_tables() -> None:
            models.Base.metadata.create_all(bind=engine)

    # -----------------------------
    # Monitoring: Prometheus Instrumentation
    # -----------------------------
    try:
        from prometheus_fastapi_instrumentator import Instrumentator

        Instrumentator().instrument(app).expose(app)
    except Exception:
        # Safe fallback — tests may not have this package installed
        pass

    # Register API routes
    _register_routes(app)

    return app


# -----------------------------
# Routes / API Endpoints
# -----------------------------
def _register_routes(app: FastAPI) -> None:

    # ---- Health Check ---------------------------------------------------
    @app.get("/health")
    def health():
        return {"ok": True}

    # ---- Basic Metrics Endpoint (backup) --------------------------------
    # Instrumentator already exposes /metrics, but this is a fallback
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

        @app.get("/metrics")
        def metrics():
            data = generate_latest()
            return Response(content=data, media_type=CONTENT_TYPE_LATEST)

    except Exception:
        pass

    # ---- CRUD: Assessments ----------------------------------------------
    @app.post("/assessments", response_model=schemas.AssessmentOut)
    def create_assessment(
        payload: schemas.AssessmentIn,
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        return service.create_assessment(payload)

    @app.get("/assessments", response_model=list[schemas.AssessmentOut])
    def list_assessments(
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        return service.list_assessments()

    @app.get("/assessments/{aid}", response_model=schemas.AssessmentOut)
    def get_assessment(
        aid: int,
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        try:
            return service.get_assessment(aid)
        except services.AssessmentNotFound as err:
            _raise_not_found(err)

    @app.put("/assessments/{aid}", response_model=schemas.AssessmentOut)
    def update_assessment(
        aid: int,
        payload: schemas.AssessmentUpdate,
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        try:
            return service.update_assessment(aid, payload)
        except services.AssessmentNotFound as err:
            _raise_not_found(err)

    @app.delete("/assessments/{aid}")
    def delete_assessment(
        aid: int,
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        try:
            service.delete_assessment(aid)
            return {"ok": True}
        except services.AssessmentNotFound as err:
            _raise_not_found(err)

    # ---- Stats: current / what-if / validate ----------------------------
    @app.get("/stats/current", response_model=schemas.CurrentStats)
    def current_stats(
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        return calculations.current_stats(service.list_for_stats())

    @app.get("/stats/what-if", response_model=schemas.WhatIf)
    def what_if(
        target: float,
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        return calculations.what_if(service.list_for_stats(), target)

    @app.get("/stats/validate", response_model=schemas.Validation)
    def validate_weights(
        service: services.AssessmentService = Depends(get_assessment_service),
    ):
        return calculations.validate_weights(service.list_for_stats())

    # ---- Serve Frontend --------------------------------------------------
    frontend_dir = Path(__file__).resolve().parents[1] / "frontend"

    if frontend_dir.exists():
        app.mount(
            "/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend"
        )


# -----------------------------
# ASGI Server Entrypoint
# -----------------------------
app = create_app()
