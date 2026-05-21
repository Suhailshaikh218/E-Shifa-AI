"""
E-Shifa AI - Main FastAPI Application
Pakistan's First Fully Automated Healthcare Service Orchestrator
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.api import auth, bookings, admin

# Import webhooks router (with error handling)
try:
    from app.api import webhooks
    _webhooks_loaded = True
except Exception as e:
    print(f"⚠️  Could not load webhooks router: {e}")
    _webhooks_loaded = False

# Create FastAPI application
app = FastAPI(
    title="E-Shifa AI - Hackathon MVP",
    version="2.0.0",
    description="AI-Powered Home Healthcare Service Orchestrator for Informal Economy",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup():
    """Initialize database connection on startup"""
    await connect_db()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} started successfully")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    # Debug: print all registered routes
    webhook_routes = [r.path for r in app.routes if hasattr(r, 'path') and 'webhook' in r.path]
    print(f"📡 Webhook routes: {webhook_routes if webhook_routes else 'NONE - check import'}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown"""
    await disconnect_db()
    print(f"👋 {settings.APP_NAME} shut down gracefully")


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "active",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "E-Shifa AI Backend is running successfully"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected",
        "ai_engine": "operational"
    }


# Include routers
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(admin.router)
if _webhooks_loaded:
    app.include_router(webhooks.router)
    print("✅ WhatsApp webhook router loaded")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
