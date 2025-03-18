import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import env
from models.session_model import Session
from models.user_model import User
from pymongo.errors import ServerSelectionTimeoutError

async def db_connect():
    client = AsyncIOMotorClient(host=env.DB_HOST,port=env.DB_PORT,username=env.DB_USER, password=env.DB_PASS,connectTimeoutMS=3000, ServerSelectionTimeoutMS=3000)

    # Initialize beanie with the Product document class
    db_connection = await init_beanie(database=client[env.DB_NAME], document_models=[User, Session])


async def db_init():
    try:
        await db_connect()
    except ServerSelectionTimeoutError as db_err:
        print("Error connecting to DB, is it even runnning!!", db_err._message)
        sys.exit(1)
    except Exception as e:
        print("Error Occured!!\n",e)
        sys.exit(1)
    else:
        # db connection here
        print('connected to db')

if __name__ == "__main__":
    asyncio.run(db_init())