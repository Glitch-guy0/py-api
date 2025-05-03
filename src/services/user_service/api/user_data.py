from fastapi import APIRouter, Header
from shared_lib.exception import ApplicationError
router = APIRouter()

@router.get("/user")
async def get_user_data(userdata = Header(None)):
   if userdata is None:
      raise ApplicationError("The server cannot meet the requirements of the Expect request-header field. Adjust the request and try again.", 417)
   return userdata
