# app/schemas/saved_job.py
"""
Pydantic schemas for saved job requests and responses.
"""
from datetime import datetime
from pydantic import BaseModel
from app.schemas.job import JobResponse


class SavedJobResponse(BaseModel):
    """Response model for saved job."""
    user_id: int
    job_id: int
    saved_at: datetime
    job: JobResponse  # Include full job details

    model_config = {
        "from_attributes": True
    }


class SavedJobCreate(BaseModel):
    """Request model for saving a job."""
    job_id: int
