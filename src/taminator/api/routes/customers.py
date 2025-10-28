"""
Customer Management API

Badass features:
- List/get/create customers
- Smart caching
- Validation before execution
- Dashboard data aggregation
"""

from fastapi import APIRouter, Depends
from typing import List
import logging

from ...models.customer import Customer, CustomerCreate, CustomerStats
from ...services import CustomerService, get_customer_service

router = APIRouter(prefix="/api/customers", tags=["customers"])
logger = logging.getLogger(__name__)


# Endpoints

@router.get("/", response_model=List[Customer])
async def list_customers(
    service: CustomerService = Depends(get_customer_service)
):
    """
    Get all customers
    
    Returns cached list for performance.
    Cache invalidated on customer add/update.
    """
    logger.info("📋 Listing all customers")
    return await service.list_customers()


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Get customer by ID
    
    Args:
        customer_id: Customer slug (e.g., 'acme')
        
    Raises:
        404: Customer not found
    """
    logger.info(f"🔍 Getting customer: {customer_id}")
    return await service.get_customer(customer_id)


@router.post("/", response_model=Customer, status_code=201)
async def create_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Create new customer
    
    Args:
        customer: Customer data with validation
        
    Returns:
        Created customer with generated ID
        
    Raises:
        422: Validation error
        409: Customer already exists
    """
    logger.info(f"➕ Creating customer: {customer.name}")
    return await service.create_customer(customer)


@router.get("/{customer_id}/stats", response_model=CustomerStats)
async def get_customer_stats(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Get customer statistics
    
    Returns aggregated metrics for dashboard display.
    """
    logger.info(f"📊 Getting stats for: {customer_id}")
    return await service.get_stats(customer_id)


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: str,
    service: CustomerService = Depends(get_customer_service)
):
    """
    Delete customer
    
    Args:
        customer_id: Customer to delete
        
    Raises:
        404: Customer not found
    """
    logger.info(f"🗑️  Deleting customer: {customer_id}")
    await service.delete_customer(customer_id)
    return None

