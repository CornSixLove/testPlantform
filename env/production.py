# -*- coding: utf-8 -*-
"""
@ Project: python_code
@ AutoName: 张小白
@ ProName: pro_setting.py
@ Time: 2023-03-13 14:46
"""


MYSQL_IP = ""
MYSQL_PORT = 3306
MYSQL_DB = ""
MYSQL_USER_NAME = ""
MYSQL_USER_PASS = ""

DEBUG = False
reload = True
port = 13590

REDIS_HOST = ""
REDIS_PORT = ""
POOL_MAX_CONNECTIONS = 1000
REDIS_PASS = ""

# 令牌相关
SALT = "I9Yt7fJc12d3Sw2L"  # 加密盐值
TOKEN_EXPIRES = 60 * 60 * 24  # token过期时间
