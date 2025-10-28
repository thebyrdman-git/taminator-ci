"""
Gmail Assistant API Routes

AI-powered Gmail draft creation with clipboard integration
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import logging

from ...core.gmail_assistant import get_gmail_assistant
from ...core.token_manager import get_token_manager

router = APIRouter(prefix="/api/gmail", tags=["gmail-assistant"])
logger = logging.getLogger(__name__)


# Models

class ClipboardDraftRequest(BaseModel):
    """Request to create draft from clipboard"""
    clipboard_content: str
    context: Optional[Dict[str, Any]] = None


class ManualDraftRequest(BaseModel):
    """Request to create draft manually"""
    to: EmailStr
    subject: str
    body: str
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None


class DraftResponse(BaseModel):
    """Response with draft information"""
    draft_id: str
    draft_url: str
    subject: str
    preview: str
    context: Optional[Dict[str, Any]] = None


class DraftListItem(BaseModel):
    """Draft list item"""
    id: str
    snippet: str


# Endpoints

@router.post("/draft/from-clipboard", response_model=DraftResponse)
async def create_draft_from_clipboard(request: ClipboardDraftRequest):
    """
    Create Gmail draft from clipboard content using AI
    
    Workflow:
    1. Detect context from clipboard (RFE, bug, customer update)
    2. Generate professional email using AI
    3. Save as Gmail draft
    4. Return draft URL for user to review
    
    Args:
        request: Clipboard content and optional context
        
    Returns:
        Draft metadata and URL
    """
    logger.info("📋 Creating draft from clipboard content")
    
    try:
        assistant = get_gmail_assistant()
        
        # Create draft with AI enhancement
        draft_info = await assistant.create_draft_from_clipboard(
            clipboard_content=request.clipboard_content,
            context=request.context
        )
        
        return DraftResponse(**draft_info)
        
    except ValueError as e:
        # Not authenticated
        raise HTTPException(
            status_code=401,
            detail={"error": "not_authenticated", "message": str(e)}
        )
    
    except Exception as e:
        logger.error(f"❌ Failed to create draft: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "draft_creation_failed", "message": str(e)}
        )


@router.post("/draft/manual", response_model=Dict[str, str])
async def create_draft_manual(request: ManualDraftRequest):
    """
    Create Gmail draft manually (no AI)
    
    Args:
        request: Draft details (to, subject, body)
        
    Returns:
        Draft ID and URL
    """
    logger.info(f"📧 Creating manual draft to: {request.to}")
    
    try:
        assistant = get_gmail_assistant()
        
        draft_id = await assistant.create_draft_manual(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            bcc=request.bcc
        )
        
        return {
            "draft_id": draft_id,
            "draft_url": f"https://mail.google.com/mail/u/0/#drafts/{draft_id}",
            "message": "Draft created successfully"
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to create draft: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "draft_creation_failed", "message": str(e)}
        )


@router.get("/drafts", response_model=List[DraftListItem])
async def list_drafts(max_results: int = 10):
    """
    List existing Gmail drafts
    
    Args:
        max_results: Maximum number of drafts to return
        
    Returns:
        List of drafts
    """
    logger.info("📋 Listing Gmail drafts")
    
    try:
        assistant = get_gmail_assistant()
        drafts = assistant.list_drafts(max_results=max_results)
        
        return [DraftListItem(**draft) for draft in drafts]
        
    except Exception as e:
        logger.error(f"❌ Failed to list drafts: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "list_failed", "message": str(e)}
        )


@router.delete("/drafts/{draft_id}")
async def delete_draft(draft_id: str):
    """
    Delete a Gmail draft
    
    Args:
        draft_id: Draft ID to delete
        
    Returns:
        Success confirmation
    """
    logger.info(f"🗑️  Deleting draft: {draft_id}")
    
    try:
        assistant = get_gmail_assistant()
        assistant.delete_draft(draft_id)
        
        return {"message": "Draft deleted successfully"}
        
    except Exception as e:
        logger.error(f"❌ Failed to delete draft: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "delete_failed", "message": str(e)}
        )


@router.post("/detect-context")
async def detect_context(content: str):
    """
    Detect context from clipboard content (without creating draft)
    
    Useful for preview/validation before creating draft.
    
    Args:
        content: Text content to analyze
        
    Returns:
        Detected context
    """
    logger.info("🔍 Detecting context from content")
    
    try:
        assistant = get_gmail_assistant()
        context = await assistant._detect_context(content)
        
        return {
            "context": context,
            "suggested_template": context["type"]
        }
        
    except Exception as e:
        logger.error(f"❌ Context detection failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "detection_failed", "message": str(e)}
        )

