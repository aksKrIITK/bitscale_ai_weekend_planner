from app.agents.nodes import fallback_plan_node
from app.agents.state import PlannerState


def test_fallback_plan_node():
    state: PlannerState = {
        "session_id": "test-fallback",
        "budget": 300.0,
        "available_minutes": 240,
        "mood": "relaxed",
        "interests": ["music"],
        "constraints": ["vegetarian", "avoid crowded places"],
        "activities": [
            {"name": "Expensive Concert", "cost": 800.0, "category": "music", "duration_minutes": 90, "crowd_level": "high"},
            {"name": "Cubbon Park Evening Walk", "cost": 0.0, "category": "walks", "duration_minutes": 60, "crowd_level": "low"}
        ],
        "food_options": [
            {"name": "Brahmin's Coffee Bar", "cuisine": "South Indian", "average_cost": 150.0, "vegetarian_friendly": True, "crowd_level": "low"}
        ]
    }

    res = fallback_plan_node(state)
    assert res["is_fallback"] is True
    assert "Adjusted plan" in res["fallback_reason"]
    assert res["candidate_plan"]["food"]["name"] == "Brahmin's Coffee Bar"
    assert res["candidate_plan"]["activities"][0]["cost"] <= 100.0
