from typing import List, Dict, Any, Tuple


def validate_plan(
    candidate_plan: Dict[str, Any],
    preferences: Dict[str, Any]
) -> Dict[str, Any]:
    """
    TOOL 5: validatePlan
    Deterministically validates budget, time limits, travel buffers, and constraint adherence.
    """
    errors: List[str] = []
    warnings: List[str] = []
    
    budget = float(preferences.get("budget", 2000.0))
    available_minutes = int(preferences.get("available_minutes", 240))
    constraints = [c.lower() for c in preferences.get("constraints", [])]
    
    activities = candidate_plan.get("activities", [])
    food = candidate_plan.get("food")
    cost_info = candidate_plan.get("cost_info", {})
    
    # 1. Budget Validation
    total_cost = float(cost_info.get("total", 0.0))
    if total_cost > budget:
        errors.append(f"Total estimated cost (₹{total_cost:.0f}) exceeds the user's budget of ₹{budget:.0f}.")
    elif total_cost > budget * 0.95:
        warnings.append(f"Plan utilizes almost the full budget (₹{total_cost:.0f} / ₹{budget:.0f}).")

    # 2. Time & Realism Validation
    # Calculate duration of activities + food (default 60 mins) + travel buffer (20 mins per transition)
    total_duration = 0
    for act in activities:
        total_duration += int(act.get("duration_minutes", 60))
        
    if food:
        total_duration += 60  # 1 hour for meal/cafe
        
    # Add travel buffers: 20 mins between stops
    stops_count = len(activities) + (1 if food else 0)
    travel_buffers = max(0, stops_count - 1) * 20
    total_time_with_travel = total_duration + travel_buffers
    
    if total_time_with_travel > available_minutes:
        errors.append(
            f"Total schedule ({total_time_with_travel} mins including travel) exceeds available time of {available_minutes} mins."
        )
    elif total_time_with_travel > available_minutes - 15:
        warnings.append(f"Schedule is tightly packed ({total_time_with_travel} mins of {available_minutes} mins).")

    # 3. Constraint Validation
    # Vegetarian check
    is_veg_req = any("veg" in c for c in constraints)
    if is_veg_req and food:
        if not food.get("vegetarian_friendly", True):
            errors.append(f"Selected restaurant '{food.get('name')}' does not have verified vegetarian options.")

    # Avoid crowded places
    avoid_crowd = any("crowd" in c for c in constraints)
    if avoid_crowd:
        for act in activities:
            if act.get("crowd_level") == "high":
                errors.append(f"Activity '{act.get('name')}' has a high crowd level, violating the low-crowd constraint.")
        if food and food.get("crowd_level") == "high":
            errors.append(f"Restaurant '{food.get('name')}' has a high crowd level, violating the low-crowd constraint.")

    # Indoor / Outdoor constraints
    if "indoor only" in constraints:
        for act in activities:
            if not act.get("is_indoor", False):
                errors.append(f"Activity '{act.get('name')}' is outdoor, violating the indoor-only constraint.")
                
    if "outdoor only" in constraints:
        for act in activities:
            if not act.get("is_outdoor", False):
                errors.append(f"Activity '{act.get('name')}' is indoor, violating the outdoor-only constraint.")

    # Avoid alcohol
    if "avoid alcohol" in constraints or "no alcohol" in constraints:
        if food and food.get("serves_alcohol", False):
            errors.append(f"Venue '{food.get('name')}' serves alcohol, violating the alcohol constraint.")

    # Realism: maximum activities check
    if len(activities) > 4:
        warnings.append("More than 4 activities might feel rushed for a single Saturday outing.")

    is_valid = len(errors) == 0
    return {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "calculated_duration": total_time_with_travel
    }
