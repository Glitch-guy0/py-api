from fastapi import APIRouter, Header
from shared_lib.exception import ApplicationError
router = APIRouter()

@router.get("/user")
async def get_user_data():
    return {"message": "user_service is working"}
