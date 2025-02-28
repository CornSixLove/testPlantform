# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-18 16:31
---------
@summary: 
---------
@author: LiFree
"""
from fastapi import Request

from env import test as settings
from common import status, codes
from core.custom_exception import RequestCheckException, ApiException
from models.response.response import ResponseModel
from utils import tools
from log import logger


def access_token_validate(request: Request):
    """ token验证 """
    try:
        return request.state.user
    except AttributeError:
        pass
    response = ResponseModel()
    response.code = codes.MINUS_CODE_1_ERROR
    response.success = False
    response.message = None

    token = request.headers.get("access_token") or request.headers.get("access-token")

    if not token:  # 如果未携带令牌或令牌认证错误，抛出异常
        logger.warning(f"{request.client.host} > 未携带token")
        response.code = status.HTTP_201_CREATED
        raise RequestCheckException(status_code=status.HTTP_201_CREATED, detail=response.model_dump(exclude_unset=True))

    try:
        # uuid, user, expire = tools.aes_decrypt_ecb(settings.SALT, token).split("_")
        # 有关鉴权
        uuid, user, role, expire = tools.aes_decrypt_ecb(settings.SALT, token).split("_")

    except Exception as e:
        logger.warning(f"ip: {request.client.host} > 令牌无效 \t{token}， {e}")
        response.code = status.HTTP_201_CREATED
        raise RequestCheckException(status_code=status.HTTP_201_CREATED, detail=response.model_dump(exclude_unset=True))
    else:
        now_time = tools.get_now_timestamp(False)
        expire = now_time - int(expire)
        if expire > settings.TOKEN_EXPIRES:  # token 过期
            response.code = codes.CODE_202_TOKEN_EXPIRED
            raise ApiException(status_code=status.HTTP_202_ACCEPTED, detail=response.model_dump(exclude_unset=True))

    setattr(request.state, 'user', user)  # 挂载到当前请求的全局

    return user


