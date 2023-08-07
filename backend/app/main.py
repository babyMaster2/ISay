import random
import aiofiles
from fastapi import FastAPI, HTTPException
from database.redis_db import redis_db_yibu
from pydantic import BaseModel

app = FastAPI()


class PoetryItem(BaseModel):
    text: str
    source: str = None
    annotation: str = None


async def get_random_name():
    filename = 'name.txt'
    async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
        names = await f.readlines()
        name = random.choice(names)
        return name.strip()


@app.post('/poetry/add')
async def add_poetry(poetry_item: PoetryItem):
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        name = await get_random_name()
        a = await redis_db_yibu.exists(name)
        if not a:
            # 加await后添加成功 看来跟异步有关  待研究
            await redis_db_yibu.set(name, poetry_item.model_dump_json())
            print(name)
            print(poetry_item.model_dump_json())
            return {'message': f'add {name} successfully'}
        attempts += 1
    raise HTTPException(status_code=400, detail='Failed to add. Name existed.')


@app.post('/poetry/update')
async def update_poetry_by_name(name, poetry_item: PoetryItem):
    pipeline = redis_db_yibu.pipeline()
    pipeline.get(name)
    result = pipeline.execute()
    if result[0] is None:
        raise HTTPException(status_code=404, detail='Name does not exist.')
    pipeline.set(name, poetry_item.model_dump_json())
    pipeline.execute()
    return {'message': 'update successfully'}


@app.get('/poetry/random/get')
async def get_random_poetry():
    pipeline = redis_db_yibu.pipeline()
    size = pipeline.dbsize()
    if size == 0:
        raise HTTPException(status_code=404, detail='Database is empty.')
    name = pipeline.randomkey()
    pipeline.get(name)
    result = pipeline.execute()
    name = result[0]
    value = result[1]
    return {'name': name, 'value': value}


@app.get('/poetry/all/get')
async def get_all_poetry():
    size = redis_db_yibu.dbsize()
    if size == 0:
        return {'message': 'Database is empty.'}
    keys = await redis_db_yibu.keys('*')
    values = await redis_db_yibu.mget(keys)
    response = [{'name': key, 'value': value} for key, value in zip(keys, values)]

    return response
@app.get('/poetry/name/get')
async def get_poetry_by_name(name):
    pipeline = redis_db_yibu.pipeline()
    pipeline.get(name)
    result = pipeline.execute()
    if not result:
        raise HTTPException(status_code=404, detail='Name does not exist.')
    value = result[0]
    return {'name': name, 'value': value}


@app.get('/create_md/{name}')
async def create_md_file(name):
    value = redis_db_yibu.get(name)
    if not value:
        raise HTTPException(status_code=404, detail='Key does not exist in the database.')

    filename = f'Md/{name}.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(value.decode('utf-8'))
    return {'message': 'MD file created successfully.'}


if __name__ == '__main__':
    pass
