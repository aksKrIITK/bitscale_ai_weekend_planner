import uuid
import asyncio
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.agents.graph import planner_graph
from app.agents.state import PlannerState
from app.services.trace_service import trace_service
from app.schemas.planner import PlanRequest, PlanResponse, FinalPlan, TraceEvent
from app.models.plan import SavedPlan
from app.models.trace import TraceLog
from app.db.database import SessionLocal


class PlannerService:
    """
    Coordinates execution of the planner LangGraph workflow, persists plans and trace logs.
    """

    async def create_plan(self, request: PlanRequest, session_id: Optional[str] = None) -> PlanResponse:
        if not session_id:
            session_id = str(uuid.uuid4())

        trace_service.init_session(session_id)

        initial_state: PlannerState = {
            "session_id": session_id,
            "raw_input": request.model_dump(),
            "city": request.city,
            "budget": request.budget,
            "available_minutes": 240,
            "mood": request.mood or "",
            "interests": request.interests,
            "constraints": request.constraints,
            "activities": [],
            "food_options": [],
            "candidate_plan": {},
            "estimated_cost": {},
            "validation_errors": [],
            "validation_warnings": [],
            "needs_clarification": False,
            "clarification_question": "",
            "is_fallback": False,
            "fallback_reason": None,
            "final_plan": {},
            "trace": []
        }

        # Execute LangGraph asynchronously in thread pool to avoid blocking async loop
        result_state = await asyncio.to_thread(planner_graph.invoke, initial_state)

        # Collect traces
        trace_events = trace_service.get_traces(session_id)
        
        final_plan_data = result_state.get("final_plan")
        final_plan_obj = FinalPlan(**final_plan_data) if final_plan_data else None

        # Persist to database if SessionLocal is available
        try:
            db = SessionLocal()
            try:
                if final_plan_obj:
                    saved_plan = SavedPlan(
                        session_id=session_id,
                        city=result_state.get("city", request.city),
                        budget=result_state.get("budget", request.budget),
                        available_time=request.available_time,
                        mood=request.mood,
                        interests=request.interests,
                        constraints=request.constraints,
                        final_plan=final_plan_data,
                        trace=trace_events
                    )
                    db.add(saved_plan)
                    db.commit()
            finally:
                db.close()
        except Exception:
            pass

        return PlanResponse(
            session_id=session_id,
            plan=final_plan_obj,
            needs_clarification=result_state.get("needs_clarification", False),
            clarification_question=result_state.get("clarification_question"),
            trace=[TraceEvent(**evt) for evt in trace_events],
            is_mock_data=True
        )


planner_service = PlannerService()
