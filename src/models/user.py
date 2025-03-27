# contains user database related functions
from beanie import Document, Indexed, PydanticObjectId
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated, Optional
from fastapi import HTTPException
from lib.auth.crypto import Crypto
from lib.logger import logger

class Update_User(BaseModel):
  model_config = ConfigDict(extra='forbid')
  username: Optional[str] = Field(None, min_length=3, max_length=20)

class Login_Data(BaseModel):
  email: EmailStr
  password: str = Field(min_length=8, max_length=20)

class Login_Info(BaseModel):
  id: PydanticObjectId
  password: bytes

class User_Schema(Document):
  username: str = Field(min_length=3, max_length=20)
  email: Annotated[EmailStr, Indexed(unique=True)]
  password: bytes

class User(BaseModel):
  username: str = Field(min_length=3, max_length=20)
  email: EmailStr
  password: str = Field(min_length=8, max_length=20)

  @staticmethod
  async def create_user(user: "User")->None:
    logger.debug(f"creating new user: {user}")
    try:
      hashed_password = Crypto.hash_password(user.password)
      new_user = User_Schema(username=user.username, email=user.email, password=hashed_password)
      logger.debug("storing user into database")
      await new_user.insert()
    except DuplicateKeyError as e:
      logger.info("User already exists")
      raise HTTPException(409, "User already exists")

  @staticmethod
  async def get_user_by_email(email: EmailStr)->Login_Info :
    logger.debug("get user id by email")
    user = await User_Schema.find_one({"email": email})
    if not user:
      logger.warning("user not found")
      raise HTTPException(404, "User not Found")
    logger.debug("user found")
    return Login_Info(id=user.id, password=user.password)
  
  @staticmethod
  async def get_user_by_id(user_id: PydanticObjectId)-> User_Schema:
    logger.debug("get user data using user id")
    user = await User_Schema.find_one({"_id": user_id})
    if not user:
      logger.warning(f"user not found: {user}")
      raise HTTPException(404, "User not Found")
    return user
  
  @staticmethod
  async def update_user(user_id: PydanticObjectId, user_data: Update_User)-> None:
    logger.info(f"update user reqeust for user id: {user_id}")
    user_data.model_dump(exclude_none=True)
    user = await User.get_user_by_id(user_id)
    logger.debug(f"user found!, updating user to {user_data}")
    await user.update({"$set": user_data})

  @staticmethod
  async def delete_user(user_id: PydanticObjectId)-> None:
    logger.debug("delete user request")
    user = await User.get_user_by_id(user_id)
    if not user:
      raise HTTPException(404, "User not Found")
    user.delete()