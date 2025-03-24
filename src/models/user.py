# contains user database related functions
from beanie import Document

class User(Document):
  name: str