from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend import models, schemas, services


def _session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    models.Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_service_crud_flow():
    session = _session()
    repo = services.AssessmentRepository(session)
    svc = services.AssessmentService(repo)

    payload = schemas.AssessmentIn(
        title="Midterm",
        weight_pct=20.0,
        due_date=date(2025, 11, 1),
        score_pct=None,
    )
    created = svc.create_assessment(payload)
    assert created.id is not None
    assert created.title == "Midterm"

    fetched = svc.get_assessment(created.id)
    assert fetched.id == created.id

    updated = svc.update_assessment(
        created.id, schemas.AssessmentUpdate(score_pct=85.0)
    )
    assert updated.score_pct == 85.0

    all_rows = svc.list_assessments()
    assert len(all_rows) == 1

    svc.delete_assessment(created.id)
    assert svc.list_assessments() == []

