from beanie import Document, PydanticObjectId, Indexed
from typing import Annotated
import secrets
from fastapi import HTTPException


class Session_Schema(Document):
  session_token: Annotated[str, Indexed(unique=True)]
  user_id: PydanticObjectId # can be unique to limit logons

  @staticmethod
  async def create_session(user_id: PydanticObjectId)-> str:
    token: str = secrets.token_hex(32)
    session = Session_Schema(session_token=token, user_id=user_id)
    await session.insert()
    return token

  @staticmethod
  async def get_session(session_token: str)-> PydanticObjectId:
    session_data = await Session_Schema.find_one(Session_Schema.session_token == session_token)
    if not session_data:
      raise HTTPException(404, "Session not Found")
    return session_data.user_id

  @staticmethod
  async def delete_session(session_token: str)->None:
    session_data = await Session_Schema.find_one(Session_Schema.session_token == session_token)
    if session_data:
      session_data.delete()