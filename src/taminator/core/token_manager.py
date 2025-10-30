"""
Token Manager - Secure Credential Storage

Badass features:
- Secure OS keyring storage (not environment variables)
- Token validation before use
- Automatic expiry detection
- No tokens ever in process list or logs
- Graceful fallback to encrypted file if keyring unavailable
"""

import keyring
import logging
import json
import threading
from enum import Enum
from typing import Optional, Dict
from datetime import datetime, timedelta
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

from .exceptions import AuthenticationError, ErrorCode, missing_token_error

logger = logging.getLogger(__name__)


def with_timeout(timeout_seconds):
    """Decorator to add timeout to function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                # Timeout occurred
                raise TimeoutError(f"Operation timed out after {timeout_seconds}s")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        return wrapper
    return decorator


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
    Secure token storage using OS keyring with encrypted file fallback
    
    Never stores tokens in:
    - Environment variables
    - Process arguments
    - Log files
    - Plain text config files
    
    Fallback strategy:
    1. Try OS keyring (with 2s timeout)
    2. If keyring unavailable/timeout, use encrypted file
    """
    
    SERVICE_NAME = "taminator"
    KEYRING_TIMEOUT = 2  # seconds
    
    def __init__(self):
        self._cache: Dict[TokenType, TokenInfo] = {}
        self._use_keyring = self._test_keyring()
        self._encrypted_storage_path = Path.home() / ".config" / "taminator" / "tokens.enc"
        self._encrypted_storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self._use_keyring:
            logger.info("🔐 TokenManager initialized with secure keyring storage")
        else:
            logger.warning("⚠️  Keyring unavailable, using encrypted file fallback")
    
    def _test_keyring(self) -> bool:
        """Test if keyring is available and responsive"""
        @with_timeout(self.KEYRING_TIMEOUT)
        def test():
            return keyring.get_password(self.SERVICE_NAME, "test")
        
        try:
            test()
            return True
        except TimeoutError:
            logger.warning("⚠️  Keyring timeout - falling back to encrypted file")
            return False
        except Exception as e:
            logger.warning(f"⚠️  Keyring unavailable ({e}) - falling back to encrypted file")
            return False
    
    def _get_encryption_key(self) -> bytes:
        """Get or create encryption key for file storage"""
        key_file = Path.home() / ".config" / "taminator" / ".key"
        key_file.parent.mkdir(parents=True, exist_ok=True)
        
        if key_file.exists():
            return key_file.read_bytes()
        
        # Generate new key
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        # Use machine ID as password base
        machine_id = self._get_machine_id()
        key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
        
        # Store key and salt
        key_data = {"key": key.decode(), "salt": base64.b64encode(salt).decode()}
        key_file.write_text(json.dumps(key_data))
        key_file.chmod(0o600)  # Owner read/write only
        
        return key
    
    def _get_machine_id(self) -> str:
        """Get a machine-specific identifier"""
        try:
            # Try /etc/machine-id first (Linux)
            machine_id_file = Path("/etc/machine-id")
            if machine_id_file.exists():
                return machine_id_file.read_text().strip()
        except:
            pass
        
        # Fallback to hostname
        import socket
        return socket.gethostname()
    
    def _read_encrypted_storage(self) -> Dict[str, str]:
        """Read tokens from encrypted file"""
        if not self._encrypted_storage_path.exists():
            return {}
        
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            encrypted_data = self._encrypted_storage_path.read_bytes()
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            logger.error(f"Failed to read encrypted storage: {e}")
            return {}
    
    def _write_encrypted_storage(self, tokens: Dict[str, str]) -> None:
        """Write tokens to encrypted file"""
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            data = json.dumps(tokens).encode()
            encrypted_data = fernet.encrypt(data)
            self._encrypted_storage_path.write_bytes(encrypted_data)
            self._encrypted_storage_path.chmod(0o600)  # Owner read/write only
        except Exception as e:
            logger.error(f"Failed to write encrypted storage: {e}")
            raise
    
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
        
        # Retrieve from keyring or encrypted file
        if self._use_keyring:
            @with_timeout(self.KEYRING_TIMEOUT)
            def get_from_keyring():
                return keyring.get_password(self.SERVICE_NAME, token_type.value)
            
            try:
                token = get_from_keyring()
            except (TimeoutError, Exception) as e:
                logger.warning(f"Keyring failed, switching to encrypted file: {e}")
                self._use_keyring = False
                token = self._read_encrypted_storage().get(token_type.value)
        else:
            token = self._read_encrypted_storage().get(token_type.value)
        
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
        
        # Store in keyring or encrypted file
        if self._use_keyring:
            @with_timeout(self.KEYRING_TIMEOUT)
            def set_in_keyring():
                keyring.set_password(self.SERVICE_NAME, token_type.value, token)
            
            try:
                set_in_keyring()
            except (TimeoutError, Exception) as e:
                logger.warning(f"Keyring failed, switching to encrypted file: {e}")
                self._use_keyring = False
                tokens = self._read_encrypted_storage()
                tokens[token_type.value] = token
                self._write_encrypted_storage(tokens)
        else:
            tokens = self._read_encrypted_storage()
            tokens[token_type.value] = token
            self._write_encrypted_storage(tokens)
        
        # Update cache
        self._cache[token_type] = TokenInfo(
            token, token_type, expires_at=expires_at
        )
        
        storage_type = "keyring" if self._use_keyring else "encrypted file"
        logger.info(f"✅ Stored {token_type.value} token securely ({storage_type})")
    
    def delete_token(self, token_type: TokenType) -> None:
        """Remove token from secure storage"""
        if self._use_keyring:
            try:
                keyring.delete_password(self.SERVICE_NAME, token_type.value)
            except keyring.errors.PasswordDeleteError:
                # Token doesn't exist, that's fine
                pass
        else:
            tokens = self._read_encrypted_storage()
            if token_type.value in tokens:
                del tokens[token_type.value]
                self._write_encrypted_storage(tokens)
        
        if token_type in self._cache:
            del self._cache[token_type]
        logger.info(f"🗑️  Deleted {token_type.value} token")
    
    def has_token(self, token_type: TokenType) -> bool:
        """Check if token exists (doesn't validate)"""
        try:
            if self._use_keyring:
                token = keyring.get_password(self.SERVICE_NAME, token_type.value)
            else:
                token = self._read_encrypted_storage().get(token_type.value)
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


