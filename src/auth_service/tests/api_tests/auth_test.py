import pytest
from httpx import AsyncClient, ASGITransport
from auth_service.api.auth import router as auth_route
from fastapi import FastAPI


config = {
    "okta_application_redirect_uri": "http://test/oauth/v2/callback",
}

app = FastAPI()
app.include_router(auth_route)


@pytest.mark.asyncio
async def test_startup_route():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/test")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_route():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/login")
        assert response.status_code == 302
        url = config.get("okta_application_redirect_uri")
        assert url is not None
        assert url in response.headers["Location"]
        assert "state=" in response.headers["Location"]
        assert "client_id=" in response.headers["Location"]
        assert "response_type=" in response.headers["Location"]
        assert "scope=" in response.headers["Location"]
        assert "redirect_uri=" in response.headers["Location"]


@pytest.mark.asyncio
async def test_auth_callback_route():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(
            "/oauth/v2/callback", params={"code": "test_code", "state": "something"}
        )
        assert response.status_code == 200
