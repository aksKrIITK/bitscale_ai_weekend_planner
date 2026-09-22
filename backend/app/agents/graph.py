from langgraph.graph import StateGraph, END
from app.agents.state import PlannerState
from app.agents.nodes import (
    parse_preferences_node,
    check_clarity_node,
    ask_clarification_node,
    search_activities_node,
    search_food_node,
    build_candidate_plan_node,
    estimate_cost_node,
    validate_plan_node,
    check_validity_node,
    fallback_plan_node,
    generate_final_plan_node,
)


def create_planner_graph():
    """
    Constructs the LangGraph state graph for the Perfect Saturday Planner.
    """
    workflow = StateGraph(PlannerState)

    # 1. Add Nodes
    workflow.add_node("parse_preferences", parse_preferences_node)
    workflow.add_node("ask_clarification", ask_clarification_node)
    workflow.add_node("search_activities", search_activities_node)
    workflow.add_node("search_food", search_food_node)
    workflow.add_node("build_candidate_plan", build_candidate_plan_node)
    workflow.add_node("estimate_cost", estimate_cost_node)
    workflow.add_node("validate_plan", validate_plan_node)
    workflow.add_node("fallback_plan", fallback_plan_node)
    workflow.add_node("generate_final_plan", generate_final_plan_node)

    # 2. Define Edges & Flow
    workflow.set_entry_point("parse_preferences")

    # Routing from parse_preferences
    workflow.add_conditional_edges(
        "parse_preferences",
        check_clarity_node,
        {
            "unclear": "ask_clarification",
            "clear": "search_activities",
        },
    )

    workflow.add_edge("ask_clarification", END)

    # Search & Candidate Building pipeline
    workflow.add_edge("search_activities", "search_food")
    workflow.add_edge("search_food", "build_candidate_plan")
    workflow.add_edge("build_candidate_plan", "estimate_cost")
    workflow.add_edge("estimate_cost", "validate_plan")

    # Routing after validation
    workflow.add_conditional_edges(
        "validate_plan",
        check_validity_node,
        {
            "valid": "generate_final_plan",
            "invalid": "fallback_plan",
        },
    )

    workflow.add_edge("fallback_plan", "generate_final_plan")
    workflow.add_edge("generate_final_plan", END)

    return workflow.compile()


planner_graph = create_planner_graph()
