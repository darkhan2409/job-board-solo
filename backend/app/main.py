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

# Add rate limiter to app state
from app.utils.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Security middleware for production
@app.middleware("http")
async def add_security_headers(request, call_next):
    """
    Add security headers to all responses.
    
    Headers added:
        - Strict-Transport-Security (HSTS): Force HTTPS for 1 year
        - X-Content-Type-Options: Prevent MIME type sniffing
        - X-Frame-Options: Prevent clickjacking
        - X-XSS-Protection: Enable XSS filter
    """
    response = await call_next(request)
    
    # Add HSTS header in production (force HTTPS)
    if not settings.DEBUG:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    
    # Security headers (always enabled)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    return response


# Configure CORS
# CORS (Cross-Origin Resource Sharing) allows the frontend to make requests to the backend
# from a different origin (domain, protocol, or port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # List of allowed origins
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,  # Allow cookies and auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Allowed HTTP methods
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "X-CSRF-Token",
    ],  # Allowed request headers
    expose_headers=[
        "Content-Length",
        "Content-Type",
        "X-Total-Count",
    ],  # Headers exposed to the browser
    max_age=settings.CORS_MAX_AGE,  # Preflight cache duration (seconds)
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


# Test endpoint to debug
@app.get("/api/test", tags=["Test"])
async def test_endpoint():
    """Test endpoint to check if API is working."""
    return {"status": "ok", "message": "API is working"}


# Include API routers
from app.routes import (
    jobs_router,
    companies_router,
    auth_router,
    saved_jobs_router,
    applications_router
)
from app.routes.hh_vacancies import router as hh_router

app.include_router(auth_router, prefix=settings.API_V1_PREFIX, tags=["Authentication"])
app.include_router(jobs_router, prefix=settings.API_V1_PREFIX, tags=["Jobs"])
app.include_router(companies_router, prefix=settings.API_V1_PREFIX, tags=["Companies"])
app.include_router(saved_jobs_router, prefix=settings.API_V1_PREFIX, tags=["Saved Jobs"])
app.include_router(applications_router, prefix=settings.API_V1_PREFIX, tags=["Applications"])
app.include_router(hh_router, prefix=settings.API_V1_PREFIX, tags=["HeadHunter"])
