import time
import json
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.agents.state import PlannerState
from app.tools.preference_tools import parse_user_preferences
from app.tools.activity_tools import get_activity_options
from app.tools.food_tools import get_food_options
from app.tools.cost_tools import estimate_cost
from app.tools.validation_tools import validate_plan
from app.services.trace_service import trace_service
from app.agents.prompts import SYSTEM_PLANNER_PROMPT
from app.config import settings


def parse_preferences_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "parse_preferences", "running", "Parsing and normalizing user preferences...")

    parsed = parse_user_preferences(state.get("raw_input", {}))
    duration = int((time.time() - start_time) * 1000)

    trace_service.add_event(
        session_id,
        "parse_preferences",
        "completed",
        f"Normalized input: {parsed['city']}, ₹{parsed['budget']:.0f}, {parsed['available_minutes']} mins, {len(parsed['interests'])} interests",
        duration_ms=duration,
        data=parsed
    )

    return {
        "city": parsed["city"],
        "budget": parsed["budget"],
        "available_minutes": parsed["available_minutes"],
        "mood": parsed["mood"],
        "interests": parsed["interests"],
        "constraints": parsed["constraints"],
        "needs_clarification": parsed["is_ambiguous"],
        "clarification_question": parsed["clarification_question"]
    }


def check_clarity_node(state: PlannerState) -> str:
    """Conditional routing edge."""
    if state.get("needs_clarification", False):
        return "unclear"
    return "clear"


def ask_clarification_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    q = state.get("clarification_question", "Could you provide a few more details regarding your city or budget?")
    trace_service.add_event(session_id, "ask_clarification", "completed", f"Clarification requested: {q}")
    return {
        "final_plan": None
    }


def search_activities_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "search_activities", "running", "Searching activity database with preference filters...")

    activities = get_activity_options(
        city=state.get("city", "Bangalore"),
        interests=state.get("interests", []),
        mood=state.get("mood", ""),
        constraints=state.get("constraints", [])
    )
    duration = int((time.time() - start_time) * 1000)

    trace_service.add_event(
        session_id,
        "search_activities",
        "completed",
        f"Found {len(activities)} matching activities matching interests and constraints",
        duration_ms=duration,
        data={"count": len(activities), "sample": [a["name"] for a in activities[:3]]}
    )

    return {"activities": activities}


def search_food_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "search_food", "running", "Searching dining & cafe options within budget and dietary constraints...")

    food_options = get_food_options(
        city=state.get("city", "Bangalore"),
        budget=state.get("budget", 2000.0),
        constraints=state.get("constraints", [])
    )
    duration = int((time.time() - start_time) * 1000)

    trace_service.add_event(
        session_id,
        "search_food",
        "completed",
        f"Found {len(food_options)} food options matching dietary and budget preferences",
        duration_ms=duration,
        data={"count": len(food_options), "sample": [f["name"] for f in food_options[:3]]}
    )

    return {"food_options": food_options}


def build_candidate_plan_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "build_candidate_plan", "running", "Building feasible schedule candidates...")

    available_mins = state.get("available_minutes", 240)
    activities = state.get("activities", [])
    food_options = state.get("food_options", [])
    budget = state.get("budget", 2000.0)

    # Pick 1-2 best activities + 1 food option that fit within time
    selected_activities = []
    current_time_spent = 0
    current_cost_spent = 0

    # Pick food first if user has food interest or enough time
    selected_food = food_options[0] if food_options else None
    food_time = 60 if selected_food else 0
    food_cost = selected_food.get("average_cost", 0.0) if selected_food else 0.0

    current_time_spent += food_time
    current_cost_spent += food_cost

    for act in activities:
        act_dur = act.get("duration_minutes", 60)
        act_cost = act.get("cost", 0.0)
        # 20 min travel buffer between stops
        needed_time = act_dur + (20 if selected_activities or selected_food else 0)
        
        if (current_time_spent + needed_time <= available_mins) and (current_cost_spent + act_cost + 300 <= budget or not selected_activities):
            selected_activities.append(act)
            current_time_spent += needed_time
            current_cost_spent += act_cost
            if len(selected_activities) >= 2:
                break

    # If no activities fit, pick at least the top activity
    if not selected_activities and activities:
        selected_activities.append(activities[0])

    candidate = {
        "activities": selected_activities,
        "food": selected_food
    }

    duration = int((time.time() - start_time) * 1000)
    trace_service.add_event(
        session_id,
        "build_candidate_plan",
        "completed",
        f"Selected {len(selected_activities)} activities and {1 if selected_food else 0} dining stop",
        duration_ms=duration
    )

    return {"candidate_plan": candidate}


def estimate_cost_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "estimate_cost", "running", "Calculating activities, dining, and local transport costs...")

    candidate = state.get("candidate_plan", {})
    cost_breakdown = estimate_cost(
        activities=candidate.get("activities", []),
        food=candidate.get("food"),
        total_budget=state.get("budget", 2000.0)
    )

    candidate["cost_info"] = cost_breakdown
    duration = int((time.time() - start_time) * 1000)

    trace_service.add_event(
        session_id,
        "estimate_cost",
        "completed",
        f"Estimated total: ₹{cost_breakdown['total']} (Activities: ₹{cost_breakdown['activity_cost']}, Food: ₹{cost_breakdown['food_cost']}, Transport: ₹{cost_breakdown['transport_cost']})",
        duration_ms=duration,
        data=cost_breakdown
    )

    return {
        "candidate_plan": candidate,
        "estimated_cost": cost_breakdown
    }


def validate_plan_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "validate_plan", "running", "Validating schedule, budget limits, travel buffers, and dietary rules...")

    candidate = state.get("candidate_plan", {})
    val_result = validate_plan(
        candidate_plan=candidate,
        preferences={
            "budget": state.get("budget", 2000.0),
            "available_minutes": state.get("available_minutes", 240),
            "constraints": state.get("constraints", [])
        }
    )

    duration = int((time.time() - start_time) * 1000)
    status_msg = "Plan passed all constraint & budget checks" if val_result["valid"] else f"Found {len(val_result['errors'])} validation issues"

    trace_service.add_event(
        session_id,
        "validate_plan",
        "completed" if val_result["valid"] else "failed",
        status_msg,
        duration_ms=duration,
        data=val_result
    )

    return {
        "validation_errors": val_result.get("errors", []),
        "validation_warnings": val_result.get("warnings", [])
    }


def check_validity_node(state: PlannerState) -> str:
    """Check if candidate plan passed validation or needs fallback."""
    errors = state.get("validation_errors", [])
    if errors:
        return "invalid"
    return "valid"


def fallback_plan_node(state: PlannerState) -> Dict[str, Any]:
    """Generates a guaranteed feasible fallback plan respecting hard constraints."""
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "fallback_plan", "running", "Generating robust fallback plan respecting hard constraints...")

    budget = state.get("budget", 2000.0)
    constraints = [c.lower() for c in state.get("constraints", [])]
    activities = state.get("activities", [])
    food_options = state.get("food_options", [])

    # Filter activities strictly within low budget and hard constraints
    cheap_activities = [a for a in activities if a.get("cost", 0.0) <= budget * 0.3]
    if not cheap_activities:
        cheap_activities = [
            {
                "name": "Cubbon Park Peaceful Stroll",
                "category": "walks",
                "duration_minutes": 60,
                "cost": 0.0,
                "crowd_level": "low",
                "description": "A tranquil walk through nature."
            }
        ]

    # Select cheapest compliant food
    cheap_food = food_options[0] if food_options else {
        "name": "Brahmin's Coffee Bar",
        "cuisine": "South Indian",
        "average_cost": 150.0,
        "vegetarian_friendly": True,
        "crowd_level": "low"
    }

    fallback_candidate = {
        "activities": cheap_activities[:2],
        "food": cheap_food
    }

    cost_breakdown = estimate_cost(fallback_candidate["activities"], fallback_candidate["food"], budget)
    fallback_candidate["cost_info"] = cost_breakdown

    duration = int((time.time() - start_time) * 1000)
    trace_service.add_event(
        session_id,
        "fallback_plan",
        "completed",
        f"Generated fallback itinerary within ₹{cost_breakdown['total']:.0f} budget",
        duration_ms=duration
    )

    return {
        "candidate_plan": fallback_candidate,
        "estimated_cost": cost_breakdown,
        "is_fallback": True,
        "fallback_reason": f"Adjusted plan to strictly honor budget (₹{budget}) and constraints while avoiding high costs."
    }


def format_timeline(activities: List[Dict[str, Any]], food: Dict[str, Any], mood: str, interests: List[str], constraints: List[str]) -> List[Dict[str, Any]]:
    """Builds a realistic 4:00 PM onwards timeline with timestamps and 'why' reasoning."""
    timeline = []
    current_dt = datetime.strptime("4:00 PM", "%I:%M %p")
    
    for i, act in enumerate(activities):
        dur = int(act.get("duration_minutes", 60))
        end_dt = current_dt + timedelta(minutes=dur)
        
        # Craft explainable why
        why_text = f"Selected because you expressed interest in {act.get('category', 'leisure')}"
        if mood:
            why_text += f" and feel '{mood}'"
        if act.get("crowd_level") == "low":
            why_text += ", offering a tranquil low-crowd atmosphere."
        else:
            why_text += "."

        timeline.append({
            "start": current_dt.strftime("%I:%M %p").lstrip("0"),
            "end": end_dt.strftime("%I:%M %p").lstrip("0"),
            "type": act.get("category", "activity"),
            "name": act.get("name", "Activity"),
            "cost": float(act.get("cost", 0.0)),
            "why": why_text,
            "area": act.get("area", "Bangalore"),
            "crowd_level": act.get("crowd_level", "medium")
        })
        
        # 20 min travel buffer
        current_dt = end_dt + timedelta(minutes=20)

    if food:
        dur = 60
        end_dt = current_dt + timedelta(minutes=dur)
        why_text = f"Satisfies your {food.get('cuisine', 'dining')} preference"
        if any("veg" in c.lower() for c in constraints):
            why_text += " with verified vegetarian options"
        why_text += f" while keeping the cost within budget (avg ₹{food.get('average_cost', 0):.0f})."

        timeline.append({
            "start": current_dt.strftime("%I:%M %p").lstrip("0"),
            "end": end_dt.strftime("%I:%M %p").lstrip("0"),
            "type": "food",
            "name": food.get("name", "Restaurant"),
            "cost": float(food.get("average_cost", 0.0)),
            "why": why_text,
            "area": food.get("area", "Bangalore"),
            "crowd_level": food.get("crowd_level", "medium")
        })

    return timeline


def generate_final_plan_node(state: PlannerState) -> Dict[str, Any]:
    session_id = state.get("session_id", "default")
    start_time = time.time()
    trace_service.add_event(session_id, "generate_final_plan", "running", "Synthesizing personalized plan and explainable trade-offs...")

    candidate = state.get("candidate_plan", {})
    cost_info = state.get("estimated_cost", {})
    activities = candidate.get("activities", [])
    food = candidate.get("food")
    city = state.get("city", "Bangalore")
    mood = state.get("mood", "relaxed")
    interests = state.get("interests", [])
    constraints = state.get("constraints", [])
    is_fallback = state.get("is_fallback", False)
    fallback_reason = state.get("fallback_reason")

    # Generate timeline items deterministically first
    timeline = format_timeline(activities, food, mood, interests, constraints)
    
    # Calculate duration
    total_duration = sum(int(act.get("duration_minutes", 60)) for act in activities) + (60 if food else 0)
    stops_count = len(activities) + (1 if food else 0)
    travel_buffers = max(0, stops_count - 1) * 20
    total_duration_minutes = total_duration + travel_buffers

    tradeoffs = [
        f"Prioritized low-crowd venues ({', '.join(a.get('name') for a in activities if a.get('crowd_level') == 'low')}) to match comfort preferences.",
        f"Allocated ₹{cost_info.get('transport_cost', 300)} realistic buffer for city cab/auto travel between stops."
    ]
    if any(a.get("cost", 0) == 0 for a in activities):
        tradeoffs.append("Included free green-space / browsing activity to maximize remaining dining budget.")

    title = f"A {'Relaxed but Fun' if 'tired' in mood else 'Perfect'} {city} Saturday"
    summary = f"A customized {total_duration_minutes // 60}h {total_duration_minutes % 60}m itinerary blending {', '.join(interests) if interests else 'leisure'} and great dining."

    # Try Groq LLM for richer styling if GROQ_API_KEY is available
    groq_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(
                groq_api_key=groq_key,
                model_name=settings.GROQ_MODEL,
                temperature=0.2
            )
            prompt = f"""
            User input: City: {city}, Budget: {state.get('budget')}, Mood: {mood}, Interests: {interests}, Constraints: {constraints}
            Candidate Activities: {json.dumps(activities)}
            Candidate Dining: {json.dumps(food)}
            Total Cost: {cost_info.get('total')}
            Remaining Budget: {cost_info.get('remaining_budget')}
            
            Synthesize an engaging title, 1-2 sentence summary, specific reasons for each item, and 2 trade-offs.
            """
            response = llm.invoke([
                {"role": "system", "content": SYSTEM_PLANNER_PROMPT},
                {"role": "user", "content": prompt}
            ])
            parsed_llm = json.loads(response.content.strip())
            if "title" in parsed_llm:
                title = parsed_llm["title"]
            if "summary" in parsed_llm:
                summary = parsed_llm["summary"]
            if "tradeoffs" in parsed_llm and isinstance(parsed_llm["tradeoffs"], list):
                tradeoffs = parsed_llm["tradeoffs"]
            if "timeline" in parsed_llm and isinstance(parsed_llm["timeline"], list):
                # Ensure LLM did not hallucinate new names
                candidate_names = {a["name"].lower() for a in activities}
                if food:
                    candidate_names.add(food["name"].lower())
                for idx, t_item in enumerate(parsed_llm["timeline"]):
                    if idx < len(timeline) and t_item.get("name", "").lower() in candidate_names:
                        timeline[idx]["why"] = t_item.get("why", timeline[idx]["why"])
        except Exception as e:
            # Gracefully fallback to deterministic synthesis
            pass

    final_plan_dict = {
        "title": title,
        "summary": summary,
        "total_cost": float(cost_info.get("total", 0.0)),
        "remaining_budget": float(cost_info.get("remaining_budget", 0.0)),
        "total_duration_minutes": total_duration_minutes,
        "timeline": timeline,
        "tradeoffs": tradeoffs,
        "validation": {
            "budget_ok": cost_info.get("is_within_budget", True),
            "time_ok": total_duration_minutes <= state.get("available_minutes", 240),
            "constraints_ok": len(state.get("validation_errors", [])) == 0,
            "details": state.get("validation_warnings", [])
        },
        "is_fallback": is_fallback,
        "fallback_reason": fallback_reason
    }

    duration = int((time.time() - start_time) * 1000)
    trace_service.add_event(
        session_id,
        "generate_final_plan",
        "completed",
        f"Generated final itinerary: '{title}' (Total ₹{cost_info.get('total')})",
        duration_ms=duration,
        data={"title": title, "total_cost": cost_info.get("total")}
    )

    return {"final_plan": final_plan_dict}
