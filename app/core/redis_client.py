import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)


async def get_redis_client():
    return redis_client


async def delete_cache_pattern(pattern: str, cache: redis.Redis):
    keys_to_delete = []

    async for key in cache.scan_iter(pattern):
        keys_to_delete.append(key)

    if keys_to_delete:
        await cache.delete(*keys_to_delete)
        print(f"Cache limpiada: {len(keys_to_delete)} llaves borradas con el patrón '{pattern}'")