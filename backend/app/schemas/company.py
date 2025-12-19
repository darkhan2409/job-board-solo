# app/schemas/company.py
"""
Pydantic schemas for Company model.
Handles request validation and response serialization.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class CompanyBase(BaseModel):
    """Base company schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=200, description="Company name")
    description: Optional[str] = Field(None, description="Company description")
    logo: Optional[str] = Field(None, max_length=500, description="Logo URL")
    website: Optional[str] = Field(None, max_length=500, description="Company website URL")


class CompanyCreate(CompanyBase):
    """
    Schema for creating a new company.
    Inherits all fields from CompanyBase.
    """
    pass


class CompanyResponse(CompanyBase):
    """
    Schema for company response.
    Includes database-generated fields.
    """
    
    id: int = Field(..., description="Company ID")
    
    model_config = {
        "from_attributes": True  # Pydantic V2: Enable ORM mode
    }


class CompanyWithJobs(CompanyResponse):
    """
    Schema for company response with nested jobs.
    Used when fetching company details with all jobs.
    """
    
    jobs: List["JobResponse"] = Field(default_factory=list, description="List of jobs from this company")
    
    model_config = {
        "from_attributes": True
    }


# Import JobResponse for forward reference
from app.schemas.job import JobResponse
CompanyWithJobs.model_rebuild()
