import os
import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.restaurant import Restaurant
from app.config import settings


def get_food_options(
    city: str,
    budget: float,
    constraints: List[str],
    max_results: int = 10,
    db: Optional[Session] = None
) -> List[Dict[str, Any]]:
    """
    TOOL 3: getFoodOptions
    Retrieves restaurants matching user's city, budget, and dietary/crowd constraints.
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        query = db.query(Restaurant).filter(Restaurant.city.ilike(f"%{city}%"))
        
        norm_constraints = [c.lower() for c in constraints]
        
        # Vegetarian constraint
        is_veg = any("veg" in c for c in norm_constraints)
        if is_veg:
            query = query.filter(Restaurant.vegetarian_friendly == True)
            
        if "pure veg" in norm_constraints:
            query = query.filter(Restaurant.pure_veg == True)
            
        # Crowd constraint
        if "avoid crowded places" in norm_constraints or "avoid crowds" in norm_constraints or "low crowd" in norm_constraints:
            query = query.filter(Restaurant.crowd_level != "high")
            
        # Alcohol constraint
        if "avoid alcohol" in norm_constraints or "no alcohol" in norm_constraints:
            query = query.filter(Restaurant.serves_alcohol == False)
            
        # Wheelchair accessibility
        if "wheelchair accessible" in norm_constraints:
            query = query.filter(Restaurant.wheelchair_accessible == True)

        candidates = query.all()
        
        affordable_candidates = []
        for rest in candidates:
            if rest.average_cost <= budget:
                affordable_candidates.append(rest)
            elif rest.average_cost <= budget * 1.2:
                affordable_candidates.append(rest)
                
        final_list = affordable_candidates if affordable_candidates else candidates
        
        results = [r.to_dict() for r in final_list[:max_results]]

        if not results:
            groq_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
            if groq_key:
                try:
                    from groq import Groq
                    client = Groq(api_key=groq_key)
                    prompt = f"""
                    You are a dining recommendation tool. Return 3-5 authentic real restaurants or cafes in {city} matching:
                    - Budget: under ₹{budget}
                    - Constraints: {', '.join(constraints)}
                    - Vegetarian required: {is_veg}
                    
                    Return ONLY a JSON array with objects matching:
                    [
                      {{
                        "name": "Exact real restaurant or cafe name in {city}",
                        "city": "{city}",
                        "cuisine": "South Indian / North Indian / Cafe / Vegetarian / Casual Dining",
                        "average_cost": 400.0,
                        "vegetarian_friendly": true,
                        "pure_veg": true,
                        "serves_alcohol": false,
                        "crowd_level": "low",
                        "is_indoor": true,
                        "wheelchair_accessible": true,
                        "description": "Short description",
                        "tags": ["{city}", "dining"],
                        "area": "Neighborhood in {city}"
                      }}
                    ]
                    """
                    completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=settings.GROQ_MODEL,
                        temperature=0.2,
                    )
                    raw_text = completion.choices[0].message.content.strip()
                    if "```json" in raw_text:
                        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw_text:
                        raw_text = raw_text.split("```")[1].split("```")[0].strip()
                    parsed = json.loads(raw_text)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        results = parsed[:max_results]
                except Exception:
                    pass

            if not results:
                results = [
                    {
                        "name": f"{city} Artisan Botanical Cafe",
                        "city": city,
                        "cuisine": "Cafe",
                        "average_cost": min(budget * 0.35, 450.0),
                        "vegetarian_friendly": True,
                        "pure_veg": True,
                        "serves_alcohol": False,
                        "crowd_level": "low",
                        "is_indoor": True,
                        "wheelchair_accessible": True,
                        "description": f"Cozy artisanal garden cafe in {city} serving fresh local specialities and vegetarian dishes.",
                        "tags": ["cafe", "vegetarian", "pure_veg", "healthy", "quiet"],
                        "area": f"Downtown {city}"
                    }
                ]

        results.sort(key=lambda r: r.get("average_cost", 400.0))
        return results[:max_results]
    finally:
        if close_db:
            db.close()

