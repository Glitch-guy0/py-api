from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


class Auth_Tokens(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None

    class Config:
        extra = "ignore"


@dataclass
class AuthenticationState:
    session_key: str
    state_token: str
    redirect_uri: str


@dataclass
class OIDC_Client(ABC):
    client_id: str
    client_secret: str
    authorize_uri: str
    application_redirect_uri: str
    scope: str
    token_uri: str
    userinfo_uri: str
    jwks_uri: str
    logout_uri: str

    @abstractmethod
    async def authenticaton_redirect(self) -> RedirectResponse:
        """Redirect to the OIDC provider for authentication"""
        pass

    @abstractmethod
    async def authenticaton_callback_handler(
        self, code: str, state: str, session_key: str
    ) -> Auth_Tokens:
        """Handle OIDC callback and return auth tokens"""
        pass

    @abstractmethod
    async def get_userclaims(self, access_token: str) -> dict:
        """Get user claims from the OIDC provider"""
        pass

    @abstractmethod
    async def logout(self) -> RedirectResponse:
        """Redirects to the OIDC provider's logout page"""
        pass
