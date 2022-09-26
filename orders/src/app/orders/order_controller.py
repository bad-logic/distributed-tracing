
from utils import Logger
from .order_model import OrderModel
from .order_service import OrderService


class OrderController:

    def __init__(self):
        self.logger = Logger().get_logger()
        self.order_service = OrderService()

    def handle_order_creation(self, order: OrderModel):
        return self.order_service.create_order(order)
