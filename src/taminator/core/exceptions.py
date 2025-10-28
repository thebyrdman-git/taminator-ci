"""
Taminator Exception System - Structured Error Handling

No more text parsing failures. Every error has:
- Specific error code
- User-friendly message
- Actionable details
- Automatic HTTP status mapping
"""

from enum import Enum
from typing import Optional, Dict, Any


class ErrorCode(str, Enum):
    """Specific error codes for precise error handling"""
    
    # Authentication & Authorization
    AUTH_TOKEN_MISSING = "auth_token_missing"
    AUTH_TOKEN_EXPIRED = "auth_token_expired"
    AUTH_TOKEN_INVALID = "auth_token_invalid"
    AUTH_UNAUTHORIZED = "auth_unauthorized"
    
    # Customer Management
    CUSTOMER_NOT_FOUND = "customer_not_found"
    CUSTOMER_ALREADY_EXISTS = "customer_already_exists"
    CUSTOMER_INVALID_CONFIG = "customer_invalid_config"
    CUSTOMER_INVALID_NAME = "customer_invalid_name"
    
    # JIRA Integration
    JIRA_API_ERROR = "jira_api_error"
    JIRA_AUTH_FAILED = "jira_auth_failed"
    JIRA_PERMISSION_DENIED = "jira_permission_denied"
    JIRA_RATE_LIMIT = "jira_rate_limit"
    JIRA_CONNECTION_ERROR = "jira_connection_error"
    JIRA_NETWORK_ERROR = "jira_network_error"
    JIRA_ISSUE_NOT_FOUND = "jira_issue_not_found"
    
    # Portal Integration
    PORTAL_API_ERROR = "portal_api_error"
    PORTAL_AUTH_FAILED = "portal_auth_failed"
    PORTAL_PERMISSION_DENIED = "portal_permission_denied"
    PORTAL_NETWORK_ERROR = "portal_network_error"
    PORTAL_UNAUTHORIZED = "portal_unauthorized"
    PORTAL_GROUP_NOT_FOUND = "portal_group_not_found"
    PORTAL_POST_FAILED = "portal_post_failed"
    
    # File System
    FILE_NOT_FOUND = "file_not_found"
    FILE_PERMISSION_DENIED = "file_permission_denied"
    FILE_CORRUPTED = "file_corrupted"
    FILE_ALREADY_EXISTS = "file_already_exists"
    
    # Validation
    VALIDATION_ERROR = "validation_error"
    INVALID_INPUT = "invalid_input"
    MISSING_REQUIRED_FIELD = "missing_required_field"
    
    # System
    SERVICE_UNAVAILABLE = "service_unavailable"
    INTERNAL_ERROR = "internal_error"
    CONFIGURATION_ERROR = "configuration_error"


class TaminatorException(Exception):
    """
    Base exception for all Taminator errors
    
    Provides structured error responses with specific codes,
    user-friendly messages, and actionable details.
    """
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None,
        status_code: int = 400
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        self.retry_after = retry_after
        self.status_code = status_code
        super().__init__(message)
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict for API responses"""
        return {
            "error": {
                "code": self.code.value,
                "message": self.message,
                "details": self.details,
                "retry_after": self.retry_after
            }
        }
    
    def __str__(self) -> str:
        return f"[{self.code.value}] {self.message}"


# Specific exception classes for common scenarios

class AuthenticationError(TaminatorException):
    """Authentication-related errors"""
    def __init__(self, code: ErrorCode, message: str, **kwargs):
        super().__init__(code, message, status_code=401, **kwargs)


class AuthorizationError(TaminatorException):
    """Authorization-related errors"""
    def __init__(self, code: ErrorCode, message: str, **kwargs):
        super().__init__(code, message, status_code=403, **kwargs)


class NotFoundError(TaminatorException):
    """Resource not found errors"""
    def __init__(self, code: ErrorCode, message: str, **kwargs):
        super().__init__(code, message, status_code=404, **kwargs)


class ValidationError(TaminatorException):
    """Input validation errors"""
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        details = {"field": field} if field else {}
        details.update(kwargs.get("details", {}))
        super().__init__(
            ErrorCode.VALIDATION_ERROR,
            message,
            details=details,
            status_code=422
        )


class RateLimitError(TaminatorException):
    """Rate limit exceeded errors"""
    def __init__(self, message: str, retry_after: int, **kwargs):
        super().__init__(
            ErrorCode.JIRA_RATE_LIMIT,
            message,
            retry_after=retry_after,
            status_code=429,
            **kwargs
        )


class ServiceError(TaminatorException):
    """Internal service errors"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            ErrorCode.INTERNAL_ERROR,
            message,
            status_code=500,
            **kwargs
        )


# Helper functions for common error scenarios

def missing_token_error(token_type: str) -> AuthenticationError:
    """Create error for missing authentication token"""
    return AuthenticationError(
        ErrorCode.AUTH_TOKEN_MISSING,
        f"{token_type} token not configured",
        details={
            "token_type": token_type,
            "help": f"Configure {token_type} token in Settings → Authentication",
            "doc_url": "/docs/authentication"
        }
    )


def customer_not_found_error(customer_id: str) -> NotFoundError:
    """Create error for customer not found"""
    return NotFoundError(
        ErrorCode.CUSTOMER_NOT_FOUND,
        f"Customer '{customer_id}' not found",
        details={
            "customer_id": customer_id,
            "help": "Check customer ID or add customer in Onboard tab"
        }
    )


def jira_connection_error(original_error: Exception) -> TaminatorException:
    """Create error for JIRA connection failure"""
    return TaminatorException(
        ErrorCode.JIRA_CONNECTION_ERROR,
        "Failed to connect to JIRA API",
        details={
            "error": str(original_error),
            "help": "Check VPN connection and JIRA token validity"
        },
        status_code=502
    )


def external_api_error(
    service_name: str,
    error_code: ErrorCode,
    message: str,
    original_error: Optional[Exception] = None,
    **kwargs
) -> TaminatorException:
    """
    Create error for external API failures
    
    Args:
        service_name: Name of the service (JIRA, Portal, etc.)
        error_code: Specific error code
        message: User-friendly error message
        original_error: Original exception (if any)
        **kwargs: Additional details
        
    Returns:
        TaminatorException with structured error info
    """
    details = {
        "service": service_name,
        **kwargs
    }
    
    if original_error:
        details["original_error"] = str(original_error)
    
    return TaminatorException(
        error_code,
        message,
        details=details,
        status_code=502
    )


def rate_limit_error(
    service_name: str,
    retry_after: int,
    details: Optional[Dict[str, Any]] = None
) -> RateLimitError:
    """
    Create error for rate limit exceeded
    
    Args:
        service_name: Name of the service
        retry_after: Seconds to wait before retry
        details: Additional error details
        
    Returns:
        RateLimitError with retry timing
    """
    return RateLimitError(
        f"{service_name} rate limit exceeded. Retry after {retry_after} seconds.",
        retry_after=retry_after,
        details=details or {}
    )


