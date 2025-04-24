from beanie import Document, Indexed
from beanie.exceptions import DocumentAlreadyCreated
from typing import Annotated
import datetime
from shared_lib.exception import ApplicationError
from auth_service.lib.oidc.interface import AuthenticationState


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

        return AuthenticationState(**state_data)
