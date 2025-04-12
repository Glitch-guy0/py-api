import pytest
from auth_service.lib.oidc_client import OIDC_Client
from fastapi import HTTPException

data = {
    "client_id": "test_client_id",
    "client_secret": "test_client_secret",
    "redirect_uri": "test_redirect_uri",
    "authorize_redirect_uri": "test_authorize_redirect_uri",
    "token_uri": "test_token_uri",
    "userinfo_uri": "test_userinfo_uri",
    "jwks_uri": "test_jwks_uri",
    "scope": ["email", "profile"],
}

state_token = "sample_token"


# creating new oidc client


def test_oidc_client_missing_data():
    with pytest.raises((TypeError, ValueError)):
        testdata = data.copy()
        testdata.pop("client_id")
        OIDC_Client(**testdata)


def test_oidc_client_with_extra_params():
    data["extra_param"] = "extra_param"
    with pytest.raises((TypeError, ValueError)):
        OIDC_Client(**data)


def test_oidc_client_with_correct_data():
    client = OIDC_Client(**data)
    assert client.__dict__ == data


@pytest.fixture
def oidc_client():
    client = OIDC_Client(**data)
    return client


def test_oidc_client_authorize_redirect(oidc_client):
    redirct_url_string = oidc_client.authorize_redirect(scope="email")
    assert redirct_url_string is not None
    assert "client_id" in redirct_url_string
    assert "redirect_uri" in redirct_url_string
    assert "response_type" in redirct_url_string
    assert "scope" in redirct_url_string
    assert "state" in redirct_url_string


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
