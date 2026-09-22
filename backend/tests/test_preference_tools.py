from app.tools.preference_tools import parse_time_to_minutes, parse_budget, parse_user_preferences


def test_parse_time_to_minutes():
    assert parse_time_to_minutes("4 hours") == 240
    assert parse_time_to_minutes("2 hours") == 120
    assert parse_time_to_minutes("6 hrs") == 360
    assert parse_time_to_minutes("90 mins") == 90
    assert parse_time_to_minutes("1.5 hours") == 90
    assert parse_time_to_minutes(180) == 180


def test_parse_budget():
    assert parse_budget("2000") == 2000.0
    assert parse_budget("₹2000") == 2000.0
    assert parse_budget("₹ 3,500") == 3500.0
    assert parse_budget(1500) == 1500.0


def test_parse_user_preferences_full():
    raw = {
        "city": "bangalore",
        "budget": "₹2000",
        "available_time": "4 hours",
        "mood": "tired but wants to do something fun",
        "interests": ["food", "music", "walks"],
        "constraints": ["vegetarian", "avoid crowded places"]
    }
    res = parse_user_preferences(raw)
    assert res["city"] == "Bangalore"
    assert res["budget"] == 2000.0
    assert res["available_minutes"] == 240
    assert "music" in res["interests"]
    assert "vegetarian" in res["constraints"]
    assert res["is_ambiguous"] is False
