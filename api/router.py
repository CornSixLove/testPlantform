# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 16:49
---------
@summary:
---------
@author: LiFree
"""

from fastapi import APIRouter

from models.response.response import ResponseModel


router = APIRouter()


@router.get("/hello")
def get_system():
    response = ResponseModel()
    response.data = "hello word"
    return response.model_dump(exclude_none=True)
