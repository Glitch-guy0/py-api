from beanie import init_beanie
from auth_service.models.state_token import StateToken
from motor.motor_asyncio import AsyncIOMotorClient
from auth_service.config import config



motor_client: AsyncIOMotorClient = AsyncIOMotorClient(config.mongo_uri, config.mongo_port, serverSelectionTimeoutMS=3000)


async def init_db():
    try:
        await init_beanie(
            motor_client.get_database(config.mongo_db_name),
            document_models=[StateToken],
        )
    except Exception as e:
        print(f"Error initializing database: {e}, is the database running?")
        raise e

