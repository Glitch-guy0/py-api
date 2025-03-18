
import datetime
from typing import Annotated
from beanie import Document, Indexed
import re
from pydantic import EmailStr
from fastapi import HTTPException


class User(Document):
  """
    Collection name: users
  """
  username: str
  email: Annotated[EmailStr, Indexed(unique=True)]
  password: str
  salt: int

  @classmethod
  def create(self, username, email, password):
    auth.password_validator(password)
    return self(username=username, email=email, password=password, salt=34)


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
    
