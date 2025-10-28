"""
Google Authentication API Routes

Endpoints for Google OAuth2 Sign-In
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import Dict, Any
from typing import Optional
import logging

from ...core.google_auth import get_google_auth_manager
from ...core.token_manager import TokenManager, get_token_manager

router = APIRouter(prefix="/api/google", tags=["google-auth"])
logger = logging.getLogger(__name__)


# Models

class OAuthFlowStart(BaseModel):
    """OAuth flow start response"""
    auth_url: str
    port: int
    message: str


class OAuthFlowComplete(BaseModel):
    """OAuth flow completion request"""
    authorization_response: str
    port: int = 8080


class GoogleAuthStatus(BaseModel):
    """Google authentication status"""
    credentials_configured: bool
    authenticated: bool
    user_email: Optional[str]
    user_name: Optional[str]
    token_path: str
    credentials_path: str


class UserInfo(BaseModel):
    """Google user information"""
    email: str
    name: str
    picture: Optional[str]
    verified_email: bool
    given_name: Optional[str]
    family_name: Optional[str]


# Endpoints

@router.get("/status", response_model=GoogleAuthStatus)
async def get_auth_status(
    token_manager: TokenManager = Depends(get_token_manager)
):
    """
    Get Google authentication status
    
    Returns:
        Authentication status with user info if authenticated
    """
    logger.info("📊 Getting Google auth status")
    
    auth_manager = get_google_auth_manager(token_manager)
    status = auth_manager.get_status()
    
    return GoogleAuthStatus(**status)


@router.post("/auth/start", response_model=OAuthFlowStart)
async def start_auth_flow(port: int = 8080):
    """
    Start Google OAuth2 flow
    
    Args:
        port: Local port for OAuth callback (default 8080)
        
    Returns:
        Authorization URL for user to visit
        
    Raises:
        400: OAuth credentials not configured
    """
    logger.info(f"🔐 Starting Google OAuth flow on port {port}")
    
    auth_manager = get_google_auth_manager()
    
    if not auth_manager.has_credentials():
        raise HTTPException(
            status_code=400,
            detail={
                "error": "google_oauth_not_configured",
                "message": "Google OAuth credentials not configured",
                "instructions": (
                    "1. Go to https://console.cloud.google.com/apis/credentials\n"
                    "2. Create OAuth 2.0 Client ID (Desktop app)\n"
                    "3. Download credentials JSON\n"
                    f"4. Save to: {auth_manager.credentials_path}"
                )
            }
        )
    
    try:
        auth_url = auth_manager.start_oauth_flow(port=port)
        
        return OAuthFlowStart(
            auth_url=auth_url,
            port=port,
            message="Open this URL in your browser to sign in with Google"
        )
    
    except Exception as e:
        logger.error(f"❌ Failed to start OAuth flow: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "oauth_flow_failed", "message": str(e)}
        )


@router.post("/auth/complete", response_model=UserInfo)
async def complete_auth_flow(request: OAuthFlowComplete):
    """
    Complete Google OAuth2 flow
    
    Args:
        request: Authorization response with code
        
    Returns:
        User information from Google account
        
    Raises:
        400: Invalid authorization code or non-Red Hat email
        500: OAuth flow completion failed
    """
    logger.info("🔐 Completing Google OAuth flow")
    
    auth_manager = get_google_auth_manager()
    
    try:
        user_info = auth_manager.complete_oauth_flow(
            authorization_response=request.authorization_response,
            port=request.port
        )
        
        logger.info(f"✅ OAuth completed for: {user_info.get('email')}")
        
        return UserInfo(**user_info)
    
    except ValueError as e:
        # Domain restriction or invalid code
        logger.warning(f"⚠️  OAuth validation failed: {e}")
        raise HTTPException(
            status_code=400,
            detail={"error": "oauth_validation_failed", "message": str(e)}
        )
    
    except Exception as e:
        logger.error(f"❌ OAuth completion failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "oauth_completion_failed", "message": str(e)}
        )


@router.get("/user", response_model=UserInfo)
async def get_user():
    """
    Get authenticated user information
    
    Returns:
        User information from Google account
        
    Raises:
        401: Not authenticated
    """
    logger.info("👤 Getting user info")
    
    auth_manager = get_google_auth_manager()
    
    if not auth_manager.has_valid_token():
        raise HTTPException(
            status_code=401,
            detail={"error": "not_authenticated", "message": "Please sign in with Google"}
        )
    
    try:
        user_info = auth_manager.get_user_info()
        return UserInfo(**user_info)
    
    except Exception as e:
        logger.error(f"❌ Failed to get user info: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "user_info_failed", "message": str(e)}
        )


@router.post("/auth/revoke")
async def revoke_auth():
    """
    Revoke Google authentication and sign out
    
    Returns:
        Success confirmation
    """
    logger.info("🔓 Revoking Google auth")
    
    auth_manager = get_google_auth_manager()
    
    try:
        auth_manager.revoke_token()
        
        return {
            "success": True,
            "message": "Successfully signed out from Google"
        }
    
    except Exception as e:
        logger.error(f"❌ Failed to revoke auth: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "revoke_failed", "message": str(e)}
        )


@router.get("/gmail/unread")
async def get_unread_emails(max_results: int = Query(10, ge=1, le=100)):
    """
    Get unread emails from Gmail
    
    Args:
        max_results: Max emails to return (1-100)
        
    Returns:
        List of unread email summaries
        
    Raises:
        401: Not authenticated
        403: Gmail access not granted
    """
    logger.info(f"📧 Getting {max_results} unread emails")
    
    auth_manager = get_google_auth_manager()
    
    if not auth_manager.has_valid_token():
        raise HTTPException(
            status_code=401,
            detail={"error": "not_authenticated", "message": "Please sign in with Google"}
        )
    
    try:
        gmail = auth_manager.get_gmail_service()
        
        # Query unread messages
        results = gmail.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        # Get message details
        email_list = []
        for msg in messages:
            msg_data = gmail.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
            
            email_list.append({
                'id': msg['id'],
                'from': headers.get('From'),
                'subject': headers.get('Subject'),
                'date': headers.get('Date'),
                'snippet': msg_data.get('snippet')
            })
        
        return {
            'count': len(email_list),
            'emails': email_list
        }
    
    except Exception as e:
        logger.error(f"❌ Failed to get emails: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "gmail_access_failed", "message": str(e)}
        )

