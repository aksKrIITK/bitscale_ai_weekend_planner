import datetime
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from app.db.database import Base


class TraceLog(Base):
    __tablename__ = "trace_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    node = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # running, completed, failed, skipped
    message = Column(Text, nullable=True)
    duration_ms = Column(Integer, default=0)
    data = Column(JSON, default=dict)
