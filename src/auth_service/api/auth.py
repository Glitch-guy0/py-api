from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse
from auth_service.lib.oidc_client import OIDC_Client
from auth_service.config import config
from auth_service.repository.state_token import StateTokenRepository

router = APIRouter()

okta_client: OIDC_Client = OIDC_Client(
    client_id=config.okta_client_id,
    client_secret=config.okta_client_secret,
    authorize_uri=config.okta_authorize_uri,
    application_redirect_uri=config.okta_application_redirect_uri,
    scope=set(["openid email"]),
    token_uri=config.okta_token_uri,
    userinfo_uri=config.okta_userinfo_uri,
    jwks_uri=config.okta_jwks_uri,
)


@router.get("/login")
async def user_login(request: Request) -> RedirectResponse:
    if not request.client:
        raise HTTPException(status_code=400, detail="Client not found")
    state_token = await StateTokenRepository.get_state_token(request.client.host)
    return okta_client.authorization_redirect("openid email", state_token)


@router.get("/callback")
async def user_callback(
    request: Request, code: str, state: str
):
    if not request.client:
        raise HTTPException(status_code=400, detail="Client not found")
    # await StateTokenRepository.verify_state_token(request.client.host, state)
    access_token = await okta_client.request_access_token(code)
    user_data = await okta_client.request_userdata(access_token)
    return user_data
