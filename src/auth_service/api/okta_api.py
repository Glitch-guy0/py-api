from fastapi import APIRouter, Request, Response, Cookie
from starlette.responses import RedirectResponse
from auth_service.lib.oidc.client.okta import Okta_Client, Auth_Tokens
from shared_lib.exception import ApplicationError

router = APIRouter(
    prefix="/oauth/v2/okta",
    tags=["okta"],
)

okta_client = Okta_Client()


# temporary browser auth handling
class BrowserAuth:
    @staticmethod
    def set_tokens_in_cookie(response: Response, tokens: Auth_Tokens) -> Response:
        response.set_cookie(key="access_token", value=f"Bearer {tokens.access_token}")
        response.set_cookie(key="id_token", value=tokens.id_token)
        return response

    @staticmethod
    def get_tokens_from_cookie(request: Request) -> Auth_Tokens:
        try:
            access_token = request.cookies.get("access_token")
            id_token = request.cookies.get("id_token")
            return Auth_Tokens(access_token=access_token, id_token=id_token)
        except Exception as e:
            raise ApplicationError(f"Failed to get tokens from cookie: {e}", 500)


@router.get("/login")
async def user_login() -> RedirectResponse:
    return await okta_client.authenticaton_redirect()


@router.get("/callback")
async def user_callback(
    code: str, state: str, response: Response, session_key: str = Cookie(...)
):
    tokens: Auth_Tokens = await okta_client.authenticaton_callback_handler(
        code=code, state=state, session_key=session_key
    )
    BrowserAuth.set_tokens_in_cookie(response, tokens)  # temp feature
    return {
        "access_token": tokens.access_token,
        "id_token": tokens.id_token,
    }


@router.get("/authenticate")
async def get_userinfo(request: Request):
    tokens: Auth_Tokens = BrowserAuth.get_tokens_from_cookie(request)  # temp feature
    return await okta_client.get_userclaims(tokens.access_token)


@router.get("/logout")
async def user_logout(request: Request):
    return await okta_client.logout()
