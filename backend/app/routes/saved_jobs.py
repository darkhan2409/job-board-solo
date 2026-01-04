# app/routes/saved_jobs.py
"""
Saved jobs API endpoints for authenticated users.
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, Request, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.saved_job_service import SavedJobService
from app.schemas.saved_job import SavedJobResponse, SavedJobCreate
from app.schemas.user import UserResponse
from app.models.user import UserRole
from app.utils.exceptions import NotFoundException, ConflictException
from app.utils.dependencies import get_current_active_user
from app.utils.rate_limit import limiter
from app.config import settings

router = APIRouter()


@router.get("/saved-jobs", response_model=List[SavedJobResponse])
@limiter.limit(settings.API_RATE_LIMIT)
async def get_saved_jobs(
    request: Request,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records")
):
    """
    Get all saved jobs for the current user.

    Args:
        current_user: Authenticated user
        skip: Pagination offset
        limit: Maximum number of results

    Returns:
        List of saved jobs with full job details
    """
    saved_jobs = await SavedJobService.get_user_saved_jobs(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return saved_jobs


@router.get("/saved-jobs/{job_id}/check")
@limiter.limit(settings.API_RATE_LIMIT)
async def check_job_saved(
    request: Request,
    job_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Check if a job is saved by the current user.

    Args:
        job_id: Job ID to check
        current_user: Authenticated user

    Returns:
        Object with is_saved boolean
    """
    is_saved = await SavedJobService.is_job_saved(
        db,
        user_id=current_user.id,
        job_id=job_id
    )
    return {"is_saved": is_saved}


@router.post(
    "/saved-jobs",
    response_model=SavedJobResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("30/minute")  # Moderate limit for saving jobs
async def save_job(
    request: Request,
    save_data: SavedJobCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Save a job for the current user.

    Args:
        save_data: Job ID to save
        current_user: Authenticated user

    Returns:
        Created saved job with full job details

    Raises:
        NotFoundException: If job not found
        ConflictException: If job already saved
    """
    saved_job = await SavedJobService.save_job(
        db,
        user_id=current_user.id,
        job_id=save_data.job_id
    )
    return saved_job


@router.delete("/saved-jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")  # Moderate limit for unsaving jobs
async def unsave_job(
    request: Request,
    job_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Remove a saved job for the current user.

    Args:
        job_id: Job ID to unsave
        current_user: Authenticated user

    Raises:
        NotFoundException: If saved job not found
    """
    deleted = await SavedJobService.unsave_job(
        db,
        user_id=current_user.id,
        job_id=job_id
    )
    if not deleted:
        raise NotFoundException("Saved job", job_id)
