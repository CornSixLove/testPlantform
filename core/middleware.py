# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:33
---------
@summary: 
---------
@author: LiFree
"""
import time

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from log import logger


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_origin_regex="https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def middle(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        m = time.time() - start_time
        response.headers["X-Run-Time"] = str(m)
        m = str(round(m, 2)) + "s" if m > 1 else str(round(m * 1000, 3)) + "ms"
        logger.info(f"访问记录:{request.method} {request.url} 耗时:{m}")

        return response
