import pytest
from auth_service.repository.state_token import StateTokenRepository
from shared_lib.exception import ApplicationError


@pytest.mark.asyncio
async def test_get_state_token(mocker):
    user_ip = "127.0.0.1"
    ###
    # todo: this should be async mock
    db_call = mocker.patch(
        "auth_service.models.state_token.StateToken.save_token", return_value=None
    )
    token = await StateTokenRepository.get_state_token(user_ip)
    ###
    assert token is not None
    assert len(token) == 32
    db_call.assert_called_once_with(user_ip=user_ip, token=token)


@pytest.mark.asyncio
async def test_verify_request(mocker):
    user_ip = "127.0.0.1"
    state_token = "random_token"
    ###
    db_call = mocker.patch(
        "auth_service.models.state_token.StateToken.get_token", return_value=state_token
    )
    await StateTokenRepository.verify_state_token(user_ip, state_token)
    ###
    db_call.assert_called_once_with(user_ip)


@pytest.mark.asyncio
async def test_verify_request_expired_state(mocker):
    user_ip = "127.0.0.1"
    ###
    db_call = mocker.patch(
        "auth_service.models.state_token.StateToken.get_token", return_value="a"
    )
    with pytest.raises(ApplicationError):
        await StateTokenRepository.verify_state_token(user_ip, "b")
    ###
    db_call.assert_called_once_with(user_ip)
