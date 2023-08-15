from src.async_redis_client import async_redis_client

redis_obj = async_redis_client
async def add():
    res = await redis_obj.hset(name='静夜思', mapping={'作者': '李白', '内容前两句': '床前明月光，疑是地上霜。', '内容后两句': '举头望明月，低头思故乡。'})
    return res


res = add()
print(res)



