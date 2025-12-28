# app/services/job_service.py
"""
Job service layer - business logic for job operations.
All database queries for jobs happen here.
"""

from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.job import Job, JobLevel
from app.schemas.job import JobCreate, JobUpdate


class JobService:
    """Service class for job-related operations."""
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        location: Optional[str] = None,
        level: Optional[JobLevel] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Job]:
        """
        Get all jobs with optional filters and pagination.
        
        Args:
            db: Database session
            location: Filter by location
            level: Filter by seniority level
            search: Search in title and description
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of jobs matching filters
        """
        query = select(Job).options(selectinload(Job.company))
        
        # Apply filters
        if location:
            query = query.where(Job.location.ilike(f"%{location}%"))
        
        if level:
            query = query.where(Job.level == level)
        
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                or_(
                    Job.title.ilike(search_pattern),
                    Job.description.ilike(search_pattern)
                )
            )
        
        # Apply pagination and ordering
        query = query.order_by(Job.created_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def get_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
        """
        Get job by ID with company information.
        
        Args:
            db: Database session
            job_id: Job ID
            
        Returns:
            Job with company or None if not found
        """
        result = await db.execute(
            select(Job)
            .where(Job.id == job_id)
            .options(selectinload(Job.company))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create(
        db: AsyncSession,
        job_data: JobCreate,
        created_by_id: Optional[int] = None
    ) -> Job:
        """
        Create a new job.

        Args:
            db: Database session
            job_data: Job creation data
            created_by_id: ID of user creating the job (optional)

        Returns:
            Created job
        """
        job_dict = job_data.model_dump()
        if created_by_id is not None:
            job_dict["created_by_id"] = created_by_id

        job = Job(**job_dict)
        db.add(job)
        await db.flush()
        await db.refresh(job, ["company"])
        return job
    
    @staticmethod
    async def update(
        db: AsyncSession,
        job_id: int,
        job_data: JobUpdate
    ) -> Optional[Job]:
        """
        Update an existing job.
        
        Args:
            db: Database session
            job_id: Job ID to update
            job_data: Job update data
            
        Returns:
            Updated job or None if not found
        """
        job = await JobService.get_by_id(db, job_id)
        if not job:
            return None
        
        # Update only provided fields
        update_data = job_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        await db.flush()
        await db.refresh(job, ["company"])
        return job
    
    @staticmethod
    async def delete(db: AsyncSession, job_id: int) -> bool:
        """
        Delete a job.
        
        Args:
            db: Database session
            job_id: Job ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        job = await JobService.get_by_id(db, job_id)
        if not job:
            return False
        
        await db.delete(job)
        await db.flush()
        return True
