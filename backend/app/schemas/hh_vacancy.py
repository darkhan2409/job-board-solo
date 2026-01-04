"""
Pydantic models for HeadHunter API responses
"""
from typing import Optional
from pydantic import BaseModel, Field


class HHSalary(BaseModel):
    """Salary information from HH API"""
    from_: Optional[int] = Field(None, alias="from")
    to: Optional[int] = None
    currency: Optional[str] = None
    gross: Optional[bool] = None


class HHEmployer(BaseModel):
    """Employer information from HH API"""
    id: str
    name: str
    url: Optional[str] = None
    alternate_url: Optional[str] = None
    logo_urls: Optional[dict] = None


class HHSnippet(BaseModel):
    """Snippet with vacancy highlights"""
    requirement: Optional[str] = None
    responsibility: Optional[str] = None


class HHVacancy(BaseModel):
    """
    HeadHunter vacancy model
    Contains only essential fields for job board aggregation
    """
    id: str
    name: str
    salary: Optional[HHSalary] = None
    employer: HHEmployer
    snippet: Optional[HHSnippet] = None
    alternate_url: str = Field(..., description="URL to vacancy on hh.ru")
    
    class Config:
        populate_by_name = True


class HHVacanciesResponse(BaseModel):
    """Response from HH API vacancies search"""
    items: list[HHVacancy]
    found: int
    pages: int
    per_page: int
    page: int
