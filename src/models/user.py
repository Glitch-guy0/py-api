# contains user database related functions
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field, EmailStr
from typing import Annotated, Optional

class Update_User(Document):
  username: Optional[str] = Field(min_length=3, max_length=20)
  password: Optional[str]


class Login_Info(Document):
  id: PydanticObjectId
  password: bytes

class User(Document):
  username: str = Field(min_length=3, max_length=20)
  email: Annotated[EmailStr, Indexed(unique=True)]
  password: bytes
