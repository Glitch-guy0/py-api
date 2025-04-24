from typing import Any
from .protocol import Logger_protocol, LogFormat
import os
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger


class JSONLogger(Logger_protocol):
    def __init__(
        self,
        service_name: str,
        log_file_path: str,
        log_max_bytes: int,
        log_backup_count: int,
    ):
        # Define the log file path and rotation settings
        LOG_FILE_PATH: str = log_file_path  # type: ignore
        LOG_MAX_BYTES: int = log_max_bytes  # type: ignore
        LOG_BACKUP_COUNT: int = log_backup_count  # type: ignore
        SERVICE_NAME: str = service_name  # type: ignore

        # Create folder and file for log file path if not exists
        log_dir = os.path.dirname(LOG_FILE_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if not os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "w") as f:
                pass

        # Create a custom JSON formatter
        class CustomJSONFormatter(jsonlogger.JsonFormatter):  # type: ignore
            def add_fields(self, log_record, record, message_dict):
                super().add_fields(log_record, record, message_dict)
                log_format = LogFormat(
                    timestamp=self.formatTime(record, self.datefmt),
                    level=record.levelname,
                    service=SERVICE_NAME,
                    message=record.getMessage(),
                    trace_id=getattr(record, "trace_id", None),
                    context=getattr(record, "context", {}),
                )
                log_record.update(log_format.model_dump())

        # Set up the logger
        logger = logging.getLogger(SERVICE_NAME)
        logger.setLevel(logging.DEBUG)

        # Create a rotating file handler
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE_PATH, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT
        )
        handler.setFormatter(CustomJSONFormatter())

        # Add the handler to the logger
        logger.addHandler(handler)

        self.logger = logger

    def debug(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        self.logger.debug(message, trace_id, context)

    def info(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        self.logger.info(message, trace_id, context)

    def warning(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        self.logger.warning(message, trace_id, context)

    def error(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        self.logger.error(message, trace_id, context)

    def critical(
        self, message: str, trace_id: str | None = None, context: dict[str, Any] = {}
    ) -> None:
        self.logger.critical(message, trace_id, context)
