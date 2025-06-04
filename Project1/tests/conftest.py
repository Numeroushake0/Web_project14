import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.database import get_db  # Якщо у тебе є окрема сесія БД

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
