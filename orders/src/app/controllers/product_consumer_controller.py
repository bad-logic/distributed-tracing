"""
    Controller for Product consumers 
"""
from fastapi import HTTPException, status as status_code
import traceback
from utils import Logger
from ..interfaces import GeneralProductInterface
from ..services import ProductService


class ProductConsumerController:
    """

        Controller for Product consumers
    """

    def __init__(self):
        self.logger = Logger().get_logger()
        self.product_service = ProductService()

    def handle_product_creation(self, product: GeneralProductInterface) -> GeneralProductInterface:
        """ controller to create a product """
        try:
            return self.product_service.create_product(product)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create product"
            ) from ex

    def handle_product_update(self, product: GeneralProductInterface) -> GeneralProductInterface:
        """ controller to update product """
        try:
            return self.product_service.update_product(product_id=product.Id, update_product=product)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update product"
            ) from ex

    def handle_product_delete(self, product: GeneralProductInterface) -> str:
        """ controller to delete a product """
        try:
            return self.product_service.delete_product(product_id=product.Id)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete product"
            ) from ex
