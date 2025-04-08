import os
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
from auth_service.config import config

# Define the log file path and rotation settings
LOG_FILE_PATH: str = config.log_file_path  # type: ignore
LOG_MAX_BYTES: int = config.log_max_bytes  # type: ignore
LOG_BACKUP_COUNT: int = config.log_backup_count  # type: ignore
SERVICE_NAME: str = config.service_name  # type: ignore


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
        log_record["time"] = self.formatTime(record, self.datefmt)
        log_record["service_name"] = SERVICE_NAME
        log_record["message"] = record.getMessage()
        log_record["error_type"] = record.levelname


# Set up the logger
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.INFO)

# Create a rotating file handler
handler = logging.handlers.RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT
)
handler.setFormatter(CustomJSONFormatter())

# Add the handler to the logger
logger.addHandler(handler)

# Example usage of the logger
# import logger
# logger.info("Auth service started successfully.")
