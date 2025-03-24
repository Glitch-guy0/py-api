# contains user database related functions
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field, EmailStr
from typing import Annotated, Optional
from fastapi import HTTPException

class Update_User(Document):
  username: Optional[str] = Field(min_length=3, max_length=20)
  password: Optional[str]

class Login_Info(Document):
  id: PydanticObjectId
  password: bytes

class User_Schema(Document):
  username: str = Field(min_length=3, max_length=20)
  email: Annotated[EmailStr, Indexed(unique=True)]
  password: bytes

class User(Document):
  username: str = Field(min_length=3, max_length=20)
  email: Annotated[EmailStr, Indexed(unique=True)]
  password: str

  @staticmethod
  async def create_user(user: "User")->None:
    try:
      # todo: validaton checks
      # password to bytes
      new_user = User_Schema(username=user.username, email=user.email, password=bytes(user.password))
      await new_user.insert()

    except Exception as e:
      print("user insertion error: ", e)
      raise HTTPException(500, "server error")

  @staticmethod
  async def get_user_by_email(email: EmailStr)->Login_Info :
    user = await User_Schema.find_one({"email": email})
    if not user:
      raise HTTPException(404, "User not Found")
    return Login_Info(id=user.id, password=user.password)
  
  @staticmethod
  async def get_user_by_id(id: PydanticObjectId)-> User_Schema:
    user = await User_Schema.find_one({"_id": id})
    if not user:
      raise HTTPException(404, "User not Found")
    return user