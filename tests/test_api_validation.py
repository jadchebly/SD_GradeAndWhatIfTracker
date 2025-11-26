# tests/test_api_validation.py

import pytest

def post(client, payload):
    return client.post("/assessments", json=payload)

def base_payload(**overrides):
    data = {
        "title": "Any",
        "weight_pct": 20.0,
        "due_date": "2025-01-10",
        "score_pct": None,
    }
    data.update(overrides)
    return data

@pytest.mark.parametrize("bad_weight", [-1, 101, 1000])
def test_post_rejects_invalid_weight_range(client, bad_weight):
    r = post(client, base_payload(weight_pct=bad_weight))
    assert r.status_code == 422

@pytest.mark.parametrize("bad_score", [-5, 105, 1000])
def test_post_rejects_invalid_score_range(client, bad_score):
    r = post(client, base_payload(score_pct=bad_score))
    assert r.status_code == 422

@pytest.mark.parametrize("bad_date", ["", "not-a-date", "2025/01/01", "13-40-9999"])
def test_post_rejects_invalid_date_format(client, bad_date):
    r = post(client, base_payload(due_date=bad_date))
    assert r.status_code == 422

def test_post_requires_title(client):
    r = post(client, {"weight_pct": 10.0, "due_date": "2025-01-01"})
    assert r.status_code == 422

def test_put_rejects_bad_updates(client):
    # create a good row
    created = post(client, base_payload(title="X")).json()
    # try to set invalid score on update
    bad = dict(created, score_pct=1000)
    r = client.put(f"/assessments/{created['id']}", json=bad)
    assert r.status_code == 422
