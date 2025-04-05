from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv

    
class System_Environment(BaseSettings):
  model_config = SettingsConfigDict(env_file=find_dotenv())

  # environment schema
  test: str


try:
  Config = System_Environment()
except ValidationError as e:
  error = e.errors()[0]
  err_message= f"{error.get('type')} environment variable {error.get('loc')} check .env file"
  print(err_message)
except Exception as e:
  print(e)
  print("Error loading environment variables")