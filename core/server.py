# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:32
---------
@summary: 
---------
@author: LiFree
"""
import logging
import os
import sys

from fastapi import FastAPI

import api.login
from api import testcase, login
from core import middleware
from db.mysqldb import Base, mysql_db
from db.redisdb import rdp
from log import logger, InterceptHandler, format_record


class InitializeApp(object):
    """
    注册App
    """

    def __new__(cls, *args, **kwargs):
        app = FastAPI()
        cls.event_init(app)
        cls.register_router(app)
        cls._log(app)

        return app

    @staticmethod
    def register_router(app: FastAPI) -> None:
        """
        注册路由
        :param app:
        :return:
        """
        # 项目API
        app.include_router(api.router, tags=["首页路由"])
        app.include_router(login.router, prefix="/user", tags=["登录验证"])
        app.include_router(testcase.testcaseLibrary.router, prefix="/testcaseLibrary", tags=["测试用例项目库"])
        app.include_router(testcase.testcaseDirection.router, prefix="/testcaseDirection", tags=["测试用例目录"])


    @staticmethod
    def event_init(app: FastAPI) -> None:
        """
        事件初始化
        :param app:
        :return:
        """

        @app.on_event("startup")
        async def startup():
            # 为所有数据模型生成数据库表
            Base.metadata.create_all(bind=mysql_db.engine)

            # 注册redis
            app.state.rdc = rdp.get_conn()

            logger.debug(f"redis初始化成功--->>{app.state.rdc}")

        @app.on_event('shutdown')
        async def shutdown():
            """
            关闭
            :return:
            """
            # await mysql.close_mysql()
            # scheduler.shutdown()

    @staticmethod
    def _log(app: FastAPI):
        # 替换框架日志引擎
        middleware.register_middleware(app)
        logging.getLogger().handlers = [InterceptHandler()]
        logger.configure(
            handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
        )
        logger.add(
            os.path.join(os.getcwd(), 'logs/{time:YYYY-MM-DD}.log'),
            encoding='utf-8',
            rotation="00:00",  # 轮转时间
            retention="7 days",  # 日志保留时间
            enqueue=True,  # 是否异步处理处理器
            diagnose=True,  # 是否启用诊断模式
            backtrace=True
        )
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
