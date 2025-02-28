# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:32
---------
@summary: 项目启动文件
---------
@author: liFree
"""
import uvicorn
from core import server
from env import test as settings

app = server.InitializeApp()


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.reload
    )
