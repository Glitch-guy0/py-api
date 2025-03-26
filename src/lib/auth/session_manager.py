# manages user sessions including
# - Cookies
# - JWT tokens

from fastapi import Response, Request, HTTPException
from dataclasses import dataclass
import jwt
from models.session import Session, Session_Schema
import env
from beanie import PydanticObjectId
import datetime

class Session_Manager:  
  @staticmethod
  async def create_session(user_id: PydanticObjectId, fastapi_response: Response)-> None:
    session_token = await Session.create_session(user_id)
    payload = JWT_Payload(auth_token=session_token) # session for user authentication / user session
    jwt_token: str = jwt.encode(payload, env.JWT_SECRET)
    await Cookie_Manager.set_jwt_token(jwt_token, fastapi_response)

  @staticmethod
  async def get_session_user_id(fastapi_request: Request)-> PydanticObjectId:
     user_session = await Session_Manager.get_session(fastapi_request)
     return user_session.id
  

  @staticmethod
  async def get_session(fastapi_request: Request)-> Session_Schema:
    jwt_cookie = await Cookie_Manager.get_jwt_token(fastapi_request)
    try:
      jwt_payload = JWT_Payload(**jwt.decode(jwt_cookie, env.JWT_SECRET))
      user_session = await Session.get_session(jwt_payload.auth_token)
      return user_session
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token signature")
    except jwt.DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=403, detail="Invalid token audience")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=403, detail="Invalid token issuer")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    
  @staticmethod
  async def delete_session(fastapi_request: Request, fastapi_response: Response)-> None:
    user_session = await Session_Manager.get_session(fastapi_request)
    await Session.delete_session(user_session.session_token)

@dataclass
class JWT_Payload:
  auth_token: str
  exp: datetime = datetime.datetime.now() + datetime.timedelta(days=1)
  iat: datetime = datetime.datetime.now()

@dataclass
class Cookie_Manager:
  auth_token: str = "access_token"
  auth_token_expiry: int = 60 * 60 * 24 # 1 Day

  @staticmethod
  async def set_jwt_token(jwt_token: str, fastapi_response: Response)-> Response:
    fastapi_response.set_cookie(
    key=Cookie_Manager.auth_token,
    value=jwt_token,
    max_age=Cookie_Manager.auth_token_expiry,
    path="/",             
    domain="example.com", 
    secure=False,  # if using HTTPS  
    httponly=False, # can be acccessed via js
    samesite="lax"        
    )
    return fastapi_response

  @staticmethod
  async def get_jwt_token(fastapi_request: Request)-> str:
    session_token = fastapi_request.cookies.get(Cookie_Manager.auth_token)
    if(not session_token):
      raise HTTPException(401, "You're not logged in. Please log in to continue.")
    return session_token

  @staticmethod
  async def delete_jwt_token(fastapi_response: Response)-> Response:
    fastapi_response.delete_cookie(Cookie_Manager.auth_token)
    return fastapi_response