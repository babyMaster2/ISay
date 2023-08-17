from enum import Enum

from pydantic import Field, BaseModel


class EnumType(str, Enum):
    """
    数据类型
    : poem: 诗词
    : isay: 一言
    : other: 其他
    """
    poem = "poem"
    isay = "isay"
    other = "other"


class IsayConfig(BaseModel):
    isay_name: str
    is_show: bool = Field(
        title="是否被一言调用",
        default=int(True),
        description="是否展示",
    )
    isay_type: EnumType = Field(
        title="数据类型",
        default=...,  # default=..., 代表必填
        description="数据的类型",
    )
    isay_from: str = Field(
        title="数据来源",
        default='i don\'t know',
    )
    isay_content: str = Field(
        title="数据内容",
        default=...,
    )
    isay_description: str = Field(
        title="数据描述",
        default='no description',
        description="数据的描述,可能是注释，解读，翻译等",
    )


