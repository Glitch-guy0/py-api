from beanie import Document, Indexed
from beanie.exceptions import DocumentAlreadyCreated
import datetime


class StateToken(Document):
    state_token: str
    user_ip: str
    created_at: int = Indexed(expireAfterSeconds=15)

    @classmethod
    async def get_state_token(cls, user_ip: str, state_token: str) -> str:
        cls_object = cls(
            user_ip=user_ip,
            state_token=state_token,
            created_at=int(datetime.datetime.now().timestamp()),
        )
        try:
            await cls_object.save()
            return cls_object.state_token
        except DocumentAlreadyCreated as e:
            # critical error
            raise e
        except Exception as e:
            raise e
