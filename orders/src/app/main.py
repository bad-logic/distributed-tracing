from fastapi import FastAPI
from db import DBConnector
from .orders import order_router

request_handler = FastAPI(title="Orders Service")

connector = DBConnector()


@request_handler.on_event("startup")
def startup_operations():
    connector.connect()


@request_handler.on_event("shutdown")
def cleanup_operations():
    connector.dispose_connection()


request_handler.include_router(order_router, prefix="/orders/order")


@request_handler.get("/health", status_code=200)
def health_check():
    return "OK"
