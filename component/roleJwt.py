# creator: LiFree
# 编写时间： 2025/2/8 17:07
from fastapi import Depends

from pydantic import BaseModel
from typing import List
from fastapi import Depends, HTTPException, status

from component.auth import access_token_validate
from models.dao import admin


class ResponseModel(BaseModel):
    code: int
    message: str


class RoleChecker:
    def __init__(self, allowed_roles: List[int]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: admin.User = Depends(access_token_validate)):
        if user.role not in self.allowed_roles:
            response = ResponseModel(code=403, message="无权限访问该接口")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=response.json(exclude_unset=True)
            )
        return user