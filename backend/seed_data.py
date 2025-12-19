# seed_data.py
"""
Database seeding script.
Populates the database with realistic tech companies and job postings.

Usage:
    python seed_data.py
"""

import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal, init_db
from app.models.company import Company
from app.models.job import Job, JobLevel


async def seed_database():
    """Seed the database with companies and jobs."""
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if data already exists
            result = await session.execute(select(Company))
            existing_companies = result.scalars().all()
            
            if existing_companies:
                print("⚠️  Database already contains data. Skipping seed.")
                return
            
            print("🌱 Seeding database...")
            
            # Create companies
            companies_data = [
                {
                    "name": "TechCorp",
                    "description": "Leading technology company specializing in cloud solutions and AI",
                    "logo": "https://via.placeholder.com/150?text=TechCorp",
                    "website": "https://techcorp.example.com"
                },
                {
                    "name": "DataFlow Inc",
                    "description": "Big data analytics and machine learning platform",
                    "logo": "https://via.placeholder.com/150?text=DataFlow",
                    "website": "https://dataflow.example.com"
                },
                {
                    "name": "CloudNine Systems",
                    "description": "Cloud infrastructure and DevOps automation tools",
                    "logo": "https://via.placeholder.com/150?text=CloudNine",
                    "website": "https://cloudnine.example.com"
                },
                {
                    "name": "WebWizards",
                    "description": "Full-stack web development and design agency",
                    "logo": "https://via.placeholder.com/150?text=WebWizards",
                    "website": "https://webwizards.example.com"
                },
                {
                    "name": "MobileFirst Labs",
                    "description": "Mobile app development for iOS and Android",
                    "logo": "https://via.placeholder.com/150?text=MobileFirst",
                    "website": "https://mobilefirst.example.com"
                },
                {
                    "name": "SecureNet",
                    "description": "Cybersecurity solutions and penetration testing",
                    "logo": "https://via.placeholder.com/150?text=SecureNet",
                    "website": "https://securenet.example.com"
                },
                {
                    "name": "GameDev Studios",
                    "description": "Indie game development studio creating immersive experiences",
                    "logo": "https://via.placeholder.com/150?text=GameDev",
                    "website": "https://gamedev.example.com"
                },
                {
                    "name": "FinTech Solutions",
                    "description": "Financial technology and blockchain applications",
                    "logo": "https://via.placeholder.com/150?text=FinTech",
                    "website": "https://fintech.example.com"
                }
            ]
            
            companies = []
            for company_data in companies_data:
                company = Company(**company_data)
                session.add(company)
                companies.append(company)
            
            await session.flush()
            print(f"✅ Created {len(companies)} companies")
            
            # Create jobs
            jobs_data = [
                # TechCorp jobs
                {
                    "title": "Senior Full-Stack Engineer",
                    "description": "We're looking for an experienced full-stack engineer to join our cloud platform team. You'll work with React, Node.js, and AWS to build scalable solutions. Must have 5+ years of experience with modern web technologies.",
                    "location": "Remote",
                    "salary": "$150,000 - $180,000",
                    "level": JobLevel.SENIOR,
                    "company_id": companies[0].id
                },
                {
                    "title": "Junior Frontend Developer",
                    "description": "Join our frontend team to build beautiful user interfaces with React and TypeScript. Perfect for recent graduates or developers with 1-2 years of experience. We provide mentorship and growth opportunities.",
                    "location": "San Francisco, CA",
                    "salary": "$80,000 - $100,000",
                    "level": JobLevel.JUNIOR,
                    "company_id": companies[0].id
                },
                {
                    "title": "DevOps Lead",
                    "description": "Lead our DevOps transformation with Kubernetes, Docker, and CI/CD pipelines. 7+ years of experience required. You'll architect our infrastructure and mentor the team.",
                    "location": "Remote",
                    "salary": "$170,000 - $200,000",
                    "level": JobLevel.LEAD,
                    "company_id": companies[0].id
                },
                
                # DataFlow Inc jobs
                {
                    "title": "Machine Learning Engineer",
                    "description": "Build and deploy ML models for our data analytics platform. Experience with Python, TensorFlow, and PyTorch required. Work on cutting-edge AI projects.",
                    "location": "New York, NY",
                    "salary": "$140,000 - $170,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[1].id
                },
                {
                    "title": "Data Engineer",
                    "description": "Design and maintain our data pipelines using Apache Spark, Kafka, and Airflow. 3-5 years of experience with big data technologies.",
                    "location": "Remote",
                    "salary": "$130,000 - $160,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[1].id
                },
                {
                    "title": "Senior Data Scientist",
                    "description": "Lead data science initiatives and develop predictive models. PhD or 5+ years of industry experience. Strong background in statistics and machine learning.",
                    "location": "Boston, MA",
                    "salary": "$160,000 - $190,000",
                    "level": JobLevel.SENIOR,
                    "company_id": companies[1].id
                },
                
                # CloudNine Systems jobs
                {
                    "title": "Cloud Architect",
                    "description": "Design cloud infrastructure solutions for enterprise clients. AWS/Azure/GCP certifications preferred. 6+ years of cloud experience.",
                    "location": "Remote",
                    "salary": "$165,000 - $195,000",
                    "level": JobLevel.SENIOR,
                    "company_id": companies[2].id
                },
                {
                    "title": "Site Reliability Engineer",
                    "description": "Ensure 99.99% uptime for our cloud services. Experience with monitoring, alerting, and incident response. On-call rotation required.",
                    "location": "Seattle, WA",
                    "salary": "$140,000 - $170,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[2].id
                },
                
                # WebWizards jobs
                {
                    "title": "React Developer",
                    "description": "Build responsive web applications with React, Next.js, and Tailwind CSS. 2-4 years of frontend experience. Portfolio required.",
                    "location": "Remote",
                    "salary": "$110,000 - $140,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[3].id
                },
                {
                    "title": "UI/UX Designer",
                    "description": "Create beautiful and intuitive user interfaces. Proficiency in Figma and design systems. Work closely with developers.",
                    "location": "Austin, TX",
                    "salary": "$95,000 - $125,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[3].id
                },
                {
                    "title": "Backend Developer (Node.js)",
                    "description": "Develop RESTful APIs with Node.js, Express, and PostgreSQL. 3+ years of backend development experience.",
                    "location": "Remote",
                    "salary": "$120,000 - $150,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[3].id
                },
                
                # MobileFirst Labs jobs
                {
                    "title": "iOS Developer",
                    "description": "Build native iOS apps with Swift and SwiftUI. 4+ years of iOS development. App Store portfolio required.",
                    "location": "Los Angeles, CA",
                    "salary": "$135,000 - $165,000",
                    "level": JobLevel.SENIOR,
                    "company_id": companies[4].id
                },
                {
                    "title": "Android Developer",
                    "description": "Create Android applications with Kotlin and Jetpack Compose. 3-5 years of Android experience.",
                    "location": "Remote",
                    "salary": "$125,000 - $155,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[4].id
                },
                {
                    "title": "Mobile QA Engineer",
                    "description": "Test mobile applications across devices and platforms. Experience with automated testing frameworks. Entry-level welcome.",
                    "location": "Remote",
                    "salary": "$75,000 - $95,000",
                    "level": JobLevel.JUNIOR,
                    "company_id": companies[4].id
                },
                
                # SecureNet jobs
                {
                    "title": "Security Engineer",
                    "description": "Implement security best practices and conduct vulnerability assessments. CISSP or CEH certification preferred.",
                    "location": "Washington, DC",
                    "salary": "$145,000 - $175,000",
                    "level": JobLevel.SENIOR,
                    "company_id": companies[5].id
                },
                {
                    "title": "Penetration Tester",
                    "description": "Perform ethical hacking and security audits. 2-4 years of pentesting experience. Bug bounty experience a plus.",
                    "location": "Remote",
                    "salary": "$115,000 - $145,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[5].id
                },
                
                # GameDev Studios jobs
                {
                    "title": "Unity Game Developer",
                    "description": "Develop 3D games using Unity and C#. 3+ years of game development experience. Passion for gaming required!",
                    "location": "Remote",
                    "salary": "$100,000 - $130,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[6].id
                },
                {
                    "title": "Game Designer",
                    "description": "Design game mechanics, levels, and player experiences. Portfolio of shipped games required.",
                    "location": "Portland, OR",
                    "salary": "$90,000 - $120,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[6].id
                },
                {
                    "title": "Technical Artist",
                    "description": "Bridge the gap between art and engineering. Experience with shaders, VFX, and optimization.",
                    "location": "Remote",
                    "salary": "$105,000 - $135,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[6].id
                },
                
                # FinTech Solutions jobs
                {
                    "title": "Blockchain Developer",
                    "description": "Build decentralized applications with Solidity and Web3. Experience with Ethereum and smart contracts.",
                    "location": "Remote",
                    "salary": "$150,000 - $180,000",
                    "level": JobLevel.SENIOR,
                    "company_id": companies[7].id
                },
                {
                    "title": "Backend Engineer (Python)",
                    "description": "Develop financial APIs with Python, FastAPI, and PostgreSQL. FinTech experience preferred.",
                    "location": "London, UK",
                    "salary": "£90,000 - £120,000",
                    "level": JobLevel.MIDDLE,
                    "company_id": companies[7].id
                },
                {
                    "title": "Junior Full-Stack Developer",
                    "description": "Learn and grow with our FinTech team. React, Python, and SQL basics required. Great for career starters.",
                    "location": "Remote",
                    "salary": "$85,000 - $105,000",
                    "level": JobLevel.JUNIOR,
                    "company_id": companies[7].id
                },
            ]
            
            for job_data in jobs_data:
                job = Job(**job_data)
                session.add(job)
            
            await session.commit()
            print(f"✅ Created {len(jobs_data)} jobs")
            print("🎉 Database seeding completed successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding database: {e}")
            raise


async def main():
    """Main entry point."""
    print("🚀 Initializing database...")
    await init_db()
    print("✅ Database initialized")
    
    await seed_database()


if __name__ == "__main__":
    asyncio.run(main())
