import pytest
from auth_service.lib.oidc_client import OIDC_Client

data = {
    "client_id": "test_client_id",
    "client_secret": "test_client_secret",
    "redirect_uri": "test_redirect_uri",
    "authorize_redirect_uri": "test_authorize_redirect_uri",
    "token_uri": "test_token_uri",
    "userinfo_uri": "test_userinfo_uri",
    "jwks_uri": "test_jwks_uri",
}

state_token = "sample_token"

# test for oidc_client creation


# missing data -1
def test_oidc_client_missing_data():
    with pytest.raises((TypeError, ValueError)):
        testdata = data.copy()
        testdata.pop("client_id")
        OIDC_Client(**testdata)


# incorrect data +1 overparams make the object creation strict
def test_oidc_client_with_extra_params():
    with pytest.raises((TypeError, ValueError)):
        OIDC_Client(**data, extra_param="extra_param")


# correct data
def test_oidc_client_with_correct_data():
    client = OIDC_Client(**data)
    assert client.__dict__ == data


@pytest.fixture
def oidc_client():
    client = OIDC_Client(**data)
    return client


def test_oidc_client_authorize_redirect(oidc_client):
    redirct_url_string = oidc_client.authorize_redirect()
    assert redirct_url_string is not None
    assert "client_id" in redirct_url_string
    assert "redirect_uri" in redirct_url_string
    assert "response_type" in redirct_url_string
    assert "scope" in redirct_url_string
    assert "state" in redirct_url_string
