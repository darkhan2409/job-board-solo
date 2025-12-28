# app/schemas/application.py
"""
Pydantic schemas for job application requests and responses.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.application import ApplicationStatus
from app.schemas.job import JobResponse


class ApplicationBase(BaseModel):
    """Base application model."""
    cover_letter: Optional[str] = Field(None, max_length=5000)
    resume_url: Optional[str] = Field(None, max_length=500)


class ApplicationCreate(ApplicationBase):
    """Request model for creating an application."""
    job_id: int


class ApplicationUpdate(BaseModel):
    """Request model for updating application status (employer only)."""
    status: ApplicationStatus


class ApplicationResponse(ApplicationBase):
    """Response model for application."""
    id: int
    user_id: int
    job_id: int
    status: ApplicationStatus
    applied_at: datetime
    updated_at: datetime
    job: JobResponse  # Include full job details

    model_config = {
        "from_attributes": True
    }


class ApplicationWithoutJob(ApplicationBase):
    """Response model for application without job details (for job employer view)."""
    id: int
    user_id: int
    job_id: int
    status: ApplicationStatus
    applied_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
