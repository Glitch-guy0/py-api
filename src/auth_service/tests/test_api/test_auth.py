import pytest
from httpx import AsyncClient, ASGITransport
from auth_service.api.auth import router as auth_route
from auth_service.config import config

from fastapi import FastAPI

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
        assert response.headers["Location"] == config.okta_authorize_redirect_uri
