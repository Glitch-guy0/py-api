from auth_service.lib.oidc.interface import Auth_Tokens
from auth_service.lib.oidc.interface import OIDC_Client
from fastapi.responses import RedirectResponse
from auth_service.repository.state_token import StateTokenRepository
from httpx import URL, AsyncClient, HTTPStatusError
from auth_service.config import Config
from shared_lib.exception import ApplicationError


class Okta_Client(OIDC_Client):
    def __init__(self):
        super().__init__(
            client_id = Config.okta_client_id,
            client_secret = Config.okta_client_secret,
            authorize_uri = Config.okta_authorize_uri,
            application_redirect_uri = Config.okta_application_redirect_uri,
            scope = Config.okta_scope,
            token_uri = Config.okta_token_uri,
            userinfo_uri = Config.okta_userinfo_uri,
            jwks_uri = Config.okta_jwks_uri,
            logout_uri = Config.okta_logout_uri
        )

    async def authenticaton_redirect(self, user_ip: str) -> RedirectResponse:

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.application_redirect_uri,
            "response_type": "code",
            "scope": self.scope,
            "state": await StateTokenRepository.get_state_token(user_ip),
        }

        redirect_url = URL(self.authorize_uri)
        return RedirectResponse(url=redirect_url.copy_merge_params(params))

    async def authenticaton_callback_handler(
        self, code: str, state: str, user_ip: str
    ) -> Auth_Tokens:
        await StateTokenRepository.verify_state_token(user_ip, state)

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.application_redirect_uri,
        }

        async with AsyncClient() as client:
            response = await client.post(self.token_uri, data=params)
            try:
                response.raise_for_status()
            except HTTPStatusError as e:
                raise ApplicationError(f"Failed to exchange code for tokens {response.text}", 500)
            
            tokens = Auth_Tokens(**response.json())
            return tokens

    async def logout(self) -> RedirectResponse:
        return RedirectResponse(url=self.logout_uri)

    async def get_userclaims(self, access_token: str) -> dict:
        async with AsyncClient() as client:
            response = await client.get(self.userinfo_uri, headers={"Authorization": f"Bearer {access_token}"})
            try:
                response.raise_for_status()
            except HTTPStatusError as e:
                raise ApplicationError(f"Unauthorized to access userinfo", 401)
            return response.json()
