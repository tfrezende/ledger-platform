from redis.asyncio import Redis
from redis.asyncio.client import Redis as RedisClient  # type alias for annotations


async def create_redis_client(url: str) -> RedisClient:
    return await Redis.from_url(
        url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=20,
    )