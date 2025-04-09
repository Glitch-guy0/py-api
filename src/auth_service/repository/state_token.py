from dataclasses import dataclass
from secrets import token_urlsafe
from auth_service.models.state_token import StateToken


@dataclass
class StateTokenRepository:
    def __init__(self, user_ip: str):
        self.user_ip = user_ip
        self.token = token_urlsafe(24)

    async def get_state_token(self):
        try:
            await StateToken.get_state_token(self.user_ip, self.token)
            return self.token
        except Exception as e:
            raise e
