from fastapi import FastAPI

request_handler = FastAPI(title="Orders Service")


@request_handler.get("/source", status_code=200)
def get_customers_info():
    return {"message": "from dapper"}
