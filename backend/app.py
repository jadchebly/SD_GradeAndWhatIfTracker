from typing import NoReturn

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from pathlib import Path


from . import db, models, schemas, calculations, services

ALLOWED_ORIGINS = (
    "http://127.0.0.1:5500",
    "http://localhost:5500",
)
NOT_FOUND_DETAIL = "Assessment not found"

app = FastAPI(
    title="Grade & What-If Tracker",
    version="1.0",
)

# CORS so the static frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(ALLOWED_ORIGINS),  # for local dev; tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup (SQLite)
models.Base.metadata.create_all(bind=db.engine)


def get_db():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_assessment_service(session: Session = Depends(get_db)) -> services.AssessmentService:
    return services.AssessmentService(session)


def _raise_not_found(err: Exception) -> NoReturn:
    raise HTTPException(status_code=404, detail=NOT_FOUND_DETAIL) from err


@app.get("/health")
def health():
    return {"ok": True}


# ---- CRUD: Assessments -------------------------------------------------------

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

# ---- Stats: current / what-if / validate ------------------------------------

@app.get("/stats/current", response_model=schemas.CurrentStats)
def current_stats(service: services.AssessmentService = Depends(get_assessment_service)):
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

# ---- Serve the frontend at "/" ----
# Points to the sibling "frontend" folder no matter where uvicorn is launched from.
FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
app.mount(
    "/",  # root path
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend",
)
