from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from shared_lib.exception import ApplicationError


       
async def init_mongo_db(mongo_uri: str, mongo_port: int, database_name: str, models: list[Document]):
    try:
        motor_client: AsyncIOMotorClient = AsyncIOMotorClient(
            mongo_uri, mongo_port, serverSelectionTimeoutMS=3000
        )
        await init_beanie(
                motor_client.get_database(database_name),
                document_models=models,
            ) 
    except Exception as e:
        raise ApplicationError(f"Failed to connect to Monogo DB: {e}", status_code=500)
