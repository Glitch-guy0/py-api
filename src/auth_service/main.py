import sys
from fastapi import FastAPI

# from auth_service.api.okta_api import router as auth_router
from auth_service.config import Config
from shared_lib.database import DBInitializer
from auth_service.models import models


async def initialize_server(app: FastAPI):
    try:
        await DBInitializer.add_monogodb(
            Config.mongo_uri, Config.mongo_port, Config.mongo_db_name, models
        )
        yield
    except Exception:
        print(
            "Failed to initialize server. Please check the logs for details.",
            file=sys.stderr,
        )
        sys.exit(1)


app = FastAPI(lifespan=initialize_server)

# app.include_router(auth_router)


# test endpoint
@app.get("/test")
async def test():
    return {"message": "Hello, World!"}
