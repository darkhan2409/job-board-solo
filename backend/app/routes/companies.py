# app/routes/companies.py
"""
Company API endpoints with RBAC protection.
"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.company_service import CompanyService
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyWithJobs
from app.schemas.user import UserResponse
from app.models.user import UserRole
from app.utils.exceptions import NotFoundException
from app.utils.dependencies import require_role
from app.utils.rate_limit import limiter
from app.config import settings

router = APIRouter()


@router.get("/companies", response_model=List[CompanyResponse])
@limiter.limit(settings.API_RATE_LIMIT)
async def get_companies(
    request: Request,
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
@limiter.limit(settings.API_RATE_LIMIT)
async def get_company(
    request: Request,
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
@limiter.limit("10/minute")  # Stricter limit for company creation
async def create_company(
    request: Request,
    company_data: CompanyCreate,
    current_user: Annotated[UserResponse, Depends(require_role([UserRole.EMPLOYER, UserRole.ADMIN]))],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Create a new company (requires EMPLOYER or ADMIN role).

    Args:
        company_data: Company creation data
        current_user: Authenticated user (EMPLOYER or ADMIN)

    Returns:
        Created company
    """
    company = await CompanyService.create(db, company_data, managed_by_id=current_user.id)
    return company
