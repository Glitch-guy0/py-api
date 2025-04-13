from dataclasses import dataclass
from starlette.responses import RedirectResponse
from httpx import URL
from .logger import logger


@dataclass
class OIDC_Client:
    client_id: str
    client_secret: str
    authorize_uri: str
    authorize_redirect_uri: str
    scope: set[str]
    token_uri: str
    userinfo_uri: str
    jwks_uri: str

    def authentication_redirect(self, scope: str, state: str) -> RedirectResponse:
        logger.debug("Starting authentication redirect process.")
        
        if scope not in self.scope:
            logger.error(f"Invalid scope '{scope}' provided. Allowed scopes are: {', '.join(self.scope)}")
            raise ValueError(
                f"Invalid scope '{scope}' provided. Allowed scopes are: {', '.join(self.scope)}"
            )

        logger.info(f"Generating authentication redirect URL for scope: {scope} and state: {state}.")
        url = URL(self.authorize_uri)
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": scope,
            "redirect_uri": self.authorize_redirect_uri,
            "state": state,
        }
        url = url.copy_merge_params(params)
        logger.debug(f"Redirect URL generated: {url}")
        return RedirectResponse(url=str(url))
