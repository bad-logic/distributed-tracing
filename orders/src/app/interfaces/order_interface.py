from enum import Enum
from typing import List
from pydantic import BaseModel


class StatusEnum(Enum):
    ORDER_PLACED = 'ORDER_PLACED'
    ORDER_ON_ROUTE = 'ORDER_ON_ROUTE'
    ORDER_DELIVERED = 'ORDER_DELIVERED'


class CreateOrderInterface(BaseModel):
    """Represents a interface for creating orders"""
    user: int
    product: List[int]
    status: StatusEnum = StatusEnum.ORDER_PLACED
    address: str


class GetOrderInterface(BaseModel):
    """Represents a interface for fetching orders"""
    id: int
    user: int
    product: List[int]
    status: StatusEnum
    address: str
