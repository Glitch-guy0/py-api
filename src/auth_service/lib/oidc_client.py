from dataclasses import dataclass
from starlette.responses import RedirectResponse
from httpx import URL, AsyncClient, TimeoutException
from .logger import logger
from shared_lib.exception import ApplicationError


@dataclass
class OIDC_Client[UserDataType]:
    client_id: str
    client_secret: str
    authorize_uri: str
    application_redirect_uri: str
    scope: set[str]
    default_scope: list[str]
    token_uri: str
    userinfo_uri: str
    jwks_uri: str

    def authorization_redirect(
        self, state: str, additional_scope: list[str] = []
    ) -> RedirectResponse:
        logger.debug("Starting authentication redirect process.")
        scope_list = set(self.default_scope + additional_scope)
        for scope in scope_list:
            if scope not in self.scope:
                logger.error(
                    f"Invalid scope '{scope}' provided. Allowed scopes are: {', '.join(self.scope)}"
                )
                raise ValueError(
                    f"Invalid scope '{scope}' provided. Allowed scopes are: {', '.join(self.scope)}"
                )
        scope = " ".join(scope_list)
        logger.info(
            f"Generating authentication redirect URL for scope: {scope} and state: {state}."
        )
        url = URL(self.authorize_uri)
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": scope,
            "redirect_uri": self.application_redirect_uri,
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
            "redirect_uri": self.application_redirect_uri,
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
                json_data = response.json()
                return json_data["access_token"]
        except TimeoutException as e:
            logger.error(f"Timeout error requesting access token: {e}")
            raise ApplicationError("Timeout error requesting access token", 504)
        except KeyError as e:
            logger.error(f"Key error access token not found!: {e}")
            raise ApplicationError("Key error access token not found!", 500)
        except Exception as e:
            logger.error(f"Error requesting access token: {e}")
            raise ApplicationError("Error requesting access token", 500)

    async def request_userdata(self, access_token: str) -> UserDataType:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        logger.info(f"Requesting user data with access token: {access_token}")
        try:
            async with AsyncClient() as client:
                response = await client.get(self.userinfo_uri, headers=headers)
                json_data: UserDataType = response.json()
                logger.debug(f"User data received: {json_data}")
                return json_data
        except TimeoutException as e:
            logger.error(f"Timeout error requesting user data: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error requesting user data: {e}")
            raise e
