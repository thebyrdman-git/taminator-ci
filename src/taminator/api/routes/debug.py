"""
Debug Logging API Routes
Control per-feature debug logging
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List
import logging

from ...core.debug_logging import get_debug_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/debug", tags=["debug"])

# Request Models
class EnableDebugRequest(BaseModel):
    """Request to enable debug logging for a module"""
    module: str


class DisableDebugRequest(BaseModel):
    """Request to disable debug logging for a module"""
    module: str


# Routes
@router.get("/status")
async def debug_status():
    """
    Get current debug logging status
    
    Returns:
        Dict of modules and their debug status
    """
    manager = get_debug_manager()
    return {
        "debug_modules": manager.get_status(),
        "available_modules": manager.list_available_modules()
    }


@router.post("/enable")
async def enable_debug(request: EnableDebugRequest):
    """
    Enable debug logging for a specific module
    
    Args:
        request: Module to enable debug for
        
    Returns:
        Success message
    """
    manager = get_debug_manager()
    manager.enable_debug(request.module)
    
    logger.info(f"🔍 Debug logging enabled for: {request.module}")
    
    return {
        "success": True,
        "message": f"Debug logging enabled for {request.module}",
        "module": request.module,
        "debug_enabled": True
    }


@router.post("/disable")
async def disable_debug(request: DisableDebugRequest):
    """
    Disable debug logging for a specific module
    
    Args:
        request: Module to disable debug for
        
    Returns:
        Success message
    """
    manager = get_debug_manager()
    manager.disable_debug(request.module)
    
    logger.info(f"Debug logging disabled for: {request.module}")
    
    return {
        "success": True,
        "message": f"Debug logging disabled for {request.module}",
        "module": request.module,
        "debug_enabled": False
    }


@router.post("/enable-all")
async def enable_all_debug():
    """
    Enable debug logging for all features
    
    Returns:
        Success message
    """
    manager = get_debug_manager()
    manager.enable_all()
    
    logger.info("🔍 Debug logging enabled for ALL features")
    
    return {
        "success": True,
        "message": "Debug logging enabled for all features",
        "debug_modules": manager.get_status()
    }


@router.post("/disable-all")
async def disable_all_debug():
    """
    Disable debug logging for all features
    
    Returns:
        Success message
    """
    manager = get_debug_manager()
    manager.disable_all()
    
    logger.info("Debug logging disabled for ALL features")
    
    return {
        "success": True,
        "message": "Debug logging disabled for all features"
    }

