"""
Sync HeadHunter Vacancies to Database
Fetches real IT vacancies from HH API and saves them to local database
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy import select, delete

from app.database import AsyncSessionLocal, init_db
from app.models.company import Company
from app.models.job import Job, JobLevel
from app.services.hh_client import HHService, HHAPIError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def map_hh_to_job_level(vacancy_name: str) -> JobLevel:
    """
    Map vacancy name to job level based on keywords
    
    Args:
        vacancy_name: Vacancy title from HH
    
    Returns:
        JobLevel enum value
    """
    name_lower = vacancy_name.lower()
    
    # Lead/Principal/Head
    if any(keyword in name_lower for keyword in ['lead', 'principal', 'head', 'chief', 'director']):
        return JobLevel.LEAD
    
    # Senior
    if any(keyword in name_lower for keyword in ['senior', 'старший', 'sr.', 'sr ']):
        return JobLevel.SENIOR
    
    # Junior
    if any(keyword in name_lower for keyword in ['junior', 'младший', 'jr.', 'jr ', 'стажер', 'intern']):
        return JobLevel.JUNIOR
    
    # Middle (default)
    return JobLevel.MIDDLE


def format_salary(salary_data) -> Optional[str]:
    """
    Format salary information from HH API
    
    Args:
        salary_data: Salary object from HH API
    
    Returns:
        Formatted salary string or None
    """
    if not salary_data:
        return None
    
    from_amount = salary_data.from_ if salary_data.from_ else None
    to_amount = salary_data.to if salary_data.to else None
    currency = salary_data.currency if salary_data.currency else ""
    
    if from_amount and to_amount:
        return f"{from_amount:,} - {to_amount:,} {currency}"
    elif from_amount:
        return f"от {from_amount:,} {currency}"
    elif to_amount:
        return f"до {to_amount:,} {currency}"
    
    return None


def clean_html(text: Optional[str]) -> str:
    """
    Remove HTML tags from text
    
    Args:
        text: Text with HTML tags
    
    Returns:
        Clean text without HTML
    """
    if not text:
        return ""
    
    import re
    # Remove <highlighttext> tags
    text = re.sub(r'<highlighttext>', '', text)
    text = re.sub(r'</highlighttext>', '', text)
    # Remove other HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


async def clear_existing_data():
    """Clear all existing jobs and companies from database"""
    async with AsyncSessionLocal() as db:
        logger.info("Clearing existing data...")
        
        # Delete all jobs first (due to foreign key)
        await db.execute(delete(Job))
        logger.info("Deleted all jobs")
        
        # Delete all companies
        await db.execute(delete(Company))
        logger.info("Deleted all companies")
        
        await db.commit()
        logger.info("Database cleared successfully")


async def get_or_create_company(db, company_name: str, company_url: Optional[str] = None) -> Company:
    """
    Get existing company or create new one
    
    Args:
        db: Database session
        company_name: Company name
        company_url: Company URL (optional)
    
    Returns:
        Company object
    """
    # Check if company exists
    result = await db.execute(
        select(Company).where(Company.name == company_name)
    )
    company = result.scalar_one_or_none()
    
    if company:
        return company
    
    # Create new company
    company = Company(
        name=company_name,
        description=f"Company profile for {company_name}",
        website=company_url
    )
    db.add(company)
    await db.flush()
    
    logger.info(f"Created company: {company_name}")
    return company


async def sync_vacancies_from_hh(
    search_queries: list[str] = None,
    area_id: int = 40,
    max_pages: int = 3,
    per_page: int = 50
):
    """
    Fetch vacancies from HH API and save to database
    
    Args:
        search_queries: List of search queries (e.g., ["Python", "Java", "Frontend"])
        area_id: Area ID (40 = Kazakhstan)
        max_pages: Maximum pages to fetch per query
        per_page: Results per page (max 100)
    """
    if search_queries is None:
        search_queries = ["Python", "Java", "JavaScript", "Frontend", "Backend", "DevOps"]
    
    async with AsyncSessionLocal() as db:
        async with HHService() as hh_client:
            total_saved = 0
            
            for query in search_queries:
                logger.info(f"Fetching vacancies for: {query}")
                
                for page in range(max_pages):
                    try:
                        response = await hh_client.get_vacancies(
                            text=query,
                            role_id="96",  # Programmer/Developer
                            area_id=area_id,
                            per_page=per_page,
                            page=page,
                            order_by="publication_time"
                        )
                        
                        logger.info(
                            f"Query: {query}, Page: {page + 1}/{response.pages}, "
                            f"Found: {len(response.items)} vacancies"
                        )
                        
                        for vacancy in response.items:
                            try:
                                # Get or create company
                                company = await get_or_create_company(
                                    db,
                                    vacancy.employer.name,
                                    vacancy.employer.alternate_url
                                )
                                
                                # Check if job already exists (by HH ID in title or description)
                                result = await db.execute(
                                    select(Job).where(
                                        Job.title == vacancy.name,
                                        Job.company_id == company.id
                                    )
                                )
                                existing_job = result.scalar_one_or_none()
                                
                                if existing_job:
                                    logger.debug(f"Job already exists: {vacancy.name}")
                                    continue
                                
                                # Build description
                                description_parts = []
                                
                                if vacancy.snippet:
                                    if vacancy.snippet.requirement:
                                        req = clean_html(vacancy.snippet.requirement)
                                        description_parts.append(f"Требования:\n{req}")
                                    
                                    if vacancy.snippet.responsibility:
                                        resp = clean_html(vacancy.snippet.responsibility)
                                        description_parts.append(f"\nОбязанности:\n{resp}")
                                
                                description_parts.append(f"\n\nПодробнее: {vacancy.alternate_url}")
                                description_parts.append(f"\nИсточник: HeadHunter (ID: {vacancy.id})")
                                
                                description = "\n".join(description_parts) if description_parts else "Описание не указано"
                                
                                # Determine location (from area or default)
                                location = "Казахстан"  # Default for area_id=40
                                
                                # Create job
                                job = Job(
                                    title=vacancy.name,
                                    description=description,
                                    location=location,
                                    salary=format_salary(vacancy.salary),
                                    level=map_hh_to_job_level(vacancy.name),
                                    company_id=company.id,
                                    created_at=datetime.utcnow()
                                )
                                
                                db.add(job)
                                total_saved += 1
                                
                                logger.debug(f"Added job: {vacancy.name} at {company.name}")
                            
                            except Exception as e:
                                logger.error(f"Error processing vacancy {vacancy.id}: {e}")
                                continue
                        
                        # Commit after each page
                        await db.commit()
                        logger.info(f"Committed {len(response.items)} vacancies from page {page + 1}")
                        
                        # Stop if we've reached the last page
                        if page >= response.pages - 1:
                            break
                        
                        # Small delay to avoid rate limiting
                        await asyncio.sleep(0.5)
                    
                    except HHAPIError as e:
                        logger.error(f"HH API error for query '{query}', page {page}: {e}")
                        break
                    
                    except Exception as e:
                        logger.exception(f"Unexpected error for query '{query}', page {page}: {e}")
                        break
            
            logger.info(f"Sync completed! Total vacancies saved: {total_saved}")


async def main():
    """Main entry point"""
    logger.info("Starting HeadHunter vacancy sync...")
    
    # Initialize database
    logger.info("Initializing database...")
    await init_db()
    
    # Clear existing data
    await clear_existing_data()
    
    # Sync vacancies from HH
    logger.info("Fetching vacancies from HeadHunter API...")
    await sync_vacancies_from_hh(
        search_queries=[
            "Python",
            "Java",
            "JavaScript",
            "TypeScript",
            "Frontend",
            "Backend",
            "React",
            "Vue",
            "Angular",
            "DevOps",
            "QA",
            "Data Science"
        ],
        area_id=40,  # Kazakhstan
        max_pages=2,  # 2 pages per query
        per_page=50   # 50 results per page
    )
    
    # Print statistics
    async with AsyncSessionLocal() as db:
        companies_count = await db.execute(select(Company))
        jobs_count = await db.execute(select(Job))
        
        companies = len(companies_count.scalars().all())
        jobs = len(jobs_count.scalars().all())
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Sync Statistics:")
        logger.info(f"  Companies: {companies}")
        logger.info(f"  Jobs: {jobs}")
        logger.info(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
