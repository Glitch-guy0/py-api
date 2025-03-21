
import datetime
from typing import Annotated
from beanie import Document, Indexed, PydanticObjectId
from fastapi import HTTPException


class Session(Document):
  """
    Collection name: sessions
  """
  session_token: Annotated[str, Indexed(unique=True)]
  user_id: PydanticObjectId
  created_at: Annotated[datetime.datetime, Indexed(expireAfterSeconds=60*60*24)]

  @classmethod
  async def create_session(cls, session_token: str, user_id: PydanticObjectId)-> None:
    new_session = cls(session_token=session_token, user_id=user_id, created_at=datetime.datetime.now())
    try:
      await new_session.save()
    except Exception as e:
      raise HTTPException(409, "Session alrady Exists")
    
  @staticmethod
  async def get_session_userid(session_token: str)-> PydanticObjectId:
    session_data:Session|None = await Session.find_one({"session_token": session_token})
    if not session_data:
      raise HTTPException(401, "Session Expired, Please Login")
    
    return session_data.user_id