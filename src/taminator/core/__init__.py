"""
Taminator Core Infrastructure

Badass components:
- TokenManager: Secure credential storage
- ConfigManager: Smart configuration handling
- CacheManager: Intelligent caching layer
- Exceptions: Structured error handling
"""

from .exceptions import (
    TaminatorException,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServiceError,
    ErrorCode,
    missing_token_error,
    customer_not_found_error,
    jira_connection_error,
)

from .token_manager import (
    TokenManager,
    TokenType,
    TokenInfo,
    get_token_manager,
)

__all__ = [
    # Exceptions
    "TaminatorException",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServiceError",
    "ErrorCode",
    "missing_token_error",
    "customer_not_found_error",
    "jira_connection_error",
    # Token Management
    "TokenManager",
    "TokenType",
    "TokenInfo",
    "get_token_manager",
]


