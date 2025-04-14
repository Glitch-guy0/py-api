from fastapi import FastAPI
from auth_service.api.auth import router as auth_router
from auth_service.lib.init_db import init_db
from auth_service.lib.logger import logger


async def lifespan(app: FastAPI):
    logger.info("Initializing database ...")
    print("Initializing database ...")
    await init_db()
    logger.info("Database initialized")
    print("Database initialized")
    yield


app = FastAPI(lifespan=lifespan)  # type: ignore

app.include_router(auth_router)


# test endpoint
@app.get("/test")
async def test():
    logger.debug("Test endpoint called")
    return {"message": "Hello, World!"}
