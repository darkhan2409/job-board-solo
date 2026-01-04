# 🚀 Job Board Solo - Full-Stack Job Board with AI Assistant

> Modern job board application with AI-powered search assistant and HeadHunter API integration

[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
[![Tests](https://img.shields.io/badge/E2E_Tests-33_Passing-success)](https://playwright.dev/)

## 📋 Overview

Job Board Solo is a full-stack job search platform featuring:

- 🔍 **Real Job Data** - Integration with HeadHunter API for live IT vacancies
- 🤖 **AI Assistant** - OpenAI GPT-4 powered chat for intelligent job search
- 🔐 **Complete Auth** - JWT-based authentication with OAuth support
- 📱 **Responsive UI** - Modern design with Tailwind CSS and shadcn/ui
- ✅ **Tested** - 33 E2E tests with Playwright (100% pass rate)
- 🔒 **Secure** - HTTPS support, rate limiting, CORS configuration

## 🛠️ Tech Stack

### Backend
- **FastAPI 0.115** - Modern Python web framework
- **SQLAlchemy 2.0** - Async ORM with SQLite
- **Pydantic V2** - Data validation
- **Alembic** - Database migrations
- **HeadHunter API** - Real job data integration

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript 5.3** - Type safety
- **Tailwind CSS 3.3** - Utility-first styling
- **shadcn/ui** - Beautiful UI components
- **Lucide React** - Icon library

### AI & Testing
- **OpenAI GPT-4 Turbo** - AI assistant
- **Playwright 1.40** - E2E testing framework

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+
- OpenAI API key (for AI assistant)

### 1. Clone Repository

```bash
git clone https://github.com/darkhan2409/job-board-solo.git
cd job-board-solo
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Generate secure SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
# Add the generated key to .env file

# Seed database with sample data
python seed_data.py

# Start server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### 3. Sync Real Job Data (Optional)

Fetch real IT vacancies from HeadHunter API:

```bash
cd backend
python sync_hh_vacancies.py
```

This will:
- Clear sample data
- Fetch 150+ real IT jobs from HeadHunter
- Save companies and vacancies to database

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local

# Add your OpenAI API key to .env.local
# OPENAI_API_KEY=sk-proj-your-key-here

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 5. Run E2E Tests (Optional)

```bash
# From project root
npm install
npx playwright install

# Run tests
npm run test:e2e

# Run tests in UI mode
npm run test:e2e:ui

# View test report
npm run test:e2e:report
```

## 📚 Key Features

### For Users
- 👤 **Authentication** - Register, login, password reset, OAuth
- 🔍 **Job Search** - Filter by keywords, location, experience level
- 🏢 **Company Profiles** - View companies and their job listings
- 🔖 **Save Jobs** - Bookmark interesting positions
- 🤖 **AI Assistant** - Chat with AI to find relevant jobs
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

### For Developers
- ⚡ **Async API** - FastAPI with async SQLAlchemy
- 🔒 **Security** - JWT tokens, password hashing, rate limiting
- 📝 **Type Safety** - TypeScript + Pydantic validation
- 🧪 **Testing** - 33 E2E tests with Playwright
- 📖 **Documentation** - OpenAPI/Swagger docs
- 🔄 **Real Data** - HeadHunter API integration

## 🔑 API Endpoints

### Authentication
```
POST   /api/auth/register          - Register new user
POST   /api/auth/login             - Login
POST   /api/auth/refresh           - Refresh access token
POST   /api/auth/forgot-password   - Request password reset
POST   /api/auth/reset-password    - Reset password
GET    /api/auth/verify-email      - Verify email
```

### Jobs
```
GET    /api/jobs                   - List jobs (with filters)
GET    /api/jobs/{id}              - Get job details
POST   /api/jobs                   - Create job (auth required)
PUT    /api/jobs/{id}              - Update job (auth required)
DELETE /api/jobs/{id}              - Delete job (auth required)
```

### Companies
```
GET    /api/companies              - List companies
GET    /api/companies/{id}         - Get company details
POST   /api/companies              - Create company (auth required)
```

### HeadHunter Integration
```
GET    /api/v1/hh/vacancies        - Search HH vacancies
GET    /api/v1/hh/vacancies/{id}   - Get HH vacancy details
GET    /api/v1/hh/areas            - List available areas
GET    /api/v1/hh/roles            - List professional roles
```

### Query Parameters for /api/jobs
- `search` - Search in title/description
- `location` - Filter by location
- `level` - Filter by level (junior/middle/senior/lead)
- `skip` - Pagination offset
- `limit` - Results per page

## 🤖 AI Assistant

The AI assistant has access to two tools:

### 1. search_jobs
Search for jobs through the backend API
```typescript
{
  search: "React",
  location: "Remote",
  level: "senior",
  limit: 5
}
```

### 2. get_company_info
Get company details and their job listings
```typescript
{
  company_id: 1
}
```

## 📊 Project Structure

```
job-board-solo/
├── 📁 backend/              # FastAPI backend
│   ├── app/                # Application code
│   ├── alembic/           # Database migrations
│   └── *.py               # Scripts (seed, sync, etc.)
│
├── 📁 frontend/            # Next.js frontend
│   ├── src/               # Source code
│   │   ├── app/          # Pages & API routes
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities
│   └── public/           # Static assets
│
├── 📁 tests/               # E2E tests (Playwright)
│   └── e2e/              # Test specifications
│
├── 📁 docs/                # Documentation
│   ├── PROJECT_STRUCTURE.md
│   ├── SECURITY.md
│   ├── WORKFLOW.md
│   └── HTTPS_SETUP.md
│
├── 📁 scripts/             # Utility scripts
│   ├── generate-certs.bat
│   └── generate-certs.sh
│
├── 📁 screenshots/         # Development evidence
├── 📁 ai-rules/           # AI assistant rules
│
├── 📄 package.json        # Root dependencies (Playwright E2E tests)
├── 📄 package-lock.json   # Lock file for root dependencies
├── 📄 playwright.config.ts # Playwright E2E test configuration
├── 📄 README.md           # This file
├── 📄 CHANGELOG.md        # Version history
├── 📄 LICENSE             # MIT License
└── 📄 .gitignore          # Git ignore rules
```

For detailed structure, see [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

## 🧪 Testing

### E2E Test Coverage

**33 tests** covering:
- ✅ Homepage navigation (5 tests)
- ✅ Jobs list and filters (7 tests)
- ✅ Job detail page (6 tests)
- ✅ Companies pages (7 tests)
- ✅ Chat widget UI (8 tests)

**Run tests:**
```bash
npm run test:e2e           # Run all tests
npm run test:e2e:ui        # Interactive UI mode
npm run test:e2e:report    # View HTML report
```

## 🔒 Security

### Important: API Keys

**⚠️ NEVER commit API keys to git!**

#### Frontend (.env.local)
```bash
# Get your key from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-key-here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend (.env)
```bash
# Generate secure key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-generated-secret-key
DATABASE_URL=sqlite+aiosqlite:///./jobs.db
```

### If You Accidentally Exposed an API Key

1. **Immediately revoke** the key at https://platform.openai.com/api-keys
2. **Generate a new key** and update your `.env.local`
3. **Clean git history** if the key was committed (see SECURITY.md)

For detailed security guidelines, see [SECURITY.md](docs/SECURITY.md)

## 🌐 HTTPS Support

The application supports HTTPS for secure communication.

### Development HTTPS Setup

```bash
# Generate self-signed certificates
# Windows:
scripts\generate-certs.bat
# Linux/Mac:
./scripts/generate-certs.sh

# Start backend with HTTPS
cd backend
python run_https.py

# Start frontend with HTTPS
cd frontend
npm run dev:https
```

Access at:
- Backend: https://localhost:8000
- Frontend: https://localhost:3000

For production HTTPS setup, see [HTTPS_SETUP.md](docs/HTTPS_SETUP.md)

## 📈 HeadHunter API Integration

### Sync Real Job Data

```bash
cd backend
python sync_hh_vacancies.py
```

**What it does:**
- Fetches real IT vacancies from HeadHunter API
- Saves 150+ jobs from 100+ companies
- Supports multiple search queries (Python, Java, JavaScript, etc.)
- Automatically maps job levels and formats salaries

**Configuration:**
Edit `sync_hh_vacancies.py` to customize:
- Search queries (technologies, roles)
- Geographic area (Kazakhstan, Moscow, etc.)
- Number of pages to fetch
- Results per page

### API Usage Examples

```bash
# Search Python vacancies in Kazakhstan
curl "http://localhost:8000/api/v1/hh/vacancies?text=Python&area_id=40&per_page=10"

# Get vacancy details
curl "http://localhost:8000/api/v1/hh/vacancies/123456"

# List available areas
curl "http://localhost:8000/api/v1/hh/areas"

# List professional roles
curl "http://localhost:8000/api/v1/hh/roles"
```

## 📖 Documentation

- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - Detailed project structure and organization
- **[docs/WORKFLOW.md](docs/WORKFLOW.md)** - Complete development workflow and AI-assisted development process
- **[docs/SECURITY.md](docs/SECURITY.md)** - Security best practices and API key management
- **[docs/HTTPS_SETUP.md](docs/HTTPS_SETUP.md)** - HTTPS configuration for development and production

## 🎯 Development Stats

- **Total Commits:** 23+
- **Files Created:** 60+
- **Lines of Code:** ~5,000+
- **Development Time:** 6-8 hours (with AI assistance)
- **Time Savings:** ~70% compared to manual development
- **E2E Tests:** 33 tests (100% pass rate)

## 🤝 Contributing

This is a solo demonstration project, but pull requests are welcome!

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

**Quick Start:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 👤 Author

**darkhan2409**
- GitHub: [@darkhan2409](https://github.com/darkhan2409)
- Repository: [job-board-solo](https://github.com/darkhan2409/job-board-solo)

## 🙏 Acknowledgments

- **Kiro AI** - AI-assisted development
- **OpenAI** - GPT-4 Turbo model
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework
- **shadcn/ui** - Beautiful UI components
- **Playwright** - E2E testing framework
- **HeadHunter** - Job data API

---

**⭐ If you find this project useful, please give it a star on GitHub!**

**📧 Questions? Create an issue in the repository.**

---

Made with ❤️ and AI in 2025
