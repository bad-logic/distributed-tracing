from enum import Enum
from logging import exception
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

from .logger import Logger

# otlp => open telemetry specification


class LogLevelEnum(Enum):
    """Enum for loglevel"""

    WARN = "warn"
    CRITICAL = "critical"
    INFO = "info"


class TelemetryLogger:
    """
        Telemetry Logger
    """

    def __init__(self):
        self.logger = Logger().get_logger()

    def log(self, span: trace.span.Span, message: str):
        """
            logs message in console and adds log event to the span
        """

        self.logger.info(message)
        span.add_event("log", {
            "severity": "info",
            "message": message
        })

    def error(self, span: trace.span.Span, exc: exception, err_level: LogLevelEnum = LogLevelEnum.WARN, message: str = None):
        """
            logs error to the console, records error and adds log event to the span
        """

        self.logger.critical(exc)

        log_message = message if message is not None else f"{exc}"
        error_code = StatusCode.OK

        if (err_level.value == LogLevelEnum.CRITICAL.value):
            error_code = StatusCode.ERROR

        span.record_exception(exc)
        span.set_status(Status(error_code, str(exc)))

        span.add_event("log", {
            "severity": err_level.value,
            "message": log_message
        })
