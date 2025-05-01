from fastapi import APIRouter, Request, Response, Cookie
from starlette.responses import RedirectResponse
from auth_service.lib.oidc.client.okta import Okta_Client, Auth_Tokens
from shared_lib.exception import ApplicationError
import datetime
from auth_service import ServiceLog as logger

router = APIRouter(
    prefix="/oauth/v2/okta",
    tags=["okta"],
)

okta_client = Okta_Client()


# temporary browser auth handling
class BrowserAuth:
    @staticmethod
    def set_tokens_in_cookie(response: Response, tokens: Auth_Tokens) -> Response:
        logger.info("Setting auth tokens in cookies", context={"action": "set_cookies"})
        logger.debug(
            "Setting access_token cookie", 
            context={
                "action": "set_access_token",
                "expiry_minutes": 15,
                "token_present": bool(tokens.access_token)
            }
        )
        response.set_cookie(
            key="access_token",
            value=f"Bearer {tokens.access_token}",
            expires=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(minutes=15),
        )
        logger.debug(
            "Setting id_token cookie", 
            context={
                "action": "set_id_token",
                "expiry_minutes": 15,
                "token_present": bool(tokens.id_token)
            }
        )
        response.set_cookie(
            key="id_token",
            value=tokens.id_token,
            expires=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(minutes=15),
        )
        return response

    @staticmethod
    def get_tokens_from_cookie(request: Request) -> Auth_Tokens:
        logger.info("Retrieving auth tokens from cookies", context={"action": "get_cookies"})
        try:
            access_token = request.cookies.get("access_token")
            id_token = request.cookies.get("id_token")
            logger.debug(
                "Retrieved tokens from cookies",
                context={
                    "action": "get_tokens",
                    "access_token_present": bool(access_token),
                    "id_token_present": bool(id_token)
                }
            )
            return Auth_Tokens(access_token=access_token, id_token=id_token)
        except Exception as e:
            logger.critical(
                "Critical security failure - could not retrieve auth tokens",
                context={
                    "action": "get_tokens",
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            raise ApplicationError(
                f"Unauthorized: Failed to get tokens from cookie: {e}", 401
            )

    @staticmethod
    def delete_tokens_from_cookie(response: Response):
        logger.info("Deleting auth tokens from cookies", context={"action": "delete_cookies"})
        logger.debug("Removing access_token cookie", context={"action": "delete_access_token"})
        response.delete_cookie("access_token")
        logger.debug("Removing id_token cookie", context={"action": "delete_id_token"})
        response.delete_cookie("id_token")
        return response


@router.get("/login")
async def user_login() -> RedirectResponse:
    logger.info("Initiating user login - redirecting to Okta", context={"action": "login_redirect"})
    logger.debug(
        "Generating authentication redirect URL",
        context={"action": "generate_auth_url"}
    )
    return await okta_client.authenticaton_redirect()

@router.get("/callback")
async def user_callback(
    code: str, state: str, response: Response, session_key: str = Cookie(...)
):
    logger.info(
        "Processing Okta authentication callback",
        context={"action": "process_callback"}
    )
    logger.debug(
        "Received callback parameters",
        context={
            "action": "callback_received",
            "state_present": bool(state),
            "code_present": bool(code),
            "session_key_present": bool(session_key)
        }
    )
    tokens: Auth_Tokens = await okta_client.authenticaton_callback_handler(
        code=code, state=state, session_key=session_key
    )
    logger.info(
        "Authentication callback successful - setting tokens",
        context={"action": "callback_success"}
    )
    logger.debug(
        "Storing tokens in cookies",
        context={
            "action": "store_tokens",
            "tokens_received": bool(tokens)
        }
    )
    BrowserAuth.set_tokens_in_cookie(response, tokens)  # temp feature
    return {
        "access_token": tokens.access_token,
        "id_token": tokens.id_token,
    }


@router.get("/authenticate")
async def get_userinfo(request: Request):
    logger.info("Getting user info from Okta", context={"action": "get_userinfo"})
    logger.debug(
        "Retrieving tokens from cookies",
        context={"action": "retrieve_tokens"}
    )
    tokens: Auth_Tokens = BrowserAuth.get_tokens_from_cookie(request)  # temp feature
    return await okta_client.get_userclaims(tokens.access_token)


@router.get("/logout")
async def user_logout(request: Request):
    logger.info("Processing user logout request", context={"action": "logout"})
    logger.debug(
        "Retrieving tokens for logout",
        context={"action": "retrieve_tokens_logout"}
    )
    tokens: Auth_Tokens = BrowserAuth.get_tokens_from_cookie(request)  # temp feature
    response = await okta_client.logout(tokens.id_token)
    logger.info("User successfully logged out", context={"action": "logout_success"})
    logger.debug(
        "Removing auth cookies",
        context={"action": "remove_auth_cookies"}
    )
    return BrowserAuth.delete_tokens_from_cookie(response)  # temp feature
