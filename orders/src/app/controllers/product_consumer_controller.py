"""
    Controller for Product consumers 
"""
from fastapi import HTTPException, status as status_code
from opentelemetry import trace
from ..interfaces import GeneralProductInterface
from ..services import ProductService
from utils import TelemetryLogger, SERVICE_NAME, LogLevelEnum


class ProductConsumerController:
    """

        Controller for Product consumers
    """

    def __init__(self):
        self.product_service = ProductService()
        self.otlp_logger = TelemetryLogger()
        self.tracer = trace.get_tracer(SERVICE_NAME)

    def handle_product_creation(self, product: GeneralProductInterface) -> GeneralProductInterface:
        """ controller to create a product """
        with self.tracer.start_as_current_span("ProductConsumerController.handle_product_creation") as curr_span:
            try:
                product = self.product_service.create_product(product)
                self.otlp_logger.log(curr_span,
                                     f"product {product['Id']} created successfully")
                return product
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create product"
                ) from ex

    def handle_product_update(self, product: GeneralProductInterface) -> GeneralProductInterface:
        """ controller to update product """
        with self.tracer.start_as_current_span("ProductConsumerController.handle_product_update") as curr_span:
            try:
                product = self.product_service.update_product(
                    product_id=product.Id, update_product=product)
                self.otlp_logger.log(curr_span,
                                     f"product {product['Id']} updated successfully")
                return product
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update product"
                ) from ex

    def handle_product_delete(self, product: GeneralProductInterface) -> str:
        """ controller to delete a product """
        with self.tracer.start_as_current_span("ProductConsumerController.handle_product_delete") as curr_span:
            try:
                self.product_service.delete_product(
                    product_id=product.Id)
                self.otlp_logger.log(curr_span,
                                     f"product {product['Id']} updated successfully")
                return f"product {product.Id} deleted successfully"
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete product"
                ) from ex
