import os
import traceback
import uvicorn
from db import DBConnector
from utils import Logger
from app import request_handler

logger = Logger().get_logger()
connector = DBConnector()

if __name__ == "__main__":
    try:
        port = os.environ.get("PORT", 8080)
        uvicorn.run("server:request_handler", host="0.0.0.0",
                    port=int(port), log_level="info", reload=True)
    except Exception as exc:
        print(exc)
        logger.fatal(traceback.format_exc())
