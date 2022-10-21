from fastapi import APIRouter

from .product_consumer_routes import product_consumer_router

consumer_router = APIRouter()


consumer_router.include_router(
    product_consumer_router, prefix="/product")
