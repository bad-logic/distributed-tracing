from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .order_model import OrderModel, OrderTable, StatusEnum
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

    def get_orders(self, offset: int = 1, limit: int = 10):
        session = Session(DBConnector().get_engine())
        orders = session.query(OrderTable).offset(
            (offset - 1) * limit).limit(limit).all()
        session.close()
        return {"orders": orders}

    def get_order(self, id: int):
        session = Session(DBConnector().get_engine())
        order = session.query(OrderTable).where(OrderTable.id == id)
        session.close()
        return {"order": order}

    def update_order_status(self, id: int, status: StatusEnum):
        session = Session(DBConnector().get_engine())
        session.update(session.query(OrderTable).where(OrderTable.id == id).values(
            status=status.value))
        session.commit()
        session.close()
        return {"id": id, "status": status.value}

    def update_order_product(self, id: int, product: List[int]):
        order = self.get_order(id)
        if (order.status != StatusEnum.placed.value):
            raise HTTPException(
                status.HTTP_403_Forbidden, "Cannot update product once {}".format(
                    order.status)
            )
        session = Session(DBConnector().get_engine())
        session.update(session.query(OrderTable).where(
            OrderTable.id == id).values(product=product))
        session.commit()
        session.close()
        return {"id": id, "product": product}

    def update_order_address(self, id: int, address: str):
        order = self.get_order(id)
        if (order.status != StatusEnum.placed.value):
            raise HTTPException(
                status.HTTP_403_Forbidden, "Cannot update address once {}".format(
                    order.status)
            )
        session = Session(DBConnector().get_engine())
        session.update(session.query(OrderTable).where(
            OrderTable.id == id).values(address=address))
        session.commit()
        session.close()
        return {"id": id, "address": address}

    def delete_order(self, id: int):
        session = Session(DBConnector().get_engine())
        session.delete(session.query(OrderTable).filter(
            OrderTable.id == id).first())
        session.commit()
        session.close()
        return {"id": id}
