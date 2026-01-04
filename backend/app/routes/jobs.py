# app/routes/jobs.py
"""
Job API endpoints with RBAC protection.
"""

from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.job_service import JobService
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.schemas.user import UserResponse
from app.models.job import JobLevel
from app.models.user import UserRole
from app.utils.exceptions import NotFoundException
from app.utils.dependencies import get_current_active_user, require_role
from app.utils.rate_limit import limiter
from app.config import settings

router = APIRouter()


@router.get("/jobs", response_model=List[JobResponse])
# @limiter.limit(settings.SEARCH_RATE_LIMIT)  # Temporarily disabled for debugging
async def get_jobs(
    request: Request,
    location: Optional[str] = Query(None, description="Filter by location"),
    level: Optional[JobLevel] = Query(None, description="Filter by seniority level"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all jobs with optional filters and pagination.
    
    Query Parameters:
        - location: Filter by location (partial match)
        - level: Filter by seniority level (junior, middle, senior, lead)
        - search: Search in job title and description
        - skip: Pagination offset (default: 0)
        - limit: Maximum results (default: 100, max: 100)
        
    Returns:
        List of jobs matching filters
    """
    jobs = await JobService.get_all(
        db=db,
        location=location,
        level=level,
        search=search,
        skip=skip,
        limit=limit
    )
    return jobs


@router.get("/jobs/{job_id}", response_model=JobResponse)
@limiter.limit(settings.API_RATE_LIMIT)
async def get_job(
    request: Request,
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get job by ID with company information.
    
    Args:
        job_id: Job ID
        
    Returns:
        Job with company details
        
    Raises:
        NotFoundException: If job not found
    """
    job = await JobService.get_by_id(db, job_id)
    if not job:
        raise NotFoundException("Job", job_id)
    return job


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")  # Stricter limit for job creation
async def create_job(
    request: Request,
    job_data: JobCreate,
    current_user: Annotated[UserResponse, Depends(require_role([UserRole.EMPLOYER, UserRole.ADMIN]))],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Create a new job (requires EMPLOYER or ADMIN role).

    Args:
        job_data: Job creation data
        current_user: Authenticated user (EMPLOYER or ADMIN)

    Returns:
        Created job with company details
    """
    job = await JobService.create(db, job_data, created_by_id=current_user.id)
    return job


@router.put("/jobs/{job_id}", response_model=JobResponse)
@limiter.limit("20/minute")  # Moderate limit for updates
async def update_job(
    request: Request,
    job_id: int,
    job_data: JobUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update an existing job (requires ownership or ADMIN role).

    Args:
        job_id: Job ID to update
        job_data: Job update data (partial updates supported)
        current_user: Authenticated user

    Returns:
        Updated job with company details

    Raises:
        NotFoundException: If job not found
        HTTPException: If user doesn't have permission
    """
    # Get existing job
    existing_job = await JobService.get_by_id(db, job_id)
    if not existing_job:
        raise NotFoundException("Job", job_id)

    # Check ownership (allow creator or admin to update)
    if current_user.role != UserRole.ADMIN and existing_job.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this job"
        )

    job = await JobService.update(db, job_id, job_data)
    return job


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")  # Stricter limit for deletion
async def delete_job(
    request: Request,
    job_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Delete a job (requires ownership or ADMIN role).

    Args:
        job_id: Job ID to delete
        current_user: Authenticated user

    Raises:
        NotFoundException: If job not found
        HTTPException: If user doesn't have permission
    """
    # Get existing job
    existing_job = await JobService.get_by_id(db, job_id)
    if not existing_job:
        raise NotFoundException("Job", job_id)

    # Check ownership (allow creator or admin to delete)
    if current_user.role != UserRole.ADMIN and existing_job.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this job"
        )

    deleted = await JobService.delete(db, job_id)
    if not deleted:
        raise NotFoundException("Job", job_id)
