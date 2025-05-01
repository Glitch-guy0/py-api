import secrets
from auth_service import ServiceLog as logger


def state_token_generator() -> str:
    token = secrets.token_urlsafe(24)
    logger.debug(
        "State token generated",
        context={
            "action": "generate_state_token",
            "token_length": len(token)
        }
    )
    return token


def session_key_generator() -> str:
    key = secrets.token_urlsafe(24)
    logger.debug(
        "Session key generated", 
        context={
            "action": "generate_session_key",
            "key_length": len(key)
        }
    )
    return key
