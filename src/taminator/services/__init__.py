"""
Taminator Business Logic Services

Service layer that implements core business logic.
Each service is responsible for a specific domain.
"""

from .customer_service import CustomerService, get_customer_service

__all__ = [
    "CustomerService",
    "get_customer_service",
]


