import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import Base, engine
from app.db.seed import seed_database
from app.api.routes_health import router as health_router
from app.api.routes_planner import router as planner_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("perfect_saturday_planner")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize tables and seed database
    logger.info("Initializing database tables and seed data...")
    Base.metadata.create_all(bind=engine)
    try:
        seed_database()
        logger.info("Database initialized and mock data verified.")
    except Exception as e:
        logger.error(f"Seeding error: {e}")
    yield
    # Shutdown
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Intelligent AI Agent for generating personalized Saturday itineraries",
    lifespan=lifespan
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    settings.FRONTEND_URL,
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(health_router)
app.include_router(planner_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root_redirect():
    return {
        "message": "Welcome to Perfect Saturday Planner API",
        "health": "/health",
        "docs": "/docs",
        "api_v1": f"{settings.API_V1_PREFIX}/planner/plan"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
