from fastapi import FastAPI
from db import DBConnector
from .orders import order_router

request_handler = FastAPI(title="Orders Service")

API_PREFIX = '/orders'

connector = DBConnector()


@request_handler.on_event("startup")
def startup_operations():
    connector.connect()


@request_handler.on_event("shutdown")
def cleanup_operations():
    connector.dispose_connection()


request_handler.include_router(order_router, prefix=API_PREFIX + "/order")


@request_handler.get("/source", status_code=200)
def get_customers_info():
    return {"message": "from dapper"}
