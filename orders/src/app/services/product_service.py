"""

    Service for products

"""

from typing import List
from fastapi import HTTPException, status as status_code
from sqlalchemy.orm import sessionmaker, Session
from opentelemetry import trace

from db import DBConnector
from utils import TelemetryLogger, SERVICE_NAME, LogLevelEnum
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
        self.otlp_logger = TelemetryLogger()
        self.tracer = trace.get_tracer(SERVICE_NAME)

    def create_product(self, product: GeneralProductInterface) -> GeneralProductInterface:
        """ service to create an product """
        with self.tracer.start_as_current_span("ProductService.create_product") as curr_span:
            self.otlp_logger.log(curr_span,
                                 f"storing {product} in the database")
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
            self.otlp_logger.log(curr_span,
                                 "product stored in database")
            return new_product

    def get_products(self, offset: int = 1, limit: int = 10) -> List[GeneralProductInterface]:
        """ service to fetch products """
        with self.tracer.start_as_current_span("ProductService.get_products") as curr_span:
            self.otlp_logger.log(curr_span,
                                 "querying database for products")
            with session_maker() as session:
                products = session.query(ProductTable).offset(
                    (offset - 1) * limit).limit(limit).all()
                products = [product.dict() for product in products]

            self.otlp_logger.log(curr_span,
                                 "products fetched from database")
            return products

    def get_product_model_object(self, product_id: int, session: Session) -> GeneralProductInterface:
        """ service to fetch an sqlalchemy product object """
        with self.tracer.start_as_current_span("ProductService.get_product_model_object") as curr_span:
            self.otlp_logger.log(curr_span,
                                 f"querying database for product {product_id}")
            product = session.query(ProductTable).filter(
                ProductTable.Id == product_id).first()
            if product is None:
                self.otlp_logger.error(curr_span, Exception(f"product {product_id} not found in database"), LogLevelEnum.INFO,
                                       f"response ended with {status_code.HTTP_404_NOT_FOUND} status code")
                raise HTTPException(
                    status_code=status_code.HTTP_404_NOT_FOUND, detail=f"product with ID {product_id} not found")
            self.otlp_logger.log(curr_span,
                                 "product fetched from database")
            return product

    def get_product(self, product_id: int) -> GeneralProductInterface:
        """ service to fetch a product """
        with self.tracer.start_as_current_span("ProductService.get_product") as _:
            with session_maker() as session:
                product = self.get_product_model_object(product_id, session)
                product = product.dict()
            return product

    def update_product(self, product_id: int, update_product: GeneralProductInterface) -> GeneralProductInterface:
        """ service to update the product """
        with self.tracer.start_as_current_span("ProductService.update_product") as curr_span:
            self.otlp_logger.log(curr_span,
                                 f"updating product {product_id}")
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
            self.otlp_logger.log(curr_span,
                                 "saved the updated product in the database")
            return product

    def delete_product(self, product_id: int) -> None:
        """ service to delete a product """
        with self.tracer.start_as_current_span("ProductService.delete_product") as curr_span:
            with session_maker() as session:
                product = self.get_product_model_object(product_id, session)
                session.delete(product)
                session.commit()
            self.otlp_logger.log(curr_span,
                                 f"successfully deleted product {product_id}")
