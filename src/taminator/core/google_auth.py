"""
Google Account Integration - OAuth2 Authentication

Features:
- Google Sign-In for TAMs
- Google Workspace integration (Gmail, Calendar, Drive)
- Secure OAuth2 token management with PKCE (RFC 7636)
- Red Hat domain restriction (@redhat.com)
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import secrets
import base64
import hashlib

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from .token_manager import TokenManager, TokenType

logger = logging.getLogger(__name__)


class GoogleAuthManager:
    """
    Google OAuth2 authentication manager
    
    Handles:
    - OAuth2 flow for Google Sign-In
    - Token refresh and storage
    - Red Hat domain restriction
    - Google API access (Gmail, Calendar, Drive)
    """
    
    # OAuth2 scopes for TAM workflows
    SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid',
        'https://www.googleapis.com/auth/gmail.compose',      # Create drafts
        'https://www.googleapis.com/auth/gmail.modify',       # Manage drafts
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/drive.file',         # Upload/download files
        'https://www.googleapis.com/auth/drive.readonly',
    ]
    
    # Red Hat domain restriction
    ALLOWED_DOMAIN = 'redhat.com'
    
    def __init__(
        self, 
        credentials_path: Path = None,
        token_manager: TokenManager = None
    ):
        """
        Initialize Google Auth Manager
        
        Args:
            credentials_path: Path to OAuth2 client credentials (from Google Cloud Console)
            token_manager: TokenManager instance (for unified token storage)
        """
        self.credentials_path = credentials_path or self._get_default_credentials_path()
        self.token_manager = token_manager  # Use unified TokenManager
        
        self.creds: Optional[Credentials] = None
        
        # PKCE state (RFC 7636 - security for public clients)
        self._code_verifier: Optional[str] = None
        self._code_challenge: Optional[str] = None
        
        logger.info("🔐 GoogleAuthManager initialized (PKCE enabled, TokenManager storage)")
    
    def _get_default_credentials_path(self) -> Path:
        """Get default path for OAuth2 credentials"""
        import platformdirs
        config_dir = Path(platformdirs.user_config_dir("taminator", "redhat"))
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "google_oauth_credentials.json"
    
    def _load_token_from_keyring(self) -> Optional[Credentials]:
        """Load Google OAuth token from OS keyring via TokenManager"""
        if not self.token_manager:
            return None
        
        try:
            token_json = self.token_manager.get_token(TokenType.GOOGLE_OAUTH)
            if token_json:
                return Credentials.from_authorized_user_info(
                    json.loads(token_json),
                    self.SCOPES
                )
        except Exception as e:
            logger.debug(f"No Google token in keyring: {e}")
        
        return None
    
    def has_credentials(self) -> bool:
        """Check if OAuth2 credentials are configured"""
        return self.credentials_path.exists()
    
    def has_valid_token(self) -> bool:
        """Check if user has valid authenticated token"""
        try:
            # Load from keyring via TokenManager
            self.creds = self._load_token_from_keyring()
            
            if not self.creds:
                return False
            
            # Check if token is still valid
            if self.creds.valid:
                return True
            
            # Try to refresh if expired
            if self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                self._save_token_to_keyring()
                return True
            
            return False
        
        except Exception as e:
            logger.warning(f"⚠️  Token validation failed: {e}")
            return False
    
    def _generate_pkce_pair(self) -> tuple[str, str]:
        """
        Generate PKCE code verifier and challenge (RFC 7636)
        
        PKCE (Proof Key for Code Exchange) protects against authorization code
        interception attacks. Required for public clients (desktop/mobile apps).
        
        Returns:
            (code_verifier, code_challenge) tuple
        """
        # Generate code verifier (43-128 chars, URL-safe)
        code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        ).decode('utf-8').rstrip('=')
        
        # Generate code challenge (SHA256 hash of verifier)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        logger.debug("🔐 Generated PKCE pair for OAuth flow")
        return code_verifier, code_challenge
    
    def start_oauth_flow(self, port: int = 8080) -> str:
        """
        Start OAuth2 flow with PKCE for user authentication
        
        Args:
            port: Local port for OAuth callback (default 8080)
            
        Returns:
            Authorization URL for user to visit
        """
        if not self.has_credentials():
            raise ValueError(
                "Google OAuth credentials not configured. "
                "Download from Google Cloud Console and save to: "
                f"{self.credentials_path}"
            )
        
        # Generate PKCE pair (RFC 7636 - security for public clients)
        self._code_verifier, self._code_challenge = self._generate_pkce_pair()
        
        # Create OAuth2 flow
        flow = Flow.from_client_secrets_file(
            str(self.credentials_path),
            scopes=self.SCOPES,
            redirect_uri=f'http://localhost:{port}'
        )
        
        # Generate authorization URL with PKCE
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            hd=self.ALLOWED_DOMAIN,  # Restrict to Red Hat domain
            code_challenge=self._code_challenge,
            code_challenge_method='S256'  # SHA256 hash
        )
        
        logger.info(f"🔗 OAuth flow started with PKCE on port {port}")
        return auth_url
    
    def complete_oauth_flow(self, authorization_response: str, port: int = 8080) -> Dict[str, str]:
        """
        Complete OAuth2 flow with PKCE verification
        
        Args:
            authorization_response: Full callback URL with code
            port: Port used in OAuth flow
            
        Returns:
            User info (email, name, etc.)
        """
        if not self._code_verifier:
            raise ValueError("OAuth flow not started. Call start_oauth_flow() first.")
        
        # Create flow
        flow = Flow.from_client_secrets_file(
            str(self.credentials_path),
            scopes=self.SCOPES,
            redirect_uri=f'http://localhost:{port}'
        )
        
        # Exchange authorization code for tokens with PKCE verifier
        flow.fetch_token(
            authorization_response=authorization_response,
            code_verifier=self._code_verifier  # PKCE verification
        )
        
        # Get credentials
        self.creds = flow.credentials
        
        # Clear PKCE state (one-time use)
        self._code_verifier = None
        self._code_challenge = None
        
        # Verify domain
        user_info = self.get_user_info()
        email = user_info.get('email', '')
        
        if not email.endswith(f'@{self.ALLOWED_DOMAIN}'):
            raise ValueError(
                f"Only @{self.ALLOWED_DOMAIN} accounts are allowed. "
                f"Got: {email}"
            )
        
        # Save token to keyring
        self._save_token_to_keyring()
        
        logger.info(f"✅ OAuth flow completed with PKCE for: {email}")
        return user_info
    
    def _save_token_to_keyring(self):
        """Save credentials to OS keyring via TokenManager"""
        if not self.creds or not self.token_manager:
            return
        
        # Store token JSON in keyring
        token_json = self.creds.to_json()
        self.token_manager.set_token(
            TokenType.GOOGLE_OAUTH,
            token_json,
            expires_in_days=None  # OAuth manages its own expiry
        )
        
        logger.info("💾 Google token saved to OS keyring")
    
    def get_user_info(self) -> Dict[str, str]:
        """
        Get authenticated user information
        
        Returns:
            User info dict with email, name, picture, etc.
        """
        if not self.creds or not self.creds.valid:
            raise ValueError("No valid credentials. Please authenticate first.")
        
        # Build OAuth2 service
        service = build('oauth2', 'v2', credentials=self.creds)
        
        # Get user info
        user_info = service.userinfo().get().execute()
        
        return {
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'picture': user_info.get('picture'),
            'verified_email': user_info.get('verified_email'),
            'given_name': user_info.get('given_name'),
            'family_name': user_info.get('family_name'),
        }
    
    def get_gmail_service(self):
        """Get authenticated Gmail API service"""
        if not self.creds or not self.creds.valid:
            raise ValueError("No valid credentials. Please authenticate first.")
        
        return build('gmail', 'v1', credentials=self.creds)
    
    def get_calendar_service(self):
        """Get authenticated Calendar API service"""
        if not self.creds or not self.creds.valid:
            raise ValueError("No valid credentials. Please authenticate first.")
        
        return build('calendar', 'v3', credentials=self.creds)
    
    def get_drive_service(self):
        """Get authenticated Drive API service"""
        if not self.creds or not self.creds.valid:
            raise ValueError("No valid credentials. Please authenticate first.")
        
        return build('drive', 'v3', credentials=self.creds)
    
    def revoke_token(self):
        """Revoke access token and delete stored credentials"""
        if self.creds:
            try:
                self.creds.revoke(Request())
                logger.info("✅ Token revoked from Google")
            except Exception as e:
                logger.warning(f"⚠️  Token revocation failed: {e}")
        
        # Delete token from keyring
        if self.token_manager:
            self.token_manager.delete_token(TokenType.GOOGLE_OAUTH)
            logger.info("🗑️  Google token deleted from OS keyring")
        
        self.creds = None
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get authentication status
        
        Returns:
            Status dict with auth state, user info, etc.
        """
        status = {
            'credentials_configured': self.has_credentials(),
            'authenticated': False,
            'user_email': None,
            'user_name': None,
            'storage': 'OS Keyring (via TokenManager)',
            'credentials_path': str(self.credentials_path),
        }
        
        if self.has_valid_token():
            try:
                user_info = self.get_user_info()
                status['authenticated'] = True
                status['user_email'] = user_info.get('email')
                status['user_name'] = user_info.get('name')
            except Exception as e:
                logger.warning(f"⚠️  Failed to get user info: {e}")
        
        return status


# Global singleton
_google_auth_manager: Optional[GoogleAuthManager] = None


def get_google_auth_manager(token_manager: TokenManager = None) -> GoogleAuthManager:
    """
    Get global GoogleAuthManager instance
    
    Args:
        token_manager: TokenManager instance for unified token storage
    """
    global _google_auth_manager
    
    if _google_auth_manager is None:
        # Import here to avoid circular dependency
        from .token_manager import get_token_manager
        
        if token_manager is None:
            token_manager = get_token_manager()
        
        _google_auth_manager = GoogleAuthManager(token_manager=token_manager)
    
    return _google_auth_manager

