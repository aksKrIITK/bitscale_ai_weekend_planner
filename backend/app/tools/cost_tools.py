from typing import List, Dict, Any,Optional


def estimate_cost(
    activities: List[Dict[str, Any]],
    food: Optional[Dict[str, Any]],
    total_budget: float,
    transport_per_trip: float = 150.0
) -> Dict[str, Any]:
    """
    TOOL 4: estimateCost
    Calculates deterministic breakdown of activity, food, and transport costs.
    """
    activity_cost = sum(float(act.get("cost", 0.0)) for act in activities)
    food_cost = float(food.get("average_cost", 0.0)) if food else 0.0
    
    # Estimate transport trips:
    # 1 trip from home to 1st venue + trips between stops + 1 trip return
    stops_count = len(activities) + (1 if food else 0)
    num_trips = max(1, stops_count)
    transport_cost = num_trips * transport_per_trip
    
    total = activity_cost + food_cost + transport_cost
    remaining = total_budget - total
    
    return {
        "activity_cost": round(activity_cost, 2),
        "food_cost": round(food_cost, 2),
        "transport_cost": round(transport_cost, 2),
        "total": round(total, 2),
        "remaining_budget": round(remaining, 2),
        "is_within_budget": remaining >= 0
    }
