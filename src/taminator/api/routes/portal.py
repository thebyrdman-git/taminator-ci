"""
Customer Portal API

Badass features:
- Post to portal with preview
- Live preview rendering
- Markdown validation
- Upload status tracking
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import logging

from ...core.token_manager import TokenManager, get_token_manager
from ...services.portal_service import PortalService, get_portal_service

router = APIRouter(prefix="/api/portal", tags=["portal"])
logger = logging.getLogger(__name__)


# Models

class PortalPostRequest(BaseModel):
    """Request to post content to portal"""
    customer_id: str
    group_id: str
    title: str
    content: str
    preview_mode: bool = False
    case_number: Optional[str] = None


class PortalPostResult(BaseModel):
    """Result of portal post"""
    success: bool
    portal_url: str
    post_id: str


class PortalPreview(BaseModel):
    """Preview of how content will look"""
    html: str
    estimated_size: int


# Endpoints

@router.post("/post", response_model=PortalPostResult)
async def post_to_portal(
    request: PortalPostRequest,
    token_manager: TokenManager = Depends(get_token_manager)
):
    """
    Post content to Customer Portal
    
    Args:
        request: Post data with content and metadata
        
    Returns:
        Post result with portal URL
        
    Raises:
        401: Portal token not configured
        403: Permission denied for group
    """
    logger.info(f"📤 Posting to portal for: {request.customer_id}")
    
    # Get Portal service
    portal_service = get_portal_service(token_manager)
    
    if request.preview_mode:
        logger.info("  (preview mode - not actually posting)")
        # Generate preview only
        from datetime import datetime
        preview = portal_service.preview_report(
            request.content,
            request.customer_id,
            datetime.now().strftime("%Y-%m")
        )
        return PortalPostResult(
            success=True,
            portal_url="",  # No URL for preview
            post_id="preview"
        )
    
    # Format and post
    from datetime import datetime
    formatted = portal_service.format_report(
        request.content,
        request.customer_id,
        datetime.now().strftime("%Y-%m")
    )
    
    result = await portal_service.post_report(
        request.customer_id,
        formatted["html"],
        request.title or formatted["title"],
        request.case_number
    )
    
    return PortalPostResult(
        success=True,
        portal_url=result.get("url", ""),
        post_id=result.get("id", "")
    )


@router.post("/preview", response_model=PortalPreview)
async def preview_portal_post(
    request: PortalPostRequest,
    token_manager: TokenManager = Depends(get_token_manager)
):
    """
    Preview how content will look on portal
    
    Renders markdown to HTML without actually posting.
    """
    logger.info(f"👁️  Previewing portal content for: {request.customer_id}")
    
    # Get Portal service
    portal_service = get_portal_service(token_manager)
    
    # Generate preview
    from datetime import datetime
    preview = portal_service.preview_report(
        request.content,
        request.customer_id,
        datetime.now().strftime("%Y-%m")
    )
    
    return PortalPreview(
        html=preview["preview_html"],
        estimated_size=len(request.content)
    )


@router.get("/{customer_id}/group")
async def get_portal_group(customer_id: str):
    """
    Get portal group info for customer
    
    Returns group ID and permissions.
    """
    logger.info(f"🔍 Getting portal group for: {customer_id}")
    
    # TODO: Implement group lookup from customer config
    return {
        "customer_id": customer_id,
        "group_id": "customer-group-123",
        "can_post": True
    }
