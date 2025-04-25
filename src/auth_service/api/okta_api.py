from fastapi import APIRouter, Request, Response
from starlette.responses import RedirectResponse
from auth_service.lib.oidc.client.okta import Okta_Client, Auth_Tokens

router = APIRouter(
    prefix="/oauth/v2/okta",
    tags=["okta"],
)

okta_client = Okta_Client()


@router.get("/login")
async def user_login() -> RedirectResponse:
    return await okta_client.authenticaton_redirect()


@router.get("/callback/{session_key}")
async def user_callback(session_key: str, code: str, state: str, response: Response):
    tokens: Auth_Tokens = await okta_client.authenticaton_callback_handler(
        code=code, state=state, session_key=session_key
    )
    response.headers["Authorization"] = f"Bearer {tokens.access_token}"
    if tokens.id_token:
        response.headers["id_token"] = tokens.id_token
    return response


@router.get("/logout")
async def user_logout(request: Request):
    return await okta_client.logout()
