# tests/test_stats_edges.py

def test_stats_on_empty_db(client):
    # current: no rows -> current=0, remaining = 100 (you can still add 100%)
    r = client.get("/stats/current")
    assert r.status_code == 200
    s = r.json()
    assert s["current_weighted"] == 0
    assert s["remaining_weight"] == 100

    # what-if on empty DB: required avg equals the target, attainable true
    r = client.get("/stats/what-if", params={"target": 70})
    assert r.status_code == 200
    wi = r.json()
    assert round(wi["required_avg"], 2) == 70.00
    assert wi["attainable"] is True

def test_stats_all_completed(client):
    # seed: everything graded already
    client.post("/assessments", json={"title":"A1","weight_pct":50.0,"due_date":"2025-01-01","score_pct":80.0})
    client.post("/assessments", json={"title":"A2","weight_pct":50.0,"due_date":"2025-02-01","score_pct":90.0})

    r = client.get("/stats/current")
    s = r.json()
    assert round(s["current_weighted"], 2) == 85.00  # 0.5*80 + 0.5*90

    # nothing remaining → required_avg is None; attainable depends on target
    r = client.get("/stats/what-if", params={"target": 90})
    wi = r.json()
    assert wi["required_avg"] is None
    assert wi["attainable"] is (85.00 >= 90.0)  # False

def test_unattainable_target_with_remaining(client):
    # seed: completed 10% at 50 → current=5; remaining=90
    client.post("/assessments", json={"title":"A1","weight_pct":10.0,"due_date":"2025-01-01","score_pct":50.0})
    client.post("/assessments", json={"title":"Big","weight_pct":90.0,"due_date":"2025-02-01","score_pct":None})

    # target 99 overall → required avg will be > 100 → unattainable
    r = client.get("/stats/what-if", params={"target": 99})
    wi = r.json()
    assert wi["required_avg"] > 100.0
    assert wi["attainable"] is False

def test_what_if_when_no_remaining_work(client):
    # All weights sum to 100 and all are scored -> remaining = 0
    client.post("/assessments", json={"title":"A1","weight_pct":50.0,"due_date":"2025-01-01","score_pct":80.0})
    client.post("/assessments", json={"title":"A2","weight_pct":50.0,"due_date":"2025-02-01","score_pct":90.0})

    r = client.get("/stats/current")
    s = r.json()
    assert s["remaining_weight"] == 0

    r = client.get("/stats/what-if", params={"target": 85})
    wi = r.json()
    # nothing left to earn -> required_avg is None; attainable depends on current >= target
    assert wi["required_avg"] is None
    assert wi["attainable"] is True  # current is exactly 85 in this seed
