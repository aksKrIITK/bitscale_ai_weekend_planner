import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

from app.schemas.planner import PlanRequest
from app.services.planner_service import planner_service
import asyncio

async def test_delhi_planning():
    print("\n==========================================")
    print("Testing Delhi Itinerary with Groq LLM")
    print("==========================================")
    delhi_request = PlanRequest(
        city="Delhi",
        budget=3000,
        available_time="6 hours",
        mood="exploratory & food loving",
        interests=["food", "nature", "books"],
        constraints=["vegetarian", "avoid crowded places"]
    )
    res = await planner_service.create_plan(delhi_request, session_id="test-delhi-session")
    print("Session ID:", res.session_id)
    if res.plan:
        print("\nTitle:", res.plan.title)
        print("Summary:", res.plan.summary)
        print(f"Total Cost: ₹{res.plan.total_cost:.0f} (Remaining: ₹{res.plan.remaining_budget:.0f})")
        print(f"Total Duration: {res.plan.total_duration_minutes} minutes")
        print("\nTimeline Schedule:")
        for idx, item in enumerate(res.plan.timeline):
            print(f"  {idx+1}. [{item.start} - {item.end}] {item.name} (Cost: ₹{item.cost:.0f})")
            print(f"     Location: {item.area}")
            print(f"     Why chosen: {item.why}")
        print("\nTrade-offs & Reasoning:")
        for t_off in res.plan.tradeoffs:
            print(f"  • {t_off}")
        print("\nValidation Status:")
        print(f"  ✓ Budget OK: {res.plan.validation.budget_ok}")
        print(f"  ✓ Time OK: {res.plan.validation.time_ok}")
        print(f"  ✓ Constraints OK: {res.plan.validation.constraints_ok}")
    print("\nAgent Trace Steps:")
    for t in res.trace:
        print(f"  ✓ [{t.node}] {t.status}: {t.message} ({t.duration_ms}ms)")

if __name__ == "__main__":
    asyncio.run(test_delhi_planning())
