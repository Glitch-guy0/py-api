# used to validate password, email and stuff
from fastapi import HTTPException
import re

class Validations:
  @staticmethod
  def password_validator(password:  str)-> None:
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#&])[A-Za-z\d@$#&]{8,20}$"
    regex = re.compile(password_regex)
    valid = re.search(regex, password)
    if valid:
      return
    else:
      raise HTTPException(
          status_code=422, # Unprocessable Entity 
          detail="Password does not meet validation criteria. Must be 8-20 characters long, contain uppercase, lowercase, digit, special characters (@$#&)"
        )