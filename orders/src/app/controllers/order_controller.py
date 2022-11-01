"""
    Controller for orders 
"""

from typing import List

from opentelemetry import trace
from fastapi import HTTPException, status as status_code

from ..interfaces import CreateOrderInterface, GetOrderInterface, StatusEnum
from ..services import OrderService
from utils import TelemetryLogger, SERVICE_NAME, LogLevelEnum


class OrderController:
    """

        Controller for Order
    """

    def __init__(self):
        self.otlp_logger = TelemetryLogger()
        self.order_service = OrderService()
        self.tracer = trace.get_tracer(SERVICE_NAME)

    def handle_order_creation(self, order: CreateOrderInterface) -> GetOrderInterface:
        """ controller to create an order """
        with self.tracer.start_as_current_span("OrderController.handle_order_creation") as curr_span:
            try:
                order = self.order_service.create_order(order)
                self.otlp_logger.log(curr_span,
                                     f"order {order['Id']} created successfully")
                return order
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create order"
                ) from ex

    def handle_orders_fetch(self, offset: int = 1, limit: int = 10) -> List[GetOrderInterface]:
        """ controller to fetch orders """
        with self.tracer.start_as_current_span("OrderController.handle_orders_fetch") as curr_span:
            try:
                orders = self.order_service.get_orders(
                    offset=offset, limit=limit)
                self.otlp_logger.log(
                    curr_span, "orders fetched successfully")
                return orders
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch orders"
                ) from ex

    def handle_order_fetch(self, order_id: int) -> GetOrderInterface:
        """ controller to fetch an order """
        with self.tracer.start_as_current_span("OrderController.handle_order_fetch") as curr_span:
            try:
                order = self.order_service.get_order(order_id)
                self.otlp_logger.log(
                    curr_span, f"order {order_id} fetched successfully")
                return order
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch order"
                ) from ex

    def handle_order_address_patch(self, order_id: int, address: str) -> GetOrderInterface:
        """ controller to update address an order """
        with self.tracer.start_as_current_span("OrderController.handle_order_address_patch") as curr_span:
            try:
                order = self.order_service.update_order_address(
                    order_id=order_id, address=address)
                self.otlp_logger.log(
                    curr_span, f"address patched for order {order_id} successfully")
                return order
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order address"
                ) from ex

    def handle_order_product_patch(self, order_id: int, product: List[int]) -> GetOrderInterface:
        """ controller to update product an order """
        with self.tracer.start_as_current_span("OrderController.handle_order_product_patch") as curr_span:
            try:
                order = self.order_service.update_order_product(
                    order_id=order_id, product=product)
                self.otlp_logger.log(
                    curr_span, f"product updated for order {order_id} successfully")
                return order
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order products"
                ) from ex

    def handle_order_status_patch(self, order_id: int, status: StatusEnum) -> GetOrderInterface:
        """ controller to update status an order """
        with self.tracer.start_as_current_span("OrderController.handle_order_status_patch") as curr_span:
            try:
                order = self.order_service.update_order_status(
                    order_id=order_id, status=status)
                self.otlp_logger.log(
                    curr_span, f"status patched for order {order_id} successfully")
                return order
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order status"
                ) from ex

    def handle_order_delete(self, order_id: int) -> str:
        """ controller to delete an order """
        with self.tracer.start_as_current_span("OrderController.handle_order_address_patch") as curr_span:
            try:
                self.order_service.delete_order(order_id)
                self.otlp_logger.log(
                    curr_span, f"order {order_id} deleted successfully")
                return f"order {order_id} deleted successfully"
            except HTTPException:
                raise
            except Exception as ex:
                self.otlp_logger.error(curr_span, ex, LogLevelEnum.CRITICAL,
                                       f"response ended with {status_code.HTTP_500_INTERNAL_SERVER_ERROR} status code")
                raise HTTPException(
                    status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete order"
                ) from ex
