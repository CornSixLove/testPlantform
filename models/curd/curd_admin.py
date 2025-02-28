# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-02 17:16
---------
@summary:
---------
@author: LiFree
"""


from sqlalchemy.orm import Query

from db.mysqldb import CustomSession
from models.dao import admin


def select_admin(session: CustomSession, username: str) -> Query:
    query = session.query(admin.User).filter(
        admin.User.username == username
    )
    return query


def select_user2admin_profile(session: CustomSession, user_id: int):
    query = session.query(
        admin.User.nickname,
        admin.User.mobile,
        admin.User.ip
    ).filter(admin.User.id == user_id)
    return query.first()
