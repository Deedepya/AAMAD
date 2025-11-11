# Backend Service - Automated Employee Onboarding Workflow

## Overview
CrewAI-powered backend service for automated employee onboarding with document processing, compliance verification, and notification management.

## Architecture
- **Framework:** FastAPI (Python 3.11+)
- **Agent Framework:** CrewAI
- **Database:** PostgreSQL (production) / SQLite (development)
- **Storage:** AWS S3 or GCP Cloud Storage

## Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── crew/
│   ├── crew_config.py      # CrewAI crew initialization
│   ├── agents/            # Agent implementations
│   ├── tasks/              # Task definitions
│   └── tools/              # Tool implementations
├── config/
│   ├── agents.yaml         # Agent configurations
│   └── tasks.yaml          # Task configurations
├── models/                 # Data models
├── database/
│   ├── models.py           # SQLAlchemy models
│   └── migrations/         # Alembic migrations
└── requirements.txt        # Python dependencies
```

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   - Copy `.env.example` to `.env` (if available)
   - Set all required environment variables (see SAD Section 10.4)

3. **Database Setup:**
   ```bash
   # Initialize database migrations
   alembic init alembic
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

4. **Run Development Server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Key Endpoints (MVP)
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/onboarding/{user_id}/status` - Get onboarding status
- `GET /api/v1/tasks/{user_id}` - List tasks
- `POST /api/v1/tasks/{task_id}/complete` - Complete task

## Reference
- SAD: `project-context/1.define/sad.md` Section 7 (Backend Architecture)

