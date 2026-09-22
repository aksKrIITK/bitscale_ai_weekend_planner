from typing import TypedDict, List, Dict, Any, Optional


class PlannerState(TypedDict, total=False):
    session_id: str
    raw_input: Dict[str, Any]

    city: str
    budget: float
    available_minutes: int
    mood: str
    interests: List[str]
    constraints: List[str]

    activities: List[Dict[str, Any]]
    food_options: List[Dict[str, Any]]

    candidate_plan: Dict[str, Any]
    estimated_cost: Dict[str, Any]

    validation_errors: List[str]
    validation_warnings: List[str]

    needs_clarification: bool
    clarification_question: str

    is_fallback: bool
    fallback_reason: Optional[str]

    final_plan: Dict[str, Any]
    trace: List[Dict[str, Any]]
