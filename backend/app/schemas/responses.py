from pydantic import BaseModel
from typing import Optional, Any


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    database: str = "connected"
    groq_configured: bool = False


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[Any] = None
