from typing import List
from fastapi import APIRouter, status as status_code

from ..interfaces import CreateOrderInterface, GetOrderInterface, PatchOrderStatusInterface, PatchOrderAddressInterface
from ..controllers import OrderController


order_router = APIRouter()

orderController = OrderController()


@order_router.post("/", status_code=status_code.HTTP_201_CREATED, response_model=GetOrderInterface)
def create_order(order: CreateOrderInterface):
    """ API to create an order """
    return orderController.handle_order_creation(order)


@order_router.get("/", status_code=status_code.HTTP_200_OK, response_model=List[GetOrderInterface])
def fetch_orders(offset: int = 1, limit: int = 10):
    """ API for fetching the list of orders """
    return orderController.handle_orders_fetch(offset=offset, limit=limit)


@order_router.get("/{order_id}", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def fetch_order(order_id: int):
    """ API for fetching an order by id """
    return orderController.handle_order_fetch(order_id=order_id)


@order_router.patch("/{order_id}/address", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def patch_order_address(order_id: int, update: PatchOrderAddressInterface):
    """ API for updating the address of an order """
    return orderController.handle_order_address_patch(order_id=order_id, address=update.Address)


@order_router.patch("/{order_id}/product", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def patch_order_product(order_id: int, product: List[int]):
    """ API for updating the products of an order """
    return orderController.handle_order_product_patch(order_id=order_id, product=product)


@order_router.patch("/{order_id}/status", status_code=status_code.HTTP_200_OK, response_model=GetOrderInterface)
def patch_order_status(order_id: int, update: PatchOrderStatusInterface):
    """ API for updating the status of an order """
    return orderController.handle_order_status_patch(order_id=order_id, status=update.Status)


@order_router.delete("/{order_id}", status_code=status_code.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    """ API for deleting an order """
    return orderController.handle_order_delete(order_id=order_id)
