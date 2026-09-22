from sqlalchemy.orm import Session
from app.db.database import Base, engine, SessionLocal
from app.models.activity import Activity
from app.models.restaurant import Restaurant

ACTIVITIES_DATA = [
    {
        "name": "Cubbon Park Evening Walk & Bamboo Grove",
        "city": "Bangalore",
        "category": "walks",
        "duration_minutes": 75,
        "cost": 0.0,
        "crowd_level": "medium",
        "is_indoor": False,
        "is_outdoor": True,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Relaxed green-space walk surrounded by heritage trees, bamboo groves, and open lawns.",
        "tags": ["nature", "walks", "parks", "quiet", "relaxing", "outdoor", "photography"],
        "area": "Central Bangalore"
    },
    {
        "name": "Lalbagh Botanical Garden Glass House Stroll",
        "city": "Bangalore",
        "category": "nature",
        "duration_minutes": 90,
        "cost": 50.0,
        "crowd_level": "medium",
        "is_indoor": False,
        "is_outdoor": True,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Expansive historic botanical garden featuring the iconic 19th-century Glass House, lotus pond, and tranquil tree paths.",
        "tags": ["nature", "walks", "parks", "flowers", "outdoor", "photography"],
        "area": "South Bangalore"
    },
    {
        "name": "Indie Acoustic Session at The Blue Room",
        "city": "Bangalore",
        "category": "music",
        "duration_minutes": 90,
        "cost": 500.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Intimate acoustic singer-songwriter live set with cozy floor cushions and warm ambient lighting.",
        "tags": ["music", "acoustic", "cozy", "indoor", "relaxing", "art"],
        "area": "Indiranagar"
    },
    {
        "name": "Blossom Book House Literary Browsing",
        "city": "Bangalore",
        "category": "books",
        "duration_minutes": 60,
        "cost": 0.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Legendary multi-storey second-hand & rare bookstore on Church Street with infinite aisles of books.",
        "tags": ["books", "shopping", "quiet", "indoor", "reading", "solo"],
        "area": "Church Street"
    },
    {
        "name": "National Gallery of Modern Art (NGMA)",
        "city": "Bangalore",
        "category": "art",
        "duration_minutes": 90,
        "cost": 100.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": True,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Heritage mansion housing Indian contemporary art, serene fountain courtyards, and sculpture gardens.",
        "tags": ["art", "culture", "quiet", "indoor", "outdoor", "photography"],
        "area": "Palace Road"
    },
    {
        "name": "Rangashankara Intimate Evening Theatre",
        "city": "Bangalore",
        "category": "art",
        "duration_minutes": 100,
        "cost": 300.0,
        "crowd_level": "medium",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Beloved cultural playhouse showcasing experimental and classical regional theatre plays.",
        "tags": ["art", "theatre", "culture", "indoor", "drama"],
        "area": "JP Nagar"
    },
    {
        "name": "Suchitra Film Society Classic Screening",
        "city": "Bangalore",
        "category": "movies",
        "duration_minutes": 120,
        "cost": 150.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Curated screening of world cinema or Indian indie classics with brief director retrospective notes.",
        "tags": ["movies", "cinema", "indoor", "quiet", "culture"],
        "area": "Banashankari"
    },
    {
        "name": "Claystation Ceramic Pottery Workshop",
        "city": "Bangalore",
        "category": "art",
        "duration_minutes": 90,
        "cost": 850.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Hands-on guided wheel pottery class where you create custom clay ceramic bowls and mugs.",
        "tags": ["art", "creative", "workshop", "hands-on", "indoor"],
        "area": "HSR Layout"
    },
    {
        "name": "Sankey Tank Sunset Promenade",
        "city": "Bangalore",
        "category": "walks",
        "duration_minutes": 60,
        "cost": 0.0,
        "crowd_level": "medium",
        "is_indoor": False,
        "is_outdoor": True,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Peaceful lake perimeter walking track lined with canopy trees and picturesque bird watching spots.",
        "tags": ["walks", "nature", "sunset", "lake", "outdoor", "photography"],
        "area": "Malleshwaram"
    },
    {
        "name": "Board 4 Bored Tabletop Game Cafe",
        "city": "Bangalore",
        "category": "sports",
        "duration_minutes": 90,
        "cost": 250.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Over 200 modern tabletop strategy and cooperative party games with friendly game gurus.",
        "tags": ["sports", "games", "indoor", "social", "fun"],
        "area": "Koramangala"
    },
    {
        "name": "Dipti Art Studio Watercolor Painting Session",
        "city": "Bangalore",
        "category": "art",
        "duration_minutes": 75,
        "cost": 400.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Relaxing weekend painting circle with organic botanical watercolours and herbal tea.",
        "tags": ["art", "creative", "relaxing", "indoor"],
        "area": "Indiranagar"
    },
    {
        "name": "The Bangalore Live Music Arena (Major Venue)",
        "city": "Bangalore",
        "category": "music",
        "duration_minutes": 150,
        "cost": 1200.0,
        "crowd_level": "high",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": False,
        "description": "Energetic high-capacity rock and electronic music concert hall.",
        "tags": ["music", "loud", "crowded", "concert", "indoor", "social"],
        "area": "Whitefield"
    },
    {
        "name": "PVR Director's Cut Luxury Movie Screen",
        "city": "Bangalore",
        "category": "movies",
        "duration_minutes": 150,
        "cost": 800.0,
        "crowd_level": "medium",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Plush recliner cinema experience with gourmet in-seat menu.",
        "tags": ["movies", "cinema", "luxury", "indoor"],
        "area": "Koramangala"
    },
    {
        "name": "Play Arena Badminton & Bouldering",
        "city": "Bangalore",
        "category": "sports",
        "duration_minutes": 90,
        "cost": 450.0,
        "crowd_level": "medium",
        "is_indoor": True,
        "is_outdoor": True,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Indoor wooden badminton courts and climbing wall for an active afternoon session.",
        "tags": ["sports", "fitness", "active", "indoor", "outdoor"],
        "area": "Sarjapur Road"
    },
    {
        "name": "Heritage Photo Walk of Basavanagudi",
        "city": "Bangalore",
        "category": "photography",
        "duration_minutes": 80,
        "cost": 0.0,
        "crowd_level": "low",
        "is_indoor": False,
        "is_outdoor": True,
        "wheelchair_accessible": False,
        "family_friendly": True,
        "description": "Stroll past antique South Indian agrahara houses, traditional flower markets, and temple architecture.",
        "tags": ["photography", "walks", "heritage", "outdoor", "culture"],
        "area": "Basavanagudi"
    },
    {
        "name": "Atta Galatta Cultural Bookstore & Spoken Word",
        "city": "Bangalore",
        "category": "books",
        "duration_minutes": 75,
        "cost": 150.0,
        "crowd_level": "low",
        "is_indoor": True,
        "is_outdoor": False,
        "wheelchair_accessible": True,
        "family_friendly": True,
        "description": "Bookstore and cultural venue hosting poetry readings, book launches, and art discussions.",
        "tags": ["books", "art", "quiet", "indoor", "culture", "poetry"],
        "area": "Koramangala"
    }
]

RESTAURANTS_DATA = [
    {
        "name": "Green Leaf Garden Cafe",
        "city": "Bangalore",
        "cuisine": "Vegetarian",
        "average_cost": 450.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "low",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Serene courtyard cafe serving fresh farm-to-table vegetarian grain bowls, herbal infusions, and South Indian tiffin specials.",
        "tags": ["vegetarian", "pure_veg", "healthy", "cafe", "quiet", "outdoor_seating"],
        "area": "Indiranagar"
    },
    {
        "name": "Mavalli Tiffin Room (MTR) Lalbagh",
        "city": "Bangalore",
        "cuisine": "South Indian",
        "average_cost": 350.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "medium",
        "is_indoor": True,
        "wheelchair_accessible": False,
        "description": "Iconic heritage vegetarian institution world-famous for rava idli, pure ghee masala dosa, and filter coffee.",
        "tags": ["south_indian", "vegetarian", "pure_veg", "heritage", "breakfast", "traditional"],
        "area": "Lalbagh"
    },
    {
        "name": "Third Wave Coffee Roasters",
        "city": "Bangalore",
        "cuisine": "Cafe",
        "average_cost": 350.0,
        "vegetarian_friendly": True,
        "pure_veg": False,
        "serves_alcohol": False,
        "crowd_level": "low",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Artisanal speciality pour-over coffees, sourdough toasts, croissants, and quiet work/reading tables.",
        "tags": ["cafe", "coffee", "quiet", "snacks", "work_friendly"],
        "area": "Indiranagar"
    },
    {
        "name": "Brahmin's Coffee Bar",
        "city": "Bangalore",
        "cuisine": "South Indian",
        "average_cost": 150.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "medium",
        "is_indoor": False,
        "wheelchair_accessible": True,
        "description": "Legendary quick-service stand-and-eat joint with cloud-soft idlis, crisp vadas, and unmatched coconut chutney.",
        "tags": ["south_indian", "vegetarian", "pure_veg", "budget", "fast"],
        "area": "Shankarapuram"
    },
    {
        "name": "Burma Burma Restaurant & Tea Room",
        "city": "Bangalore",
        "cuisine": "Vegetarian",
        "average_cost": 1200.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "medium",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Award-winning pure vegetarian Pan-Asian & Burmese dining featuring samuza thoke, khao suey, and artisan teas.",
        "tags": ["vegetarian", "pure_veg", "pan_asian", "luxury", "tea"],
        "area": "Indiranagar"
    },
    {
        "name": "Vidyarthi Bhavan",
        "city": "Bangalore",
        "cuisine": "South Indian",
        "average_cost": 200.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "high",
        "is_indoor": True,
        "wheelchair_accessible": False,
        "description": "Historic 1943 Gandhi Bazaar eatery famous for crispy butter masala dosas stacked high on servers' trays.",
        "tags": ["south_indian", "vegetarian", "pure_veg", "heritage", "budget", "crowded"],
        "area": "Gandhi Bazaar"
    },
    {
        "name": "Yogisthaan Organic Ayurvedic Cafe",
        "city": "Bangalore",
        "cuisine": "Healthy Food",
        "average_cost": 500.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "low",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Wholesome, satvik vegetarian cafe with hammocks, lush green foliage, herbal teas, and fresh poha/khichdi.",
        "tags": ["healthy", "organic", "vegetarian", "pure_veg", "peaceful", "quiet"],
        "area": "Indiranagar"
    },
    {
        "name": "Truffles Gourmet Burgers & Shakes",
        "city": "Bangalore",
        "cuisine": "Casual Dining",
        "average_cost": 500.0,
        "vegetarian_friendly": True,
        "pure_veg": False,
        "serves_alcohol": False,
        "crowd_level": "high",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Youth hotspot celebrated for hearty American burgers, peri-peri fries, pasta, and Dutch truffles.",
        "tags": ["casual_dining", "burgers", "shakes", "high_energy"],
        "area": "Koramangala"
    },
    {
        "name": "The Hole in the Wall Cafe",
        "city": "Bangalore",
        "cuisine": "Cafe",
        "average_cost": 600.0,
        "vegetarian_friendly": True,
        "pure_veg": False,
        "serves_alcohol": False,
        "crowd_level": "medium",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Quaint English breakfast cafe serving fluffy blueberry pancakes, grilled paninis, and hot cocoa.",
        "tags": ["cafe", "breakfast", "waffles", "cozy"],
        "area": "Koramangala"
    },
    {
        "name": "Punjab Grill",
        "city": "Bangalore",
        "cuisine": "North Indian",
        "average_cost": 1100.0,
        "vegetarian_friendly": True,
        "pure_veg": False,
        "serves_alcohol": True,
        "crowd_level": "medium",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Rich gourmet North Indian cuisine with slow-cooked dal makhani, paneer tikka, and royal biryanis.",
        "tags": ["north_indian", "mughlai", "curry", "upscale"],
        "area": "Whitefield"
    },
    {
        "name": "Davanagere Benne Dosa Point",
        "city": "Bangalore",
        "cuisine": "South Indian",
        "average_cost": 180.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "low",
        "is_indoor": False,
        "wheelchair_accessible": True,
        "description": "Crispy butter open dosas served with spicy potato palya and mild coconut chutney.",
        "tags": ["south_indian", "vegetarian", "pure_veg", "budget", "quick"],
        "area": "Jayanagar"
    },
    {
        "name": "Toit Brewpub",
        "city": "Bangalore",
        "cuisine": "Casual Dining",
        "average_cost": 1200.0,
        "vegetarian_friendly": True,
        "pure_veg": False,
        "serves_alcohol": True,
        "crowd_level": "high",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Lively microbrewery with wood-fired sourdough pizzas, craft beers, and buzzing crowd.",
        "tags": ["brewery", "casual_dining", "pizza", "alcohol", "crowded"],
        "area": "Indiranagar"
    },
    {
        "name": "Carrots - The Plant Kitchen",
        "city": "Bangalore",
        "cuisine": "Healthy Food",
        "average_cost": 650.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "low",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "100% plant-based creative kitchen with gluten-free pizzas, dairy-free cheesecakes, and organic pasta.",
        "tags": ["healthy", "vegan", "vegetarian", "pure_veg", "gluten_free", "quiet"],
        "area": "Koramangala"
    },
    {
        "name": "Tea Villa Cafe",
        "city": "Bangalore",
        "cuisine": "Cafe",
        "average_cost": 400.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "low",
        "is_indoor": True,
        "wheelchair_accessible": True,
        "description": "Vegetarian tea lounge with over 80 exotic teas, bubble waffles, and fondues in an elegant pastel setting.",
        "tags": ["cafe", "tea", "vegetarian", "pure_veg", "desserts", "quiet"],
        "area": "Jayanagar"
    },
    {
        "name": "CTR (Shri Sagar) Malleshwaram",
        "city": "Bangalore",
        "cuisine": "South Indian",
        "average_cost": 220.0,
        "vegetarian_friendly": True,
        "pure_veg": True,
        "serves_alcohol": False,
        "crowd_level": "high",
        "is_indoor": True,
        "wheelchair_accessible": False,
        "description": "Historic Malleshwaram landmark famed for Benne Masala Dosa, poori sagu, and filter kaapi.",
        "tags": ["south_indian", "vegetarian", "pure_veg", "heritage", "crowded"],
        "area": "Malleshwaram"
    }
]


def seed_database(db: Session = None):
    """Seed the database with initial mock activities and restaurants."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    close_after = False
    if db is None:
        db = SessionLocal()
        close_after = True

    try:
        # Check if already seeded
        existing_activities = db.query(Activity).count()
        if existing_activities == 0:
            for item in ACTIVITIES_DATA:
                activity = Activity(**item)
                db.add(activity)
            db.commit()
            print(f"Seeded {len(ACTIVITIES_DATA)} activities.")

        existing_restaurants = db.query(Restaurant).count()
        if existing_restaurants == 0:
            for item in RESTAURANTS_DATA:
                restaurant = Restaurant(**item)
                db.add(restaurant)
            db.commit()
            print(f"Seeded {len(RESTAURANTS_DATA)} restaurants.")
    finally:
        if close_after:
            db.close()


if __name__ == "__main__":
    seed_database()
    print("Database seeding completed successfully.")
