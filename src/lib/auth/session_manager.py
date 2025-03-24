from models.user import Login_Info
from fastapi import Response

class Session_Manager:
  def create_session(user_info: Login_Info, fastapi_response: Response)-> Response:
    print("got id", user_info.id)
    return fastapi_response