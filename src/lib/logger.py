
"""
usage:

from logger import logger

logger.<log_level>("message")
"""

import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
import sys
import env
import os

# Define the log format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# Define log file path
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Ensure directory exists
os.makedirs(LOG_DIR, exist_ok=True)  # Creates directory if it doesn't exist

# Create a logger
logger = logging.getLogger("fastapi_app")
if env.LOG_VERBOSITY == "DEBUG":
  logger.setLevel(LOG_LEVELS.get(env.LOG_VERBOSITY, logging.INFO))  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  

# StreamHandler (Logs to Console)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# RotatingFileHandler (Logs to File)                     5MB
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(jsonlogger.JsonFormatter(LOG_FORMAT))

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)





