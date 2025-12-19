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
│   │   ├── __init__.py
│   │   ├── company.py
│   │   └── job.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── company.py
│   │   └── job.py
│   ├── routes/              # API endpoints (routers)
│   │   ├── __init__.py
│   │   ├── jobs.py
│   │   └── companies.py
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── job_service.py
│   │   └── company_service.py
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py    # Custom HTTP exceptions
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
├── seed_data.py             # Database seeding script
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

## Architecture Layers (STRICT SEPARATION)

### Layer 1: Models (SQLAlchemy ORM)
**Purpose:** Database table definitions only
**Rules:**
- One model = one table
- Use SQLAlchemy 2.0 Mapped types
- Define relationships with back_populates
- Add indexes on filter/search columns
- Use enums for status/level fields
- Include timestamps (created_at, updated_at)

### Layer 2: Schemas (Pydantic)
**Purpose:** Request validation + response serialization
**Rules:**
- Separate schemas: Create, Update, Response
- Use Field() for validation constraints
- Response schemas inherit from Base
- Use `from_attributes = True` for ORM conversion
- Include nested schemas for relationships

### Layer 3: Services (Business Logic)
**Purpose:** Reusable business operations
**Rules:**
- All DB queries happen here (not in routes)
- One service per model
- All functions are async
- Return None for not found (don't raise here)
- Use select() for queries

### Layer 4: Routes (API Endpoints)
**Purpose:** HTTP interface only
**Rules:**
- Thin controllers (call services)
- Use Depends(get_db) for DB session
- Raise HTTP exceptions (404, 400, etc)
- Add OpenAPI docstrings
- Use router.prefix for URL grouping
- Include response_model in decorators

## Database Requirements

### SQLAlchemy Models Must Have:
- Primary key with index=True
- Proper type hints with Mapped[]
- Foreign keys for relations
- Indexes on filter columns (location, level, etc)
- Cascade delete rules
- Timestamps (created_at)
- Enums for categorical fields

### Required Relations:
- Company → Jobs (one-to-many)
- Job → Company (many-to-one)
- Use relationship() with back_populates

### Database Session:
- Async session only (AsyncSession)
- Create via dependency injection (get_db)
- Auto-commit on success
- Auto-rollback on exception
- Always close session in finally block

## API Endpoint Requirements

### Jobs Endpoints (MANDATORY):
- GET /api/jobs - List with filters (location, level, search, pagination)
- GET /api/jobs/{id} - Single job with company data
- POST /api/jobs - Create new job
- PUT /api/jobs/{id} - Update job
- DELETE /api/jobs/{id} - Delete job

### Companies Endpoints (MANDATORY):
- GET /api/companies - List all companies
- GET /api/companies/{id} - Single company with all jobs
- POST /api/companies - Create company

### Response Format (CONSISTENT):
- Success: Return data directly or list
- Error: FastAPI default (detail field)
- Always use response_model
- Always include status codes

### Query Parameters:
- Use Query() with validation
- Provide descriptions
- Set defaults and constraints
- Support multiple filters simultaneously

## CORS Configuration (CRITICAL)

### Requirements:
- Allow origins: http://localhost:3000 (frontend)
- Allow methods: GET, POST, PUT, DELETE, OPTIONS
- Allow headers: Content-Type, Authorization
- Allow credentials: True
- Max age: 3600

### In main.py:
- Import CORSMiddleware from fastapi.middleware.cors
- Add middleware with above settings
- Support preflight OPTIONS requests

## Error Handling (MANDATORY)

### Custom Exceptions:
- Inherit from HTTPException
- One exception per error type
- Include clear detail messages
- Use proper status codes (404, 400, 409, 500)

### Exception Types Needed:
- NotFoundExceptions (404) - for each model
- ValidationException (400) - for business rule violations
- ConflictException (409) - for duplicates

## Service Layer Patterns

### All Services Must:
- Accept AsyncSession as first parameter
- Return model instances or None
- Use async/await for all DB calls
- Use select() with options for eager loading
- Filter with where() clauses
- Use joinedload() for relationships
- Handle not found gracefully (return None)

### CRUD Operations Pattern:
- get_all() - with filters
- get_by_id() - single record
- create() - from Pydantic schema
- update() - partial update
- delete() - return bool

## Seed Data Requirements

### Must Include:
- 5-10 realistic companies
- 20-30 jobs across companies
- Mix of locations (Remote, cities)
- Mix of levels (junior, middle, senior, lead)
- Realistic descriptions with tech stacks
- Salary ranges

### Implementation:
- Async function using AsyncSession
- Check if data exists (don't duplicate)
- Commit after all inserts
- Print confirmation messages
- Runnable as script: `python seed_data.py`

## Environment Variables

### Required in .env:
- DATABASE_URL - SQLite path (default: sqlite+aiosqlite:///./jobs.db)
- CORS_ORIGINS - Comma-separated list (default: http://localhost:3000)
- DEBUG - Boolean flag
- SECRET_KEY - For future auth

## Main App Configuration

### FastAPI App Must Have:
- Title, version, description
- Lifespan events (startup/shutdown)
- CORS middleware
- Exception handlers
- Router includes
- Health check endpoint
- OpenAPI docs enabled

## Response Standards

### Success Responses:
- GET list: Return array directly
- GET single: Return object directly
- POST: Return created object, status 201
- PUT: Return updated object, status 200
- DELETE: Return 204 No Content

## Anti-Patterns (NEVER DO)

### ❌ Forbidden:
- Sync database calls
- dict instead of Pydantic models
- Bare except clauses
- Hardcoded configuration
- print() for logging
- Missing error handling
- Non-async endpoints with DB calls
- Raw SQL queries (use ORM)
- Missing type hints
- Incomplete implementations

## Output Format

### When Generating Code:
1. Show file path as comment
2. Generate complete code (no placeholders)
3. Explain architectural decision (1-2 sentences)
4. Suggest next step

### Example:
```
# app/models/job.py
[complete code here]

Architectural decision: Used enum for job levels to enforce valid values at DB level.
Next step: "Generate Pydantic schemas for Job (Create, Update, Response)"
```

## Commit Message Format
```
feat(backend): AI-generated [component]

[What was created]
Generated by: [Cursor/Windsurf/Claude]
```

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