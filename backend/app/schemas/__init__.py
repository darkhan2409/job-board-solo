# app/schemas/__init__.py
"""
Pydantic schemas package for request/response validation.
"""

from app.schemas.company import (
    CompanyBase,
    CompanyCreate,
    CompanyResponse,
    CompanyWithJobs
)
from app.schemas.job import (
    JobBase,
    JobCreate,
    JobUpdate,
    JobResponse,
    JobFilters
)

__all__ = [
    "CompanyBase",
    "CompanyCreate",
    "CompanyResponse",
    "CompanyWithJobs",
    "JobBase",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "JobFilters"
]
