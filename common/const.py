# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:29
---------
@summary:
---------
@author: LiFree
"""


ROOT_BASE = "RootPath"  # 项目根目录环境变量

BASE_PATH = "FastApi"
CONST_TYC_TOKEN_KEY = BASE_PATH + ":const:Token"

# 后台token验证key
SESSION_ID = "sessionId"

USERNAME = "username"
PASSWORD = "password"


# JWT校验参数
class JWTSettings:
    # 其他配置...

    JWT_SECRET_KEY = "your-secret-key"  # 替换为你的密钥
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE_MINUTES = 30
    ACCESS_TOKEN_EXPIRE_MINUTES = JWT_EXPIRE_MINUTES