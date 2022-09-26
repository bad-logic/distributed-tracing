from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.engine import Engine

from db import DBConnector
from utils import Logger
from .order_model import OrderModel

order_router = APIRouter()
engine = DBConnector().get_engine()


logger = Logger().get_logger()


@order_router.post("/", status_code=200)
def create_order(order: OrderModel, engine: Engine = Depends(engine)):
    print(order)
    return Response(content={"success": "OK"}, media_type="application/json")
