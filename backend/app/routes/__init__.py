# app/routes/__init__.py
"""
API routes package.
"""

from app.routes.jobs import router as jobs_router
from app.routes.companies import router as companies_router
from app.routes.auth import router as auth_router
from app.routes.saved_jobs import router as saved_jobs_router
from app.routes.applications import router as applications_router

__all__ = [
    "jobs_router",
    "companies_router",
    "auth_router",
    "saved_jobs_router",
    "applications_router",
]
