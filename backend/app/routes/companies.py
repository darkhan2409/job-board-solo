# app/routes/companies.py
"""
Company API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.company_service import CompanyService
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyWithJobs
from app.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/companies", response_model=List[CompanyResponse])
async def get_companies(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all companies.
    
    Returns:
        List of all companies
    """
    companies = await CompanyService.get_all(db)
    return companies


@router.get("/companies/{company_id}", response_model=CompanyWithJobs)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get company by ID with all jobs.
    
    Args:
        company_id: Company ID
        
    Returns:
        Company with all jobs
        
    Raises:
        NotFoundException: If company not found
    """
    company = await CompanyService.get_by_id(db, company_id)
    if not company:
        raise NotFoundException("Company", company_id)
    return company


@router.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new company.
    
    Args:
        company_data: Company creation data
        
    Returns:
        Created company
    """
    company = await CompanyService.create(db, company_data)
    return company
