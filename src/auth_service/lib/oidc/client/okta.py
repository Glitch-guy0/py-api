import datetime
from auth_service.lib import session_key_generator, state_token_generator
from auth_service.lib.oidc.interface import Auth_Tokens
from auth_service.lib.oidc.interface import OIDC_Client
from fastapi.responses import RedirectResponse
from httpx import URL, AsyncClient, HTTPStatusError
from auth_service.config import Config
from shared_lib.exception import ApplicationError
from auth_service.repository.auth_state import AuthStateRepository, AuthenticationState
from auth_service.lib.oidc.interface import Auth_Tokens
from auth_service import ServiceLog


class Okta_Client(OIDC_Client):
    def __init__(self):
        super().__init__(
            client_id=Config.okta_client_id,
            client_secret=Config.okta_client_secret,
            authorize_uri=Config.okta_authorize_uri,
            application_redirect_uri=Config.okta_application_redirect_uri,
            scope=Config.okta_scope,
            token_uri=Config.okta_token_uri,
            userinfo_uri=Config.okta_userinfo_uri,
            jwks_uri=Config.okta_jwks_uri,
            logout_uri=Config.okta_logout_uri,
        )
        ServiceLog.debug("Okta client initialized")

    async def authenticaton_redirect(self) -> RedirectResponse:
        state_token = state_token_generator()
        session_key = session_key_generator()
        redirect_uri = self.application_redirect_uri

        ServiceLog.debug(
            "Generated auth parameters",
            context={
                "session_key": session_key,
                "state_token": state_token,
                "redirect_uri": redirect_uri,
            },
        )

        auth_state = AuthenticationState(
            session_key=session_key,
            state_token=state_token,
            redirect_uri=redirect_uri,
        )
        await AuthStateRepository.save_auth_state(auth_state)
        ServiceLog.info(
            "Authentication redirect initiated",
            context={
                "session_key": session_key,
                "state_token": state_token,
                "redirect_uri": redirect_uri,
            },
        )

        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": self.scope,
            "state": state_token,
        }

        redirect_url = URL(self.authorize_uri)
        redirect_uri = redirect_url.copy_merge_params(params)
        ServiceLog.debug(
            "Redirect URL generated",
            context={
                "redirect_url": str(redirect_uri),
                "session_key": session_key,
                "state_token": state_token,
                "redirect_uri": redirect_uri,
            },
        )
        response = RedirectResponse(
            url=str(redirect_uri),
            status_code=302,
        )
        response.set_cookie(
            key="session_key",
            value=session_key,
            expires=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(minutes=5),
        )
        return response

    async def authenticaton_callback_handler(
        self, code: str, state: str, session_key: str
    ) -> Auth_Tokens:
        ServiceLog.debug(
            "Processing authentication callback",
            context={
                "session_key": session_key,
                "state": state,
            },
        )

        auth_state: AuthenticationState = await AuthStateRepository.get_auth_state(
            session_key
        )
        if auth_state.state_token != state:
            ServiceLog.warning(
                "Invalid state token received",
                context={
                    "session_key": session_key,
                    "received_state": state,
                    "expected_state": auth_state.state_token,
                },
            )
            raise ApplicationError("Invalid state token", 400)

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": auth_state.redirect_uri,
        }

        ServiceLog.debug(
            "Attempting to exchange code for tokens",
            context={
                "session_key": session_key,
                "token_uri": self.token_uri,
            },
        )

        async with AsyncClient() as client:
            response = await client.post(self.token_uri, data=params)
            try:
                response.raise_for_status()
            except HTTPStatusError:
                ServiceLog.error(
                    "Failed to exchange code for tokens",
                    context={
                        "session_key": session_key,
                        "error_response": response.text,
                    },
                )
                raise ApplicationError(
                    f"Failed to exchange code for tokens {response.text}", 500
                )

            tokens = Auth_Tokens(**response.json())
            ServiceLog.info(
                "Successfully obtained auth tokens",
                context={"session_key": session_key},
            )
            return tokens

    async def logout(self) -> RedirectResponse:
        ServiceLog.debug("Logout initiated")
        ServiceLog.info("Logout initiated")
        return RedirectResponse(url=self.logout_uri)

    async def get_userclaims(self, access_token: str) -> dict:
        ServiceLog.debug("Fetching user claims")
        async with AsyncClient() as client:
            response = await client.get(
                self.userinfo_uri, headers={"Authorization": f"Bearer {access_token}"}
            )
            try:
                response.raise_for_status()
            except HTTPStatusError as e:
                ServiceLog.error(
                    "Failed to get user claims",
                    context={"error": str(e)},
                )
                raise ApplicationError(f"Unauthorized to access userinfo", 401)
            ServiceLog.info("Successfully retrieved user claims")
            return response.json()
