# Perfect Saturday Planner 🌟

An intelligent, production-ready AI-powered web application that turns your weekend preferences into a realistic, personalized, constraint-checked Saturday itinerary in seconds.

Built for the **AI Engineer Assignment**.

---

## 🎯 Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          React + TypeScript + Vite                     │
│               (Tailwind CSS, Lucide Icons, Interactive Timeline)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / SSE Trace Stream
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                              FastAPI Backend                           │
│               /health | /api/planner/plan | /api/planner/stream        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        LangGraph Decision Graph                        │
│                                                                        │
│   [START]                                                              │
│      │                                                                 │
│      ▼                                                                 │
│   parse_preferences ──(unclear)──► ask_clarification ──► [END]         │
│      │ (clear)                                                         │
│      ▼                                                                 │
│   search_activities ◄────────► [Tool 2: Activity DB / pgvector]        │
│      │                                                                 │
│      ▼                                                                 │
│   search_food ◄──────────────► [Tool 3: Restaurant DB]                 │
│      │                                                                 │
│      ▼                                                                 │
│   build_candidate_plan                                                 │
│      │                                                                 │
│      ▼                                                                 │
│   estimate_cost ◄────────────► [Tool 4: Cost & Transport Engine]       │
│      │                                                                 │
│      ▼                                                                 │
│   validate_plan ◄────────────► [Tool 5: Constraint & Time Engine]      │
│      │                                                                 │
│      ├──(invalid)──► fallback_plan                                     │
│      │                     │                                           │
│      └──(valid)────────────┼──► generate_final_plan (Groq / Fallback)  │
│                                           │                            │
│                                           ▼                            │
│                                         [END]                          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┴────────────────────────────┐
       ▼                                                         ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ PostgreSQL 16 + pgvector     │        │ Groq LLM Inference           │
│ (Seeded Activities & Dining) │        │ (Llama-3.3-70b-versatile)    │
└──────────────────────────────┘        └──────────────────────────────┘
```

---

## ✨ Features

- **Personalized Saturday Planning**: Tailored itineraries matching mood, budget, available time, interests, and constraints.
- **LangGraph Agentic Architecture**: Explicit multi-node state graph orchestrating tools deterministically.
- **Independent Python Tools**:
  1. `parse_user_preferences`: Normalizes time (e.g. 4 hours → 240m), currency, and checks for ambiguity.
  2. `get_activity_options`: Queries verified candidate activities with category, crowd, and mood scoring.
  3. `get_food_options`: Filters dining options matching strict dietary preferences (Pure Veg, Vegetarian) and budget limits.
  4. `estimate_cost`: Deterministic breakdown of activities, dining, and auto/cab transit buffers.
  5. `validate_plan`: Mathematically validates budget limits, time windows, and hard constraints.
- **Deterministic Math & Constraints**: No LLM hallucinations for pricing, time schedules, or dietary safety.
- **Live SSE Agent Trace**: Real-time event streaming showing what the agent is thinking, tool payloads, and latency in milliseconds.
- **Graceful Fallback Planning**: If exact preferences exceed budget or time limits, automatically devises a compliant fallback plan.
- **Clarification Loop**: Detects missing or ambiguous inputs and prompts user before running full planning.
- **Offline / Zero-Key Resilient**: Operates seamlessly with or without `GROQ_API_KEY` using smart deterministic synthesis.

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- (Optional) Docker & Docker Compose

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run seed script (Seeds 16 activities + 15 restaurants in Bangalore)
python -m app.db.seed

# Start FastAPI dev server
uvicorn app.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Frontend will be live at `http://localhost:5173`.

---

## 🐳 Running with Docker Compose

To spin up the complete stack (Postgres with pgvector + Backend + Frontend):

```bash
docker-compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

---

## ⚙️ Environment Variables

Create a `.env` file in the root or `backend/` folder:

```env
# Groq API Key (Optional: App features offline deterministic fallback if omitted)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Groq Model
GROQ_MODEL=llama-3.3-70b-versatile

# Database URL
# PostgreSQL: postgresql://postgres:postgrespassword@localhost:5432/saturday_planner
# SQLite (Default zero-config): sqlite:///./saturday_planner.db
DATABASE_URL=sqlite:///./saturday_planner.db

# Frontend CORS
FRONTEND_URL=http://localhost:5173

# pgvector toggle
USE_PGVECTOR=false
```

---

## 🧪 Testing

Run the automated test suite covering all tools, constraints, budget checks, fallback behavior, and API endpoints:

```bash
cd backend
python -m pytest
```

---

## 🚢 Deployment

### Frontend (Vercel)
1. Push repo to GitHub.
2. Import repo in Vercel with Root Directory set to `frontend`.
3. Add environment variable `VITE_API_URL=https://your-backend.railway.app`.

### Backend (Railway / Render)
1. Deploy `backend` folder as a Python service.
2. Configure environment variables: `DATABASE_URL`, `GROQ_API_KEY`, `FRONTEND_URL`.
3. Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

---

## 📍 Mock Data Disclaimer

> **Notice**: The current assignment version uses seeded mock activity and restaurant data for Bangalore rather than live third-party location APIs to guarantee evaluator demo reliability and deterministic reproducibility. The tool layer is intentionally decoupled so that live APIs (e.g. Google Places, Zomato) can seamlessly replace these data providers.

---

## 🤖 AI Tools Disclosure

> **AI-assisted development**: AI coding tools were used during development to accelerate scaffolding, boilerplate generation, debugging, and implementation of the LangGraph workflow. The final architecture, tool boundaries, validation logic, prompts, and product decisions were reviewed, verified, and adapted for this assignment.
