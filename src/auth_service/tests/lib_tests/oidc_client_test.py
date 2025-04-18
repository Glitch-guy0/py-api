from httpx import URL
import pytest
from auth_service.lib.oidc_client import OIDC_Client
from urllib.parse import urlparse, parse_qs

from shared_lib.exception import ApplicationError

data = {
    "client_id": "test_client_id",
    "client_secret": "test_client_secret",
    "authorize_uri": "test_redirect_uri",
    "application_redirect_uri": "test_application_redirect_uri",
    "scope": set(["email", "profile"]),
    "default_scope": ["email"],
    "token_uri": "test_token_uri",
    "userinfo_uri": "test_userinfo_uri",
    "jwks_uri": "test_jwks_uri",
}


def compare_urls(url1: str, url2: str) -> bool:
    # Step 1: Parse both URLs
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)

    # Step 2: Compare scheme, host, path
    if (
        parsed1.scheme != parsed2.scheme
        or parsed1.netloc != parsed2.netloc
        or parsed1.path != parsed2.path
    ):
        return False

    # Step 3: Parse query strings into dicts
    query1 = parse_qs(parsed1.query)
    query2 = parse_qs(parsed2.query)

    # Step 4: Early exit if keys mismatch
    if query1.keys() != query2.keys():
        return False

    # Step 5: Compare values
    for key in query1:
        vals1 = query1[key]
        vals2 = query2[key]
        if key == "scope":
            # Order doesn't matter for scope
            if sorted(vals1[0].split()) != sorted(vals2[0].split()):
                return False
        else:
            # Order *does* matter for other keys
            if vals1 != vals2:
                return False

    return True


@pytest.fixture
def oidc_client():
    client = OIDC_Client(**data)
    return client


def test_authorize_redirect_default_scope(oidc_client):
    state_token = "sample_token"
    expected_params = {
        "client_id": oidc_client.client_id,
        "response_type": "code",
        "scope": " ".join(oidc_client.default_scope),
        "redirect_uri": oidc_client.application_redirect_uri,
        "state": state_token,
    }
    expected_url = URL(oidc_client.authorize_uri)
    expected_url = expected_url.copy_merge_params(expected_params)
    ###
    redirect_url_string = oidc_client.authorization_redirect(state=state_token)
    redirect_url = redirect_url_string.headers["Location"]
    ###
    assert redirect_url is not None
    assert compare_urls(
        str(expected_url), str(redirect_url)
    ), "redirect url is not equal to expected url"


def test_authorize_redirect_custom_scope(oidc_client):
    state_token = "sample_token"
    additional_scope = ["profile"]
    expected_params = {
        "client_id": oidc_client.client_id,
        "response_type": "code",
        "scope": " ".join(oidc_client.default_scope + additional_scope),
        "redirect_uri": oidc_client.application_redirect_uri,
        "state": state_token,
    }
    expected_url = URL(oidc_client.authorize_uri)
    expected_url = expected_url.copy_merge_params(expected_params)
    ###
    redirect_url_string = oidc_client.authorization_redirect(
        state=state_token, additional_scope=additional_scope
    )
    redirect_url = redirect_url_string.headers["Location"]
    ###
    assert redirect_url is not None
    assert compare_urls(
        str(expected_url), str(redirect_url)
    ), "redirect url is not equal to expected url"


def test_authorize_redirect_unknown_scope(oidc_client):
    state_token = "sample_token"
    additional_scope = ["unknown_scope"]
    ###
    with pytest.raises(ValueError):
        oidc_client.authorization_redirect(
            state=state_token, additional_scope=additional_scope
        )


@pytest.mark.asyncio
async def test_request_access_token(oidc_client, mocker):
    code = "test_code"
    expected_json_data = {"access_token": "some token", "id_token": "someother data"}
    ###
    response_data_mock = mocker.Mock()
    response_data_mock.json = mocker.Mock(return_value=expected_json_data)

    async_request_mock = mocker.AsyncMock()
    async_request_mock.post.return_value = response_data_mock

    connection_mock = mocker.AsyncMock()
    connection_mock.__aenter__.return_value = async_request_mock
    connection_mock.__aexit__.return_value = None

    mocker.patch(
        "auth_service.lib.oidc_client.AsyncClient", return_value=connection_mock
    )
    response = await oidc_client.request_access_token(code)
    ###
    async_request_mock.post.assert_called_once_with(
        oidc_client.token_uri,
        data={
            "client_id": oidc_client.client_id,
            "client_secret": oidc_client.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": oidc_client.application_redirect_uri,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    assert (
        response == expected_json_data["access_token"]
    ), "response is not equal to expected json data"


@pytest.mark.asyncio
async def test_request_access_token_invalid_code(oidc_client, mocker):
    code = "invalid_code"
    ###
    with pytest.raises(ApplicationError):
        await oidc_client.request_access_token(code)


@pytest.mark.asyncio
async def test_request_userdata(oidc_client, mocker):
    access_token = "test_token"
    some_user_data = {"some": "data", "other": "data", "another": "data"}
    ###
    return_data_mock = mocker.Mock()
    return_data_mock.json = mocker.Mock(return_value=some_user_data)

    async_request_mock = mocker.AsyncMock()
    async_request_mock.get.return_value = return_data_mock

    connection_mock = mocker.AsyncMock()
    connection_mock.__aenter__.return_value = async_request_mock
    connection_mock.__aexit__.return_value = None

    mocker.patch(
        "auth_service.lib.oidc_client.AsyncClient", return_value=connection_mock
    )

    response = await oidc_client.request_userdata(access_token)
    ###
    async_request_mock.get.assert_called_once_with(
        oidc_client.userinfo_uri,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    assert response == some_user_data
