from dataclasses import dataclass
from secrets import token_urlsafe
from fastapi import HTTPException
from auth_service.models.state_token import StateToken


@dataclass
class StateTokenRepository:
    def __init__(self, user_ip: str):
        self.user_ip = user_ip
        self.token = token_urlsafe(24)

    async def get_state_token(self):
        try:
            await StateToken.save_token(**self.__dict__)
            return self.token
        except Exception as e:
            # todo: proper exception handling
            raise e

    async def verify_state_token(self, user_ip: str, state_token: str) -> None:
        try:
            token = await StateToken.get_token(user_ip)
            if token != state_token:
                raise HTTPException(
                    status_code=401, detail="Unauthorized: Invalid state token"
                )
        except Exception as e:
            raise e
