"""
Service Logs API

Badass features:
- View recent logs
- Log statistics
- Log file management
- Tail logs in real-time
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import logging

from ...core.logging_config import get_logger

router = APIRouter(prefix="/api/logs", tags=["logs"])
logger = logging.getLogger(__name__)


# Models

class LogStats(BaseModel):
    """Log file statistics"""
    exists: bool
    path: str
    size: int
    size_mb: float
    lines: int
    modified: str


class LogResponse(BaseModel):
    """Recent log entries"""
    lines: List[str]
    total_lines: int
    log_file: str


# Endpoints

@router.get("/recent", response_model=LogResponse)
async def get_recent_logs(lines: int = 100):
    """
    Get recent log entries
    
    Args:
        lines: Number of recent lines to return (default 100, max 1000)
        
    Returns:
        Recent log entries
    """
    # Cap max lines
    lines = min(lines, 1000)
    
    logger.info(f"📋 Fetching recent logs: {lines} lines")
    
    log_manager = get_logger()
    recent_logs = log_manager.get_recent_logs(lines)
    log_file_path = str(log_manager.get_log_file_path())
    
    return LogResponse(
        lines=recent_logs,
        total_lines=len(recent_logs),
        log_file=log_file_path
    )


@router.get("/stats", response_model=LogStats)
async def get_log_stats():
    """
    Get log file statistics
    
    Returns:
        Log file info (size, location, line count)
    """
    logger.info("📊 Getting log statistics")
    
    log_manager = get_logger()
    stats = log_manager.get_log_stats()
    
    return LogStats(**stats)


@router.delete("/clear")
async def clear_logs():
    """
    Clear current log file
    
    WARNING: This deletes all current logs!
    
    Returns:
        Success confirmation
    """
    logger.warning("🗑️  Clearing logs - this action cannot be undone")
    
    log_manager = get_logger()
    log_manager.clear_logs()
    
    return {
        "success": True,
        "message": "Logs cleared successfully"
    }


@router.get("/tail")
async def tail_logs(lines: int = 50):
    """
    Tail log file (like tail -f)
    
    Args:
        lines: Number of lines from end (default 50)
        
    Returns:
        Most recent log lines
    """
    lines = min(lines, 500)
    
    log_manager = get_logger()
    recent_logs = log_manager.get_recent_logs(lines)
    
    return {
        "lines": recent_logs,
        "count": len(recent_logs)
    }

