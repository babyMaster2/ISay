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


class EnumSource(str, Enum):
    """
    数据来源
    : author: 作者
    : book: 书籍
    : other: 其他
    """
    author = "author"
    book = "book"
    other = "other"


class EnumContent(str, Enum):
    """
    数据内容
    """
    content = "content"


class EnumDescription(str, Enum):
    """
    数据描述
    : description: 描述
    : translation: 翻译
    """
    description = "description"
    translation = "translation"


class IsayConfig(BaseModel):
    isay_name: str
    isay_type: EnumType = Field(
        title="数据类型",
        default=...,  # default=..., 代表必填
        description="数据的类型，将决定数据是仅存储还是会被调用到一言",
    )
    isay_from: EnumSource = Field(
        title="数据来源",
        default='other',
    )
    isay_content: EnumContent = Field(
        title="数据内容",
        default=...,
    )
    isay_description: EnumDescription = Field(
        title="数据描述",
        default=None,
        description="数据的描述,可能是注释，解读，翻译等",
    )


