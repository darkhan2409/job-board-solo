# seed_data.py
"""
Database seeding script.
Populates database with realistic tech companies and job postings.
"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select

from app.database import AsyncSessionLocal, init_db
from app.models.company import Company
from app.models.job import Job, JobLevel


async def seed_database():
    """Seed database with companies and jobs."""
    
    async with AsyncSessionLocal() as db:
        # Check if data already exists
        result = await db.execute(select(Company))
        existing_companies = result.scalars().all()
        
        if existing_companies:
            print("WARNING: Database already contains data. Skipping seed.")
            return

        print("Seeding database...")
        
        # Companies data
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
                "name": "WebWorks Studio",
                "description": "Full-stack web development and design agency",
                "logo": "https://via.placeholder.com/150?text=WebWorks",
                "website": "https://webworks.example.com"
            },
            {
                "name": "MobileFirst Labs",
                "description": "Mobile app development for iOS and Android",
                "logo": "https://via.placeholder.com/150?text=MobileFirst",
                "website": "https://mobilefirst.example.com"
            },
            {
                "name": "SecureNet Solutions",
                "description": "Cybersecurity and network protection services",
                "logo": "https://via.placeholder.com/150?text=SecureNet",
                "website": "https://securenet.example.com"
            },
            {
                "name": "GameDev Studios",
                "description": "Indie game development studio creating innovative experiences",
                "logo": "https://via.placeholder.com/150?text=GameDev",
                "website": "https://gamedev.example.com"
            },
            {
                "name": "FinTech Innovations",
                "description": "Financial technology and blockchain solutions",
                "logo": "https://via.placeholder.com/150?text=FinTech",
                "website": "https://fintech.example.com"
            }
        ]
        
        # Create companies
        companies = []
        for company_data in companies_data:
            company = Company(**company_data)
            db.add(company)
            companies.append(company)
        
        await db.flush()
        print(f"Created {len(companies)} companies")
        
        # Jobs data
        jobs_data = [
            # TechCorp jobs
            {
                "title": "Senior Full-Stack Engineer",
                "description": "We're looking for an experienced full-stack engineer to join our cloud platform team. You'll work with React, Node.js, and AWS to build scalable solutions.\n\nRequirements:\n- 5+ years of experience with React and Node.js\n- Strong understanding of AWS services\n- Experience with microservices architecture\n- Excellent problem-solving skills",
                "location": "Remote",
                "salary": "$150,000 - $180,000",
                "level": JobLevel.SENIOR,
                "company_id": companies[0].id
            },
            {
                "title": "DevOps Engineer",
                "description": "Join our infrastructure team to build and maintain CI/CD pipelines and cloud infrastructure.\n\nRequirements:\n- Experience with Kubernetes and Docker\n- Strong knowledge of AWS/GCP\n- Infrastructure as Code (Terraform, CloudFormation)\n- Monitoring and logging tools",
                "location": "San Francisco, CA",
                "salary": "$140,000 - $170,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[0].id
            },
            
            # DataFlow Inc jobs
            {
                "title": "Machine Learning Engineer",
                "description": "Build and deploy ML models for our data analytics platform. Work with Python, TensorFlow, and big data technologies.\n\nRequirements:\n- Strong Python and ML framework experience\n- Experience with TensorFlow or PyTorch\n- Understanding of data pipelines\n- PhD or Master's in CS/ML preferred",
                "location": "New York, NY",
                "salary": "$160,000 - $200,000",
                "level": JobLevel.SENIOR,
                "company_id": companies[1].id
            },
            {
                "title": "Data Engineer",
                "description": "Design and build data pipelines for processing terabytes of data daily.\n\nRequirements:\n- Experience with Spark, Kafka, or similar\n- Strong SQL and Python skills\n- Cloud data warehouse experience\n- ETL pipeline development",
                "location": "Remote",
                "salary": "$130,000 - $160,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[1].id
            },
            {
                "title": "Junior Data Analyst",
                "description": "Start your career in data analytics! Work with our team to analyze data and create insights.\n\nRequirements:\n- Basic SQL and Python knowledge\n- Understanding of statistics\n- Eagerness to learn\n- Bachelor's degree in related field",
                "location": "New York, NY",
                "salary": "$70,000 - $90,000",
                "level": JobLevel.JUNIOR,
                "company_id": companies[1].id
            },
            
            # CloudNine Systems jobs
            {
                "title": "Cloud Architect",
                "description": "Lead cloud infrastructure design for enterprise clients. Work with AWS, Azure, and GCP.\n\nRequirements:\n- 7+ years of cloud architecture experience\n- Multiple cloud certifications\n- Experience with multi-cloud strategies\n- Strong leadership skills",
                "location": "Remote",
                "salary": "$180,000 - $220,000",
                "level": JobLevel.LEAD,
                "company_id": companies[2].id
            },
            {
                "title": "Site Reliability Engineer",
                "description": "Ensure 99.99% uptime for our cloud services. Build monitoring and automation tools.\n\nRequirements:\n- Strong Linux/Unix background\n- Experience with monitoring tools (Prometheus, Grafana)\n- Scripting skills (Python, Bash)\n- On-call rotation participation",
                "location": "Seattle, WA",
                "salary": "$140,000 - $170,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[2].id
            },
            
            # WebWorks Studio jobs
            {
                "title": "Frontend Developer (React)",
                "description": "Create beautiful, responsive web applications using React and modern CSS.\n\nRequirements:\n- 3+ years of React experience\n- Strong CSS/SCSS skills\n- Experience with Next.js\n- Eye for design and UX",
                "location": "London, UK",
                "salary": "£60,000 - £80,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[3].id
            },
            {
                "title": "UI/UX Designer",
                "description": "Design user interfaces and experiences for web and mobile applications.\n\nRequirements:\n- Portfolio of design work\n- Proficiency in Figma/Sketch\n- Understanding of web technologies\n- User research experience",
                "location": "Remote",
                "salary": "$90,000 - $120,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[3].id
            },
            {
                "title": "Junior Frontend Developer",
                "description": "Learn and grow as a frontend developer in our supportive team environment.\n\nRequirements:\n- Basic HTML, CSS, JavaScript knowledge\n- Familiarity with React\n- Portfolio or personal projects\n- Passion for web development",
                "location": "London, UK",
                "salary": "£35,000 - £45,000",
                "level": JobLevel.JUNIOR,
                "company_id": companies[3].id
            },
            
            # MobileFirst Labs jobs
            {
                "title": "iOS Developer (Swift)",
                "description": "Build native iOS applications using Swift and SwiftUI.\n\nRequirements:\n- 4+ years of iOS development\n- Strong Swift skills\n- Experience with SwiftUI\n- Published apps in App Store",
                "location": "Berlin, Germany",
                "salary": "€70,000 - €90,000",
                "level": JobLevel.SENIOR,
                "company_id": companies[4].id
            },
            {
                "title": "Android Developer (Kotlin)",
                "description": "Develop Android applications using Kotlin and Jetpack Compose.\n\nRequirements:\n- 3+ years of Android development\n- Strong Kotlin skills\n- Experience with Jetpack Compose\n- Material Design knowledge",
                "location": "Berlin, Germany",
                "salary": "€65,000 - €85,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[4].id
            },
            {
                "title": "Mobile Team Lead",
                "description": "Lead our mobile development team across iOS and Android platforms.\n\nRequirements:\n- 8+ years of mobile development\n- Leadership experience\n- Both iOS and Android knowledge\n- Agile/Scrum experience",
                "location": "Remote",
                "salary": "$170,000 - $200,000",
                "level": JobLevel.LEAD,
                "company_id": companies[4].id
            },
            
            # SecureNet Solutions jobs
            {
                "title": "Security Engineer",
                "description": "Protect our infrastructure and applications from security threats.\n\nRequirements:\n- 5+ years in cybersecurity\n- Penetration testing experience\n- Security certifications (CISSP, CEH)\n- Incident response experience",
                "location": "Remote",
                "salary": "$150,000 - $180,000",
                "level": JobLevel.SENIOR,
                "company_id": companies[5].id
            },
            {
                "title": "Junior Security Analyst",
                "description": "Start your cybersecurity career monitoring and responding to security events.\n\nRequirements:\n- Basic networking knowledge\n- Understanding of security concepts\n- Security+ or similar certification\n- Analytical mindset",
                "location": "Austin, TX",
                "salary": "$65,000 - $85,000",
                "level": JobLevel.JUNIOR,
                "company_id": companies[5].id
            },
            
            # GameDev Studios jobs
            {
                "title": "Game Developer (Unity)",
                "description": "Create engaging game mechanics and systems using Unity and C#.\n\nRequirements:\n- 3+ years of Unity development\n- Strong C# skills\n- Published games portfolio\n- Passion for gaming",
                "location": "Remote",
                "salary": "$100,000 - $130,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[6].id
            },
            {
                "title": "3D Artist",
                "description": "Create 3D models, textures, and animations for our games.\n\nRequirements:\n- Proficiency in Blender/Maya\n- Strong portfolio\n- Understanding of game engines\n- Artistic creativity",
                "location": "Los Angeles, CA",
                "salary": "$80,000 - $110,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[6].id
            },
            
            # FinTech Innovations jobs
            {
                "title": "Blockchain Developer",
                "description": "Build decentralized applications and smart contracts on Ethereum.\n\nRequirements:\n- Experience with Solidity\n- Understanding of blockchain concepts\n- Web3.js or ethers.js knowledge\n- Security-first mindset",
                "location": "Remote",
                "salary": "$140,000 - $180,000",
                "level": JobLevel.SENIOR,
                "company_id": companies[7].id
            },
            {
                "title": "Backend Engineer (Python)",
                "description": "Build scalable backend services for our fintech platform using Python and FastAPI.\n\nRequirements:\n- 4+ years of Python development\n- Experience with FastAPI or Django\n- Database design skills\n- Financial domain knowledge a plus",
                "location": "Singapore",
                "salary": "$120,000 - $150,000",
                "level": JobLevel.MIDDLE,
                "company_id": companies[7].id
            },
            {
                "title": "Engineering Manager",
                "description": "Lead our engineering team to deliver high-quality fintech solutions.\n\nRequirements:\n- 10+ years of software development\n- 3+ years of management experience\n- Strong technical background\n- Excellent communication skills",
                "location": "Singapore",
                "salary": "$180,000 - $220,000",
                "level": JobLevel.LEAD,
                "company_id": companies[7].id
            }
        ]
        
        # Create jobs with staggered creation dates
        base_date = datetime.utcnow() - timedelta(days=30)
        for i, job_data in enumerate(jobs_data):
            job_data["created_at"] = base_date + timedelta(days=i)
            job = Job(**job_data)
            db.add(job)
        
        await db.commit()
        print(f"Created {len(jobs_data)} jobs")
        print("Database seeding completed!")


async def main():
    """Main entry point."""
    print("Initializing database...")
    await init_db()
    await seed_database()


if __name__ == "__main__":
    asyncio.run(main())
