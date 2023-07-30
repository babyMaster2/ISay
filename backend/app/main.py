import random
from fastapi import FastAPI
from database.redis_db import redis_db_yibu
from pydantic import BaseModel

app = FastAPI()


class PoetryItem(BaseModel):
    text: str
    source: str = None
    annotation: str = None


async def get_random_name():
    filename = 'name.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        names = f.readlines()
        name = random.choice(names)
        return name.strip()


@app.post('/poetry/add')
async def add_poetry(poetry_item: PoetryItem):
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        name = await get_random_name()
        if not redis_db_yibu.exists(name):
            redis_db_yibu.rpush(name, poetry_item.model_dump_json())
            return {'message': 'add successfully'}
        attempts += 1
    return {'message': 'failed to add'}  # 达到最大尝试次数后返回失败信息


@app.get('/poetry/random/get')
async def get_random_poetry():
    pipeline = redis_db_yibu.pipeline()
    size = pipeline.dbsize()
    if size == 0:
        return {'message': 'db is null'}
    name = pipeline.randomkey()
    pipeline.get(name)
    result = pipeline.execute()
    name = result[1]
    value = result[2]
    return {'name': name, 'value': value}
