# manages user sessions including
# - Cookies
# - JWT tokens

from fastapi import Response, Request, HTTPException
from dataclasses import dataclass, field
import jwt
from models.session import Session, Session_Schema
import env
from beanie import PydanticObjectId
import datetime
from lib.logger import logger

class Session_Manager:  
  @staticmethod
  async def create_session(user_id: PydanticObjectId, fastapi_response: Response)-> None:
    session_token = await Session.create_session(user_id)
    payload = JWT_Payload(auth_token=session_token) # session for user authentication / user session
    logger.debug("creating jwt payload")
    jwt_token: str = jwt.encode(payload.to_json(), env.JWT_SECRET, algorithm="HS256")
    logger.debug("calling cookie-manager to send metadata")
    await Cookie_Manager.set_jwt_token(jwt_token, fastapi_response)

  @staticmethod
  async def get_session_user_id(fastapi_request: Request)-> PydanticObjectId:
     logger.info("user_id request from session-manager")
     user_session = await Session_Manager.get_session(fastapi_request)
     return user_session.id
  

  @staticmethod
  async def get_session(fastapi_request: Request)-> Session_Schema:
    logger.debug("get-session reqeust for session-schema")
    jwt_cookie = await Cookie_Manager.get_jwt_token(fastapi_request)
    try:
      logger.debug("decoding jwt payload")
      jwt_payload = JWT_Payload(**jwt.decode(jwt_cookie, env.JWT_SECRET,algorithms=["HS256"]))
      user_session = await Session.get_session(jwt_payload.auth_token)
      return user_session
    
    except jwt.ExpiredSignatureError as e:
        logger.warning(f"Expired Token: {e}")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidSignatureError as e:
        logger.warning(f"JWT Signature error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token signature")
    except jwt.DecodeError as e:
        logger.error(f"JWT Decoding error: {e}")
        raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.InvalidAudienceError as e:
        logger.warning(f"audience error: {e}")
        raise HTTPException(status_code=403, detail="Invalid token audience")
    except jwt.InvalidIssuerError as e:
        logger.error(f"invalid issuer error: {e}")
        raise HTTPException(status_code=403, detail="Invalid token issuer")
    except jwt.InvalidTokenError as e:
        logger.error(f"invalid token: {e}")
        raise HTTPException(status_code=400, detail="Invalid token")
    
    
  @staticmethod
  async def delete_session(fastapi_request: Request, fastapi_response: Response)-> None:
    logger.info("delete session request")
    logger.debug("calling session-manager to get current session")
    user_session = await Session_Manager.get_session(fastapi_request)
    await Session.delete_session(user_session.session_token)

@dataclass
class JWT_Payload:
  auth_token: str
  exp: datetime.datetime = field(default_factory=lambda: datetime.datetime.now() + datetime.timedelta(days=1))
  iat: datetime.datetime = field(default_factory=datetime.datetime.now)

  def to_json(self):
     json_payload = {
        "auth_token": self.auth_token,
        # JWT requires numeric dates
        "exp": int(self.exp.timestamp()),
        "iat": int(self.iat.timestamp())
     }
     logger.debug(f"jwt-payload to json format: {json_payload}")
     return json_payload

@dataclass
class Cookie_Manager:
  auth_token: str = "access_token"
  auth_token_expiry: int = 60 * 60 * 24 # 1 Day

  @staticmethod
  async def set_jwt_token(jwt_token: str, fastapi_response: Response)-> Response:
    logger.debug(f"cookie-manager to set jwt token {jwt_token}")
    fastapi_response.set_cookie(
    key=Cookie_Manager.auth_token,
    value=jwt_token,
    max_age=Cookie_Manager.auth_token_expiry,          
    secure=False,  # if using HTTPS  
    httponly=False, # can be acccessed via js
    samesite="lax"        
    )
    logger.info("added cookie")
    return fastapi_response

  @staticmethod
  async def get_jwt_token(fastapi_request: Request)-> str:
    logger.info("get jwt token from request")
    jwt_token = fastapi_request.cookies.get(Cookie_Manager.auth_token)
    if(not jwt_token):
      logger.debug("cookie not found")
      raise HTTPException(401, "You're not logged in. Please log in to continue.")
    logger.debug("cookie found")
    return jwt_token

  @staticmethod
  async def delete_jwt_token(fastapi_response: Response)-> Response:
    logger.info("deleting cookie")
    fastapi_response.delete_cookie(Cookie_Manager.auth_token)
    return fastapi_response