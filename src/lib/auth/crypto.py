# this is where bcrypt and jwt goes
import bcrypt
import random
from .validations import Validations
from fastapi import HTTPException
from lib.logger import logger

class Crypto:
  @staticmethod
  def hash_password(password: str)-> bytes:
    logger.debug("hashing password")
    Validations.password_validator(password)
    salt = bcrypt.gensalt(rounds=random.randint(12, 15))
    return bcrypt.hashpw(Crypto.__encode_password(password), salt)

  def __encode_password(password: str)-> bytes:
    logger.debug("password encoder call")
    return password.encode("utf-8")
  
  def verify_password(password: str, db_password: bytes):
    if not bcrypt.checkpw(Crypto.__encode_password(password), db_password):
      logger.debug("password is not matching")
      logger.error("incorrect password attempt")
      raise HTTPException(401, "Unauthorized Access")