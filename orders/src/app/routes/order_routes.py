from typing import List
import traceback
from fastapi import APIRouter, HTTPException, status as status_code
from utils import Logger
from ..interfaces import CreateOrderInterface, GetOrderInterface, StatusEnum
from ..controllers import OrderController

order_router = APIRouter()

orderController = OrderController()

logger = Logger().get_logger()


@order_router.post("/", status_code=status_code.HTTP_201_CREATED, response_model=GetOrderInterface)
def create_order(order: CreateOrderInterface):
    """ API to create an order """
    try:
        return orderController.handle_order_creation(order)
    except HTTPException:
        raise
    except Exception as general:
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create order"
        ) from general


@order_router.get("/", status_code=status_code.HTTP_200_OK, response_model=List[GetOrderInterface])
def fetch_orders(offset: int = 1, limit: int = 10):
    """ API for fetching the list of orders """
    try:
        return orderController.handle_orders_fetch(offset=offset, limit=limit)
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch orders"
        ) from ex


@order_router.get("/{order_id}", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def fetch_order(order_id: int):
    """ API for fetching an order by id """
    try:
        return orderController.handle_order_fetch(order_id=order_id)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch order"
        ) from ex


@order_router.patch("/{order_id}/address", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def patch_order_address(order_id: int, address: str):
    """ API for updating the address of an order """
    try:
        return orderController.handle_order_address_patch(order_id=order_id, address=address)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order address"
        ) from ex


@order_router.patch("/{order_id}/product", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def patch_order_product(order_id: int, product: List[int]):
    """ API for updating the products of an order """
    try:
        return orderController.handle_order_product_patch(order_id=order_id, product=product)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order products"
        ) from ex


@order_router.patch("/{order_id}/status", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def patch_order_status(order_id: int, status: StatusEnum):
    """ API for updating the status of an order """
    try:
        return orderController.handle_order_status_patch(order_id=order_id, status=status)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update order status"
        ) from ex


@order_router.delete("/{order_id}", status_code=status_code.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    """ API for deleting an order """
    try:
        return orderController.handle_order_delete(order_id=order_id)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete order"
        ) from ex
