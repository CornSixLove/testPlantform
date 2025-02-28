# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-02 16:23
---------
@summary:
---------
@author: LiFree
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, text

from db.mysqldb import Base


class TestcaseLibrary(Base):
    __tablename__ = 'testcase_Library'
    __table_args__ = {'comment': ''}

    id = Column(Integer, primary_key=True)
    testLibrary_name = Column(String(50), comment='测试库名称')
    testLibrary_code = Column(String(20), unique=True, comment='用例库编号')
    testLibrary_detaills = Column(String(50), comment='用例库描述')
    testLibrary_icon = Column(String(50), comment='用例库icon')
    testLibrary_num = Column(Integer, comment='测试用例库里的测试用例数')
    testLibrary_status = Column(Integer, comment='测试用例库的状态: 1-存在  0-删除')
    createTime = Column(Integer, comment='创建测试用例库时间')
    updateTime = Column(Integer, comment='更新测试用例库时间')
    created_by = Column(String(20), comment='创建人')
    updated_by = Column(String(20), comment='更新人')


