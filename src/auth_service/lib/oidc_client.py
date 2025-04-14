from dataclasses import dataclass
from starlette.responses import RedirectResponse
from httpx import URL, AsyncClient, TimeoutException
from .logger import logger


@dataclass
class OIDC_Client[UserDataType]:
    client_id: str
    client_secret: str
    authorize_uri: str
    authorize_redirect_uri: str
    scope: set[str]
    token_uri: str
    userinfo_uri: str
    jwks_uri: str

    def authorization_redirect(self, scope: str, state: str) -> RedirectResponse:
        logger.debug("Starting authentication redirect process.")

        if scope not in self.scope:
            logger.error(
                f"Invalid scope '{scope}' provided. Allowed scopes are: {', '.join(self.scope)}"
            )
            raise ValueError(
                f"Invalid scope '{scope}' provided. Allowed scopes are: {', '.join(self.scope)}"
            )

        logger.info(
            f"Generating authentication redirect URL for scope: {scope} and state: {state}."
        )
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

    async def request_access_token(self, code: str) -> str:
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        try:
            async with AsyncClient() as client:
                response = await client.post(
                    self.token_uri, data=params, headers=headers
                )
                json_data = await response.json()
                return json_data["access_token"]
        except TimeoutException as e:
            logger.error(f"Timeout error requesting access token: {e}")
            # todo: add http exception
            raise e
        except KeyError as e:
            logger.error(f"Key error requesting access token: {e}")
            # todo: add http exception
            raise e
        except Exception as e:
            logger.error(f"Error requesting access token: {e}")
            # todo: add http exception
            raise e

    async def request_userdata(self, access_token: str) -> UserDataType:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        logger.info(f"Requesting user data with access token: {access_token}")
        try:
            async with AsyncClient() as client:
                response = await client.get(self.userinfo_uri, headers=headers)
                json_data: UserDataType = await response.json()
                logger.debug(f"User data received: {json_data}")
                return json_data
        except TimeoutException as e:
            logger.error(f"Timeout error requesting user data: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error requesting user data: {e}")
            raise e
