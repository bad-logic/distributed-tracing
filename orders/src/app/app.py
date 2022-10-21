from fastapi import FastAPI, status
from db import DBConnector
from .routes import order_router, consumer_router

request_handler = FastAPI(title="Orders Service", debug=True)

connector = DBConnector()


@request_handler.on_event("startup")
def startup_operations():
    """ function to run the operation needed before server startup """
    connector.connect()


@request_handler.on_event("shutdown")
def cleanup_operations():
    """ function to run cleanups after shutdown """
    connector.dispose_connection()


request_handler.include_router(order_router, prefix="/orders/order")
request_handler.include_router(
    consumer_router, prefix="/orders/consume")


@request_handler.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """ API for health check """
    return "OK"
