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

**IMPORTANT: Generate secure secret keys!**

```bash
# Generate SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

Add the generated keys to your `.env` file. See [SECURITY_KEYS.md](SECURITY_KEYS.md) for details.

**Validate your configuration:**

```bash
python validate_secrets.py
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
├── tests/                   # Test suite
│   ├── test_cors_configuration.py
│   ├── test_email_verification.py
│   ├── test_oauth_csrf.py
│   ├── test_rate_limiting.py
│   └── test_security_fix.py
├── alembic/                 # Database migrations
├── requirements.txt
├── package.json             # NPM scripts for convenience
├── pytest.ini               # Pytest configuration
├── .env.example
└── README.md
```

## Running the Server

### Using NPM scripts (recommended)
```bash
npm run dev      # Development server with auto-reload
npm run start    # Production server
npm test         # Run tests
```

### Using Python directly
```bash
uvicorn app.main:app --reload --port 8000
```

## Testing

Run all tests:
```bash
npm test
# or
pytest tests/
```

Run tests with verbose output:
```bash
npm run test:verbose
```

Run tests with coverage:
```bash
npm run test:coverage
```

See [tests/README.md](tests/README.md) for more details.

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
