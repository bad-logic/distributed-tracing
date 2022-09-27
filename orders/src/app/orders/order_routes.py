from fastapi import APIRouter, HTTPException, status
from utils import Logger
from .order_model import OrderModel, StatusEnum
from .order_controller import OrderController
import traceback
from typing import List

order_router = APIRouter()

orderController = OrderController()

logger = Logger().get_logger()


@order_router.post("/", status_code=201)
def create_order(order: OrderModel):
    try:
        return orderController.handle_order_creation(order)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create order"
        )


@order_router.get("/", status_code=200)
def fetch_orders(offset: int = 1, limit: int = 10):
    try:
        return orderController.handle_orders_fetch(offset=offset, limit=limit)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch orders"
        )


@order_router.get("/{id}", status_code=200)
def fetch_order(id: int):
    try:
        return orderController.handle_order_fetch(id)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch order"
        )


@order_router.patch("/{id}/address", status_code=200)
def patch_order_address(id: int, address: str):
    try:
        return orderController.handle_order_address_patch(id=id, address=address)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order address"
        )


@order_router.patch("/{id}/product", status_code=200)
def patch_order_product(id: int, product: List[int]):
    try:
        return orderController.handle_order_product_patch(id=id, product=product)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order products"
        )


@order_router.patch("/{id}/status", status_code=200)
def patch_order_status(id: int, status: StatusEnum):
    try:
        return orderController.handle_order_status_patch(id=id, status=status)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order status"
        )


@order_router.delete("/{id}", status_code=200)
def delete_order(id: int):
    try:
        return orderController.handle_order_delete(id=id)
    except Exception:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete order"
        )
