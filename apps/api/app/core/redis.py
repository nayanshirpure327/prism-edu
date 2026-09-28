import aioredis
from app.core.config import settings

redis_client = aioredis.from_url(settings.redis_url, decode_responses=True)

async def get_redis():
    return redis_client

async def cache_get(key: str):
    return await redis_client.get(key)

async def cache_set(key: str, value: str, expire: int = 3600):
    await redis_client.set(key, value, ex=expire)

async def cache_delete(key: str):
    await redis_client.delete(key)

async def check_redis_connection():
    try:
        await redis_client.ping()
        return True
    except Exception:
        return False
