# User Service

This microservice handles user management


# Environment Variables

The service requires the following environment variables to be set:

| Variable | Description | Example |
|----------|-------------|---------|
| **SERVICE_NAME** | Name of the service | "user_service" |
| **LOG_FILE_PATH** | Path to log file | "logs/user_service.log" |
| **LOG_MAX_BYTES** | Maximum log file size in bytes | 5MB |
| **LOG_BACKUP_COUNT** | Number of backup log files to keep | 3 |
| **SHARED_LIB_LOG_FILE_PATH** | Path to shared library log file | "logs/shared_lib.log" |

