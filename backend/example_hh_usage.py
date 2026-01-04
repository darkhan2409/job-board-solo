"""
Example usage of HeadHunter API Client
Demonstrates how to use HHService to fetch vacancies
"""
import asyncio
import logging
from app.services.hh_client import HHService, HHAPIError, HHRateLimitError, HHForbiddenError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def example_basic_search():
    """Basic example: Search for Python vacancies in Kazakhstan"""
    print("\n" + "="*60)
    print("Example 1: Basic Search - Python vacancies in Kazakhstan")
    print("="*60 + "\n")
    
    async with HHService() as hh_client:
        try:
            # Search for Python vacancies
            response = await hh_client.get_vacancies(
                text="Python",
                role_id="96",  # Программист, разработчик
                area_id=40,    # Kazakhstan
                per_page=5
            )
            
            print(f"✅ Found {response.found} vacancies total")
            print(f"📄 Showing page {response.page + 1} of {response.pages}")
            print(f"📊 Results per page: {response.per_page}\n")
            
            for idx, vacancy in enumerate(response.items, 1):
                print(f"{idx}. {vacancy.name}")
                print(f"   🏢 Company: {vacancy.employer.name}")
                
                if vacancy.salary:
                    salary_from = vacancy.salary.from_ or "—"
                    salary_to = vacancy.salary.to or "—"
                    currency = vacancy.salary.currency or ""
                    print(f"   💰 Salary: {salary_from} - {salary_to} {currency}")
                else:
                    print(f"   💰 Salary: Not specified")
                
                if vacancy.snippet:
                    if vacancy.snippet.requirement:
                        print(f"   📋 Requirements: {vacancy.snippet.requirement[:100]}...")
                    if vacancy.snippet.responsibility:
                        print(f"   📝 Responsibilities: {vacancy.snippet.responsibility[:100]}...")
                
                print(f"   🔗 URL: {vacancy.alternate_url}")
                print()
        
        except HHAPIError as e:
            logger.error(f"HH API Error: {e}")


async def example_different_regions():
    """Example: Search in different regions"""
    print("\n" + "="*60)
    print("Example 2: Search in Different Regions")
    print("="*60 + "\n")
    
    regions = [
        (40, "Kazakhstan"),
        (1, "Moscow"),
        (2, "St. Petersburg"),
    ]
    
    async with HHService() as hh_client:
        for area_id, region_name in regions:
            try:
                response = await hh_client.get_vacancies(
                    text="Java",
                    area_id=area_id,
                    per_page=3
                )
                
                print(f"📍 {region_name}: {response.found} Java vacancies found")
                for vacancy in response.items[:3]:
                    print(f"   • {vacancy.name} - {vacancy.employer.name}")
                print()
            
            except HHAPIError as e:
                logger.error(f"Error searching in {region_name}: {e}")


async def example_pagination():
    """Example: Paginated search"""
    print("\n" + "="*60)
    print("Example 3: Pagination - First 3 pages")
    print("="*60 + "\n")
    
    async with HHService() as hh_client:
        for page_num in range(3):
            try:
                response = await hh_client.get_vacancies(
                    text="Frontend",
                    area_id=40,
                    per_page=5,
                    page=page_num
                )
                
                print(f"📄 Page {page_num + 1}:")
                for vacancy in response.items:
                    print(f"   • {vacancy.name}")
                print()
            
            except HHAPIError as e:
                logger.error(f"Error fetching page {page_num + 1}: {e}")


async def example_error_handling():
    """Example: Error handling"""
    print("\n" + "="*60)
    print("Example 4: Error Handling")
    print("="*60 + "\n")
    
    # Example with bad User-Agent (will fail)
    try:
        async with HHService(user_agent="BadBot/1.0") as hh_client:
            response = await hh_client.get_vacancies(text="Python")
            print(f"Found {response.found} vacancies")
    
    except HHForbiddenError as e:
        print(f"❌ Forbidden Error: {e}")
    
    except HHRateLimitError as e:
        print(f"❌ Rate Limit Error: {e}")
    
    except HHAPIError as e:
        print(f"❌ API Error: {e}")


async def example_get_vacancy_details():
    """Example: Get detailed vacancy information"""
    print("\n" + "="*60)
    print("Example 5: Get Vacancy Details")
    print("="*60 + "\n")
    
    async with HHService() as hh_client:
        try:
            # First, search for a vacancy
            response = await hh_client.get_vacancies(
                text="Python",
                area_id=40,
                per_page=1
            )
            
            if response.items:
                vacancy_id = response.items[0].id
                print(f"Fetching details for vacancy ID: {vacancy_id}\n")
                
                # Get full details
                details = await hh_client.get_vacancy_by_id(vacancy_id)
                
                print(f"📋 Vacancy: {details['name']}")
                print(f"🏢 Company: {details['employer']['name']}")
                print(f"📍 Area: {details['area']['name']}")
                
                if details.get('description'):
                    print(f"\n📝 Description (first 200 chars):")
                    print(details['description'][:200] + "...")
        
        except HHAPIError as e:
            logger.error(f"Error: {e}")


async def main():
    """Run all examples"""
    print("\n" + "🚀 HeadHunter API Client Examples" + "\n")
    
    # Run examples
    await example_basic_search()
    await example_different_regions()
    await example_pagination()
    # await example_error_handling()  # Uncomment to test error handling
    await example_get_vacancy_details()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
