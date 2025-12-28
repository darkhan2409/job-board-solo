# app/services/saved_job_service.py
"""
Saved job service for managing user's saved/bookmarked jobs.
"""
import logging
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.saved_job import SavedJob
from app.models.job import Job
from app.utils.exceptions import NotFoundException, ConflictException

logger = logging.getLogger(__name__)


class SavedJobService:
    """Service for managing saved jobs."""

    @staticmethod
    async def get_user_saved_jobs(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[SavedJob]:
        """
        Get all saved jobs for a user.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of saved jobs with job details
        """
        stmt = (
            select(SavedJob)
            .options(joinedload(SavedJob.job).joinedload(Job.company))
            .where(SavedJob.user_id == user_id)
            .order_by(SavedJob.saved_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    @staticmethod
    async def is_job_saved(
        db: AsyncSession,
        user_id: int,
        job_id: int
    ) -> bool:
        """
        Check if a job is saved by a user.

        Args:
            db: Database session
            user_id: User ID
            job_id: Job ID

        Returns:
            True if job is saved, False otherwise
        """
        stmt = select(SavedJob).where(
            and_(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def save_job(
        db: AsyncSession,
        user_id: int,
        job_id: int
    ) -> SavedJob:
        """
        Save a job for a user.

        Args:
            db: Database session
            user_id: User ID
            job_id: Job ID

        Returns:
            Created saved job

        Raises:
            NotFoundException: If job not found
            ConflictException: If job already saved
        """
        # Check if job exists
        job_stmt = select(Job).where(Job.id == job_id)
        job_result = await db.execute(job_stmt)
        job = job_result.scalar_one_or_none()
        if not job:
            raise NotFoundException("Job", job_id)

        # Check if already saved
        is_saved = await SavedJobService.is_job_saved(db, user_id, job_id)
        if is_saved:
            raise ConflictException(f"Job {job_id} is already saved")

        # Create saved job
        saved_job = SavedJob(user_id=user_id, job_id=job_id)
        db.add(saved_job)
        await db.flush()

        # Reload with job details
        await db.refresh(saved_job, ["job"])
        await db.refresh(saved_job.job, ["company"])

        logger.info(f"User {user_id} saved job {job_id}")
        return saved_job

    @staticmethod
    async def unsave_job(
        db: AsyncSession,
        user_id: int,
        job_id: int
    ) -> bool:
        """
        Remove a saved job for a user.

        Args:
            db: Database session
            user_id: User ID
            job_id: Job ID

        Returns:
            True if deleted, False if not found
        """
        stmt = select(SavedJob).where(
            and_(
                SavedJob.user_id == user_id,
                SavedJob.job_id == job_id
            )
        )
        result = await db.execute(stmt)
        saved_job = result.scalar_one_or_none()

        if not saved_job:
            return False

        await db.delete(saved_job)
        await db.flush()

        logger.info(f"User {user_id} unsaved job {job_id}")
        return True
