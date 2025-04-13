from httpx import URL
import pytest
from auth_service.lib.oidc_client import OIDC_Client
from fastapi import HTTPException

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
    assert redirect_url is not None
    assert "client_id" in redirect_url
    assert "redirect_uri" in redirect_url
    assert "response_type" in redirect_url
    assert "scope" in redirect_url
    assert "state" in redirect_url


def test_verify_request(oidc_client, mocker):
    user_ip = "127.0.0.1"
    expired_state_token = "random_token"
    verify_call = mocker.patch(
        "auth_service.repository.state_token.StateTokenRepository.verify_state_token",
        return_value=True,
    )
    oidc_client.verify_request(user_ip, expired_state_token)

    verify_call.assert_called_once_with(user_ip, expired_state_token)


def test_verify_request_expired_state(oidc_client, mocker):
    user_ip = "127.0.0.1"
    expired_state_token = "random_token"
    mocker.patch(
        "auth_service.repository.state_token.StateTokenRepository.verify_state_token",
        return_value=False,
    )
    with pytest.raises(HTTPException):
        oidc_client.verify_request(user_ip, expired_state_token)


def test_request_access_token[T](oidc_client, mocker):
    code = "test_code"
    request_mock = mocker.patch(
        "auth_service.lib.odic_client.requests.post", return_value=T
    )
    oidc_client.request_access_token(code)
    request_mock.assert_called_once_with(
        oidc_client.token_uri,
        data={"code": code, "grant_type": "authorization_code"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def test_request_userdata[T](oidc_client, mocker):
    access_token = "test_token"
    request_mock = mocker.patch(
        "auth_service.lib.odic_client.requests.post", return_value=T
    )
    oidc_client.request_userdata(access_token)
    request_mock.assert_called_once_with(
        oidc_client.userinfo_uri,
        headers={"Authorization": f"Bearer {access_token}"},
    )
