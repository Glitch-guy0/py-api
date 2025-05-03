from beanie import Document, Indexed
from beanie.exceptions import DocumentAlreadyCreated
from typing import Annotated
import datetime
from shared_lib.exception import ApplicationError
from lib.oidc.interface import AuthenticationState
from config import ServiceLog as logger

class AuthState(Document):
    session_key: Annotated[str, Indexed(unique=True)]
    state_token: str
    redirect_uri: str
    created_at: Annotated[datetime.datetime, Indexed(expireAfterSeconds=15)]

    @classmethod
    async def save_state(cls, auth_state: AuthenticationState) -> None:
        cls_object = cls(
            session_key=auth_state.session_key,
            state_token=auth_state.state_token,
            redirect_uri=auth_state.redirect_uri,
            created_at=datetime.datetime.now().timestamp(),
        )
        try:
            await cls_object.save()
            logger.debug(
                "Authentication state saved successfully",
                context={
                    "action": "save_auth_state",
                    "session_key_length": len(auth_state.session_key),
                    "state_token_length": len(auth_state.state_token)
                }
            )
        except Exception as e:
            if isinstance(e, DocumentAlreadyCreated):
                raise ApplicationError(
                    "Something went wrong, please try again later", status_code=500
                )
            raise e

    @staticmethod
    async def get_state(session_key: str) -> AuthenticationState:
        state_data = await AuthState.find_one(AuthState.session_key == session_key)
        if not state_data:
            raise ApplicationError("Unauthorized: Session not found", status_code=401)

        logger.debug(
            "Authentication state retrieved successfully",
            context={
                "action": "get_auth_state",
                "session_key_length": len(session_key),
                "state_token_length": len(state_data.state_token)
            }
        )
        return AuthenticationState(
            session_key=state_data.session_key,
            state_token=state_data.state_token,
            redirect_uri=state_data.redirect_uri,
        )
