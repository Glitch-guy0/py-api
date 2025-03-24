# this is where bcrypt and jwt goes
import bcrypt
import random

class Crypto:
  @staticmethod
  def hash_password(password: str)-> bytes:
    salt = bcrypt.gensalt(rounds=random.randint(12, 15))
    return bcrypt.hashpw(Crypto.__encode_password(password), salt)

  def __encode_password(password: str)-> bytes:
    return password.encode("utf-8")