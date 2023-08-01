import random
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
    name = result[1]
    value = result[2]
    return {'name': name, 'value': value}


@app.get('/poetry/get')
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
    value = await redis_db_yibu.get(name)
    if not value:
        raise HTTPException(status_code=404, detail='Key does not exist in the database.')

    filename = f'Md/{name}.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(value.decode('utf-8'))

    return {'message': 'MD file created successfully.'}
