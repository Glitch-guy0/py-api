import pytest
from auth_service.models.state_token import StateToken
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_get_state_token(mocker):
    user_ip = "127.0.0.1"
    ###
    state_token_instance = mocker.Mock()
    state_token_instance.save = AsyncMock(return_value=True)
    mocker.patch(
        "auth_service.models.state_token.StateToken", return_value=state_token_instance
    )
    token = await StateToken.get_state_token(user_ip)
    ###
    assert token is not None
    assert len(token) == 32
    assert state_token_instance.save.call_count == 1
    assert state_token_instance.save.call_args[0][0].user_ip == user_ip
