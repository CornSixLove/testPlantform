# -*- coding: utf-8 -*-
#                                  _oo8oo_
#                                 o8888888o
#                                 88" . "88
#                                 (| -_- |)
#                                 0\  =  /0
#                               ___/'==='\___
#                             .' \\|     |# '.
#                            / \\|||  :  |||# \
#                           / _||||| -:- |||||_ \
#                          |   | \\\  -  #/ |   |
#                          | \_|  ''\---/''  |_/ |
#                          \  .-\__  '-'  __/-.  /
#                        ___'. .'  /--.--\  '. .'___
#                     ."" '<  '.___\_<|>_/___.'  >' "".
#                    | | :  `- \`.:`\ _ /`:.`/ -`  : | |
#                    \  \ `-.   \_ __\ /__ _/   .-` /  /
#                =====`-.____`.___ \_____/ ___.`____.-`=====
#                                  `=---=`
#
#
#               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                          强大爷保佑         永不宕机/永无bug
# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:41
---------
@summary:
---------
@author: LiFree
"""

MYSQL_IP = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DB = "platform"
MYSQL_USER_NAME = "root"
MYSQL_USER_PASS = "root"

DEBUG = True
reload = True
workers = 1
port = 7001


REDIS_HOST = "127.0.0.1"
REDIS_PORT = "6379"
POOL_MAX_CONNECTIONS = 1000
REDIS_PASS = ""

# 令牌相关
SALT = "I9Yt7fJc12d3Sw2L"  # 加密盐值
TOKEN_EXPIRES = 60 * 60 * 24  # token过期时间
