from pydantic import ValidationError, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv
import sys


class System_Environment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(raise_error_if_not_found=True), extra="ignore"
    )

    service_name: str = Field(..., validation_alias="SERVICE_NAME")
    log_file_path: str = Field(..., validation_alias="LOG_FILE_PATH")
    log_max_bytes: int = Field(..., validation_alias="LOG_MAX_BYTES")
    log_backup_count: int = Field(..., validation_alias="LOG_BACKUP_COUNT")


try:
    Config = System_Environment()  # type: ignore
except ValidationError as e:
    error = e.errors()[0]
    err_message = (
        f"{error.get('type')} environment variable {error.get('loc')} check .env file"
    )
    print(err_message)
    sys.exit(1)
except Exception as e:
    print(e)
    print("Error loading environment variables")
