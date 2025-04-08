from pydantic import ValidationError, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv
import sys
from typing import Optional
    
class System_Environment(BaseSettings):
  model_config = SettingsConfigDict(env_file=find_dotenv())

  # environment schema
  log_file_path: Optional[str] = Field('logs/auth_service.log', validation_alias='LOG_FILE_PATH')
  log_max_bytes: Optional[int] = Field(5 * 1024 * 1024, validation_alias='LOG_MAX_BYTES') # 5 MB
  log_backup_count: Optional[int] = Field(3, validation_alias='LOG_BACKUP_COUNT')
  service_name: str = Field('auth_service', validation_alias='SERVICE_NAME')

try:
  config = System_Environment()
except ValidationError as e:
  error = e.errors()[0]
  err_message= f"{error.get('type')} environment variable {error.get('loc')} check .env file"
  print(err_message)
  sys.exit(1)
except Exception as e:
  print(e)
  print("Error loading environment variables")