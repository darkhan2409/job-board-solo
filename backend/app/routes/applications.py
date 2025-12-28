# app/routes/applications.py
"""
Job application API endpoints.
"""
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.application_service import ApplicationService
from app.services.job_service import JobService
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithoutJob
)
from app.schemas.user import UserResponse
from app.models.user import UserRole
from app.models.application import ApplicationStatus
from app.utils.exceptions import NotFoundException
from app.utils.dependencies import get_current_active_user

router = APIRouter()


@router.get("/applications/me", response_model=List[ApplicationResponse])
async def get_my_applications(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status_filter: Optional[ApplicationStatus] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get all applications submitted by the current user.

    Args:
        current_user: Authenticated user
        status_filter: Optional status filter
        skip: Pagination offset
        limit: Maximum number of results

    Returns:
        List of applications with job details
    """
    applications = await ApplicationService.get_user_applications(
        db,
        user_id=current_user.id,
        status=status_filter,
        skip=skip,
        limit=limit
    )
    return applications


@router.get("/jobs/{job_id}/applications", response_model=List[ApplicationWithoutJob])
async def get_job_applications(
    job_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status_filter: Optional[ApplicationStatus] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get all applications for a job (employer/admin only).

    Employers can only see applications for jobs they created.
    Admins can see all applications.

    Args:
        job_id: Job ID
        current_user: Authenticated user (must be job creator or admin)
        status_filter: Optional status filter
        skip: Pagination offset
        limit: Maximum number of results

    Returns:
        List of applications for the job

    Raises:
        NotFoundException: If job not found
        HTTPException: If user doesn't have permission
    """
    # Check if job exists and user has permission
    job = await JobService.get_by_id(db, job_id)
    if not job:
        raise NotFoundException("Job", job_id)

    # Check permission: must be job creator or admin
    if current_user.role != UserRole.ADMIN and job.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view applications for this job"
        )

    applications = await ApplicationService.get_job_applications(
        db,
        job_id=job_id,
        status=status_filter,
        skip=skip,
        limit=limit
    )
    return applications


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Get a specific application by ID.

    Users can only view their own applications.
    Employers can view applications for their jobs.
    Admins can view all applications.

    Args:
        application_id: Application ID
        current_user: Authenticated user

    Returns:
        Application details

    Raises:
        NotFoundException: If application not found
        HTTPException: If user doesn't have permission
    """
    application = await ApplicationService.get_by_id(db, application_id)
    if not application:
        raise NotFoundException("Application", application_id)

    # Check permission
    is_applicant = application.user_id == current_user.id
    is_job_owner = application.job.created_by_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN

    if not (is_applicant or is_job_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this application"
        )

    return application


@router.post(
    "/applications",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_application(
    application_data: ApplicationCreate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Submit a job application.

    Args:
        application_data: Application details
        current_user: Authenticated user

    Returns:
        Created application with job details

    Raises:
        NotFoundException: If job not found
        ConflictException: If user already applied to this job
    """
    application = await ApplicationService.create(
        db,
        user_id=current_user.id,
        application_data=application_data
    )
    return application


@router.patch("/applications/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: int,
    status_update: ApplicationUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Update application status (employer/admin only).

    Employers can only update applications for jobs they created.
    Admins can update any application.

    Args:
        application_id: Application ID
        status_update: New status
        current_user: Authenticated user (must be job creator or admin)

    Returns:
        Updated application

    Raises:
        NotFoundException: If application not found
        HTTPException: If user doesn't have permission
    """
    application = await ApplicationService.get_by_id(db, application_id)
    if not application:
        raise NotFoundException("Application", application_id)

    # Check permission: must be job creator or admin
    is_job_owner = application.job.created_by_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN

    if not (is_job_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this application"
        )

    updated_application = await ApplicationService.update_status(
        db,
        application_id=application_id,
        status_update=status_update
    )
    return updated_application


@router.post("/applications/{application_id}/withdraw", response_model=ApplicationResponse)
async def withdraw_application(
    application_id: int,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Withdraw an application (applicant only).

    Users can only withdraw their own applications.

    Args:
        application_id: Application ID
        current_user: Authenticated user (must be application owner)

    Returns:
        Updated application with withdrawn status

    Raises:
        NotFoundException: If application not found or not owned by user
    """
    application = await ApplicationService.withdraw(
        db,
        application_id=application_id,
        user_id=current_user.id
    )
    if not application:
        raise NotFoundException("Application", application_id)

    return application
