from typing import List, Union

from fastapi import APIRouter, Query, HTTPException

from src.api.tools import get_random_name
from src.async_redis_client import async_redis_client
from src.models.config import IsayConfig

isay_route = APIRouter()


# redis通常为键值对存储，所以使用HSET命令，这样可以实现将多个键值对存储在一个hash表中，即key value([field value] [field value]...)
# 根据条件获取时考虑到哈希存储的特性，只能先获取所有存储的键，然后再根据条件筛选，这里可能会比较臃肿，todo 可以优化吗？
# todo 抛出异常部分是否也能优化？


@isay_route.post(
    "/add", summary="添加isay", response_model=IsayConfig
)
async def add_isay(
        isay: IsayConfig,
        name: str = None,
):
    """
    添加isay
    """
    mapping = {
        'is_show': isay.is_show,
        'type': isay.isay_type,
        'source': isay.isay_from,
        'content': isay.isay_content,
        'description': isay.isay_description
        }
    max_attempts = 5
    attempt = 0
    if name:
        name_exit = await async_redis_client.exists(name)
        if name_exit:
            raise HTTPException(status_code=400, detail='Failed to add. Name existed.')
        await async_redis_client.hset(name=name, mapping=mapping)
        return f'add {name} success, value is {isay}'
    elif not name:
        while attempt < max_attempts:
            name = await get_random_name()
            name_exit = await async_redis_client.exists(name)
            if not name_exit:
                await async_redis_client.hset(name=name, mapping=mapping)
                return f'add {name} success, value is {isay}'
            attempt += 1
        raise HTTPException(status_code=400, detail='Failed to add. Name existed and i have try 5 次.')


@isay_route.post(
    "/add_batch", summary="批量添加isay", response_model=IsayConfig
)
async def add_isay_batch(
        isay_list: List[IsayConfig],
):
    """
    批量添加isay
    """
    result_list = []
    for isay in isay_list:
        try:
            result = await add_isay(isay=isay, name=isay.isay_name)
            result_list.append(result)
        except Exception as e:
            result_list.append(e)
    return result_list
@isay_route.get(
    "/get_all_keys", summary="获取所有键", response_model=Union[IsayConfig, None, str]
)
async def get_keys():
    keys = await async_redis_client.keys('*')
    keys = [key.decode() for key in keys]
    return keys


@isay_route.get(
    "/get_all_", summary="获取所有内容", response_model=Union[IsayConfig, None, str]
)
async def get_isays():
    keys = await get_keys()
    values = []
    for key in keys:
        value = await get_isay_by_name(key)
        values.append(value)
    return values



@isay_route.get(
    "/get_by_name", summary="根据isay_name获取内容", response_model=Union[IsayConfig, None, str]
)
async def get_isay_by_name(
        isay_name: str = Query(),
):
    key = isay_name
    # 获取的是包含字节字符串的字典
    value = await async_redis_client.hgetall(key)
    decoded_value = {k.decode(): v.decode() for k, v in value.items()}
    return decoded_value


@isay_route.get(
    "/get_by_keywords", summary="根据关键字获取列表", response_model=List[Union[IsayConfig, None, str]]
)
async def get_isays_by_keywords(
        keywords: str = Query(),
):
    keys = await get_keys()
    values = []
    for key in keys:
        value = await get_isay_by_name(key)
        for item in value.values():
            if keywords in item:
                values.append({key: value})
    return values


@isay_route.post(
    "/update", summary="更新isay", response_model=IsayConfig
)
async def update_isay(
        name: str,
        poem: IsayConfig,
):
    """
    更新isay
    """
    name_exit = await async_redis_client.exists(name)
    if not name_exit:
        return f'{name} not exit'
    mapping = {
        'is_show': poem.is_show,
        'type': poem.isay_type,
        'source': poem.isay_from,
        'content': poem.isay_content,
        'description': poem.isay_description
        }
    await async_redis_client.hset(name=name, mapping=mapping)
    return f'update {name} success, value is {poem}'


@isay_route.post(
    "/delete_by_name", summary="通过is_name删除isay", response_model=IsayConfig
)
async def delete_isay(
        name: str = Query(),
):
    """
    删除isay
    """
    name_exit = await async_redis_client.exists(name)
    if not name_exit:
        return f'{name} not exit'
    await async_redis_client.delete(name)
    return f'delete {name} success'


@isay_route.post(
    "/delete_by_keywords", summary="通过关键字删除isay", response_model=IsayConfig
)
async def delete_isay_by_keywords(
        keywords: str = Query(),
):
    """
    根据关键字删除isay
    """
    values = await get_isays_by_keywords(keywords)
    delete_list = []
    for value in values:
        for key in value.keys():
            await async_redis_client.delete(key)
            delete_list.append({key: value})
    return f'delete {delete_list} success'
