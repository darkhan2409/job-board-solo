# Job Board Backend API

FastAPI backend for job board application with async SQLAlchemy and SQLite.

## Tech Stack

- **Python:** 3.11+
- **Framework:** FastAPI 0.104+
- **Database:** SQLite with aiosqlite
- **ORM:** SQLAlchemy 2.0+ (async mode)
- **Validation:** Pydantic V2
- **Server:** Uvicorn

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Seed the database (optional)

```bash
python seed_data.py
```

This will populate the database with:
- 8 tech companies
- 22 job postings across different locations and levels

### 6. Access API documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, CORS, lifespan
│   ├── config.py            # Settings from environment
│   ├── database.py          # Async SQLAlchemy setup
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   └── utils/               # Utilities and exceptions
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints (Coming Soon)

### Jobs
- `GET /api/jobs` - List jobs with filters
- `GET /api/jobs/{id}` - Get single job
- `POST /api/jobs` - Create job
- `PUT /api/jobs/{id}` - Update job
- `DELETE /api/jobs/{id}` - Delete job

### Companies
- `GET /api/companies` - List companies
- `GET /api/companies/{id}` - Get company with jobs
- `POST /api/companies` - Create company

## Development

Generated with AI assistance using Kiro.
