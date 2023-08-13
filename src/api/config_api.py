from tools import get_random_name
from typing import List, Union

from fastapi import APIRouter, Query

from src.async_redis_client import async_redis_client
from src.models.config import IsayConfig
from tools import get_random_name

isay_route = APIRouter()
# redis通常为键值对存储，所以使用HSET命令，将键值对存储在一个hash表中


@isay_route.post(
    "/add", summary="添加isay", response_model=IsayConfig
)
async def add_isay(
        isay: IsayConfig,
        name: str = None,
):
    """
    添加诗词
    """
    max_attempts = 5
    if not name:
        name = get_random_name()
    while async_redis_client.exists(name) and max_attempts > 0:
        name = get_random_name()
        max_attempts -= 1
    async_redis_client.hset(key=name, type=isay.isay_type, source=isay.isay_from, content=isay.isay_content, description=isay.isay_description)
    return f'add {name} success, value is {isay}'


@isay_route.get(
    "/get_by_name", summary="根据isay_name获取内容", response_model=Union[IsayConfig, None, str]
)
async def get_config_by_name(
        isay_name: str = Query(),
):

    key = isay_name
    value = async_redis_client.get(key)
    return value


@isay_route.get(
    "/get_by_type", summary="分类获取列表：poem,isay,other", response_model=List[Union[IsayConfig, None, str]]
)
async def get_poem_by_author(
        type: str = Query('isay'),
):
    key = '*'
    values = async_redis_client.get(key)
    value_list = []
    for value in values:
        if value['type'] == type:
            value_list.append(value)
    return value_list


@isay_route.get(
    "/get_by_keywords", summary="根据关键字获取列表", response_model=List[Union[IsayConfig, None, str]]
)
async def get_poem_by_keywords(
        keywords: str = Query(),
):

    key = '*'
    values = async_redis_client.get(key)
    value_list = []
    for value in values:
        if keywords in value:
            value_list.append(value)
    return value_list



# todo 更新诗词
@isay_route.post(
    "/update", summary="更新诗词", response_model=IsayConfig
)
async def update_poem(
        poem: IsayConfig,
):
    """
    更新诗词
    """
    poem = async_redis_client.set(f"{poem.poem_title}:{poem.poet}", poem.poem_verse)
    return poem


@isay_route.post(
    "/delete", summary="通过诗名删除诗词", response_model=IsayConfig
)
async def delete_poem(
        poem_title: str = Query(),
):
    """
    删除诗词
    """
    poem = async_redis_client.delete(f"{poem_title}:*")
    return poem


@isay_route.post(
    "/delete", summary="通过诗人删除诗词", response_model=IsayConfig
)
async def delete_poem(
        poet: str = Query(),
):
    """
    删除诗词
    """
    poem = async_redis_client.delete(f"*:{poet}")
    return poem
