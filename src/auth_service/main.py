from fastapi import FastAPI
from auth_service.api.okta_api import router as auth_router
from auth_service.lib.logger import logger
from auth_service.config import Config
from shared_lib.database import DBInitializer
from auth_service.models import models


async def initialize_server(app: FastAPI):
    await DBInitializer.add_monogodb(Config.mongo_uri, Config.mongo_port, Config.mongo_db_name, models)
    

app = FastAPI(lifespan=initialize_server)  # type: ignore

app.include_router(auth_router)


# test endpoint
@app.get("/test")
async def test():
    logger.debug("Test endpoint called")
    return {"message": "Hello, World!"}
