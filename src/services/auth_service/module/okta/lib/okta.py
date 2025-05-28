import datetime
from lib import session_key_generator, state_token_generator
from lib.oidc.interface import Auth_Tokens
from lib.oidc.interface import OIDC_Client
from fastapi.responses import RedirectResponse
from httpx import URL, AsyncClient, HTTPStatusError
from config import Config
from shared_lib.exception import ApplicationError
from repository.auth_state import AuthStateRepository, AuthenticationState
from lib.oidc.interface import Auth_Tokens
from config import ServiceLog as logger

class Okta_Client(OIDC_Client):
    def __init__(self):
        logger.debug("Initializing Okta client", context={"action": "init_okta_client"})
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

    async def authenticaton_redirect(self) -> RedirectResponse:
        logger.info("Generating authentication redirect", context={"action": "auth_redirect"})
        state_token = state_token_generator()
        session_key = session_key_generator()
        redirect_uri = self.application_redirect_uri

        auth_state = AuthenticationState(
            session_key=session_key,
            state_token=state_token,
            redirect_uri=redirect_uri,
        )
        await AuthStateRepository.save_auth_state(auth_state)
        logger.debug(
            "Created and saved authentication state",
            context={
                "action": "save_auth_state",
                "session_key_length": len(session_key),
                "state_token_length": len(state_token)
            }
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
        logger.debug(
            "Set session cookie",
            context={
                "action": "set_session_cookie",
                "expiry_minutes": 5
            }
        )
        return response

    async def authenticaton_callback_handler(
        self, code: str, state: str, session_key: str
    ) -> Auth_Tokens:
        logger.info("Processing authentication callback", context={"action": "auth_callback"})
        auth_state: AuthenticationState = await AuthStateRepository.get_auth_state(
            session_key
        )
        logger.debug(
            "Retrieved authentication state",
            context={
                "action": "get_auth_state",
                "state_token_match": auth_state.state_token == state
            }
        )

        if auth_state.state_token != state:
            logger.error(
                "State token mismatch",
                context={
                    "action": "validate_state",
                    "expected": auth_state.state_token,
                    "received": state
                }
            )
            raise ApplicationError("Invalid state token", 400)

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": auth_state.redirect_uri,
        }

        async with AsyncClient() as client:
            logger.debug("Exchanging code for tokens", context={"action": "token_exchange"})
            response = await client.post(self.token_uri, data=params)
            try:
                response.raise_for_status()
            except HTTPStatusError:
                logger.error(
                    "Token exchange failed",
                    context={
                        "action": "token_exchange",
                        "status_code": response.status_code,
                        "response": response.text
                    }
                )
                raise ApplicationError(
                    f"Failed to exchange code for tokens {response.text}", 500
                )

            tokens = Auth_Tokens(**response.json())
            logger.debug(
                "Successfully exchanged code for tokens",
                context={
                    "action": "token_exchange",
                    "access_token_present": bool(tokens.access_token),
                    "id_token_present": bool(tokens.id_token),
                    "refresh_token_present": bool(tokens.refresh_token)
                }
            )
            return tokens

    async def logout(self, id_token: str) -> RedirectResponse:
        logger.info("Processing logout request", context={"action": "logout"})
        redirect_uri = URL(self.logout_uri)
        redirect_uri = redirect_uri.copy_merge_params(
            {
                "id_token_hint": id_token,
                "post_logout_redirect_uri": Config.post_logout_redirect_uri,
            }
        )
        logger.debug(
            "Generated logout redirect URL",
            context={
                "action": "logout_redirect",
                "redirect_uri": str(redirect_uri)
            }
        )
        return RedirectResponse(url=str(redirect_uri), status_code=302)

    async def get_userclaims(self, access_token: str) -> dict:
        logger.info("Retrieving user claims", context={"action": "get_userclaims"})
        async with AsyncClient() as client:
            response = await client.get(
                self.userinfo_uri, headers={"Authorization": access_token}
            )
            try:
                response.raise_for_status()
            except HTTPStatusError as e:
                logger.error(
                    "Failed to retrieve user claims",
                    context={
                        "action": "get_userclaims",
                        "status_code": response.status_code,
                        "error": str(e)
                    }
                )
                raise ApplicationError(f"Unauthorized to access userinfo", 401)
            
            logger.debug("Successfully retrieved user claims", context={"action": "get_userclaims"})
            return response.json()
