"""
Customer Data Models

Type-safe representations of customer data with validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    """Base customer fields"""
    name: str = Field(..., min_length=1, max_length=100)
    account_number: str = Field(..., pattern=r"^\d+$")
    support_level: str = Field(default="premium")


class CustomerCreate(CustomerBase):
    """Customer creation request"""
    group_id: str = Field(..., min_length=1)
    discover_rfes: bool = Field(default=True)


class Customer(CustomerBase):
    """Full customer data"""
    id: str
    group_id: str
    open_rfes: int = 0
    open_bugs: int = 0
    last_updated: Optional[str] = None
    config_path: Optional[str] = None
    
    class Config:
        from_attributes = True


class CustomerStats(BaseModel):
    """Customer statistics for dashboard"""
    total_rfes: int
    total_bugs: int
    total_cases: int
    last_checked: Optional[str] = None


class CustomerDashboard(BaseModel):
    """Complete dashboard data for a customer"""
    customer: Customer
    stats: CustomerStats
    recent_activity: list = []


