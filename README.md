# AI Writing Assistant (Web App)

An end-to-end AI-powered writing assistant that helps users generate, edit, and refine text with a low-latency web experience.

## Highlights

- **End-to-end writing workflow**: Generate drafts, edit for tone/clarity, and refine for structure.
- **Scalable backend**: Built with **FastAPI + SQLAlchemy** and supports SQLite (local) or PostgreSQL.
- **Reliability-focused**: Request IDs, health endpoint, and graceful error handling.
- **UX-first web client**: Simple browser UI for creating sessions and iterating on content quickly.

## Architecture

- **Frontend**: Static HTML/CSS/JS served by FastAPI (`/` route).
- **API**: REST endpoints for sessions, generation, editing, and refinement.
- **Persistence**: SQLite by default; PostgreSQL supported via environment configuration.
- **AI layer**: `AIWriterService` abstraction (currently heuristic fallback, pluggable for LLM provider).

## Quick Start (No Docker)

### 1) Clone and enter project

```bash
git clone https://github.com/Sai-Mannava/ChatApp.git
cd ChatApp
```

### 2) Configure environment

```bash
cp .env.example .env
```

### 3) Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Run app

```bash
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## Optional: Run with PostgreSQL

```bash
docker compose up -d db
# update DATABASE_URL in .env to postgres connection string
```

## API Endpoints

- `GET /health` — health check with dependency status
- `POST /api/sessions` — create a user session
- `GET /api/sessions/{session_id}` — fetch session + content history
- `POST /api/write/generate` — create a draft from prompt
- `POST /api/write/edit` — rewrite an existing text with instruction
- `POST /api/write/refine` — improve readability and structure

## Notes on latency and reliability

- SQLite default reduces setup friction for local usage.
- PostgreSQL mode enables scaled production-style operation.
- Request-scoped correlation ID middleware helps debugging in production.
