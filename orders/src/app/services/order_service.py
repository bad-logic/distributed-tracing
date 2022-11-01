"""

    Service for orders

"""

from typing import List
from fastapi import HTTPException, status as status_code
from sqlalchemy.orm import sessionmaker, Session

from db import DBConnector
from utils import Logger
from ..interfaces import CreateOrderInterface, GetOrderInterface, StatusEnum
from ..models import OrderTable

connector = DBConnector()
connector.connect()
session_maker = sessionmaker(bind=connector.get_engine())


class OrderService:

    """

        Service for order
    """

    def __init__(self) -> None:
        self.logger = Logger().get_logger()

    def create_order(self, order: CreateOrderInterface) -> GetOrderInterface:
        """ service to create an order """
        with session_maker() as session:
            new_order = OrderTable(
                user=order.user,
                product=order.product,
                status=order.status.value,
                address=order.address
            )
            session.add(new_order)
            session.commit()
            session.refresh(new_order, attribute_names=["id"])
            new_order = new_order.dict()
        return new_order

    def get_orders(self, offset: int = 1, limit: int = 10) -> List[GetOrderInterface]:
        """ service to fetch orders """
        with session_maker() as session:
            orders = session.query(OrderTable).offset(
                (offset - 1) * limit).limit(limit).all()
            orders = [order.dict() for order in orders]
        return orders

    def get_order_model_object(self, order_id: int, session: Session) -> GetOrderInterface:
        """ service to fetch an sqlalchemy order object """
        order = session.query(OrderTable).filter(
            OrderTable.Id == order_id).first()
        if order is None:
            raise HTTPException(
                status_code=status_code.HTTP_404_NOT_FOUND, detail=f"order with ID {order_id} not found")
        return order

    def get_order(self, order_id: int) -> GetOrderInterface:
        """ service to fetch an order """
        with session_maker() as session:
            order = self.get_order_model_object(order_id, session)
            order = order.dict()
        return order

    def update_order_status(self, order_id: int, status: StatusEnum) -> GetOrderInterface:
        """ service to update the status of an order """
        with session_maker() as session:
            order = self.get_order_model_object(order_id, session)
            order.status = status.value
            session.add(order)
            session.commit()
            order = order.dict()
        return order

    def update_order_product(self, order_id: int, product: List[int]) -> GetOrderInterface:
        """ service to update the product of an order """
        with session_maker() as session:
            order = self.get_order_model_object(order_id, session)
            if (order.status.value != StatusEnum.ORDER_PLACED.value):
                raise HTTPException(
                    status_code.HTTP_403_FORBIDDEN, detail=f"Cannot update product once order status is {order.status.value}"
                )
            order.product = product
            session.add(order)
            session.commit()
            order = order.dict()
        return order

    def update_order_address(self, order_id: int, address: str) -> GetOrderInterface:
        """ service to update the address of an order """
        with session_maker() as session:
            order = self.get_order_model_object(order_id, session)
            if (order.status.value != StatusEnum.ORDER_PLACED.value):
                raise HTTPException(
                    status_code.HTTP_403_FORBIDDEN, detail=f"Cannot update address once order status is {order.status.value}"
                )
            order.address = address
            session.add(order)
            session.commit()
            order = order.dict()
        return order

    def delete_order(self, order_id: int) -> None:
        """ service to delete an order """
        with session_maker() as session:
            order = self.get_order_model_object(order_id, session)
            session.delete(order)
            session.commit()
