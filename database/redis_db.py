from redis import asyncio as aioredis


redis_config = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
}

redis_db_yibu = aioredis.Redis(**redis_config)