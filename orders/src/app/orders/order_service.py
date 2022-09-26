from sqlalchemy.orm import Session
from .order_model import OrderModel, OrderTable
from db import DBConnector


class OrderService:

    def create_order(self, order: OrderModel):
        session = Session(DBConnector().get_engine())
        new_order = OrderTable(
            user=order.user,
            product=order.product,
            status=order.status.value,
            address=order.address
        )
        session.add(new_order)
        session.commit()
        session.refresh(new_order, attribute_names=["id"])
        session.close()
        return {"id": new_order.id}
