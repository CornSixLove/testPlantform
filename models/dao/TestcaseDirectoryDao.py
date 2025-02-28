# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-08 16:23
---------
@summary:
---------
@author: LiFree
"""
from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref

from db.mysqldb import Base


# 定义数据库模型
# class TestcaseDirectory(Base):
#     __tablename__ = "testcase_directory"
#     __table_args__ = (
#         ForeignKeyConstraint(['pid'], ['testcase_directory.id'], ondelete='cascade'),
#         {'comment': ''}
#     )
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     pid = Column(Integer, ForeignKey("testcase_directory.id"), nullable=True)
#     Library_Id = Column(Integer, comment='所属测试用例库id')
#     testDirectory_name = Column(String(50), comment='测试项目名称')
#     testcase_num = Column(Integer, comment='测试项目下所创建的测试用例数')
#     testDirectory_status = Column(Integer, comment='测试项目的状态: 1-存在  0-删除')
#     createTime = Column(Integer, comment='创建测试项目时间')
#     updateTime = Column(Integer, comment='更新测试项目时间')
#     created_by = Column(String(20), comment='创建人')
#     updated_by = Column(String(20), comment='更新人')
#     parent = relationship("TestcaseDirectory", remote_side=[id], backref=backref("children", cascade="all, delete-orphan"))


class TestcaseDirectory(Base):
    __tablename__ = "testcase_directory"
    __table_args__ = (
        ForeignKeyConstraint(['pid'], ['testcase_directory.id'], ondelete='cascade'),
        ForeignKeyConstraint(['Library_Id'], ['testcase_Library.id'], ondelete='CASCADE'),
        {'comment': ''}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, ForeignKey("testcase_directory.id"), nullable=True)
    # 修改这里，添加 ondelete='cascade'
    Library_Id = Column(Integer, ForeignKey("testcase_Library.id", ondelete='cascade'), comment='所属测试用例库id')
    testDirectory_name = Column(String(50), comment='测试项目名称')
    testcase_num = Column(Integer, comment='测试项目下所创建的测试用例数')
    testDirectory_status = Column(Integer, comment='测试项目的状态: 1-存在  0-删除')
    createTime = Column(Integer, comment='创建测试项目时间')
    updateTime = Column(Integer, comment='更新测试项目时间')
    created_by = Column(String(20), comment='创建人')
    updated_by = Column(String(20), comment='更新人')
    parent = relationship("TestcaseDirectory", remote_side=[id],
                          backref=backref("children", cascade="all, delete-orphan"))
