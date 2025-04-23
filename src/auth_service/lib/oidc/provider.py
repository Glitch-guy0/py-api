from fastapi.responses import RedirectResponse
from auth_service.lib.oidc.interface import OIDC_Client, Auth_Tokens


class OIDC_Provider:
    oidc_client: OIDC_Client

    def __init__(self, oidc_client: OIDC_Client):
        self.oidc_client = oidc_client

    async def authentication_redirect(self) -> RedirectResponse:
        return await self.oidc_client.authentication_redirect()

    async def authentication_callback_handler(
        self, code: str, state: str
    ) -> Auth_Tokens:
        return await self.oidc_client.authentication_callback_handler(code, state)

    async def get_userclaims(self, access_token: str) -> dict:
        return await self.oidc_client.get_userclaims(access_token)

    async def logout(self) -> RedirectResponse:
        return await self.oidc_client.logout()
