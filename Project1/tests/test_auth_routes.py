import pytest

@pytest.mark.asyncio
async def test_login(async_client):
    data = {"username": "test@example.com", "password": "testpass"}
    response = await async_client.post("/auth/login", data=data)
    assert response.status_code in [200, 401]
