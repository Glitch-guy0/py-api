from dataclasses import field
from typing import Any, Protocol
from datetime import datetime
from pydantic import BaseModel


class LogFormat(BaseModel):
    """A data model representing the structure of a log entry.

    Attributes:
        timestamp (str): ISO format timestamp of when the log was created
        level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        trace_id (str): Unique identifier for tracing requests across services
        service (str): Name of the service generating the log
        message (str): The actual log message content
        context (dict[str, Any]): Additional contextual data for the log entry
    """

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    level: str
    trace_id: str | None = None
    service: str
    message: str
    context: dict[str, Any]


class Logger_protocol(Protocol):
    def debug(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        pass

    def info(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        pass

    def warning(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        pass

    def error(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        pass

    def critical(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        pass
