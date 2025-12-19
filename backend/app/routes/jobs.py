# app/routes/jobs.py
"""
Job API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.job_service import JobService
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.models.job import JobLevel
from app.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/jobs", response_model=List[JobResponse])
async def get_jobs(
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
async def get_job(
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
async def create_job(
    job_data: JobCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new job.
    
    Args:
        job_data: Job creation data
        
    Returns:
        Created job with company details
    """
    job = await JobService.create(db, job_data)
    return job


@router.put("/jobs/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing job.
    
    Args:
        job_id: Job ID to update
        job_data: Job update data (partial updates supported)
        
    Returns:
        Updated job with company details
        
    Raises:
        NotFoundException: If job not found
    """
    job = await JobService.update(db, job_id, job_data)
    if not job:
        raise NotFoundException("Job", job_id)
    return job


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a job.
    
    Args:
        job_id: Job ID to delete
        
    Raises:
        NotFoundException: If job not found
    """
    deleted = await JobService.delete(db, job_id)
    if not deleted:
        raise NotFoundException("Job", job_id)
