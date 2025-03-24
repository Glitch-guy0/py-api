from fastapi import APIRouter, Request, HTTPException, Response
router = APIRouter(prefix="/user")
from models.user import User, Login_Data, Login_Info
from lib.auth.session_manager import Session_Manager
from lib.auth.login_manager import Login_Manager

@router.post("/")
async def create_user(request: Request, response: Response):
  data = await request.json()
  user_data = User(**data)
  await User.create_user(user_data)
  return {"message": "User Created"}


@router.get("/")
async def login_user(request: Request, response: Response):
  data = await request.json()
  login_data = Login_Data(**data)
  user_data = await Login_Manager.verify_login_data(login_data)
  Session_Manager.create_session(user_data, response)
  return {"detail": "Login Successful"}