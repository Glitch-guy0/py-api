from fastapi import FastAPI
from user_service.api.user_data import router as user_data_router

app = FastAPI()

app.include_router(user_data_router)
