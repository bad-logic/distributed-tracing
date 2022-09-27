
from audioop import add
from utils import Logger
from .order_model import OrderModel, StatusEnum
from .order_service import OrderService
from typing import List


class OrderController:

    def __init__(self):
        self.logger = Logger().get_logger()
        self.order_service = OrderService()

    def handle_order_creation(self, order: OrderModel):
        return self.order_service.create_order(order)

    def handle_orders_fetch(self, offset: int = 1, limit: int = 10):
        return self.order_service.get_orders(offset=offset, limit=limit)

    def handle_order_fetch(self, id: int):
        return self.order_service.get_order(id)

    def handle_order_address_patch(self, id: int, address: str):
        return self.order_service.update_order_address(id=id, address=address)

    def handle_order_product_patch(self, id: int, product: List[int]):
        return self.order_service.update_order_product(id=id, product=product)

    def handle_order_status_patch(self, id: int, status: StatusEnum):
        return self.order_service.update_order_status(id=id, status=status)

    def handle_order_delete(self, id: int):
        return self.order_service.delete_order(id)
