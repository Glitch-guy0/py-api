# provides decorator for private routes
from fastapi import Request
from ..session_manager import Session_Manager
from lib.logger import logger

def protected_route(fastapi_request: Request):
  def decorator(func):
    async def wrapper(*args, **kwargs):
        logger.debug("proteced route decorator")
        user_id = await Session_Manager.get_session_user_id(fastapi_request)
        return await func(user_id, *args, **kwargs)
    return wrapper
  return decorator
