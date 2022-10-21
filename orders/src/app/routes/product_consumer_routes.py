import traceback
from fastapi import APIRouter, HTTPException, status as status_code
from utils import Logger
from ..interfaces import GeneralProductInterface
from ..controllers import ProductConsumerController

product_consumer_router = APIRouter()

productConsumerController = ProductConsumerController()

logger = Logger().get_logger()


@product_consumer_router.post("/created", status_code=status_code.HTTP_200_OK, response_model=GeneralProductInterface)
def consume_product_created(product: GeneralProductInterface):
    """ API to consumer a productCreated topic """
    try:
        return productConsumerController.handle_product_creation(product=product)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create product"
        ) from ex


@product_consumer_router.post("/updated", status_code=status_code.HTTP_200_OK, response_model=GeneralProductInterface)
def consumer_product_updated(product: GeneralProductInterface):
    """ API to consumer a productUpdated topic """
    try:
        return productConsumerController.handle_product_update(product=product)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update product"
        ) from ex


@product_consumer_router.post("/deleted", status_code=status_code.HTTP_200_OK)
def consume_product_deleted(product: GeneralProductInterface):
    """ API to consumer a productDeleted topic """
    try:
        return productConsumerController.handle_product_delete(product=product)
    except HTTPException:
        raise
    except Exception as ex:
        logger.exception(traceback.format_exc())
        raise HTTPException(
            status_code.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete product"
        ) from ex
