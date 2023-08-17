import asyncio

from src.async_redis_client import async_redis_client

redis_obj = async_redis_client


async def add():
    name = '静夜思'
    mapping = {'作者': '李白', '内容前两句': '床前明月光，疑是地上霜。', '内容后两句': '举头望明月，低头思故乡。'}
    await redis_obj.hset(name=name, mapping=mapping)

    return f'add success, name is{name}, value is {mapping}'


async def main():
    result = await add()
    print(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
