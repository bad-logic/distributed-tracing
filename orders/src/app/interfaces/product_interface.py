from datetime import datetime
from pydantic import BaseModel


class GeneralProductInterface(BaseModel):
    """Represents a general interface for product"""
    Id: int
    UserId: int
    Name: str
    Price: float
    ShortDesc: str
    CreatedAt: datetime
    UpdatedAt: datetime
