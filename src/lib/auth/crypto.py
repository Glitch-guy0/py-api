# this is where bcrypt and jwt goes
import bcrypt
import random
from .validations import Validations

class Crypto:
  @staticmethod
  def hash_password(password: str)-> bytes:
    Validations.password_validator(password)
    salt = bcrypt.gensalt(rounds=random.randint(12, 15))
    return bcrypt.hashpw(Crypto.__encode_password(password), salt)

  def __encode_password(password: str)-> bytes:
    return password.encode("utf-8")