from dataclasses import dataclass
from auth_service.lib.oidc.interface import AuthenticationState
from auth_service.models.auth_state import AuthState
from auth_service.lib.logger import logger
import time


@dataclass
class Auth_State_Repository:
    @staticmethod
    async def save_auth_state(auth_state: AuthenticationState) -> None:
        start_time = time.monotonic()
        await AuthState.save_state(auth_state)
        if (time.monotonic() - start_time) > 1:  # if operation took more than 1sec
            logger.warning("Auth state save operation took more than 1 second")

    @staticmethod
    async def get_auth_state(session_key: str) -> AuthenticationState:
        start_time = time.monotonic()
        auth_state = await AuthState.get_state(session_key)
        if (time.monotonic() - start_time) > 1:  # if operation took more than 1sec
            logger.warning("Auth state get operation took more than 1 second")
        return auth_state
