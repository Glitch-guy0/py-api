from httpx import URL
import pytest
from auth_service.lib.oidc_client import OIDC_Client

data = {
    "client_id": "test_client_id",
    "client_secret": "test_client_secret",
    "authorize_uri": "test_redirect_uri",
    "authorize_redirect_uri": "test_authorize_redirect_uri",
    "scope": set(["email", "profile"]),
    "token_uri": "test_token_uri",
    "userinfo_uri": "test_userinfo_uri",
    "jwks_uri": "test_jwks_uri",
}

state_token = "sample_token"


@pytest.fixture
def oidc_client():
    client = OIDC_Client(**data)
    return client


def test_authorize_redirect(oidc_client):
    redirect_url_string = oidc_client.authorization_redirect(
        scope="email", state=state_token
    )
    redirect_url = redirect_url_string.headers["Location"]
    # todo(improvement): replace with url builder
    assert redirect_url is not None
    assert "client_id" in redirect_url
    assert "redirect_uri" in redirect_url
    assert "response_type" in redirect_url
    assert "scope" in redirect_url
    assert "state" in redirect_url


def test_request_access_token(oidc_client, mocker):
    code = "test_code"
    expected_json_data = {"access_token": "some token", "id_token": "someother data"}
    ###
    # data mock
    response_data_mock = mocker.Mock()  # think of it as response class
    response_data_mock.json = expected_json_data  # it contains .json value (dataclass)

    # (function mock)  .post is an async function so
    async_request_mock = mocker.AsyncMock()
    async_request_mock.post.return_value = response_data_mock  # when you call `client.get()` it will return the response data

    # (mock implemented)
    mocker.patch(
        "auth_service.lib.oidc_client.AsyncClient", return_value=async_request_mock
    )  # module is replace with mock
    response = oidc_client.request_access_token(code)
    # todo: test for request exception and unauthorized exception
    ###
    async_request_mock.post.assert_called_once_with(
        oidc_client.token_uri,
        data={"code": code, "grant_type": "authorization_code"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response == expected_json_data


def test_request_userdata(oidc_client, mocker):
    access_token = "test_token"
    some_user_data = {"some": "data", "other": "data", "another": "data"}
    ###
    return_data_mock = mocker.Mock()
    return_data_mock.json.return_value = (
        some_user_data  # because you get this data as `response.json()` so
    )

    async_request_mock = mocker.AsyncMock()
    async_request_mock.get.return_value = return_data_mock

    mocker.patch(
        "auth_service.lib.oidc_client.AsyncClient", return_value=async_request_mock
    )

    response = oidc_client.request_userdata(access_token)
    ###
    async_request_mock.get.assert_called_once_with(
        oidc_client.userinfo_uri,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response == some_user_data
