from pydantic import ValidationError, Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv
import sys
from typing import Optional


class System_Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv())

    service_name: str = Field("auth_service", validation_alias="SERVICE_NAME")

    # logging config
    log_file_path: Optional[str] = Field(
        "logs/auth_service.log", validation_alias="LOG_FILE_PATH"
    )
    log_max_bytes: Optional[int] = Field(
        5 * 1024 * 1024, validation_alias="LOG_MAX_BYTES"
    )  # 5 MB
    log_backup_count: Optional[int] = Field(3, validation_alias="LOG_BACKUP_COUNT")

    # okta config
    okta_authorize_uri: str = Field(..., validation_alias="OKTA_AUTHORIZE_URI")
    okta_authorize_redirect_uri: str = Field(
        ..., validation_alias="OKTA_AUTHORIZE_REDIRECT_URI"
    )
    okta_client_id: str = Field(..., validation_alias="OKTA_CLIENT_ID")
    okta_client_secret: str = Field(..., validation_alias="OKTA_CLIENT_SECRET")
    okta_token_uri: str = Field(..., validation_alias="OKTA_TOKEN_URI")
    okta_userdata_uri: str = Field(..., validation_alias="OKTA_USERDATA_URI")
    okta_jwks_uri: str = Field(..., validation_alias="OKTA_JWKS_URI")


try:
    config = System_Environment()  # type: ignore
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
