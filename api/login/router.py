# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-14 16:29
---------
@summary: 
---------
@author: LiFree
"""

from fastapi import APIRouter, Depends, Request

from models.vo import userForm
from component import auth
from env import test as settings
from common import codes, messages
from db.mysqldb import mysql_db, CustomSession
from models.dao import admin
from models.curd import curd_admin
from models.response.response import ResponseModel
from utils import tools

router = APIRouter()


@router.post("/login")
def login(request: Request, forms: userForm.base.LoginBody, session: CustomSession = Depends(mysql_db.get_db)):
    response = ResponseModel()
    query = curd_admin.select_admin(session, username=forms.username)
    admin_user: admin.User = query.first()

    if not admin_user:  # 用户不存在
        response.code = codes.CODE_10001_ADMIN_UNREGISTERED
        response.message = messages.MESSAGE_ADMIN_UNREGISTERED
        return response

    if admin_user.password != forms.password:  # 密码不匹配
        response.code = codes.CODE_10010_ADMIN_ERROR
        response.message = messages.MESSAGE_ADMIN_ERROR
        return response

    # token = tools.get_uuid().hex.upper()[16:] + f"_{admin_user.id}" + f"_{tools.get_now_timestamp(False)}"

    # 有关鉴权 token修改
    token = tools.get_uuid().hex.upper()[16:] + f"_{admin_user.id}" + f"_{admin_user.role}" + f"_{tools.get_now_timestamp(False)}"

    token = tools.aes_encrypt_ecb(settings.SALT, token, is_hex=True)
    response.token = token

    query.update({
        admin.User.logonTimes: tools.ensure_int(admin_user.logonTimes) + 1,
    })
    session.commit()
    # rdc.hset("fastapi:session", admin_user.id, token)
    return response.model_dump(exclude_none=True)


@router.get("/profile", dependencies=[Depends(auth.access_token_validate)])
def profile(request: Request, session: CustomSession = Depends(mysql_db.get_db)):
    response = ResponseModel()
    user = request.state.user
    response.data = curd_admin.select_user2admin_profile(session, user_id=user)

    return response.model_dump()


@router.post("/register")
def register(request: Request, forms: userForm.base.RegisterBody, session: CustomSession = Depends(mysql_db.get_db)):
    response = ResponseModel()

    # 检查有用户是否存在
    if curd_admin.select_admin(session, username=forms.mobile).first():
        response.code = codes.CODE_10080_ADMIN_REGISTERED
        response.message = messages.MESSAGE_ADMIN_REGISTERED
        return response

    # 注册新用户
    user = admin.User()
    user.username = forms.username
    user.password = forms.password
    user.mobile = forms.mobile
    user.ip = request.client.host
    user.nickname = forms.nickname
    session.add(user)
    session.commit()

    response.message = messages.MESSAGE_REGISTER_OK
    return response


@router.post("/logout", dependencies=[Depends(auth.access_token_validate)])
def logout(request: Request):
    response = ResponseModel()
    admin_user = request.state.user
    print(admin_user)
    # rdc.delete(''.join([const.CACHE_ADMIN_TOKEN_KEY, str(admin_user)]))
    return response
