from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"


def test_plan_api_demo_scenario():
    payload = {
        "city": "Bangalore",
        "budget": 2000,
        "available_time": "4 hours",
        "mood": "tired but wants to do something fun",
        "interests": ["food", "music", "walks"],
        "constraints": ["vegetarian", "avoid crowded places"]
    }
    response = client.post("/api/planner/plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["plan"] is not None
    plan = data["plan"]
    assert plan["total_cost"] <= 2000
    assert len(plan["timeline"]) >= 2
    assert len(data["trace"]) >= 4
    assert plan["validation"]["budget_ok"] is True
    assert plan["validation"]["constraints_ok"] is True
