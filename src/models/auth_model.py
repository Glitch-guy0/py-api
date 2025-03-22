from fastapi import HTTPException
import re


class Auth:
  @staticmethod
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
