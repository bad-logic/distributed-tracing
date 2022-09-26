from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, JSON, Enum as SqlColumnEnum
from sqlalchemy.orm import declarative_base
from typing import Optional
from enum import Enum
from typing import List

Base = declarative_base()


class StatusEnum(Enum):
    placed = 'ORDER_PLACED'
    onRoute = 'ORDER_ON_ROUTE'
    delivered = 'ORDER_DELIVERED'


class OrderModel(BaseModel):
    """Represents a order model for the orders API's"""
    id: Optional[int]
    user: int
    product: List[int]
    status: StatusEnum = StatusEnum.placed
    address: str


class OrderTable(Base):
    """Represents a order model for the orders Table."""

    __tablename__ = "order"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user = Column(Integer, nullable=False)
    product = Column(JSON, nullable=False, default=[])
    status = Column(SqlColumnEnum(StatusEnum), default=StatusEnum.placed.value)
    address = Column(String(50), nullable=False)
