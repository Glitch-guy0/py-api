from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from typing import Optional

from lib.database import Database
from lib.logger import logger
from User.route import router as user_route
from env import Environment

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize database connection on application startup.
    Exits the application if database connection fails.
    """
    try:
        await Database.db_connect()
        Environment.load_env()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}")
        raise
    yield


# Initialize FastAPI app
app = FastAPI(
    title="User Management API",
    description="API for managing user accounts and sessions",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(user_route)

@app.get("")
async def root() -> dict[str, str]:
    """
    Root endpoint to check if the server is running.
    
    Returns:
        dict: A message indicating the server is running
    """
    return {"status": "Server Running"}

def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True) -> None:
    """
    Start the FastAPI server with the specified configuration.
    
    Args:
        host (str): The host to bind the server to
        port (int): The port to bind the server to
        reload (bool): Whether to enable auto-reload on code changes
    """
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    start_server()
