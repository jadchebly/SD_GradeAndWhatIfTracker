from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from . import models, schemas


class AssessmentNotFound(Exception):
    """Raised when an assessment row cannot be located."""

    def __init__(self, assessment_id: int) -> None:
        super().__init__(f"Assessment {assessment_id} not found")
        self.assessment_id = assessment_id


class AssessmentRepository:
    """Persistence boundary for assessments."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self, ordered: bool = True) -> list[models.Assessment]:
        query = self._session.query(models.Assessment)
        if ordered:
            query = query.order_by(models.Assessment.due_date)
        return query.all()

    def get(self, assessment_id: int) -> models.Assessment | None:
        return self._session.get(models.Assessment, assessment_id)

    def save(self, assessment: models.Assessment) -> models.Assessment:
        self._session.add(assessment)
        self._session.commit()
        self._session.refresh(assessment)
        return assessment

    def delete(self, assessment: models.Assessment) -> None:
        self._session.delete(assessment)
        self._session.commit()


class AssessmentService:
    """Encapsulates CRUD operations for assessments."""

    def __init__(self, repository: AssessmentRepository) -> None:
        self._repository = repository

    def list_assessments(self, ordered: bool = True) -> list[models.Assessment]:
        return self._repository.list(ordered)

    def get_assessment(self, assessment_id: int) -> models.Assessment:
        assessment = self._repository.get(assessment_id)
        if assessment is None:
            raise AssessmentNotFound(assessment_id)
        return assessment

    def create_assessment(self, payload: schemas.AssessmentIn) -> models.Assessment:
        assessment = models.Assessment(**payload.dict())
        return self._repository.save(assessment)

    def update_assessment(
        self, assessment_id: int, payload: schemas.AssessmentUpdate
    ) -> models.Assessment:
        assessment = self.get_assessment(assessment_id)
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(assessment, field, value)
        return self._repository.save(assessment)

    def delete_assessment(self, assessment_id: int) -> None:
        assessment = self.get_assessment(assessment_id)
        self._repository.delete(assessment)

    def list_for_stats(self) -> Iterable[models.Assessment]:
        """Internal helper to keep stats queries consistent."""
        return self.list_assessments(ordered=False)
