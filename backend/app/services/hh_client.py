"""
HeadHunter API Client Service
Handles all interactions with hh.ru API
"""
import logging
from typing import Optional
import httpx
from app.schemas.hh_vacancy import HHVacanciesResponse, HHVacancy

logger = logging.getLogger(__name__)


class HHAPIError(Exception):
    """Base exception for HH API errors"""
    pass


class HHRateLimitError(HHAPIError):
    """Raised when rate limit is exceeded (429)"""
    pass


class HHForbiddenError(HHAPIError):
    """Raised when access is forbidden (403)"""
    pass


class HHService:
    """
    Service for interacting with HeadHunter API
    
    Handles:
    - Vacancy search with filters
    - Error handling (403, 429, connection errors)
    - Proper User-Agent header (required by HH API)
    """
    
    BASE_URL = "https://api.hh.ru"
    
    def __init__(
        self,
        user_agent: str = "JobBoardKZ/1.0 (d.seilbekov@mail.ru)",
        timeout: float = 10.0
    ):
        """
        Initialize HH API client
        
        Args:
            user_agent: User-Agent header (REQUIRED by HH API)
                       Format: AppName/Version (contact-email)
            timeout: Request timeout in seconds
        """
        self.user_agent = user_agent
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=self.timeout,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._client:
            await self._client.aclose()
    
    async def get_vacancies(
        self,
        text: str,
        role_id: str = "96",
        area_id: int = 40,
        per_page: int = 20,
        page: int = 0,
        order_by: str = "publication_time"
    ) -> HHVacanciesResponse:
        """
        Search for vacancies on HeadHunter
        
        Args:
            text: Search query (e.g., "Python", "Java Developer")
            role_id: Professional role ID (default: "96" = "Программист, разработчик")
            area_id: Area/region ID (default: 40 = Kazakhstan)
                    Common values: 1 = Moscow, 2 = St. Petersburg, 113 = Russia
            per_page: Results per page (max 100)
            page: Page number (starts from 0)
            order_by: Sort order (publication_time, salary_desc, salary_asc, relevance)
        
        Returns:
            HHVacanciesResponse with list of vacancies
        
        Raises:
            HHRateLimitError: When rate limit exceeded (429)
            HHForbiddenError: When access forbidden (403)
            HHAPIError: For other API errors
            httpx.HTTPError: For connection errors
        """
        if not self._client:
            raise RuntimeError("HHService must be used as async context manager")
        
        params = {
            "text": text,
            "professional_role": role_id,
            "area": area_id,
            "per_page": per_page,
            "page": page,
            "order_by": order_by,
            "search_field": "name"  # Search only in vacancy title for better precision
        }
        
        try:
            logger.info(f"Fetching vacancies: text={text}, area={area_id}, page={page}")
            response = await self._client.get("/vacancies", params=params)
            
            # Handle specific error codes
            if response.status_code == 429:
                logger.error("Rate limit exceeded (429)")
                raise HHRateLimitError("Too many requests. Please try again later.")
            
            if response.status_code == 403:
                logger.error("Access forbidden (403)")
                raise HHForbiddenError("Access forbidden. Check your User-Agent or API permissions.")
            
            if response.status_code == 400:
                error_data = response.json()
                logger.error(f"Bad request (400): {error_data}")
                raise HHAPIError(f"Bad request: {error_data.get('description', 'Unknown error')}")
            
            # Raise for other error status codes
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            logger.info(f"Successfully fetched {len(data.get('items', []))} vacancies")
            
            return HHVacanciesResponse(**data)
        
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise HHAPIError(f"Request timeout: {e}")
        
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")
            raise HHAPIError(f"Failed to connect to HH API: {e}")
        
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise HHAPIError(f"HTTP error occurred: {e}")
    
    async def get_vacancy_by_id(self, vacancy_id: str) -> dict:
        """
        Get detailed vacancy information by ID
        
        Args:
            vacancy_id: Vacancy ID from HH
        
        Returns:
            Full vacancy details as dict
        """
        if not self._client:
            raise RuntimeError("HHService must be used as async context manager")
        
        try:
            logger.info(f"Fetching vacancy details: id={vacancy_id}")
            response = await self._client.get(f"/vacancies/{vacancy_id}")
            
            if response.status_code == 404:
                raise HHAPIError(f"Vacancy {vacancy_id} not found")
            
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            logger.error(f"Error fetching vacancy {vacancy_id}: {e}")
            raise HHAPIError(f"Failed to fetch vacancy: {e}")
