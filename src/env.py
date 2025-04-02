from dotenv import dotenv_values
from pathlib import Path
import os

class Environment:
  env = {}

  @staticmethod
  def load_env():
    secrets_path = os.getenv('SECRETS_PATH')
    if not secrets_path:
      raise ValueError('SECRETS_PATH environment variable is not set')
    secrets_path = Path(secrets_path)
    if not secrets_path.is_file():
      raise FileNotFoundError(f'{secrets_path} does not exist')
    Environment.env = dotenv_values(secrets_path)
    