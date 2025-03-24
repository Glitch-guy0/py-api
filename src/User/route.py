from fastapi import APIRouter, Request, Response
router = APIRouter("/user")
from models.user import User


@router.post("/")
async def create_user(request: Request):
  data = await request.json()
  user_data = User(**data)
  await User.create_user(user_data)
  return {"message": "User Created"}
