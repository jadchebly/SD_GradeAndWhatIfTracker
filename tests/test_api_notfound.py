# tests/test_api_notfound.py

def test_get_missing_returns_404(client):
    r = client.get("/assessments/999999")
    assert r.status_code == 404

def test_put_missing_returns_404(client):
    r = client.put("/assessments/999999", json={
        "id": 999999,
        "title": "Nope",
        "weight_pct": 10.0,
        "due_date": "2025-01-01",
        "score_pct": None
    })
    assert r.status_code == 404

def test_delete_missing_returns_404(client):
    r = client.delete("/assessments/999999")
    assert r.status_code == 404
