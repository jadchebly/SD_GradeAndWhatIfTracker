# tests/test_api_stats.py

def seed(client):
    """Create a stable set of rows for stats tests."""
    client.post("/assessments", json={"title":"A1","weight_pct":30.0,"due_date":"2025-10-01","score_pct":90.0})  # contributes 27
    client.post("/assessments", json={"title":"A2","weight_pct":30.0,"due_date":"2025-11-01","score_pct":80.0})  # contributes 24
    client.post("/assessments", json={"title":"Final","weight_pct":40.0,"due_date":"2025-12-01","score_pct":None})  # remaining 40

def test_current_and_remaining(client):
    seed(client)
    r = client.get("/stats/current")
    assert r.status_code == 200
    stats = r.json()
    # 0.3*90 + 0.3*80 = 27 + 24 = 51 ; remaining = 40
    assert round(stats["current_weighted"], 2) == 51.00
    assert round(stats["remaining_weight"], 2) == 40.00

def test_validate_weights(client):
    seed(client)  # <-- important
    r = client.get("/stats/validate")
    assert r.status_code == 200
    v = r.json()
    assert round(v["total_weight"], 2) == 100.00

def test_what_if(client):
    seed(client)  # <-- important
    r = client.get("/stats/what-if", params={"target": 70})
    assert r.status_code == 200
    w = r.json()
    # With the seeded data: completed = 51, remaining = 40 → (70 - 51)*100/40 = 47.5
    assert round(w["required_avg"], 2) == 47.50
