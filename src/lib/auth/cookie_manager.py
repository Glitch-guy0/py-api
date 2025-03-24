from fastapi import Response, Request, HTTPException
import jwt
import env
from datetime import datetime


class Cookie_Manager:
  access_key: str = "access-token"

  @staticmethod
  def create_jwt_token(fastapi_response: Response, session_token: str)->Response:
    jwt_payload = {
      Cookie_Manager.access_key: session_token,
      "iat": datetime.datetime.utcnow(), 
      "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    jwt_token = jwt.encode(jwt_payload,env.JWT_SECRET)
    fastapi_response.set_cookie(Cookie_Manager.access_key, jwt_token)
    return fastapi_response
  
  @staticmethod
  def verify_jwt_token(fastapi_request: Request)-> str:
    try:
      jwt_token = fastapi_request.cookies.get(Cookie_Manager.access_key)
      jwt_payload = jwt.decode(jwt_token, env.JWT_SECRET)
      return jwt_payload.get(Cookie_Manager.access_key)
    except Exception as e:
      raise HTTPException(401, "Unauthorized Access, Login Required")

  @staticmethod
  def delete_jwt_token(fastapi_response: Response)-> Response:
    fastapi_response.delete_cookie(Cookie_Manager.access_key)
    return fastapi_response