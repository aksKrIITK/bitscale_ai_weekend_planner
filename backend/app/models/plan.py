import datetime
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from app.db.database import Base


class SavedPlan(Base):
    __tablename__ = "saved_plans"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    city = Column(String(100), nullable=False)
    budget = Column(Float, nullable=False)
    available_time = Column(String(100), nullable=False)
    mood = Column(String(255), nullable=True)
    interests = Column(JSON, default=list)
    constraints = Column(JSON, default=list)
    final_plan = Column(JSON, nullable=False)
    trace = Column(JSON, default=list)
