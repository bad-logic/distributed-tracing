"""
    Controller for Product consumers 
"""

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
        return self.product_service.create_product(product)

    def handle_product_update(self, product: GeneralProductInterface) -> GeneralProductInterface:
        """ controller to update product """
        return self.product_service.update_product(product_id=product.Id, product=product)

    def handle_product_delete(self, product: GeneralProductInterface) -> str:
        """ controller to delete a product """
        return self.product_service.delete_product(product_id=product.Id)
