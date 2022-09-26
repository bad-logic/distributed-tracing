import os
import uvicorn
from app import request_handler


if __name__ == "__main__":
    port = os.environ.get("PORT", 8080)
    uvicorn.run("server:request_handler", host="0.0.0.0",
                port=int(port), log_level="info", reload=True)
