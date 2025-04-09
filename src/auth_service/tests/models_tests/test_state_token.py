import pytest
from auth_service.repository.state_token import StateTokenRepository


@pytest.mark.asyncio
async def test_get_state_token(mocker):
    user_ip = "127.0.0.1"
    ###
    db_call = mocker.patch(
        "auth_service.models.state_token.StateToken.get_state_token", return_value=None
    )
    token = await StateTokenRepository(user_ip).get_state_token()
    ###
    assert token is not None
    assert len(token) == 32
    db_call.assert_called_once_with(user_ip, token)
