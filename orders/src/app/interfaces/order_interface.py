from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel


class StatusEnum(Enum):
    """Enum for status of the order"""
    ORDER_PLACED = 'ORDER_PLACED'
    ORDER_ON_ROUTE = 'ORDER_ON_ROUTE'
    ORDER_DELIVERED = 'ORDER_DELIVERED'


class CreateOrderInterface(BaseModel):
    """Represents a interface for creating orders"""
    User: int
    Product: List[int]
    Status: StatusEnum = StatusEnum.ORDER_PLACED
    Address: str


class GetOrderInterface(BaseModel):
    """Represents a interface for fetching orders"""
    Id: int
    User: int
    Product: List[int]
    Status: StatusEnum
    Address: str
    CreatedAt: datetime
    UpdatedAt: datetime
