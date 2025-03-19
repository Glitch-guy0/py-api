

from typing import Annotated
from beanie import Document, Indexed
import re
from pydantic import EmailStr, Field
from fastapi import HTTPException
import env
import bcrypt
import random

class User(Document):
  """
    Collection name: users
  """
  username: str = Field(min_length=3, max_length=20)
  email: Annotated[EmailStr, Indexed(unique=True)]
  password: bytes # bcrypt returns byte data
  # bcrypt stores salt and other metadata internally

  @classmethod
  def create(self, username:str, email:EmailStr, password:str):
    auth.password_validator(password)
    salt: bytes = bcrypt.gensalt(random.randint(12,15))
    hashed_password: bytes = bcrypt.hashpw(User.__encode_password(password),salt)
    return self(username=username, email=email, password=hashed_password)

  @staticmethod
  def __encode_password(password:str)->bytes:
    return password.encode('utf-8')

class auth:
  def password_validator(password: str) -> bool:
    """
      just a function call to validate password, in case of error it will automatically send response back.
      Raises:
        HTTPException: if password didn't meet the criteria
    """
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#&])[A-Za-z\d@$#&]{8,20}$"
    regex = re.compile(password_regex)
    valid = re.search(regex, password)
    if valid:
      return True
    else:
      raise HTTPException(
          status_code=422, # Unprocessable Entity 
          detail="Password does not meet validation criteria. Must be 8-20 characters long, contain uppercase, lowercase, digit, special characters (@$#&)"
        )
    
