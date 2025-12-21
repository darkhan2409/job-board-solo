# app/main.py
"""
FastAPI application entry point.
Configures CORS, lifespan events, and routes.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    Startup:
        - Initialize database tables
        
    Shutdown:
        - Close database connections
    """
    # Startup
    print(">> Starting Job Board API...")
    await init_db()
    print(">> Database initialized")
    
    yield
    
    # Shutdown
    print(">> Shutting down Job Board API...")
    await close_db()
    print(">> Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status and version information
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": settings.PROJECT_NAME
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: Welcome message and documentation links
    """
    return {
        "message": "Welcome to Job Board API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Include API routers
from app.routes import jobs_router, companies_router

app.include_router(jobs_router, prefix=settings.API_V1_PREFIX, tags=["Jobs"])
app.include_router(companies_router, prefix=settings.API_V1_PREFIX, tags=["Companies"])
