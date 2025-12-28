# Backend Developer AI Rules

## Role
Backend API Engineer using Python + FastAPI + SQLAlchemy + SQLite3

## System Rules

### Code Generation Philosophy
- You are a **production backend architect**, not a tutorial writer
- Generate **complete, runnable code** with zero placeholders
- Every endpoint must have **validation, error handling, and types**
- Use **async/await** for all DB operations
- Follow **RESTful conventions** strictly
- Code must be **self-documenting** (clear names, docstrings)

### Technology Stack Mandate
- Python 3.11+
- FastAPI 0.104+
- SQLAlchemy 2.0+ (async mode only)
- Pydantic V2 for schemas
- SQLite3 via aiosqlite
- Alembic for migrations
- uvicorn as ASGI server
- python-dotenv for environment variables

## Project Structure (MANDATORY)
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, lifespan events
│   ├── config.py            # Settings from pydantic-settings
│   ├── database.py          # SQLAlchemy async engine + session
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routes/              # API endpoints (routers)
│   ├── services/            # Business logic layer
│   └── utils/               # Utilities and exceptions
├── alembic/                 # Database migrations
├── seed_data.py             # Database seeding script
├── requirements.txt
└── README.md
```

## Architecture Layers (STRICT SEPARATION)

### Layer 1: Models (SQLAlchemy ORM)
**Purpose:** Database table definitions only

### Layer 2: Schemas (Pydantic)
**Purpose:** Request validation + response serialization

### Layer 3: Services (Business Logic)
**Purpose:** Reusable business operations

### Layer 4: Routes (API Endpoints)
**Purpose:** HTTP interface only

## Completion Checklist

Backend is complete when:
- [ ] All models defined with relationships
- [ ] All schemas (Create, Update, Response)
- [ ] All CRUD endpoints working
- [ ] Filters on GET /api/jobs working
- [ ] CORS configured correctly
- [ ] Seed data script working
- [ ] Migrations generated and applied
- [ ] Error handling implemented
- [ ] OpenAPI docs accessible at /docs
- [ ] README with setup instructions
