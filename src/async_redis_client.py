from redis import asyncio as aioredis

from config import env_config


class AsyncRedisClient:
    def __init__(self, host: str, port: int, db: int, password: str) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = aioredis.Redis(host=host, port=port, db=db, password=password)


async_redis_client = AsyncRedisClient(
    env_config["redis"]["host"],
    env_config["redis"]["port"],
    env_config["redis"]["db"],
    env_config["redis"]["password"],
).client


