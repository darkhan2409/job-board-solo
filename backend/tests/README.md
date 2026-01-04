# Backend Tests

This directory contains all tests for the Job Board API backend.

## Test Structure

```
tests/
├── __init__.py
├── test_cors_configuration.py      # CORS configuration tests
├── test_email_verification.py      # Email verification tests
├── test_email_verification_complete.py  # Complete email verification flow
├── test_oauth_csrf.py              # OAuth CSRF protection tests
├── test_rate_limiting.py           # Rate limiting tests
└── test_security_fix.py            # Security fixes tests
```

## Running Tests

### Run all tests
```bash
npm test
# or
pytest tests/
```

### Run tests with verbose output
```bash
npm run test:verbose
# or
pytest tests/ -v
```

### Run tests with coverage
```bash
npm run test:coverage
# or
pytest tests/ --cov=app --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_cors_configuration.py
```

### Run specific test function
```bash
pytest tests/test_cors_configuration.py::TestCORSConfiguration::test_cors_allowed_origin_http
```

## Test Categories

Tests are organized by functionality:

- **CORS Tests** (`test_cors_configuration.py`): Verify Cross-Origin Resource Sharing configuration
- **Email Tests** (`test_email_verification*.py`): Verify email verification and change flows
- **OAuth Tests** (`test_oauth_csrf.py`): Verify OAuth CSRF protection
- **Rate Limiting Tests** (`test_rate_limiting.py`): Verify API rate limiting
- **Security Tests** (`test_security_fix.py`): Verify security fixes and protections

## Writing New Tests

When adding new tests:

1. Create test file with `test_` prefix: `test_feature_name.py`
2. Use descriptive test function names: `test_feature_does_something()`
3. Group related tests in classes: `class TestFeatureName:`
4. Add docstrings to explain what is being tested
5. Use pytest fixtures for common setup/teardown

Example:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMyFeature:
    """Test suite for my feature."""
    
    def test_feature_works(self):
        """Test that feature works correctly."""
        response = client.get("/api/endpoint")
        assert response.status_code == 200
```

## Dependencies

Tests require:
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `httpx` - HTTP client for FastAPI TestClient

Install test dependencies:
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```
