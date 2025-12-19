# app/routes/__init__.py
"""
API routes package.
"""

from app.routes.jobs import router as jobs_router
from app.routes.companies import router as companies_router

__all__ = ["jobs_router", "companies_router"]
