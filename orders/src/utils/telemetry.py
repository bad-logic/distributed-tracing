
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.sdk.resources import Resource

from .logger import Logger
from .singleton import Singleton

# otlp => open telemetry specification


SERVICE_NAME = "order_ms"


class Telemetry(metaclass=Singleton):
    """"
        Telemetry 
    """

    def __init__(self) -> None:
        """Initialize"""
        self.service_instance = os.getenv("HOSTNAME")
        self.provider = None
        self.logger = Logger().get_logger()

    def setup_telemetry_tracer_provider(self):
        """
            configure opentelemetry sdk
        """
        self.provider = TracerProvider(
            resource=Resource.create({
                "service.namespace": "shop",
                "service.name": SERVICE_NAME,
                "service.instance.id": self.service_instance,
                "service.version": "v1.0.0",
            }),
        )

        otlp_exporter = OTLPSpanExporter(endpoint=os.getenv(
            "LOG_COLLECTOR_ENDPOINT"), insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter)
        self.provider.add_span_processor(span_processor)

        # Sets the global default tracer provider
        trace.set_tracer_provider(self.provider)

    def close_telemetry_tracer_provider(self):
        """
            shutdown tracer provider
        """
        self.provider.shutdown()
