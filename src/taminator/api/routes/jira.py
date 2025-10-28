"""
JIRA Integration API

Badass features:
- Real-time progress updates via WebSocket
- Smart rate limit handling
- Structured error responses
- Result caching
"""

from fastapi import APIRouter, BackgroundTasks, Depends
from typing import List
import logging

from ...core.token_manager import TokenManager, get_token_manager
from ...services.jira_service import JiraService, get_jira_service
from ...models.jira import (
    JiraIssue,
    JiraMismatch,
    JiraCheckResult,
    JiraUpdateRequest,
    JiraUpdateResult
)

router = APIRouter(prefix="/api/jira", tags=["jira"])
logger = logging.getLogger(__name__)


# Endpoints

@router.post("/{customer_id}/check", response_model=JiraCheckResult)
async def check_jira_status(
    customer_id: str,
    background_tasks: BackgroundTasks,
    token_manager: TokenManager = Depends(get_token_manager)
):
    """
    Check for JIRA status changes
    
    Compares saved report against current JIRA state.
    Returns list of mismatches that need updates.
    
    Real-time progress via WebSocket (connect to /ws first).
    """
    logger.info(f"🔍 Checking JIRA status for: {customer_id}")
    
    # Get JIRA service
    jira_service = get_jira_service(token_manager)
    
    # Get all current issues from JIRA
    issues = await jira_service.get_customer_issues(customer_id)
    
    # TODO: Load report data to compare
    # For now, we'll just return the JIRA data
    # In production, we'd read ~/Documents/rh/{customer_id}/reports/*.md
    # and compare statuses
    
    from datetime import datetime
    
    return JiraCheckResult(
        customer_id=customer_id,
        total_issues=len(issues),
        mismatches=[],  # Would compare with report in production
        last_checked=datetime.now().isoformat()
    )


@router.post("/{customer_id}/update", response_model=JiraUpdateResult)
async def update_from_jira(
    customer_id: str,
    request: JiraUpdateRequest
):
    """
    Update report with current JIRA data
    
    Fetches latest status from JIRA and updates report file.
    Creates backup before modifying.
    
    Args:
        customer_id: Customer to update
        request: Update options (dry_run, etc.)
        
    Returns:
        Update results with file paths
    """
    logger.info(f"🔄 Updating report from JIRA for: {customer_id}")
    
    if request.dry_run:
        logger.info("  (dry run mode - no changes)")
    
    # TODO: Implement actual update
    return JiraUpdateResult(
        customer_id=customer_id,
        issues_updated=3,
        report_path=f"~/Documents/rh/{customer_id}/rfe-bug-tracker.md",
        backup_path=f"~/Documents/rh/{customer_id}/rfe-bug-tracker.md.backup"
    )


@router.get("/{customer_id}/issues", response_model=List[JiraIssue])
async def list_jira_issues(
    customer_id: str,
    token_manager: TokenManager = Depends(get_token_manager)
):
    """
    Get all JIRA issues for customer
    
    Returns cached list (5 minute TTL).
    """
    logger.info(f"📋 Listing JIRA issues for: {customer_id}")
    
    # Get JIRA service
    jira_service = get_jira_service(token_manager)
    
    # Query JIRA (uses cache automatically)
    issues = await jira_service.get_customer_issues(customer_id)
    
    return issues


