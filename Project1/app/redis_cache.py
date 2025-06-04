import aioredis
from app.core.config import settings

redis = None

async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis

async def cache_user(user_id: int, user_data: dict, expire: int = 3600):
    r = await get_redis()
    await r.hset(f"user:{user_id}", mapping=user_data)
    await r.expire(f"user:{user_id}", expire)

async def get_cached_user(user_id: int):
    r = await get_redis()
    user = await r.hgetall(f"user:{user_id}")
    return user if user else None

async def delete_cached_user(user_id: int):
    r = await get_redis()
    await r.delete(f"user:{user_id}")
