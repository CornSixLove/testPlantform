# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:40
---------
@summary:
---------
@author: LiFree
"""

MYSQL_IP = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "pythonweb"
MYSQL_USER_NAME = "root"
MYSQL_USER_PASS = "python"

# fastapi服务相关
DEBUG = True
reload = True  # 是否热加载
workers = 1
port = 13590  # 对外暴露的端口号

# redis链接
REDIS_HOST = "localhost"
REDIS_PORT = 6379
POOL_MAX_CONNECTIONS = 1000  # 连接池最大连接数
REDIS_PASS = "python"

# 令牌相关
SALT = "I9Yt7fJc12d3Sw2L"  # 加密盐值
TOKEN_EXPIRES = 60 * 60 * 24  # token过期时间
