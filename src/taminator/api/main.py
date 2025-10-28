"""
Taminator API Service - Main Application

Production-grade architecture:
- FastAPI service (not process spawning)
- Structured errors (not text parsing)
- Real-time updates (WebSocket)
- Smart caching (not reload-everything)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from ..core.exceptions import TaminatorException
from ..core.logging_config import setup_logging
from .routes import health, customers, jira, portal, logs, rhcase, debug, diagnostics

# Setup logging (file + console with rotation)
setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage service lifecycle"""
    logger.info("🚀 Starting Taminator API Service v2.0")
    logger.info("📡 Service URL: http://localhost:8765")
    yield
    logger.info("🛑 Shutting down Taminator API Service")


app = FastAPI(
    title="Taminator API",
    description="Professional TAM automation service with real-time updates",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware - Allow Electron GUI to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:*",
        "file://*",  # Electron apps
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for structured errors
@app.exception_handler(TaminatorException)
async def taminator_exception_handler(request: Request, exc: TaminatorException):
    """Convert TaminatorException to structured JSON response"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


# Register routes
app.include_router(health.router)
app.include_router(customers.router)
app.include_router(jira.router)
app.include_router(portal.router)
app.include_router(logs.router)
app.include_router(rhcase.router)
app.include_router(debug.router)
app.include_router(diagnostics.router)

# Deferred to v2.1+ (not in alpha):
# - google_auth.router (Google OAuth)
# - drive_storage.router (Google Drive)
# - gmail_assistant.router (Clippy Gmail)


@app.get("/")
async def root():
    """API root - service info"""
    return {
        "service": "Taminator API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run service
    uvicorn.run(
        "taminator.api.main:app",
        host="127.0.0.1",
        port=8765,
        log_level="info",
        reload=False  # Production mode
    )


