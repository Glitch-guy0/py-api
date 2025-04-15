from beanie import Document, Indexed
from beanie.exceptions import DocumentAlreadyCreated
from typing import Annotated
import datetime
from shared_lib.exception import ApplicationError


class StateToken(Document):
    state_token: str
    user_ip: str
    created_at: Annotated[datetime.datetime, Indexed(expireAfterSeconds=15)]

    @classmethod
    async def save_token(cls, user_ip: str, state_token: str) -> str:
        cls_object = cls(
            user_ip=user_ip,
            state_token=state_token,
            created_at=datetime.datetime.now().timestamp(),
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
            raise ApplicationError("Unauthorized: Token not found", status_code=401)

        return token.state_token
