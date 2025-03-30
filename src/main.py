from lib.database import Database
import uvicorn
from fastapi import FastAPI
app = FastAPI()
from User.route import router as user_route
from lib.logger import logger

@app.on_event("startup")
async def startup():
  await Database.db_connect()


app.include_router(user_route)

@app.get("")
def root():
  return "Server Running"

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0")
