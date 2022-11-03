from utils import SERVICE_NAME, Telemetry
from .routes import order_router, consumer_router
from db import DBConnector
from fastapi import FastAPI, status, Request
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


request_handler = FastAPI(title="Orders Service", debug=True)


connector = DBConnector()
telemetry = Telemetry()


@request_handler.on_event("startup")
def startup_operations():
    """ function to run the operation needed before server startup """
    connector.connect()
    telemetry.setup_telemetry_tracer_provider()


@request_handler.on_event("shutdown")
def cleanup_operations():
    """ function to run cleanups after shutdown """
    connector.dispose_connection()
    telemetry.close_telemetry_tracer_provider()


@request_handler.middleware("http")
async def set_opentelemetry_context(request: Request, call_next):
    """
        middleware to create a span for method and url of the request
    """
    # transparent: {version}-{trace_id}-{span_id}-{trace_flags}
    traceparent = request.headers.get("traceparent") or None

    carrier = {'traceparent': request.headers.get("traceparent")
               } if traceparent is not None else {}

    # Then we use a propagator to get a context from it.
    ctx = TraceContextTextMapPropagator().extract(carrier=carrier)

    tracer = trace.get_tracer(SERVICE_NAME)
    with tracer.start_as_current_span(f"{request.method}:{request.url.path}", context=ctx) as parent:
        parent.set_attribute("http.method", request.method)
        parent.set_attribute("http.route", request.url.path)
        response = await call_next(request)
        return response


request_handler.include_router(order_router, prefix="/order")
request_handler.include_router(
    consumer_router, prefix="/consume")


@request_handler.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """ API for health check """
    return "OK"
