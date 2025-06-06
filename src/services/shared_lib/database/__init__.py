from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from shared_lib.exception import ApplicationError
from shared_lib import lib_logger as logger
from shared_lib.logger import JSONLogger

class DBInitializer:
    @staticmethod
    async def add_monogodb(
        mongo_uri: str,
        mongo_port: int,
        database_name: str,
        models: list[Document],
        serverSelectionTimeoutMS: int = 3000,
        max_attempts: int = 3,
    ):
        attempts = 1

        def cleanup(logger: JSONLogger):
            logger.debug(
                message="Cleaning up mongo db initialization logger",
                context={},
            )
            del logger

        while attempts <= max_attempts:
            try:
                motor_client: AsyncIOMotorClient = AsyncIOMotorClient(
                    mongo_uri,
                    mongo_port,
                    serverSelectionTimeoutMS=serverSelectionTimeoutMS,
                )
                await init_beanie(
                    motor_client.get_database(database_name),
                    document_models=models,
                )
                cleanup(logger)
                return
            except ValueError as e:
                cleanup(logger)
                raise ApplicationError(
                    f"Error while connecting to database: {e.args[0]}", status_code=500
                )
            except Exception:
                logger.error(
                    message=f"Failed to connect to Monogo DB retrying {attempts}/{max_attempts} ...",
                    context={"attempts": attempts, "max_attempts": max_attempts},
                )
                attempts += 1
        cleanup(logger)
        raise ApplicationError(f"Failed to connect to Monogo DB", status_code=500)
