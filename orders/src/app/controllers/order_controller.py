"""
    Controller for orders 
"""

from typing import List
import traceback

from fastapi import HTTPException, status as status_code

from ..interfaces import CreateOrderInterface, GetOrderInterface, StatusEnum
from ..services import OrderService
from utils import Logger


class OrderController:
    """

        Controller for Order
    """

    def __init__(self):
        self.logger = Logger().get_logger()
        self.order_service = OrderService()

    def handle_order_creation(self, order: CreateOrderInterface) -> GetOrderInterface:
        """ controller to create an order """
        try:
            return self.order_service.create_order(order)
        except HTTPException:
            raise
        except Exception as ex:
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create order"
            ) from ex

    def handle_orders_fetch(self, offset: int = 1, limit: int = 10) -> List[GetOrderInterface]:
        """ controller to fetch orders """
        try:
            return self.order_service.get_orders(offset=offset, limit=limit)
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch orders"
            ) from ex

    def handle_order_fetch(self, order_id: int) -> GetOrderInterface:
        """ controller to fetch an order """
        try:
            return self.order_service.get_order(order_id)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch order"
            ) from ex

    def handle_order_address_patch(self, order_id: int, address: str) -> GetOrderInterface:
        """ controller to update address an order """
        try:
            return self.order_service.update_order_address(order_id=order_id, address=address)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order address"
            ) from ex

    def handle_order_product_patch(self, order_id: int, product: List[int]) -> GetOrderInterface:
        """ controller to update product an order """
        try:
            return self.order_service.update_order_product(order_id=order_id, product=product)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order products"
            ) from ex

    def handle_order_status_patch(self, order_id: int, status: StatusEnum) -> GetOrderInterface:
        """ controller to update status an order """
        try:
            return self.order_service.update_order_status(order_id=order_id, status=status)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order status"
            ) from ex

    def handle_order_delete(self, order_id: int) -> str:
        """ controller to delete an order """
        try:
            return self.order_service.delete_order(order_id)
        except HTTPException:
            raise
        except Exception as ex:
            self.logger.exception(traceback.format_exc())
            raise HTTPException(
                status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete order"
            ) from ex
