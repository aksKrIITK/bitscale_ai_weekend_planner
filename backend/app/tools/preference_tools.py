import re
from typing import Dict, Any, List, Tuple


def parse_time_to_minutes(time_str: Any) -> int:
    """Convert time strings like '4 hours', '2h', '90 mins', 'custom' to integer minutes."""
    if isinstance(time_str, (int, float)):
        return int(time_str)
    
    if not time_str or not isinstance(time_str, str):
        return 240  # Default 4 hours
    
    time_str = time_str.strip().lower()
    
    # Check for "X hour(s)" or "X hr(s)"
    hour_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hour|hr|h)', time_str)
    if hour_match:
        return int(float(hour_match.group(1)) * 60)
    
    # Check for "X min(s)" or "X minute(s)"
    min_match = re.search(r'(\d+)\s*(?:minute|min|m)', time_str)
    if min_match:
        return int(min_match.group(1))
    
    # Plain number check
    num_match = re.search(r'(\d+)', time_str)
    if num_match:
        val = int(num_match.group(1))
        # If <= 12, assume hours, otherwise minutes
        return val * 60 if val <= 12 else val
    
    return 240


def parse_budget(budget_input: Any) -> float:
    """Normalize budget string/number to float."""
    if isinstance(budget_input, (int, float)):
        return float(budget_input)
    
    if not budget_input or not isinstance(budget_input, str):
        return 2000.0
    
    # Strip currency symbols and commas like ₹, $, Rs, ,
    cleaned = re.sub(r'[^\d.]', '', budget_input)
    try:
        return float(cleaned) if cleaned else 2000.0
    except ValueError:
        return 2000.0


def parse_user_preferences(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    TOOL 1: parse_user_preferences
    Normalizes city, budget, available time, mood, interests, constraints.
    Detects ambiguity / missing info.
    """
    raw_city = str(input_data.get("city", "")).strip()
    city = raw_city.title() if raw_city else "Bangalore"
    
    budget = parse_budget(input_data.get("budget", 2000))
    available_minutes = parse_time_to_minutes(input_data.get("available_time", "4 hours"))
    
    raw_mood = str(input_data.get("mood", "")).strip()
    mood = raw_mood.lower() if raw_mood else "relaxed"
    
    raw_interests = input_data.get("interests", [])
    if isinstance(raw_interests, str):
        interests = [i.strip().lower() for i in raw_interests.split(",") if i.strip()]
    elif isinstance(raw_interests, list):
        interests = [str(i).strip().lower() for i in raw_interests if str(i).strip()]
    else:
        interests = []
        
    raw_constraints = input_data.get("constraints", [])
    if isinstance(raw_constraints, str):
        constraints = [c.strip().lower() for c in raw_constraints.split(",") if c.strip()]
    elif isinstance(raw_constraints, list):
        constraints = [str(c).strip().lower() for c in raw_constraints if str(c).strip()]
    else:
        constraints = []
        
    # Clarity check
    is_ambiguous = False
    clarification_question = ""
    
    if not raw_city and (budget <= 0 or not raw_interests):
        is_ambiguous = True
        clarification_question = "Where are you spending Saturday, and roughly what is your budget or interest?"
    elif budget <= 0:
        is_ambiguous = True
        clarification_question = "Please let us know your approximate budget for the Saturday plan."
    elif available_minutes <= 30:
        is_ambiguous = True
        clarification_question = "How much time do you have available for your Saturday outing (e.g. 2 hours, 4 hours)?"

    return {
        "city": city,
        "budget": budget,
        "available_minutes": available_minutes,
        "mood": mood,
        "interests": interests,
        "constraints": constraints,
        "is_ambiguous": is_ambiguous,
        "clarification_question": clarification_question
    }
