import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.schemas.responses import HealthResponse
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def get_health(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    groq_configured = bool(settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY"))

    return HealthResponse(
        status="ok",
        version=settings.PROJECT_VERSION,
        database=db_status,
        groq_configured=groq_configured
    )
