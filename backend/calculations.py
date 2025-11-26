from typing import Iterable, Protocol

from . import schemas

# rows are objects with: weight_pct (float), score_pct (float|None)
class AssessmentScore(Protocol):
    weight_pct: float
    score_pct: float | None


def _split(rows: Iterable[AssessmentScore]) -> tuple[list[AssessmentScore], float]:
    scored = [r for r in rows if getattr(r, "score_pct", None) is not None]
    weight_done = sum(float(r.weight_pct) for r in scored)
    return scored, weight_done


def current_stats(rows: Iterable[AssessmentScore]) -> schemas.CurrentStats:
    scored, weight_done = _split(rows)
    completed = sum(float(r.weight_pct) * float(r.score_pct) for r in scored)
    current_weighted = (completed / 100.0) if weight_done > 0 else 0.0
    remaining = max(0.0, 100.0 - weight_done)
    return schemas.CurrentStats(
        current_weighted=round(current_weighted, 2),
        weight_done=round(weight_done, 2),
        remaining_weight=round(remaining, 2),
    )


def what_if(rows: Iterable[AssessmentScore], target: float) -> schemas.WhatIf:
    stats = current_stats(rows)
    rem = stats.remaining_weight
    if rem == 0:
        return schemas.WhatIf(
            target=target,
            required_avg=None,
            attainable=stats.current_weighted >= target,
        )
    req = (target - stats.current_weighted) * 100.0 / rem
    return schemas.WhatIf(
        target=target,
        required_avg=round(req, 2),
        attainable=0 <= req <= 100,
    )


def validate_weights(rows: Iterable[AssessmentScore]) -> schemas.Validation:
    total = round(sum(float(r.weight_pct) for r in rows), 2)
    is_exact = abs(total - 100.0) < 1e-6
    if is_exact:
        msg = "Weights sum to 100%."
    elif total < 100.0:
        msg = f"Weights sum to {total}%. You can still add {round(100.0 - total, 2)}%."
    else:
        msg = f"Weights exceed 100% (total {total}%). Consider reducing some weights."
    return schemas.Validation(
        total_weight=total,
        is_exactly_100=bool(is_exact),
        message=msg,
    )
