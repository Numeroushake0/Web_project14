import pytest

@pytest.mark.asyncio
async def test_register_user(async_client):
    user_data = {
        "email": "newuser@example.com",
        "password": "newpass123"
    }
    response = await async_client.post("/auth/register", json=user_data)
    assert response.status_code == 200 or response.status_code == 409
