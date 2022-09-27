from sqlalchemy import Column, Integer, String, JSON, Enum as SqlColumnEnum
from sqlalchemy.orm import declarative_base
from ..interfaces import StatusEnum

Base = declarative_base()


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
            "status": self.status.value,
            "address": self.address
        }
