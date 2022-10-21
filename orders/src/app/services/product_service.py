"""

    Service for products

"""

from typing import List
from fastapi import HTTPException, status as status_code
from sqlalchemy.orm import sessionmaker, Session

from db import DBConnector
from utils import Logger
from ..interfaces import GeneralProductInterface
from ..models import ProductTable

connector = DBConnector()
connector.connect()
session_maker = sessionmaker(bind=connector.get_engine())


class ProductService:

    """

        Service for product
    """

    def __init__(self) -> None:
        self.logger = Logger().get_logger()

    def create_product(self, product: GeneralProductInterface) -> GeneralProductInterface:
        """ service to create an product """
        with session_maker() as session:
            new_product = ProductTable(
                Id=product.Id,
                Name=product.Name,
                Price=product.Price,
                UserId=product.UserId,
                ShortDesc=product.ShortDesc,
                CreatedAt=product.CreatedAt,
                UpdatedAt=product.UpdatedAt
            )
            session.add(new_product)
            session.commit()
            new_product = new_product.dict()
        return new_product

    def get_products(self, offset: int = 1, limit: int = 10) -> List[GeneralProductInterface]:
        """ service to fetch products """
        with session_maker() as session:
            products = session.query(ProductTable).offset(
                (offset - 1) * limit).limit(limit).all()
            products = [product.dict() for product in products]
        return products

    def get_product_model_object(self, product_id: int, session: Session) -> GeneralProductInterface:
        """ service to fetch an sqlalchemy product object """
        order = session.query(ProductTable).filter(
            ProductTable.id == product_id).first()
        if order is None:
            raise HTTPException(
                status_code=status_code.HTTP_404_NOT_FOUND, detail=f"order with ID {product_id} not found")
        return order

    def get_product(self, product_id: int) -> GeneralProductInterface:
        """ service to fetch a product """
        with session_maker() as session:
            product = self.get_product_model_object(product_id, session)
            product = product.dict()
        return product

    def update_product(self, product_id: int, update_product: GeneralProductInterface) -> GeneralProductInterface:
        """ service to update the product """
        with session_maker() as session:
            product = self.get_product_model_object(product_id, session)
            product.Name = update_product.Name
            product.Price = update_product.Price
            product.UserId = update_product.UserId
            product.ShortDesc = update_product.ShortDesc
            product.CreatedAt = update_product.CreatedAt
            product.UpdatedAt = update_product.UpdatedAt
            session.add(product)
            session.commit()
            product = product.dict()
        return product

    def delete_product(self, product_id: int) -> None:
        """ service to delete a product """
        with session_maker() as session:
            product = self.get_product_model_object(product_id, session)
            session.delete(product)
            session.commit()
