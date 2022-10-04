import datetime
from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, Enum as SqlColumnEnum
from sqlalchemy.orm import declarative_base
from ..interfaces import StatusEnum

Base = declarative_base()


class OrderTable(Base):
    """Represents a order schema for the order Table."""

    __tablename__ = "order"
    Id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    User = Column(Integer, nullable=False)
    Product = Column(JSON, nullable=False, default=[])
    Status = Column(SqlColumnEnum(StatusEnum), nullable=False,
                    default=StatusEnum.ORDER_PLACED.value)
    Address = Column(String(50), nullable=False)
    CreatedAt = Column(TIMESTAMP, nullable=False,
                       default=datetime.datetime.now)
    UpdatedAt = Column(TIMESTAMP, nullable=False,
                       onupdate=datetime.datetime.now)

    def dict(self):
        """ returns the dictionary object for the order table """
        return {
            "Id": self.Id,
            "User": self.User,
            "Product": self.Product,
            "Status": self.Status.value,
            "Address": self.Address,
            "CreatedAt": self.CreatedAt,
            "UpdatedAt": self.UpdatedAt,
        }
