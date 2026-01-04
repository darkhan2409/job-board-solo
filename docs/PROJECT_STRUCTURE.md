# Project Structure

This document describes the organization of the Job Board Solo project.

## Directory Structure

```
job-board-solo/
├── backend/                    # Backend API (FastAPI)
│   ├── app/                   # Application code
│   │   ├── models/           # Database models (SQLAlchemy)
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routes/           # API endpoints
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utilities
│   ├── alembic/              # Database migrations
│   ├── .env.example          # Environment variables template
│   ├── requirements.txt      # Python dependencies
│   ├── seed_data.py         # Database seeder
│   ├── sync_hh_vacancies.py # HeadHunter API sync script
│   └── README.md            # Backend documentation
│
├── frontend/                  # Frontend application (Next.js)
│   ├── src/
│   │   ├── app/             # Pages (App Router)
│   │   │   ├── api/        # API routes (AI chat)
│   │   │   ├── jobs/       # Jobs pages
│   │   │   └── companies/  # Companies pages
│   │   ├── components/      # React components
│   │   │   └── ui/         # shadcn/ui components
│   │   ├── contexts/        # React contexts
│   │   ├── hooks/           # Custom hooks
│   │   └── lib/             # Utilities and API client
│   ├── public/              # Static assets
│   ├── .env.example         # Environment variables template
│   ├── package.json         # Node dependencies
│   └── README.md           # Frontend documentation
│
├── tests/                    # E2E tests
│   └── e2e/                 # Playwright test specs
│       ├── homepage.spec.ts
│       ├── jobs.spec.ts
│       ├── job-detail.spec.ts
│       ├── companies.spec.ts
│       └── chat.spec.ts
│
├── docs/                     # Project documentation
│   ├── SECURITY.md          # Security guidelines
│   ├── WORKFLOW.md          # Development workflow
│   ├── HTTPS_SETUP.md       # HTTPS configuration
│   └── PROJECT_STRUCTURE.md # This file
│
├── scripts/                  # Utility scripts
│   ├── generate-certs.bat   # SSL certificate generator (Windows)
│   └── generate-certs.sh    # SSL certificate generator (Linux/Mac)
│
├── screenshots/              # Development screenshots
│   ├── README.md            # Screenshots documentation
│   └── *.png                # Screenshot files
│
├── ai-rules/                 # AI assistant rules
│   ├── ai.md                # General AI rules
│   ├── backend.md           # Backend development rules
│   ├── frontend.md          # Frontend development rules
│   └── qa.md                # QA and testing rules
│
├── playwright-report/        # Playwright test reports
├── test-results/            # Test execution results
├── node_modules/            # Node.js dependencies (root)
│
├── .gitignore               # Git ignore rules
├── package.json             # Root package.json (for Playwright)
├── playwright.config.ts     # Playwright configuration
└── README.md                # Main project documentation
```

## Key Directories

### `/backend`
Contains the FastAPI backend application with:
- RESTful API endpoints
- Database models and migrations
- Business logic and services
- HeadHunter API integration
- Authentication and authorization

### `/frontend`
Contains the Next.js frontend application with:
- Server-side rendered pages
- React components and UI
- AI chat integration
- API client for backend communication

### `/tests`
Contains end-to-end tests using Playwright:
- 33 tests covering all major features
- Page object patterns
- Test fixtures and helpers

### `/docs`
Contains project documentation:
- Security best practices
- Development workflow
- HTTPS setup guide
- Project structure (this file)

### `/scripts`
Contains utility scripts:
- SSL certificate generation
- Database management
- Deployment helpers

### `/screenshots`
Contains development evidence:
- AI-assisted development screenshots
- Feature implementation evidence
- MCP usage examples

### `/ai-rules`
Contains AI assistant configuration:
- Development guidelines
- Code style rules
- Testing strategies

## Configuration Files

### Root Level
- `package.json` - Root dependencies (Playwright for E2E tests)
- `package-lock.json` - Lock file for root dependencies
- `playwright.config.ts` - E2E test configuration
- `.gitignore` - Git ignore patterns

**Why in root?**
- Playwright requires configuration in project root
- E2E tests run from root directory (`npm run test:e2e`)
- Tests are located in `/tests/e2e` (relative to root)
- This is standard practice for monorepo structures

### Backend
- `backend/.env` - Environment variables (not in git)
- `backend/.env.example` - Environment template
- `backend/requirements.txt` - Python dependencies
- `backend/alembic.ini` - Database migration config

### Frontend
- `frontend/.env.local` - Environment variables (not in git)
- `frontend/.env.example` - Environment template
- `frontend/package.json` - Node dependencies
- `frontend/next.config.js` - Next.js configuration
- `frontend/tailwind.config.ts` - Tailwind CSS config
- `frontend/tsconfig.json` - TypeScript config

## Important Files

### Documentation
- `README.md` - Main project documentation
- `docs/SECURITY.md` - Security guidelines
- `docs/WORKFLOW.md` - Development process
- `docs/HTTPS_SETUP.md` - HTTPS setup

### Backend Scripts
- `backend/seed_data.py` - Populate database with sample data
- `backend/sync_hh_vacancies.py` - Sync real jobs from HeadHunter
- `backend/check_db.py` - Database statistics checker
- `backend/validate_secrets.py` - Environment validation

### Frontend Scripts
- `frontend/server.js` - HTTPS development server

### Utility Scripts
- `scripts/generate-certs.bat` - Generate SSL certificates (Windows)
- `scripts/generate-certs.sh` - Generate SSL certificates (Linux/Mac)

## Development Workflow

1. **Backend Development**
   - Work in `/backend` directory
   - Run `uvicorn app.main:app --reload`
   - Access API docs at http://localhost:8000/docs

2. **Frontend Development**
   - Work in `/frontend` directory
   - Run `npm run dev`
   - Access app at http://localhost:3000

3. **Testing**
   - Write tests in `/tests/e2e`
   - Run `npm run test:e2e` from root
   - View reports in `/playwright-report`

4. **Documentation**
   - Update docs in `/docs` directory
   - Keep README.md in sync with changes
   - Document new features and APIs

## File Naming Conventions

### Backend (Python)
- Models: `snake_case.py` (e.g., `job.py`, `company.py`)
- Schemas: `snake_case.py` (e.g., `job_schema.py`)
- Routes: `snake_case.py` (e.g., `jobs.py`, `auth.py`)
- Services: `snake_case.py` (e.g., `job_service.py`)

### Frontend (TypeScript)
- Components: `PascalCase.tsx` (e.g., `JobCard.tsx`)
- Pages: `lowercase.tsx` (e.g., `page.tsx`, `layout.tsx`)
- Utilities: `camelCase.ts` (e.g., `apiClient.ts`)
- Types: `camelCase.ts` (e.g., `types.ts`)

### Tests
- Test files: `kebab-case.spec.ts` (e.g., `job-detail.spec.ts`)

### Documentation
- Docs: `SCREAMING_SNAKE_CASE.md` (e.g., `README.md`, `SECURITY.md`)

## Environment Variables

### Backend (.env)
```bash
SECRET_KEY=<generated-secret>
DATABASE_URL=sqlite+aiosqlite:///./jobs.db
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```bash
OPENAI_API_KEY=sk-proj-<your-key>
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Dependencies Management

### Backend
- Install: `pip install -r requirements.txt`
- Update: `pip freeze > requirements.txt`
- Virtual env: `python -m venv venv`

### Frontend
- Install: `npm install`
- Update: `npm update`
- Add package: `npm install <package>`

### Root (Playwright)
- Install: `npm install`
- Update browsers: `npx playwright install`

## Build and Deployment

### Backend
```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Development
npm run dev

# Production build
npm run build
npm start
```

### Tests
```bash
# Run all tests
npm run test:e2e

# Run specific test
npx playwright test tests/e2e/jobs.spec.ts

# UI mode
npm run test:e2e:ui
```

## Git Workflow

### Branches
- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - Feature branches
- `fix/*` - Bug fix branches

### Commits
Follow conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Code style
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

## Security Notes

### Never Commit
- `.env` files
- `.env.local` files
- `*.pem` files (SSL certificates)
- `*.key` files (private keys)
- API keys or secrets

### Always Check
- `.gitignore` is up to date
- No secrets in code
- Environment templates are current
- Dependencies are secure

## Additional Resources

- [Backend README](../backend/README.md)
- [Frontend README](../frontend/README.md)
- [Security Guide](SECURITY.md)
- [Development Workflow](WORKFLOW.md)
- [HTTPS Setup](HTTPS_SETUP.md)

---

**Last Updated:** January 4, 2026
