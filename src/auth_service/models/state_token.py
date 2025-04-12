from beanie import Document, Indexed
from beanie.exceptions import DocumentAlreadyCreated
import datetime

from fastapi import HTTPException


class StateToken(Document):
    state_token: str
    user_ip: str
    created_at: int = Indexed(expireAfterSeconds=15)

    @classmethod
    async def save_token(cls, user_ip: str, state_token: str) -> str:
        cls_object = cls(
            user_ip=user_ip,
            state_token=state_token,
            created_at=int(datetime.datetime.now().timestamp()),
        )
        try:
            await cls_object.save()
            return cls_object.state_token
        except Exception as e:
            raise e

    @staticmethod
    async def get_token(user_ip: str) -> str:
        token = await StateToken.find_one(StateToken.user_ip == user_ip)
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized: Token not found")

        return token.state_token
