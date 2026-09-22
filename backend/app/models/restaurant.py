from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON
from app.db.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    city = Column(String(100), nullable=False, index=True, default="Bangalore")
    cuisine = Column(String(100), nullable=False, index=True)  # South Indian, North Indian, Cafe, Vegetarian, Healthy, Casual Dining
    average_cost = Column(Float, nullable=False, default=400.0)  # average cost for 1-2 people
    vegetarian_friendly = Column(Boolean, default=True)
    pure_veg = Column(Boolean, default=False)
    serves_alcohol = Column(Boolean, default=False)
    crowd_level = Column(String(50), nullable=False, default="medium")  # low, medium, high
    is_indoor = Column(Boolean, default=True)
    wheelchair_accessible = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # ["quiet", "coffee", "cozy", "tiffin"]
    area = Column(String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "cuisine": self.cuisine,
            "average_cost": self.average_cost,
            "vegetarian_friendly": self.vegetarian_friendly,
            "pure_veg": self.pure_veg,
            "serves_alcohol": self.serves_alcohol,
            "crowd_level": self.crowd_level,
            "is_indoor": self.is_indoor,
            "wheelchair_accessible": self.wheelchair_accessible,
            "description": self.description,
            "tags": self.tags or [],
            "area": self.area
        }
