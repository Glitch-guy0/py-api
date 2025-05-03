from dataclasses import dataclass
from lib.oidc.interface import AuthenticationState
from models.auth_state import AuthState
from config import ServiceLog as logger
import time

@dataclass
class AuthStateRepository:
    @staticmethod
    async def save_auth_state(auth_state: AuthenticationState) -> None:
        logger.info("Saving authentication state", context={"action": "save_auth_state"})
        start_time = time.monotonic()
        await AuthState.save_state(auth_state)
        duration = time.monotonic() - start_time
        logger.debug(
            "Auth state save completed",
            context={
                "action": "save_auth_state",
                "duration_seconds": duration,
                "session_key_length": len(auth_state.session_key),
                "state_token_length": len(auth_state.state_token)
            }
        )
        if duration > 1:  # if operation took more than 1sec
            logger.warning(
                "Auth state save operation took more than 1 second",
                context={
                    "action": "save_auth_state",
                    "duration_seconds": duration
                }
            )

    @staticmethod
    async def get_auth_state(session_key: str) -> AuthenticationState:
        logger.info("Retrieving authentication state", context={"action": "get_auth_state"})
        start_time = time.monotonic()
        auth_state = await AuthState.get_state(session_key)
        duration = time.monotonic() - start_time
        logger.debug(
            "Auth state retrieval completed",
            context={
                "action": "get_auth_state", 
                "duration_seconds": duration,
                "session_key_length": len(session_key)
            }
        )
        if duration > 1:  # if operation took more than 1sec
            logger.warning(
                "Auth state get operation took more than 1 second",
                context={
                    "action": "get_auth_state",
                    "duration_seconds": duration
                }
            )
        return auth_state
