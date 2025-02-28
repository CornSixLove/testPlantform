# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:42
---------
@summary:
---------
@author: LiFree
"""
import os
from typing import Union


StrPath = Union[str, os.PathLike]  # stable
BytesPath = Union[bytes, os.PathLike]  # stable
StrOrBytesPath = Union[str, bytes, os.PathLike]  # stable


class DateFormat:
    YMD = "%Y%m%d"
    YMD_CN = "%Y年%m月%d日"
    YMD_HMS = "%Y%m%d %H:%M:%S"
    Y_M_D = "%Y-%m-%d"
    Y_M_D_HMS = "%Y-%m-%d %H:%M:%S"
    a_b_d_Y_M_D_HMS = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"