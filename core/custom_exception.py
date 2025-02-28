# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 16:41
---------
@summary:
---------
@author: LiFree
"""
from fastapi import HTTPException

from common import status


class RequestCheckException(HTTPException):
    """ 自定义请求验证异常类 """

    def __init__(self, status_code: int, detail: dict):
        self.status_code = status_code
        self.detail = detail


class ApiException(HTTPException):
    """ 访问异常 """

    def __init__(self, detail, status_code: int = status.HTTP_200_OK):
        super().__init__(status_code=status_code, detail=detail)

class SQLException(HTTPException):
    """ 自定义请求验证异常类 """

    def __init__(self, status_code: int, detail: dict):
        self.status_code = status_code
        self.detail = detail