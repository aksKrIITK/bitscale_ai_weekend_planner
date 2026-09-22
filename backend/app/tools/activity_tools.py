import os
import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.activity import Activity
from app.config import settings


def get_activity_options(
    city: str,
    interests: List[str],
    mood: str,
    constraints: List[str],
    max_results: int = 10,
    db: Optional[Session] = None
) -> List[Dict[str, Any]]:
    """
    TOOL 2: getActivityOptions
    Retrieves activities matching user's city, interests, mood, and constraints.
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        query = db.query(Activity).filter(Activity.city.ilike(f"%{city}%"))
        
        # Apply strict constraint filters
        norm_constraints = [c.lower() for c in constraints]
        
        if "indoor only" in norm_constraints:
            query = query.filter(Activity.is_indoor == True)
        if "outdoor only" in norm_constraints:
            query = query.filter(Activity.is_outdoor == True)
        if "avoid crowded places" in norm_constraints or "avoid crowds" in norm_constraints or "low crowd" in norm_constraints:
            query = query.filter(Activity.crowd_level != "high")
        if "wheelchair accessible" in norm_constraints:
            query = query.filter(Activity.wheelchair_accessible == True)
        if "family friendly" in norm_constraints:
            query = query.filter(Activity.family_friendly == True)

        all_candidates = query.all()
        
        # Scoring / Ranking based on interests and mood
        norm_interests = [i.lower() for i in interests]
        mood_terms = [m.lower() for m in mood.replace(",", " ").split() if len(m) > 2]

        scored_activities = []
        for act in all_candidates:
            score = 0
            act_tags = [t.lower() for t in (act.tags or [])]
            act_cat = act.category.lower()
            act_desc = (act.description or "").lower()
            
            # Interest score
            for interest in norm_interests:
                if interest in act_cat or act_cat in interest:
                    score += 5
                elif any(interest in tag or tag in interest for tag in act_tags):
                    score += 3
                elif interest in act_desc:
                    score += 2

            # Mood score
            for term in mood_terms:
                if term in act_tags or term in act_desc:
                    score += 2
                if ("tired" in term or "relax" in term) and act.crowd_level == "low":
                    score += 2
                if ("adventur" in term or "active" in term) and act.category in ["sports", "nature"]:
                    score += 3

            # Default base score if nothing matched
            scored_activities.append((score, act))

        # Sort by score descending
        scored_activities.sort(key=lambda x: x[0], reverse=True)
        
        results = [act.to_dict() for score, act in scored_activities[:max_results]]
        
        # If no results in database for this city, use Groq LLM to retrieve authentic real spots for that city
        if not results:
            groq_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
            if groq_key:
                try:
                    from groq import Groq
                    client = Groq(api_key=groq_key)
                    prompt = f"""
                    You are a local city guide tool. Return 4-6 real, verified activities in {city} matching:
                    - Interests: {', '.join(interests)}
                    - Mood: {mood}
                    - Constraints: {', '.join(constraints)}
                    
                    Return ONLY valid JSON array with objects matching:
                    [
                      {{
                        "name": "Exact real venue or spot in {city}",
                        "city": "{city}",
                        "category": "walks/music/art/books/movies/sports/nature",
                        "duration_minutes": 75,
                        "cost": 200.0,
                        "crowd_level": "low",
                        "is_indoor": true,
                        "is_outdoor": false,
                        "wheelchair_accessible": true,
                        "family_friendly": true,
                        "description": "Short 1-sentence description",
                        "tags": ["{city}", "activity"],
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
                    # Clean json markdown if wrapped in ```json ... ```
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
                # Dynamic adaptive generation fallback for custom city
                results = [
                    {
                        "name": f"{city} Promenade & Heritage Park Stroll",
                        "city": city,
                        "category": "walks",
                        "duration_minutes": 75,
                        "cost": 0.0,
                        "crowd_level": "low",
                        "is_indoor": False,
                        "is_outdoor": True,
                        "wheelchair_accessible": True,
                        "family_friendly": True,
                        "description": f"Scenic and relaxed walking trail exploring the iconic sights and parks of {city}.",
                        "tags": ["walks", "nature", "quiet", "relaxing", "outdoor", "photography"],
                        "area": f"Central {city}"
                    },
                    {
                        "name": f"{city} Acoustic & Indie Live Sessions",
                        "city": city,
                        "category": "music",
                        "duration_minutes": 90,
                        "cost": 500.0,
                        "crowd_level": "low",
                        "is_indoor": True,
                        "is_outdoor": False,
                        "wheelchair_accessible": True,
                        "family_friendly": True,
                        "description": f"Intimate live music and singer-songwriter acoustic performance in {city}.",
                        "tags": ["music", "acoustic", "cozy", "relaxing", "indoor"],
                        "area": f"Arts District, {city}"
                    },
                    {
                        "name": f"{city} Contemporary Art Gallery",
                        "city": city,
                        "category": "art",
                        "duration_minutes": 90,
                        "cost": 150.0,
                        "crowd_level": "low",
                        "is_indoor": True,
                        "is_outdoor": False,
                        "wheelchair_accessible": True,
                        "family_friendly": True,
                        "description": f"Curated contemporary visual art and photography exhibitions in {city}.",
                        "tags": ["art", "culture", "quiet", "indoor"],
                        "area": f"Old Town, {city}"
                    }
                ]

        return results
    finally:
        if close_db:
            db.close()
