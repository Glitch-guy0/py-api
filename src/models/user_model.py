
from __future__ import annotations
from typing import Annotated, Optional
from beanie import Document, Indexed, PydanticObjectId
import re
from pydantic import EmailStr, Field, BaseModel
from fastapi import HTTPException
from pymongo import UpdateMany
import env
import bcrypt
import random
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from auth_model import Auth

class Update_User(BaseModel):
  username: Optional[str] = Field(min_length=3, max_length=20)
  email: Optional[EmailStr] = None
  password: Optional[bytes] = None # bcrypt returns byte data


class User(Document):
  """
    Collection name: users
  """
  username: str = Field(min_length=3, max_length=20)
  email: Annotated[EmailStr, Indexed(unique=True)]
  password: bytes # bcrypt returns byte data
  # bcrypt stores salt and other metadata internally


  # note: class mehtod is class *not instance* similar to static methods
  @classmethod
  async def create(cls, username:str, email:EmailStr, password:str):
    try:
      Auth.password_validator(password)
      salt: bytes = bcrypt.gensalt(random.randint(12,15))
      hashed_password: bytes = bcrypt.hashpw(User.__encode_password(password),salt)
      new_user:User = cls(username=username, email=email, password=hashed_password)
      await new_user.save()
    
    except DuplicateKeyError:
      raise HTTPException(409, "User already Exist!")
    
  @staticmethod
  def __encode_password(password:str)->bytes:
    return password.encode('utf-8')


  @staticmethod
  async def get_user_by_id(user_id: ObjectId):
    """
      returns user details using user_id?
    """
    user = await User.find_one({"_id": user_id})
    
    if not user:
      raise HTTPException(404, "user not found!!")
    
    return user

  @staticmethod
  async def get_user_login_details(user_email: EmailStr):
    """
      returns dict(id, password) if exists
      Raises:
        HTTPException: user not found
        # HTTPException: Email format is not correct
    """
    user = await User.find_one({"email": user_email})
    if(not user):
      raise HTTPException(404, "User not Found")
    
    login_data = dict()
    login_data["id"] = user.id
    login_data["password"] = user.password
    return login_data

  @staticmethod
  async def update_user(userid: PydanticObjectId, user_data: Update_User )-> None:
    modified_data_fields = user_data.model_dump(exclude_none=True)
    response :UpdateMany = await User.find_one({"_id": userid}).update({"$set": modified_data_fields})
    
    if not response.raw_result.get('updatedExisting'):
      raise HTTPException(404, "User does not exist")
    
  @staticmethod
  async def delete_user(user_id: PydanticObjectId)->None:
    response = await User.find_one({"_id": user_id}).delete()
    if not response:
      raise HTTPException(404, "User Not Found")