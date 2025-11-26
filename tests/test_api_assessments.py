# tests/test_api_assessments.py
from datetime import date

def make_assessment(client, title, weight, due, score=None):
    payload = {"title": title, "weight_pct": weight, "due_date": due}
    if score is not None:
        payload["score_pct"] = score
    r = client.post("/assessments", json=payload)
    assert r.status_code == 200, r.text
    return r.json()

def test_crud_flow(client):
    # Create
    created = make_assessment(client, "Midterm", 20.0, "2025-11-01")

    # Read one
    r = client.get(f"/assessments/{created['id']}")
    assert r.status_code == 200
    got = r.json()
    assert got["title"] == "Midterm"

    # Update
    update = dict(created, title="Midterm (updated)", score_pct=85.0)
    r = client.put(f"/assessments/{created['id']}", json=update)
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"].endswith("(updated)")
    assert updated["score_pct"] == 85.0

    # List
    r = client.get("/assessments")
    assert r.status_code == 200
    rows = r.json()
    assert any(row["title"].endswith("(updated)") for row in rows)

    # Delete
    r = client.delete(f"/assessments/{created['id']}")
    assert r.status_code in (200, 204)

    # Verify gone
    r = client.get("/assessments")
    assert all(row["id"] != created["id"] for row in r.json())
