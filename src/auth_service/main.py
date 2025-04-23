from fastapi import FastAPI
from auth_service.api.okta_api import router as auth_router
from shared_lib.database.init_mongodb import init_db
from auth_service.lib.logger import logger
from auth_service.config import Config


async def initialize_server(app: FastAPI):
    logger.info(f"Initializing {Config.service_name} ...")
    logger.info("Initiating MongoDB ...")
    await init_db()
    logger.info("MongoDB OK")
    yield
    logger.info(f"Shutting down {Config.service_name} ...")


app = FastAPI(lifespan=initialize_server)  # type: ignore

app.include_router(auth_router)


# test endpoint
@app.get("/test")
async def test():
    logger.debug("Test endpoint called")
    return {"message": "Hello, World!"}
