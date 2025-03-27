from fastapi import APIRouter, Request, HTTPException, Response
router = APIRouter(prefix="/user")
from models.user import User, Login_Data, Update_User
from lib.auth.session_manager import Session_Manager
from lib.auth.account_manager import Account_Manager
from lib.logger import logger
from lib.auth.session_manager import Session_Manager
from pydantic import ValidationError

@router.post("/")
async def create_user(request: Request, response: Response):
  logger.info("create user reqeust")
  data = await request.json()
  logger.debug("parsing http body")
  try:
    user_data = User(**data)
  except ValidationError as e:
    for error in e.errors():
      logger.warning(f"body-data Validation error: {error}")
      raise HTTPException(422, error.get('msg'))
  logger.debug("calling account manager to create user")
  await Account_Manager.create_user(user_data)
  return {"detail": "User Created"}


@router.get("/")
async def login_user(request: Request, response: Response):
  data = await request.json()
  try:
    login_data = Login_Data(**data)
  except ValidationError as e:
    for error in e.errors():
      logger.warning(f"body-data Validation error: {error}")
      raise HTTPException(422, error.get('msg'))
  user_data = await Account_Manager.verify_user_login(login_data)
  await Session_Manager.create_session(user_data.id, response)
  return {"detail": "Login Successful"}


@router.put("/")
async def update_user(request: Request, response: Response):
  logger.info("update user request")
  user_id = await Session_Manager.get_session_user_id(request)
  logger.debug(f"got user_id from session-manager: {user_id}")
  logger.info("Valid User")
  try:
    user_data = Update_User(**await request.json())
  except ValidationError as e:
    for error in e.errors():
      logger.warning(f"body-data Validation error: {error}")
      raise HTTPException(422, error.get('msg'))
  await User.update_user(user_id,user_data)
  return {"detail": "Update Successful"}


@router.delete("/")
async def delete_user(request: Request, response: Response):
  logger.info("user deleting request")
  user_id = await Session_Manager.get_session_user_id(request)
  logger.debug(f"got user_id from session-manager: {user_id}")
  logger.info("Deleting User")
  await Account_Manager.delete_user(user_id)
  await Session_Manager.delete_session(request, response)
  return {"detail": "Deleted User"}