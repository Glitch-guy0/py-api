from fastapi import APIRouter, Request, HTTPException, Response
router = APIRouter(prefix="/user")
from models.user import User, Login_Data, Update_User
from lib.auth.session_manager import Session_Manager
from lib.auth.account_manager import Account_Manager
from lib.logger import logger
from lib.auth.session_manager import Session_Manager

@router.post("/")
async def create_user(request: Request, response: Response):
  logger.info("create user reqeust")
  data = await request.json()
  logger.debug("parsing http body")
  user_data = User(**data)
  logger.debug("calling account manager to create user")
  await Account_Manager.create_user(user_data)
  return {"message": "User Created"}


@router.get("/")
async def login_user(request: Request, response: Response):
  data = await request.json()
  login_data = Login_Data(**data)
  user_data = await Account_Manager.verify_user_login(login_data)
  await Session_Manager.create_session(user_data.id, response)
  return {"detail": "Login Successful"}


@router.put("/")
async def update_user(request: Request, response: Response):
  logger.info("update user request")
  user_id = await Session_Manager.get_session_user_id(request)
  logger.debug(f"got user_id from session-manager: {user_id}")
  logger.info("Valid User")
  user_data = Update_User(**await request.json())
  await User.update_user(user_id,user_data)
  return {"detail": "Update Successful"}