# Contributing to Job Board Solo

Thank you for your interest in contributing to Job Board Solo! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)

## 🤝 Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 16+
- Git
- OpenAI API key (for AI features)

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/job-board-solo.git
   cd job-board-solo
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your settings
   python seed_data.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your OpenAI API key
   ```

4. **Run Tests**
   ```bash
   # From project root
   npm install
   npx playwright install
   npm run test:e2e
   ```

## 🔄 Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch (create PRs here)
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in your feature branch
2. Write or update tests as needed
3. Update documentation if required
4. Ensure all tests pass
5. Commit your changes following commit guidelines

## 📝 Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for classes and functions
- Keep functions small and focused
- Use async/await for I/O operations

**Example:**
```python
async def get_job_by_id(job_id: int) -> Optional[Job]:
    """
    Retrieve a job by its ID.
    
    Args:
        job_id: The unique identifier of the job
        
    Returns:
        Job object if found, None otherwise
    """
    async with get_session() as session:
        result = await session.get(Job, job_id)
        return result
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Define interfaces for data structures
- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names

**Example:**
```typescript
interface JobCardProps {
  job: Job;
  onSave?: (jobId: number) => void;
}

export function JobCard({ job, onSave }: JobCardProps) {
  // Component implementation
}
```

### File Naming

- **Backend:** `snake_case.py`
- **Frontend Components:** `PascalCase.tsx`
- **Frontend Utilities:** `camelCase.ts`
- **Tests:** `kebab-case.spec.ts`
- **Documentation:** `SCREAMING_SNAKE_CASE.md`

## 💬 Commit Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Examples

```bash
feat(backend): add job filtering by salary range

Implement salary range filtering in jobs API endpoint.
Supports min and max salary parameters.

Closes #123
```

```bash
fix(frontend): resolve chat widget scroll issue

Fixed scroll behavior in chat widget when new messages arrive.
Widget now automatically scrolls to bottom on new messages.
```

```bash
docs: update HTTPS setup guide

Added instructions for production deployment with Let's Encrypt.
```

## 🔀 Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout your-feature-branch
   git rebase develop
   ```

2. **Run tests**
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests (if any)
   cd frontend
   npm test

   # E2E tests
   npm run test:e2e
   ```

3. **Check code quality**
   ```bash
   # Backend
   cd backend
   flake8 app/
   mypy app/

   # Frontend
   cd frontend
   npm run lint
   ```

### Submitting PR

1. Push your branch to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create Pull Request on GitHub
   - Base: `develop`
   - Compare: `your-feature-branch`

3. Fill out PR template:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if UI changes)

### PR Review Process

- At least one approval required
- All tests must pass
- No merge conflicts
- Code follows project standards
- Documentation updated if needed

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
pytest tests/test_jobs.py  # Specific test file
pytest -v  # Verbose output
```

### Frontend Tests

```bash
cd frontend
npm test
npm test -- --watch  # Watch mode
```

### E2E Tests

```bash
# Run all tests
npm run test:e2e

# Run specific test
npx playwright test tests/e2e/jobs.spec.ts

# UI mode (interactive)
npm run test:e2e:ui

# Debug mode
npx playwright test --debug
```

### Writing Tests

#### Backend Test Example
```python
import pytest
from app.models import Job

@pytest.mark.asyncio
async def test_create_job(client):
    """Test job creation endpoint."""
    response = await client.post(
        "/api/jobs",
        json={
            "title": "Python Developer",
            "company_id": 1,
            "location": "Remote"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Developer"
```

#### E2E Test Example
```typescript
import { test, expect } from '@playwright/test';

test('should display job list', async ({ page }) => {
  await page.goto('http://localhost:3000/jobs');
  
  await expect(page.locator('h1')).toContainText('Jobs');
  await expect(page.locator('[data-testid="job-card"]')).toHaveCount(10);
});
```

## 📚 Documentation

### When to Update Documentation

- Adding new features
- Changing API endpoints
- Modifying configuration
- Adding dependencies
- Changing project structure

### Documentation Files

- `README.md` - Main project documentation
- `docs/PROJECT_STRUCTURE.md` - Project organization
- `docs/SECURITY.md` - Security guidelines
- `docs/WORKFLOW.md` - Development process
- `docs/HTTPS_SETUP.md` - HTTPS configuration
- `backend/README.md` - Backend specifics
- `frontend/README.md` - Frontend specifics

### API Documentation

Update OpenAPI/Swagger docs when changing API:
- Add docstrings to route functions
- Define request/response schemas
- Include example requests/responses

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify it's reproducible
3. Test on latest version

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11]
- Python: [e.g., 3.11]
- Node: [e.g., 16.14]
- Browser: [e.g., Chrome 120]

**Screenshots**
If applicable
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives**
Other solutions considered

**Additional Context**
Any other information
```

## 🎯 Good First Issues

Look for issues labeled:
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `documentation` - Documentation improvements

## 📞 Getting Help

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** Create an issue instead

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Job Board Solo! 🚀
