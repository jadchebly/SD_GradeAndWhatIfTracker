from datetime import date

from backend import calculations, schemas


class Obj:
    """Lightweight helper to mimic Assessment rows."""

    def __init__(self, weight_pct, score_pct):
        self.weight_pct = weight_pct
        self.score_pct = score_pct


def test_current_stats_mixes_completed_and_pending():
    rows = [
        Obj(30.0, 90.0),  # contributes 27
        Obj(20.0, 50.0),  # contributes 10
        Obj(50.0, None),
    ]
    stats = calculations.current_stats(rows)
    assert isinstance(stats, schemas.CurrentStats)
    assert stats.current_weighted == 37.0
    assert stats.weight_done == 50.0
    assert stats.remaining_weight == 50.0


def test_what_if_with_remaining_work():
    rows = [Obj(40.0, 80.0), Obj(60.0, None)]
    result = calculations.what_if(rows, target=75.0)
    assert isinstance(result, schemas.WhatIf)
    # Need ~71.67 on remaining 60% to reach target
    assert result.required_avg == 71.67
    assert result.attainable is True


def test_what_if_when_no_remaining_work():
    rows = [Obj(50.0, 80.0), Obj(50.0, 90.0)]
    result = calculations.what_if(rows, target=85.0)
    assert result.required_avg is None
    assert result.attainable is True


def test_validate_weights_messages():
    rows = [Obj(40.0, 80.0), Obj(30.0, None)]
    res = calculations.validate_weights(rows)
    assert isinstance(res, schemas.Validation)
    assert res.total_weight == 70.0
    assert res.is_exactly_100 is False
    assert "You can still add" in res.message
