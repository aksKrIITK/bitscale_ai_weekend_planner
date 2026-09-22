import json
import asyncio
from fastapi import APIRouter, HTTPException, Query
from sse_starlette.sse import EventSourceResponse

from app.schemas.planner import PlanRequest, PlanResponse, ClarifyRequest
from app.services.planner_service import planner_service
from app.services.trace_service import trace_service

router = APIRouter(prefix="/planner", tags=["Planner"])


@router.post("/plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest, session_id: str = Query(None)):
    """
    Generate a personalized Saturday itinerary using the LangGraph agent.
    """
    try:
        response = await planner_service.create_plan(request, session_id=session_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning execution error: {str(e)}")


@router.get("/{session_id}/stream")
async def stream_trace(session_id: str):
    """
    SSE stream endpoint that delivers real-time trace events to the frontend.
    """
    async def event_generator():
        async for event in trace_service.subscribe(session_id):
            yield {
                "event": "trace",
                "data": json.dumps(event)
            }

    return EventSourceResponse(event_generator())


@router.post("/clarify", response_model=PlanResponse)
async def clarify_plan(request: ClarifyRequest):
    """
    Resume planning with additional user clarifications.
    """
    plan_request = PlanRequest(
        city="Bangalore",
        budget=2000.0,
        available_time="4 hours",
        mood=request.clarification,
        interests=["food", "walks"],
        constraints=["vegetarian"]
    )
    return await planner_service.create_plan(plan_request, session_id=request.session_id)
