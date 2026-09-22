from app.tools.cost_tools import estimate_cost


def test_estimate_cost_valid():
    activities = [{"name": "Indie Acoustic Session", "cost": 500.0}]
    food = {"name": "Green Leaf Cafe", "average_cost": 450.0}
    budget = 2000.0

    breakdown = estimate_cost(activities, food, budget, transport_per_trip=150.0)
    assert breakdown["activity_cost"] == 500.0
    assert breakdown["food_cost"] == 450.0
    assert breakdown["transport_cost"] == 300.0  # 2 stops * 150
    assert breakdown["total"] == 1250.0
    assert breakdown["remaining_budget"] == 750.0
    assert breakdown["is_within_budget"] is True


def test_estimate_cost_exceeds_budget():
    activities = [{"name": "Concert Arena", "cost": 1500.0}]
    food = {"name": "Luxury Dining", "average_cost": 1200.0}
    budget = 2000.0

    breakdown = estimate_cost(activities, food, budget, transport_per_trip=150.0)
    assert breakdown["total"] == 3000.0
    assert breakdown["remaining_budget"] == -1000.0
    assert breakdown["is_within_budget"] is False
