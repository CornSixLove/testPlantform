# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 16:23
---------
@summary:
---------
@author: LiFree
"""

from sqlalchemy import Column, DateTime, Integer, String, text

from db.mysqldb import Base


class User(Base):
    __tablename__ = 'platform_user'
    __table_args__ = {'comment': '平台用户表'}

    id = Column(Integer, primary_key=True, comment='用户ID')
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    password = Column(String(255), nullable=False, comment='密码')
    mobile = Column(String(20), unique=True, comment='手机号')
    nickname = Column(String(50), comment='昵称')
    mail = Column(String(80), comment='电子邮箱')
    role = Column(Integer, default=1, comment='用户角色: 0-超管, 1-普通用户, 2-测试, 3-开发')  # 新增的字段
    createTime = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), comment='注册时间')
    updateTime = Column(DateTime, onupdate=text("CURRENT_TIMESTAMP"), comment='更新时间')  # 如果使用了SQLAlchemy的事件监听机制自动更新此字段，则需相应配置
    logonTimes = Column(Integer, default=0, comment='登陆次数')