"""
HeadHunter Vacancies API Routes
Endpoints for searching and fetching vacancies from HH.ru
"""
from fastapi import APIRouter, HTTPException, Query, Request
from typing import Optional
import logging

from app.services.hh_client import (
    HHService,
    HHAPIError,
    HHRateLimitError,
    HHForbiddenError
)
from app.schemas.hh_vacancy import HHVacanciesResponse
from app.utils.rate_limit import limiter
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/hh/vacancies", response_model=HHVacanciesResponse)
@limiter.limit(settings.SEARCH_RATE_LIMIT)  # Stricter limit for external API calls
async def search_hh_vacancies(
    request: Request,
    text: str = Query(..., description="Search query (e.g., 'Python', 'Java Developer')"),
    role_id: str = Query("96", description="Professional role ID (96 = Programmer/Developer)"),
    area_id: int = Query(40, description="Area ID (40 = Kazakhstan, 1 = Moscow, 113 = Russia)"),
    per_page: int = Query(20, ge=1, le=100, description="Results per page (max 100)"),
    page: int = Query(0, ge=0, description="Page number (starts from 0)"),
    order_by: str = Query(
        "publication_time",
        description="Sort order: publication_time, salary_desc, salary_asc, relevance"
    )
):
    """
    Search for IT vacancies on HeadHunter
    
    This endpoint aggregates vacancies from hh.ru API with filters for:
    - Search text (job title, skills)
    - Professional role (default: Programmer/Developer)
    - Geographic area (default: Kazakhstan)
    - Pagination and sorting
    
    Returns:
        List of vacancies with essential information
    
    Raises:
        429: Rate limit exceeded
        403: Access forbidden (check User-Agent)
        500: Internal server error
    """
    try:
        async with HHService() as hh_client:
            response = await hh_client.get_vacancies(
                text=text,
                role_id=role_id,
                area_id=area_id,
                per_page=per_page,
                page=page,
                order_by=order_by
            )
            
            logger.info(
                f"Successfully fetched {len(response.items)} vacancies "
                f"for query: {text}, area: {area_id}"
            )
            
            return response
    
    except HHRateLimitError as e:
        logger.error(f"Rate limit exceeded: {e}")
        raise HTTPException(
            status_code=429,
            detail="Too many requests to HeadHunter API. Please try again later."
        )
    
    except HHForbiddenError as e:
        logger.error(f"Access forbidden: {e}")
        raise HTTPException(
            status_code=403,
            detail="Access to HeadHunter API forbidden. Please contact support."
        )
    
    except HHAPIError as e:
        logger.error(f"HH API error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch vacancies from HeadHunter: {str(e)}"
        )
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching vacancies"
        )


@router.get("/hh/vacancies/{vacancy_id}")
@limiter.limit(settings.API_RATE_LIMIT)
async def get_hh_vacancy_details(
    request: Request,
    vacancy_id: str
):
    """
    Get detailed information about a specific vacancy from HeadHunter
    
    Args:
        vacancy_id: HeadHunter vacancy ID
    
    Returns:
        Full vacancy details including description, requirements, etc.
    
    Raises:
        404: Vacancy not found
        500: Internal server error
    """
    try:
        async with HHService() as hh_client:
            vacancy = await hh_client.get_vacancy_by_id(vacancy_id)
            
            logger.info(f"Successfully fetched vacancy details: {vacancy_id}")
            
            return vacancy
    
    except HHAPIError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=404,
                detail=f"Vacancy {vacancy_id} not found"
            )
        
        logger.error(f"HH API error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch vacancy details: {str(e)}"
        )
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching vacancy details"
        )


@router.get("/hh/areas")
@limiter.limit(settings.API_RATE_LIMIT)
async def get_popular_areas(request: Request):
    """
    Get list of popular area IDs for HeadHunter search
    
    Returns:
        Dictionary of popular areas with their IDs
    """
    return {
        "areas": [
            {"id": 40, "name": "Kazakhstan", "description": "All of Kazakhstan"},
            {"id": 1, "name": "Moscow", "description": "Moscow, Russia"},
            {"id": 2, "name": "St. Petersburg", "description": "St. Petersburg, Russia"},
            {"id": 113, "name": "Russia", "description": "All of Russia"},
            {"id": 5, "name": "Almaty", "description": "Almaty, Kazakhstan"},
            {"id": 159, "name": "Astana", "description": "Astana (Nur-Sultan), Kazakhstan"},
        ]
    }


@router.get("/hh/roles")
@limiter.limit(settings.API_RATE_LIMIT)
async def get_professional_roles(request: Request):
    """
    Get list of popular professional role IDs for HeadHunter search
    
    Returns:
        Dictionary of popular IT roles with their IDs
    """
    return {
        "roles": [
            {"id": "96", "name": "Programmer, Developer", "description": "General programming roles"},
            {"id": "104", "name": "Web Developer", "description": "Frontend/Backend web development"},
            {"id": "113", "name": "QA Engineer", "description": "Quality Assurance, Testing"},
            {"id": "10", "name": "Analyst", "description": "Business/System Analyst"},
            {"id": "73", "name": "DevOps Engineer", "description": "DevOps, Infrastructure"},
            {"id": "124", "name": "Data Scientist", "description": "Data Science, ML"},
        ]
    }
