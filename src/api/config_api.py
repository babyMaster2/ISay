import random
from typing import List, Union

from fastapi import APIRouter, Query

from src.async_redis_client import async_redis_client
from src.models.config import IsayConfig

isay_route = APIRouter()


# redis通常为键值对存储，所以使用HSET命令，这样可以实现将多个键值对存储在一个hash表中，即key value([field value] [field value]...)
# 根据条件获取时考虑到哈希存储的特性，只能先获取所有存储的键，然后再根据条件筛选，这里可能会比较臃肿，todo 可以优化吗？
# todo 抛出异常部分是否也能优化？


@isay_route.post(
    "/add", summary="添加isay", response_model=Union[IsayConfig, str]
)
async def add_isay(
        isay: IsayConfig,
):
    """
    添加isay
    """
    mapping = {
        'is_show': isay.is_show,
        'type': isay.type,
        'source': isay.source,
        'content': isay.content,
        'description': isay.description
        }

    name_exit = await async_redis_client.exists(isay.name)
    if name_exit:
        return f"The name:'{isay.name}' exit"
    await async_redis_client.hset(name=isay.name, mapping=mapping)
    print(isay)
    print(isay.model_dump())
    return isay.model_dump()


@isay_route.post(
    "/add_batch", summary="批量添加isay", response_model=List[Union[IsayConfig, str]]
)
async def add_isay_batch(
        isay_list: List[IsayConfig],
):
    """
    批量添加isay
    """
    result_list = []
    for isay in isay_list:
        result = await add_isay(isay=isay)
        result_list.append(result)
    return result_list


@isay_route.get(
    "/get_all_keys", summary="获取所有键", response_model=List
)
async def get_keys():
    keys = await async_redis_client.keys('*')
    # 这里在fastapi的docs展示会自动解码，但是在这里实际的keys，需要手动解码，所以下面的解码是为了在本地测试时能看到正确的结果
    keys = [key.decode() for key in keys]
    return keys


@isay_route.get(
    "/get_by_name", summary="根据name获取内容", response_model=Union[IsayConfig, None, str]
)
async def get_isay_by_name(
        name: str = Query(),
):
    if not name:
        return f"No name,what are you doing?"
    # 获取的是包含字节字符串的字典
    value = await async_redis_client.hgetall(name)
    if not value:
        return f"The name'{name}' not exit"
    isay = {'name': name}
    # # 同理上面，这里解码也是为了在本地测试时能看到正确的结果
    for key, value in value.items():
        isay[key.decode()] = value.decode()
    try:
        return IsayConfig(**isay)
    except Exception:
        return f"The name:'{name}'的内容不是isay格式"


@isay_route.get(
    "/get_by_keywords", summary="根据关键字获取列表", response_model=Union[List, None, str]
)
async def get_isays_by_keywords(
        keywords: str = Query(),
):
    isays = await get_isays()
    result = []
    for isay in isays:
        if isinstance(isay, IsayConfig):
            for key, value in isay.model_dump().items():
                if keywords in value:
                    result.append(isay)
                    break
    return result


@isay_route.get(
    "/get_all_", summary="获取所有内容", response_model=Union[List, None, str]
)
async def get_isays():
    keys = await get_keys()
    isays = []
    for key in keys:
        value = await get_isay_by_name(key)
        isays.append(value)
    return isays


@isay_route.post(
    "/update", summary="更新isay", response_model=Union[IsayConfig, str]
)
async def update_isay(
        isay: IsayConfig,
):
    """
    更新isay
    """
    name = isay.name
    name_exit = await async_redis_client.exists(name)
    if not name_exit:
        return f"The name:'{name}' not exit"
    mapping = {
        'is_show': isay.is_show,
        'type': isay.type,
        'source': isay.source,
        'content': isay.content,
        'description': isay.description
        }
    await async_redis_client.hset(name=name, mapping=mapping)
    return isay.model_dump()


@isay_route.post(
    "/delete_by_name", summary="通过name删除isay", response_model=str
)
async def delete_isay(
        name: str = Query(),
):
    """
    删除isay
    """
    name_exit = await async_redis_client.exists(name)
    if not name_exit:
        return f"The name:'{name}' not exit"
    value = await get_isay_by_name(name)
    await async_redis_client.delete(name)
    return f"delete name:'{name} 'success,value is {value}"


@isay_route.post(
    "/delete_by_keywords", summary="通过关键字删除isay", response_model=List
)
async def delete_isay_by_keywords(
        keywords: str = Query(),
):
    """
    根据关键字删除isay
    """
    values = await get_isays_by_keywords(keywords)
    result = []
    for value in values:
        result.append(await delete_isay(value.name))
    return result


@isay_route.get(
    "/get_random", summary="随机获取isay", response_model=Union[IsayConfig, None, str]
)
async def get_random_isay():
    max_attempts = 5

    keys = await get_keys()

    for _ in range(max_attempts):
        name = random.choice(keys)
        isay = await get_isay_by_name(name)

        if isay.is_show == 1:
            return isay

    return "没有可展示的isay"


