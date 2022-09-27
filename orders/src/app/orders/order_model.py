from enum import Enum
from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, JSON, Enum as SqlColumnEnum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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


class OrderTable(Base):
    """Represents a order schema for the orders Table."""

    __tablename__ = "order"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user = Column(Integer, nullable=False)
    product = Column(JSON, nullable=False, default=[])
    status = Column(SqlColumnEnum(StatusEnum),
                    default=StatusEnum.ORDER_PLACED.value)
    address = Column(String(50), nullable=False)

    def dict(self):
        """ returns the dictionary object for the order table """
        return {
            "id": self.id,
            "user": self.user,
            "product": self.product,
            "status": self.status.name,
            "address": self.address
        }
