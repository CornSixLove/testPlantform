# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 16:50
---------
@summary:
---------
@author: LiFree
"""
from typing import Any, Optional

from pydantic import BaseModel, Field, Extra

from common import codes, messages


class ResponseModel(BaseModel):
    """ 接口响应模型 """
    code: int = Field(default=codes.CODE_1_OK, description="状态码")
    data: Any = Field(default=None, description="响应数据")
    success: Optional[bool] = Field(default=True, description="状态")
    message: str = Field(default=messages.MESSAGE_OK, description="响应描述")
    detail: str = Field(default=None, description="响应描述详情")

    class Config:
        extra = Extra.allow  # 允许添加未定义的变量
