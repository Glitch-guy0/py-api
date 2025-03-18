import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import env
from models.session_model import Session
from models.user_model import User


async def db_init():
    client = AsyncIOMotorClient(f"mongodb://{env.DB_USER}:{env.DB_PASS}@{env.DB_HOST}/{env.DB_NAME}")

    if not client:
        print("Error Connecting to DB, is it running?")
        raise SystemExit(1)

    # Initialize beanie with the Product document class
    db_connection = await init_beanie(database=client.db_name, document_models=[User, Session])