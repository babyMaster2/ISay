import asyncio

from src.async_redis_client import async_redis_client

redis_obj = async_redis_client


async def add():
    name = '静夜思'
    mapping = {'作者': '李白?', '内容前两句': '床前明月光，疑是地上霜。', '内容后两句': '举头望明月，低头思故乡。'}
    await redis_obj.hset(name=name, mapping=mapping)
    print(f'add success, name is{name}, value is {mapping}')
    return f'add success, name is{name}, value is {mapping}'


async def select(key):
    # 获取的是包含字节字符串的字典
    v = await redis_obj.exists(key)
    print(v)


async def get(key):
    # 获取的是包含字节字符串的字典
    result = await redis_obj.hgetall(key)
    decoded_result = {k.decode(): v.decode() for k, v in result.items()}
    print(decoded_result)
    return decoded_result


async def get_all_keys():
    keys = await redis_obj.keys('*')
    keys = [key.decode() for key in keys]
    print(keys)
    return keys


async def get_by_keywords(keywords):
    keys = await get_all_keys()
    values = []
    for key in keys:
        value = await get(key)
        for v in value.values():
            if keywords in v:
                values.append({key: value})

    print(values)


async def delete(name):
    name_exit = await redis_obj.exists(name)
    if not name_exit:
        print(f'{name} not exit')
        return f'{name} not exit'
    await redis_obj.delete(name)
    print(f'delete success, name is {name}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(add())
    # loop.run_until_complete(select(None))
    # loop.run_until_complete(get('静夜思'))
    # loop.run_until_complete(get_all())
    # loop.run_until_complete(get_by_keywords('李白'))
    loop.run_until_complete(delete('咏鹅'))
