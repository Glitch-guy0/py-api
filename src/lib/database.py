from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.errors import ServerSelectionTimeoutError
import env
import sys
from models.user import User_Schema
from models.session import Session_Schema
from lib.logger import logger

class Database:

  @staticmethod
  async def __init_connection():
    logger.info("initiation db connection")
    database_client = AsyncIOMotorClient(host=env.DB_HOST,port=env.DB_PORT,username=env.DB_USER, password=env.DB_PASS,connectTimeoutMS=3000, ServerSelectionTimeoutMS=3000)
    await init_beanie(database=database_client[env.DB_NAME], document_models=[User_Schema, Session_Schema])

  @staticmethod
  async def db_connect():
    try:
      await Database.__init_connection()
    except ServerSelectionTimeoutError as conn_err:
      logger.critical("Error Connecting to DB, is it even Running!!")
      sys.exit(1)
    except Exception as e:
      logger.error("Database connection error", e)
      sys.exit(1)
    else:
      logger.info("connected to DB")
      








# async def db_connect():
#     client = AsyncIOMotorClient(host=env.DB_HOST,port=env.DB_PORT,username=env.DB_USER, password=env.DB_PASS,connectTimeoutMS=3000, ServerSelectionTimeoutMS=3000)

#     # Initialize beanie with the Product document class
#     db_connection = await init_beanie(database=client[env.DB_NAME], document_models=[User, Session])


# async def db_init():
#     try:
#         await db_connect()
#     except ServerSelectionTimeoutError as db_err:
#         print("Error connecting to DB, is it even runnning!!", db_err._message)
#         sys.exit(1)
#     except Exception as e:
#         print("Error Occured!!\n",e)
#         sys.exit(1)
#     else:
#         # db connection here
#         print('connected to db')