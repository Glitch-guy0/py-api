
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
  async def create(cls, session_token: str, user_id: PydanticObjectId):
    new_session = cls(session_token=session_token, user_id=user_id, created_at=datetime.datetime.now())
    try:
      await new_session.save()
    except Exception as e:
      raise HTTPException(409, "Session alrady Exists")