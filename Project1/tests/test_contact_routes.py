import pytest

@pytest.mark.asyncio
async def test_create_contact(async_client):
    contact_data = {
        "name": "Test",
        "email": "test@user.com",
        "phone": "1234567890"
    }
    response = await async_client.post("/contacts/", json=contact_data)
    assert response.status_code in [200, 401]
