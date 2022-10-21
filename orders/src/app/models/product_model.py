from sqlalchemy import Column, Integer, Float, String,  TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProductTable(Base):
    """Represents a product schema for the product Table."""

    __tablename__ = "product"
    Id = Column(Integer, primary_key=True, nullable=False)
    UserId = Column(Integer, nullable=False)
    Name = Column(String(128), nullable=False)
    Price = Column(Float, nullable=False)
    ShortDesc = Column(String(128), nullable=True)
    CreatedAt = Column(TIMESTAMP, nullable=False)
    UpdatedAt = Column(TIMESTAMP, nullable=False)

    def dict(self):
        """ returns the dictionary object for the order table """
        return {
            "Id": self.Id,
            "UserId": self.UserId,
            "Name": self.Name,
            "Price": self.Price,
            "ShortDesc": self.ShortDesc,
            "CreatedAt": self.CreatedAt,
            "UpdatedAt": self.UpdatedAt,
        }
