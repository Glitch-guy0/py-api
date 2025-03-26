from models.user import Login_Info
from fastapi import Response, Request, HTTPException
from dataclasses import dataclass
import jwt

class Session_Manager:
  def create_session(user_info: Login_Info, fastapi_response: Response)-> Response:
    print("got id", user_info.id)
    return fastapi_response
  
@dataclass
class Cookie_Manager:
  auth_token: str = "access_token"
  auth_token_expiry: int = 60 * 60 * 24 # 1 Day

  @staticmethod
  async def set_auth_token(session_token: str, fastapi_response: Response)-> Response:
    fastapi_response.set_cookie(
    key=Cookie_Manager.auth_token,
    value=session_token,
    max_age=Cookie_Manager.auth_token_expiry,
    path="/",             
    domain="example.com", 
    secure=False,  # if using HTTPS  
    httponly=False, # can be acccessed via js
    samesite="lax"        
    )
    return fastapi_response

  @staticmethod
  async def get_auth_token(fastapi_request: Request)-> str:
    session_token = fastapi_request.cookies.get(Cookie_Manager.auth_token)
    if(not session_token):
      raise HTTPException(401, "You're not logged in. Please log in to continue.")
    return session_token

  @staticmethod
  async def delete_auth_token(fastapi_response: Response)-> Response:
    fastapi_response.delete_cookie(Cookie_Manager.auth_token)
    return fastapi_response