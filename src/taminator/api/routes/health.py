"""
Health Check Endpoint

Critical for:
- Service lifecycle management
- GUI detecting if service is running
- Monitoring and alerting
- AI model availability verification
"""

from fastapi import APIRouter, Depends
from typing import Dict, List, Optional
import platform
import psutil
from datetime import datetime
import httpx
import asyncio

from ...core import get_token_manager, TokenManager
from ...services.rhcase_service import RhcaseService

router = APIRouter(tags=["health"])

# Initialize rhcase service
_rhcase_service = RhcaseService()

# Service start time
_start_time = datetime.now()

# AI Model Configuration
LITELLM_URLS = [
    "http://localhost:4000",  # Local LiteLLM proxy
    "http://rhgrimm:4000"     # Remote grimm machine (if accessible)
]

# Red Hat approved models
RED_HAT_MODELS = [
    "granite-3.2-8b-instruct",
    "granite-3.1-8b-instruct", 
    "granite-8b-code-instruct",
    "mistral-7b-instruct"
]


async def check_litellm_availability() -> Dict:
    """
    Check if LiteLLM proxy is accessible and what models are available
    
    Returns status of AI infrastructure
    """
    result = {
        "available": False,
        "proxy_url": None,
        "models": [],
        "error": None
    }
    
    # Try each LiteLLM endpoint
    async with httpx.AsyncClient(timeout=2.0) as client:
        for url in LITELLM_URLS:
            try:
                response = await client.get(f"{url}/health")
                if response.status_code == 200:
                    result["available"] = True
                    result["proxy_url"] = url
                    
                    # Try to get model list
                    try:
                        models_response = await client.get(f"{url}/models")
                        if models_response.status_code == 200:
                            all_models = models_response.json().get("data", [])
                            # Filter to Red Hat approved models
                            result["models"] = [
                                m["id"] for m in all_models 
                                if any(rh in m["id"] for rh in ["granite", "mistral"])
                            ]
                    except:
                        pass
                    
                    break  # Found working proxy
                    
            except Exception as e:
                result["error"] = str(e)
                continue
    
    return result


@router.get("/health")
async def health_check(
    token_manager: TokenManager = Depends(get_token_manager)
) -> Dict:
    """
    Comprehensive health check
    
    Returns:
        - Service status
        - Version info
        - Token availability
        - System metrics
        - AI model availability (NEW!)
    """
    uptime = (datetime.now() - _start_time).total_seconds()
    
    # Check AI availability (non-blocking)
    ai_status = await check_litellm_availability()
    
    # Check rhcase availability
    rhcase_status = _rhcase_service.get_info()
    
    return {
        "status": "healthy",
        "version": "2.0.0",
        "service": "taminator-api",
        "uptime_seconds": int(uptime),
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_available_mb": int(psutil.virtual_memory().available / 1024 / 1024),
        },
        "authentication": token_manager.get_status(),
        "ai": ai_status,
        "rhcase": rhcase_status,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/health/ready")
async def readiness_check(
    token_manager: TokenManager = Depends(get_token_manager)
) -> Dict:
    """
    Readiness check - is service ready to handle requests?
    
    Returns 200 if all required tokens are configured,
    503 if service is not ready
    """
    token_status = token_manager.get_status()
    
    # Check if at least JIRA token is configured
    is_ready = token_status.get("jira", False)
    
    if not is_ready:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "message": "JIRA token not configured",
                "authentication": token_status
            }
        )
    
    return {
        "status": "ready",
        "message": "Service is ready to handle requests",
        "authentication": token_status
    }


@router.get("/health/live")
async def liveness_check() -> Dict:
    """
    Liveness check - is service process alive?
    
    Simple endpoint that just returns OK.
    Used by orchestrators to detect if service needs restart.
    """
    return {"status": "alive"}

