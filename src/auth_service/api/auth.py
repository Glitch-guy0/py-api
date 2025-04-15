from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from auth_service.lib.oidc_client import OIDC_Client
from auth_service.config import config
from auth_service.repository.state_token import StateTokenRepository
from shared_lib.exception import ApplicationError

router = APIRouter()

okta_client: OIDC_Client = OIDC_Client(
    client_id=config.okta_client_id,
    client_secret=config.okta_client_secret,
    authorize_uri=config.okta_authorize_uri,
    application_redirect_uri=config.okta_application_redirect_uri,
    scope=set(
        ["openid", "email", "profile", "address", "phone", "offline_access", "groups"]
    ),
    default_scope=["openid", "email", "profile"],
    token_uri=config.okta_token_uri,
    userinfo_uri=config.okta_userinfo_uri,
    jwks_uri=config.okta_jwks_uri,
)


@router.get("/oauth/v2/login")
async def user_login(request: Request, scope: str = None) -> RedirectResponse:
    if not request.client:
        raise ApplicationError("Client not found", 400)
    state_token = await StateTokenRepository.get_state_token(request.client.host)
    return okta_client.authorization_redirect(
        state_token, scope.split(" ") if scope else []
    )


@router.get("/oauth/v2/callback")
async def user_callback(request: Request, code: str, state: str):
    if not request.client:
        raise ApplicationError("Client not found", 400)
    await StateTokenRepository.verify_state_token(request.client.host, state)
    access_token = await okta_client.request_access_token(code)
    user_data = await okta_client.request_userdata(access_token)
    return user_data
