import sys
from fastapi import FastAPI

from auth_service.config import Config
from shared_lib.database import DBInitializer
from auth_service.models import models
from auth_service.api.okta_api import router as auth_router
from auth_service import ServiceLog as logger

async def initialize_server(app: FastAPI):
    logger.info("Initializing server", context={"action": "initialize_server"})
    try:
        logger.debug(
            "Connecting to MongoDB",
            context={
                "action": "db_connect",
                "uri": Config.mongo_uri,
                "port": Config.mongo_port,
                "db": Config.mongo_db_name
            }
        )
        await DBInitializer.add_monogodb(
            Config.mongo_uri, Config.mongo_port, Config.mongo_db_name, models
        )
        logger.info("Server initialization complete", context={"action": "initialize_server"})
        yield
    except Exception as e:
        logger.critical(
            "Failed to initialize server - application shutting down",
            context={
                "action": "initialize_server",
                "error": str(e)
            }
        )
        print(
            "Failed to initialize server. Please check the logs for details.",
            file=sys.stderr,
        )
        sys.exit(1)


app = FastAPI(lifespan=initialize_server)

logger.info("Adding routes to application", context={"action": "add_routes"})
app.include_router(auth_router)


# test endpoint
@app.get("/test")
async def test():
    logger.debug("Test endpoint called", context={"action": "test_endpoint"})
    return {"message": "Hello, World!"}
