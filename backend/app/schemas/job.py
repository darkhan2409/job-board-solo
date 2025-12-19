# app/schemas/job.py
"""
Pydantic schemas for Job model.
Handles request validation, response serialization, and filtering.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.job import JobLevel


class JobBase(BaseModel):
    """Base job schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Job title")
    description: str = Field(..., min_length=1, description="Job description")
    location: str = Field(..., min_length=1, max_length=200, description="Job location")
    salary: Optional[str] = Field(None, max_length=100, description="Salary range")
    level: JobLevel = Field(..., description="Seniority level")


class JobCreate(JobBase):
    """
    Schema for creating a new job.
    Requires company_id to associate with a company.
    """
    
    company_id: int = Field(..., gt=0, description="Company ID")


class JobUpdate(BaseModel):
    """
    Schema for updating a job.
    All fields are optional for partial updates.
    """
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    salary: Optional[str] = Field(None, max_length=100)
    level: Optional[JobLevel] = None
    company_id: Optional[int] = Field(None, gt=0)


class JobResponse(JobBase):
    """
    Schema for job response.
    Includes database-generated fields and nested company info.
    """
    
    id: int = Field(..., description="Job ID")
    company_id: int = Field(..., description="Company ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    company: "CompanyResponse" = Field(..., description="Company information")
    
    model_config = {
        "from_attributes": True  # Pydantic V2: Enable ORM mode
    }


class JobFilters(BaseModel):
    """
    Schema for job filtering and pagination.
    Used as query parameters in GET /api/jobs endpoint.
    """
    
    location: Optional[str] = Field(None, description="Filter by location")
    level: Optional[JobLevel] = Field(None, description="Filter by seniority level")
    search: Optional[str] = Field(None, description="Search in title and description")
    skip: int = Field(0, ge=0, description="Number of records to skip (pagination)")
    limit: int = Field(100, ge=1, le=100, description="Maximum number of records to return")


# Import CompanyResponse for forward reference
from app.schemas.company import CompanyResponse
JobResponse.model_rebuild()
