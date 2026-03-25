# AI Writing Assistant (Web App)

An end-to-end AI-powered writing assistant that helps users generate, edit, and refine text with a low-latency web experience.

## Highlights

- **End-to-end writing workflow**: Generate drafts, edit for tone/clarity, and refine for structure.
- **Scalable backend**: Built with **FastAPI + PostgreSQL** and clean service boundaries.
- **Reliability-focused**: Request IDs, health endpoint, DB connection pooling, and graceful error handling.
- **UX-first web client**: Simple browser UI for creating sessions and iterating on content quickly.

## Architecture

- **Frontend**: Static HTML/CSS/JS served by FastAPI (`/` route).
- **API**: REST endpoints for sessions, generation, editing, and refinement.
- **Persistence**: PostgreSQL via SQLAlchemy ORM.
- **AI layer**: `AIWriterService` abstraction (currently heuristic fallback, pluggable for LLM provider).

## Quick Start

### 1) Configure environment

```bash
cp .env.example .env
```

### 2) Start PostgreSQL

```bash
docker compose up -d db
```

### 3) Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Run app

```bash
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## API Endpoints

- `GET /health` — health check with dependency status
- `POST /api/sessions` — create a user session
- `GET /api/sessions/{session_id}` — fetch session + content history
- `POST /api/write/generate` — create a draft from prompt
- `POST /api/write/edit` — rewrite an existing text with instruction
- `POST /api/write/refine` — improve readability and structure

## Notes on latency and reliability

- SQLAlchemy connection pooling + pre-ping for resilient DB usage.
- Lightweight AI processing path to keep response time low.
- Request-scoped correlation ID middleware for easier debugging in production.
- Centralized exception handling for predictable API behavior.
