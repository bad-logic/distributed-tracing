"""
    Controller for orders 
"""

from typing import List
from utils import Logger
from .order_model import CreateOrderInterface, GetOrderInterface, StatusEnum
from .order_service import OrderService


class OrderController:
    """

        Controller for Order
    """

    def __init__(self):
        self.logger = Logger().get_logger()
        self.order_service = OrderService()

    def handle_order_creation(self, order: CreateOrderInterface) -> GetOrderInterface:
        """ controller to create an order """
        return self.order_service.create_order(order)

    def handle_orders_fetch(self, offset: int = 1, limit: int = 10) -> List[GetOrderInterface]:
        """ controller to fetch orders """
        return self.order_service.get_orders(offset=offset, limit=limit)

    def handle_order_fetch(self, order_id: int) -> GetOrderInterface:
        """ controller to fetch an order """
        return self.order_service.get_order(order_id)

    def handle_order_address_patch(self, order_id: int, address: str) -> GetOrderInterface:
        """ controller to update address an order """
        return self.order_service.update_order_address(order_id=order_id, address=address)

    def handle_order_product_patch(self, order_id: int, product: List[int]) -> GetOrderInterface:
        """ controller to update product an order """
        return self.order_service.update_order_product(order_id=order_id, product=product)

    def handle_order_status_patch(self, order_id: int, status: StatusEnum) -> GetOrderInterface:
        """ controller to update status an order """
        return self.order_service.update_order_status(order_id=order_id, status=status)

    def handle_order_delete(self, order_id: int) -> str:
        """ controller to delete an order """
        return self.order_service.delete_order(order_id)
