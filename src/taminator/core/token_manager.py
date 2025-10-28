"""
Token Manager - Secure Credential Storage

Badass features:
- Secure OS keyring storage (not environment variables)
- Token validation before use
- Automatic expiry detection
- No tokens ever in process list or logs
"""

import keyring
import logging
from enum import Enum
from typing import Optional, Dict
from datetime import datetime, timedelta

from .exceptions import AuthenticationError, ErrorCode, missing_token_error

logger = logging.getLogger(__name__)


class TokenType(str, Enum):
    """Supported authentication token types"""
    JIRA = "jira"
    PORTAL = "portal"
    GOOGLE_OAUTH = "google_oauth"  # Google OAuth2 credentials


class TokenInfo:
    """Token metadata and validation"""
    def __init__(
        self,
        token: str,
        token_type: TokenType,
        created_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None
    ):
        self.token = token
        self.token_type = token_type
        self.created_at = created_at or datetime.now()
        self.expires_at = expires_at
    
    def is_expired(self) -> bool:
        """Check if token is expired"""
        if not self.expires_at:
            return False  # No expiry set
        return datetime.now() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if token is valid"""
        if not self.token or len(self.token) < 10:
            return False
        if self.is_expired():
            return False
        return True


class TokenManager:
    """
    Secure token storage using OS keyring
    
    Never stores tokens in:
    - Environment variables
    - Process arguments
    - Log files
    - Plain text config files
    """
    
    SERVICE_NAME = "taminator"
    
    def __init__(self):
        self._cache: Dict[TokenType, TokenInfo] = {}
        logger.info("🔐 TokenManager initialized with secure keyring storage")
    
    def get_token(self, token_type: TokenType) -> str:
        """
        Get token from secure storage
        
        Args:
            token_type: Type of token to retrieve
            
        Returns:
            Token string
            
        Raises:
            AuthenticationError: If token missing or invalid
        """
        # Check cache first
        if token_type in self._cache:
            token_info = self._cache[token_type]
            if token_info.is_valid():
                return token_info.token
            else:
                # Remove expired token
                del self._cache[token_type]
                if token_info.is_expired():
                    raise AuthenticationError(
                        ErrorCode.AUTH_TOKEN_EXPIRED,
                        f"{token_type.value} token has expired",
                        details={
                            "token_type": token_type.value,
                            "expired_at": token_info.expires_at.isoformat()
                        }
                    )
        
        # Retrieve from keyring
        token = keyring.get_password(self.SERVICE_NAME, token_type.value)
        
        if not token:
            raise missing_token_error(token_type.value)
        
        # Validate and cache
        token_info = TokenInfo(token, token_type)
        if not token_info.is_valid():
            raise AuthenticationError(
                ErrorCode.AUTH_TOKEN_INVALID,
                f"{token_type.value} token is invalid",
                details={"token_type": token_type.value}
            )
        
        self._cache[token_type] = token_info
        logger.debug(f"✅ Retrieved {token_type.value} token from keyring")
        return token
    
    def set_token(
        self,
        token_type: TokenType,
        token: str,
        expires_in_days: Optional[int] = None
    ) -> None:
        """
        Store token securely
        
        Args:
            token_type: Type of token
            token: Token string
            expires_in_days: Optional expiry in days
        """
        if not token or len(token) < 10:
            raise ValueError("Token is too short or empty")
        
        # Calculate expiry
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now() + timedelta(days=expires_in_days)
        
        # Store in keyring
        keyring.set_password(self.SERVICE_NAME, token_type.value, token)
        
        # Update cache
        self._cache[token_type] = TokenInfo(
            token, token_type, expires_at=expires_at
        )
        
        logger.info(f"✅ Stored {token_type.value} token securely")
    
    def delete_token(self, token_type: TokenType) -> None:
        """Remove token from secure storage"""
        try:
            keyring.delete_password(self.SERVICE_NAME, token_type.value)
            if token_type in self._cache:
                del self._cache[token_type]
            logger.info(f"🗑️  Deleted {token_type.value} token")
        except keyring.errors.PasswordDeleteError:
            # Token doesn't exist, that's fine
            pass
    
    def has_token(self, token_type: TokenType) -> bool:
        """Check if token exists (doesn't validate)"""
        try:
            token = keyring.get_password(self.SERVICE_NAME, token_type.value)
            return token is not None and len(token) > 0
        except Exception:
            return False
    
    def validate_token(self, token_type: TokenType) -> bool:
        """
        Validate token without raising exception
        
        Returns:
            True if valid, False otherwise
        """
        try:
            token = self.get_token(token_type)
            return bool(token)
        except AuthenticationError:
            return False
    
    def clear_all(self) -> None:
        """Clear all tokens (for testing or reset)"""
        for token_type in TokenType:
            self.delete_token(token_type)
        self._cache.clear()
        logger.warning("⚠️  All tokens cleared")
    
    def get_status(self) -> Dict[str, bool]:
        """Get status of all token types"""
        return {
            token_type.value: self.has_token(token_type)
            for token_type in TokenType
        }


# Global singleton instance
_token_manager: Optional[TokenManager] = None


def get_token_manager() -> TokenManager:
    """Get global TokenManager instance (dependency injection)"""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager


