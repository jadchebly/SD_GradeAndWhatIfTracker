from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# --------- Assessment I/O models ----------


class AssessmentBase(BaseModel):
    title: str
    weight_pct: float = Field(ge=0, le=100)
    due_date: date
    score_pct: Optional[float] = Field(default=None, ge=0, le=100)


class AssessmentIn(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    weight_pct: Optional[float] = Field(default=None, ge=0, le=100)
    due_date: Optional[date] = None
    score_pct: Optional[float] = Field(default=None, ge=0, le=100)


class AssessmentOut(AssessmentBase):
    id: int

    class Config:
        orm_mode = True


# --------- Stats response models ----------


class CurrentStats(BaseModel):
    current_weighted: float
    weight_done: float
    remaining_weight: float


class WhatIf(BaseModel):
    target: float
    required_avg: Optional[float]  # None if no remaining work
    attainable: bool


class Validation(BaseModel):
    total_weight: float
    is_exactly_100: bool
    message: str
