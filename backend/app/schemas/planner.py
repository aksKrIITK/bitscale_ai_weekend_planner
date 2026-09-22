from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class PlanRequest(BaseModel):
    city: str = Field(..., description="City name (e.g. Bangalore)")
    budget: float = Field(..., description="Total budget in INR (e.g. 2000)")
    available_time: str = Field(..., description="Available duration (e.g. '4 hours', '2 hours', 'custom')")
    mood: Optional[str] = Field(default="", description="Current mood or vibe")
    interests: List[str] = Field(default_factory=list, description="List of user interests")
    constraints: List[str] = Field(default_factory=list, description="List of constraints or preferences")


class ClarifyRequest(BaseModel):
    session_id: str
    clarification: str


class TimelineItem(BaseModel):
    start: str
    end: str
    type: str  # activity, food, music, walk, etc.
    name: str
    cost: float
    why: str
    area: Optional[str] = None
    crowd_level: Optional[str] = None


class ValidationStatus(BaseModel):
    budget_ok: bool = True
    time_ok: bool = True
    constraints_ok: bool = True
    details: Optional[List[str]] = None


class FinalPlan(BaseModel):
    title: str
    summary: str
    total_cost: float
    remaining_budget: float
    total_duration_minutes: int
    timeline: List[TimelineItem]
    tradeoffs: List[str] = Field(default_factory=list)
    validation: ValidationStatus = Field(default_factory=ValidationStatus)
    is_fallback: bool = False
    fallback_reason: Optional[str] = None


class TraceEvent(BaseModel):
    node: str
    status: str  # running, completed, failed, skipped
    message: str
    duration_ms: int = 0
    data: Optional[Dict[str, Any]] = None


class PlanResponse(BaseModel):
    session_id: str
    plan: Optional[FinalPlan] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    trace: List[TraceEvent] = Field(default_factory=list)
    is_mock_data: bool = True
