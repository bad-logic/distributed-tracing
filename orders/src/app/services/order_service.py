"""

    Service for orders

"""

from typing import List
from fastapi import HTTPException, status as status_code
from sqlalchemy.orm import sessionmaker, Session
from opentelemetry import trace

from db import DBConnector
from utils import TelemetryLogger, SERVICE_NAME
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
        self.otlp_logger = TelemetryLogger()
        self.tracer = trace.get_tracer(SERVICE_NAME)

    def create_order(self, order: CreateOrderInterface) -> GetOrderInterface:
        """ service to create an order """
        with self.tracer.start_as_current_span("OrderService.create_order") as curr_span:
            self.otlp_logger.log(curr_span,
                                 f"storing {order} in the database")
            with session_maker() as session:
                new_order = OrderTable(
                    User=order.User,
                    Product=order.Product,
                    Status=order.Status.value,
                    Address=order.Address
                )
                session.add(new_order)
                session.commit()
                session.refresh(new_order, attribute_names=["Id"])
                new_order = new_order.dict()

            self.otlp_logger.log(curr_span,
                                 "order stored in database")
            return new_order

    def get_orders(self, offset: int = 1, limit: int = 10) -> List[GetOrderInterface]:
        """ service to fetch orders """
        with self.tracer.start_as_current_span("OrderService.get_orders") as curr_span:
            self.otlp_logger.log(curr_span,
                                 "querying database for order")
            with session_maker() as session:
                orders = session.query(OrderTable).offset(
                    (offset - 1) * limit).limit(limit).all()
                orders = [order.dict() for order in orders]
            self.otlp_logger.log(curr_span,
                                 "orders fetched from database")
            return orders

    def get_order_model_object(self, order_id: int, session: Session) -> GetOrderInterface:
        """ service to fetch an sqlalchemy order object """
        with self.tracer.start_as_current_span("OrderService.get_order_model_object") as curr_span:
            self.otlp_logger.log(curr_span,
                                 f"querying database for order {order_id}")
            order = session.query(OrderTable).filter(
                OrderTable.Id == order_id).first()
            if order is None:
                raise HTTPException(
                    status_code=status_code.HTTP_404_NOT_FOUND, detail=f"order with ID {order_id} not found")
            self.otlp_logger.log(curr_span,
                                 "order fetched from database")
            return order

    def get_order(self, order_id: int) -> GetOrderInterface:
        """ service to fetch an order """
        with self.tracer.start_as_current_span("OrderService.get_order") as _:
            with session_maker() as session:
                order = self.get_order_model_object(order_id, session)
                order = order.dict()
            return order

    def update_order_status(self, order_id: int, status: StatusEnum) -> GetOrderInterface:
        """ service to update the status of an order """
        with self.tracer.start_as_current_span("OrderService.update_order_status") as curr_span:
            self.otlp_logger.log(curr_span,
                                 f"updating order {order_id} status to {status.value}")
            with session_maker() as session:
                order = self.get_order_model_object(order_id, session)
                order.Status = status.value
                session.add(order)
                session.commit()
                order = order.dict()
            self.otlp_logger.log(curr_span,
                                 "saved the updated order status to the database")
            return order

    def update_order_product(self, order_id: int, product: List[int]) -> GetOrderInterface:
        """ service to update the product of an order """
        with self.tracer.start_as_current_span("OrderService.update_order_product") as curr_span:
            with session_maker() as session:
                order = self.get_order_model_object(order_id, session)
                if (order.Status.value != StatusEnum.ORDER_PLACED.value):
                    raise HTTPException(
                        status_code.HTTP_403_FORBIDDEN, detail=f"Cannot update product once order status is {order.status.value}"
                    )
                order.Product = product
                session.add(order)
                session.commit()
                order = order.dict()
            self.otlp_logger.log(curr_span,
                                 "updated order product to the database")
            return order

    def update_order_address(self, order_id: int, address: str) -> GetOrderInterface:
        """ service to update the address of an order """
        with self.tracer.start_as_current_span("OrderService.update_order_address") as curr_span:
            with session_maker() as session:
                order = self.get_order_model_object(order_id, session)
                if (order.Status.value != StatusEnum.ORDER_PLACED.value):
                    raise HTTPException(
                        status_code.HTTP_403_FORBIDDEN, detail=f"Cannot update address once order status is {order.status.value}"
                    )
                order.Address = address
                session.add(order)
                session.commit()
                order = order.dict()
            self.otlp_logger.log(curr_span,
                                 "updated order address to the database")
            return order

    def delete_order(self, order_id: int) -> None:
        """ service to delete an order """
        with self.tracer.start_as_current_span("OrderService.delete_order") as curr_span:
            with session_maker() as session:
                order = self.get_order_model_object(order_id, session)
                session.delete(order)
                session.commit()
            self.otlp_logger.log(curr_span,
                                 f"successfully deleted order {order_id}")
