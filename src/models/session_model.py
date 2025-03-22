
import datetime
from typing import Annotated
from beanie import Document, Indexed, PydanticObjectId
from fastapi import HTTPException
import string
import secrets


class Session(Document):
  """
    Collection name: sessions
  """
  session_token: Annotated[str, Indexed(unique=True)]
  user_id: PydanticObjectId
  created_at: Annotated[datetime.datetime, Indexed(expireAfterSeconds=60*60*24)]


  @staticmethod
  def __generate_token(length=32):
    """
      randomly selects 32 characters
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

  @classmethod
  async def create_session(cls, user_id: PydanticObjectId)-> str:
    token = Session.__generate_token()
    new_session = cls(session_token=token, user_id=user_id, created_at=datetime.datetime.now())
    try:
      await new_session.save()
      return token
    except Exception as e:
      raise HTTPException(500, "Internal Server Error")
    
  @staticmethod
  async def get_session_userid(session_token: str)-> PydanticObjectId:
    session_data:Session|None = await Session.find_one({"session_token": session_token})
    if not session_data:
      raise HTTPException(401, "Session Expired, Please Login")
    
    return session_data.user_id
  

  @staticmethod
  async def delete_session(session_token: str)-> None:
    await Session.find_one({"session_token": session_token}).delete()
