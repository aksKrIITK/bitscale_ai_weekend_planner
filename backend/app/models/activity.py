from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON
from app.db.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True, default="Bangalore")
    category = Column(String(100), nullable=False, index=True)  # walk, music, art, park, movie, books, coffee, sports, photo
    duration_minutes = Column(Integer, nullable=False, default=60)
    cost = Column(Float, nullable=False, default=0.0)
    crowd_level = Column(String(50), nullable=False, default="medium")  # low, medium, high
    is_indoor = Column(Boolean, default=False)
    is_outdoor = Column(Boolean, default=True)
    wheelchair_accessible = Column(Boolean, default=True)
    family_friendly = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # ["nature", "quiet", "relaxing", "evening"]
    area = Column(String(100), nullable=True)  # e.g., "Koramangala", "Indiranagar", "MG Road"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "category": self.category,
            "duration_minutes": self.duration_minutes,
            "cost": self.cost,
            "crowd_level": self.crowd_level,
            "is_indoor": self.is_indoor,
            "is_outdoor": self.is_outdoor,
            "wheelchair_accessible": self.wheelchair_accessible,
            "family_friendly": self.family_friendly,
            "description": self.description,
            "tags": self.tags or [],
            "area": self.area
        }
