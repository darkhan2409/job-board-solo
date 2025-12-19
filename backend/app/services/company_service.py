# app/services/company_service.py
"""
Company service layer - business logic for company operations.
All database queries for companies happen here.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.company import Company
from app.schemas.company import CompanyCreate


class CompanyService:
    """Service class for company-related operations."""
    
    @staticmethod
    async def get_all(db: AsyncSession) -> List[Company]:
        """
        Get all companies.
        
        Args:
            db: Database session
            
        Returns:
            List of all companies
        """
        result = await db.execute(select(Company))
        return list(result.scalars().all())
    
    @staticmethod
    async def get_by_id(db: AsyncSession, company_id: int) -> Optional[Company]:
        """
        Get company by ID with all jobs.
        
        Args:
            db: Database session
            company_id: Company ID
            
        Returns:
            Company with jobs or None if not found
        """
        result = await db.execute(
            select(Company)
            .where(Company.id == company_id)
            .options(selectinload(Company.jobs))
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, company_data: CompanyCreate) -> Company:
        """
        Create a new company.
        
        Args:
            db: Database session
            company_data: Company creation data
            
        Returns:
            Created company
        """
        company = Company(**company_data.model_dump())
        db.add(company)
        await db.flush()
        await db.refresh(company)
        return company
