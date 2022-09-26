from fastapi import APIRouter, HTTPException, status
from utils import Logger
from .order_model import OrderModel
from .order_controller import OrderController
import traceback

order_router = APIRouter()

orderController = OrderController()

logger = Logger().get_logger()


@order_router.post("/", status_code=200)
def create_order(order: OrderModel):
    try:
        return orderController.handle_order_creation(order)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create order"
        )
