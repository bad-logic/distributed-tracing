from fastapi import APIRouter, status as status_code
from utils import Logger
from ..interfaces import GeneralProductInterface
from ..controllers import ProductConsumerController

product_consumer_router = APIRouter()

productConsumerController = ProductConsumerController()

logger = Logger().get_logger()


@product_consumer_router.post("/created", status_code=status_code.HTTP_200_OK, response_model=GeneralProductInterface)
def consume_product_created(product: GeneralProductInterface):
    """ API to consumer a productCreated topic """
    return productConsumerController.handle_product_creation(product=product)


@product_consumer_router.post("/updated", status_code=status_code.HTTP_200_OK, response_model=GeneralProductInterface)
def consumer_product_updated(product: GeneralProductInterface):
    """ API to consumer a productUpdated topic """
    return productConsumerController.handle_product_update(product=product)


@product_consumer_router.post("/deleted", status_code=status_code.HTTP_200_OK)
def consume_product_deleted(product: GeneralProductInterface):
    """ API to consumer a productDeleted topic """
    return productConsumerController.handle_product_delete(product=product)
