from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import aioredis
import os
from jose import JWTError, jwt
from app.models import User  # твоя модель користувача
from app.core.config import settings

# Підключення OAuth2 для отримання токена з заголовку Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Підключення до бази даних (асинхронний движок)
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Функція для отримання сесії БД
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Підключення до Redis
redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)

async def get_redis():
    yield redis

# Функція для отримання поточного користувача за JWT токеном
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if not user:
        raise credentials_exception
    return user
