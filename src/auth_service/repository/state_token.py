from dataclasses import dataclass
from secrets import token_urlsafe
from auth_service.models.state_token import StateToken
from auth_service.lib.logger import logger
from shared_lib.exception import ApplicationError


@dataclass
class StateTokenRepository:
    @staticmethod
    async def get_state_token(user_ip: str):
        try:
            state_token = token_urlsafe(24)
            logger.debug("Attempting to save state token")
            await StateToken.save_token(user_ip, state_token)
            logger.info("State token successfully saved")
            return state_token
        except Exception as e:
            logger.error(f"Failed to save state token, error: {str(e)}")
            raise e

    @staticmethod
    async def verify_state_token(user_ip: str, state_token: str) -> None:
        try:
            logger.debug("Verifying state token")
            token = await StateToken.get_token(user_ip)
            if token != state_token:
                logger.warning("Unauthorized access attempt with invalid state token")
                raise ApplicationError("Unauthorized: Invalid state token", 401)
            logger.info("State token verified successfully")
        except Exception as e:
            logger.error(f"Error verifying state token, error: {str(e)}")
            raise e
