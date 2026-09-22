from app.tools.validation_tools import validate_plan


def test_validate_plan_valid():
    candidate_plan = {
        "activities": [
            {"name": "Cubbon Park Walk", "duration_minutes": 75, "cost": 0.0, "crowd_level": "medium", "is_indoor": False, "is_outdoor": True},
            {"name": "Indie Acoustic Session", "duration_minutes": 90, "cost": 500.0, "crowd_level": "low", "is_indoor": True, "is_outdoor": False}
        ],
        "food": {
            "name": "Green Leaf Cafe",
            "average_cost": 450.0,
            "vegetarian_friendly": True,
            "crowd_level": "low",
            "serves_alcohol": False
        },
        "cost_info": {
            "total": 1250.0
        }
    }
    preferences = {
        "budget": 2000.0,
        "available_minutes": 270,  # 75 + 90 + 60 + 40 (buffers) = 265
        "constraints": ["vegetarian", "avoid crowded places"]
    }
    res = validate_plan(candidate_plan, preferences)
    assert res["valid"] is True
    assert len(res["errors"]) == 0


def test_validate_plan_budget_violation():
    candidate_plan = {
        "activities": [],
        "food": None,
        "cost_info": {"total": 2300.0}
    }
    preferences = {
        "budget": 2000.0,
        "available_minutes": 240,
        "constraints": []
    }
    res = validate_plan(candidate_plan, preferences)
    assert res["valid"] is False
    assert any("exceeds the user's budget" in err for err in res["errors"])


def test_validate_plan_vegetarian_violation():
    candidate_plan = {
        "activities": [],
        "food": {
            "name": "Steakhouse Non-Veg",
            "average_cost": 500.0,
            "vegetarian_friendly": False,
            "crowd_level": "low"
        },
        "cost_info": {"total": 800.0}
    }
    preferences = {
        "budget": 2000.0,
        "available_minutes": 240,
        "constraints": ["vegetarian"]
    }
    res = validate_plan(candidate_plan, preferences)
    assert res["valid"] is False
    assert any("does not have verified vegetarian options" in err for err in res["errors"])


def test_validate_plan_time_violation():
    candidate_plan = {
        "activities": [
            {"name": "Long Movie", "duration_minutes": 180, "cost": 300, "crowd_level": "low"},
            {"name": "Pottery Workshop", "duration_minutes": 120, "cost": 500, "crowd_level": "low"}
        ],
        "food": {"name": "Cafe", "average_cost": 300, "vegetarian_friendly": True, "crowd_level": "low"},
        "cost_info": {"total": 1400.0}
    }
    # Total = 180 + 120 + 60 + 40 = 400 mins (vs 240 mins available)
    preferences = {
        "budget": 2000.0,
        "available_minutes": 240,
        "constraints": []
    }
    res = validate_plan(candidate_plan, preferences)
    assert res["valid"] is False
    assert any("exceeds available time" in err for err in res["errors"])
