from beanie import Document, PydanticObjectId, Indexed
from typing import Annotated
import secrets
from fastapi import HTTPException
from lib.logger import logger


class Session_Schema(Document):
  session_token: Annotated[str, Indexed(unique=True)]
  user_id: PydanticObjectId # can be unique to limit logons

class Session:
  @staticmethod
  async def create_session(user_id: PydanticObjectId)-> str:
    logger.debug(f"creating new session for user: {user_id}")
    token: str = secrets.token_hex(32)
    session = Session_Schema(session_token=token, user_id=user_id)
    logger.debug("store user session in database")
    await session.insert()
    logger.debug("returning token")
    return token

  @staticmethod
  async def get_session(session_token: str)-> Session_Schema:
    logger.info("get user session")
    session_data = await Session_Schema.find_one(Session_Schema.session_token == session_token)
    if not session_data:
      logger.warning("user session not found")
      raise HTTPException(404, "Session not Found")
    logger.debug("found user session")
    return session_data

  @staticmethod
  async def delete_session(session_token: str)->None:
    logger.debug("request to delete user session")
    session_data = await Session_Schema.find_one(Session_Schema.session_token == session_token)
    if session_data:
      session_data.delete()