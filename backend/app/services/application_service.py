# app/services/application_service.py
"""
Application service for managing job applications.
"""
import logging
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.application import Application, ApplicationStatus
from app.models.job import Job
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from app.utils.exceptions import NotFoundException, ConflictException

logger = logging.getLogger(__name__)


class ApplicationService:
    """Service for managing job applications."""

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        application_id: int
    ) -> Optional[Application]:
        """
        Get an application by ID.

        Args:
            db: Database session
            application_id: Application ID

        Returns:
            Application if found, None otherwise
        """
        stmt = (
            select(Application)
            .options(
                joinedload(Application.job).joinedload(Job.company),
                joinedload(Application.user)
            )
            .where(Application.id == application_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_applications(
        db: AsyncSession,
        user_id: int,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Application]:
        """
        Get all applications by a user.

        Args:
            db: Database session
            user_id: User ID
            status: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of applications with job details
        """
        stmt = (
            select(Application)
            .options(joinedload(Application.job).joinedload(Job.company))
            .where(Application.user_id == user_id)
        )

        if status:
            stmt = stmt.where(Application.status == status)

        stmt = stmt.order_by(Application.applied_at.desc()).offset(skip).limit(limit)

        result = await db.execute(stmt)
        return list(result.scalars().unique().all())

    @staticmethod
    async def get_job_applications(
        db: AsyncSession,
        job_id: int,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Application]:
        """
        Get all applications for a job.

        Args:
            db: Database session
            job_id: Job ID
            status: Optional status filter
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of applications
        """
        stmt = select(Application).where(Application.job_id == job_id)

        if status:
            stmt = stmt.where(Application.status == status)

        stmt = stmt.order_by(Application.applied_at.desc()).offset(skip).limit(limit)

        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def has_applied(
        db: AsyncSession,
        user_id: int,
        job_id: int
    ) -> bool:
        """
        Check if a user has already applied to a job.

        Args:
            db: Database session
            user_id: User ID
            job_id: Job ID

        Returns:
            True if user has applied, False otherwise
        """
        stmt = select(Application).where(
            and_(
                Application.user_id == user_id,
                Application.job_id == job_id
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def create(
        db: AsyncSession,
        user_id: int,
        application_data: ApplicationCreate
    ) -> Application:
        """
        Create a new job application.

        Args:
            db: Database session
            user_id: User ID
            application_data: Application creation data

        Returns:
            Created application

        Raises:
            NotFoundException: If job not found
            ConflictException: If user already applied to this job
        """
        # Check if job exists
        job_stmt = select(Job).where(Job.id == application_data.job_id)
        job_result = await db.execute(job_stmt)
        job = job_result.scalar_one_or_none()
        if not job:
            raise NotFoundException("Job", application_data.job_id)

        # Check if already applied
        has_applied = await ApplicationService.has_applied(
            db, user_id, application_data.job_id
        )
        if has_applied:
            raise ConflictException(
                f"You have already applied to job {application_data.job_id}"
            )

        # Create application
        application = Application(
            user_id=user_id,
            job_id=application_data.job_id,
            cover_letter=application_data.cover_letter,
            resume_url=application_data.resume_url,
            status=ApplicationStatus.PENDING
        )
        db.add(application)
        await db.flush()

        # Reload with job details
        await db.refresh(application, ["job"])
        await db.refresh(application.job, ["company"])

        logger.info(f"User {user_id} applied to job {application_data.job_id}")
        return application

    @staticmethod
    async def update_status(
        db: AsyncSession,
        application_id: int,
        status_update: ApplicationUpdate
    ) -> Optional[Application]:
        """
        Update application status (employer only).

        Args:
            db: Database session
            application_id: Application ID
            status_update: New status

        Returns:
            Updated application if found, None otherwise
        """
        application = await ApplicationService.get_by_id(db, application_id)
        if not application:
            return None

        application.status = status_update.status
        await db.flush()
        await db.refresh(application)

        logger.info(
            f"Application {application_id} status updated to {status_update.status}"
        )
        return application

    @staticmethod
    async def withdraw(
        db: AsyncSession,
        application_id: int,
        user_id: int
    ) -> Optional[Application]:
        """
        Withdraw an application (user only).

        Args:
            db: Database session
            application_id: Application ID
            user_id: User ID (for ownership check)

        Returns:
            Updated application if found and owned by user, None otherwise
        """
        application = await ApplicationService.get_by_id(db, application_id)
        if not application or application.user_id != user_id:
            return None

        application.status = ApplicationStatus.WITHDRAWN
        await db.flush()
        await db.refresh(application)

        logger.info(f"User {user_id} withdrew application {application_id}")
        return application
