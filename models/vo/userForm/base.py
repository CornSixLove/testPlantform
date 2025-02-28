"""
@ Created on 2025-01-11 17:23
---------
@summary:
---------
@author: LiFree
"""

from pydantic import BaseModel, Field


class PageBase(BaseModel):
    page: int = Field(default=1, description="")
    size: int = Field(default=20, description="")


class AdminBaseBody(BaseModel):
    username: str = Field(default=..., description="账号")
    password: str = Field(default=..., description="密码")
    code: str = Field(default=None, description="验证码")


class LoginBody(AdminBaseBody):
    """ 登录 """


class RegisterBody(AdminBaseBody):
    """ 注册 """
    confirmPassword: str = Field(..., description="确认密码")
    mobile: str = Field(..., description="手机号")
    nickname: str = Field(..., description="昵称")
