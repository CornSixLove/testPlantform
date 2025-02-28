# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-02 18:16
---------
@summary:
---------
@author: LiFree
"""

from sqlalchemy.orm import Query
from sqlalchemy import update
from db.mysqldb import CustomSession
from models.dao import TestcaseLibraryDao
from utils.tools import Unix_current_timestamp


def selectByTestLibraryName(session: CustomSession, testLibraryName: str) -> Query:
    query = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
        TestcaseLibraryDao.TestcaseLibrary.testLibrary_name == testLibraryName
    )
    return query

def selectByTestLibraryCode(session: CustomSession, testLibraryCode: str) -> Query:
    query = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
        TestcaseLibraryDao.TestcaseLibrary.testLibrary_code == testLibraryCode
    )
    return query

def selectByTestLibrarycodeAndName(session: CustomSession, testLibraryName: str, testLibraryCode: str):
    query = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
        TestcaseLibraryDao.TestcaseLibrary.testLibrary_code == testLibraryCode,
        TestcaseLibraryDao.TestcaseLibrary.testLibrary_name == testLibraryName
    ).all
    return query

def changeTestLibrary(session: CustomSession, NewTestCaseLibrary: TestcaseLibraryDao.TestcaseLibrary, testLibraryNewName: str, testLibraryDetails: str, testLibraryUpdateBy: str):

    current_time = Unix_current_timestamp()

    # 构建UPDATE语句
    stmt = (
        update(TestcaseLibraryDao.TestcaseLibrary)
        .where(TestcaseLibraryDao.TestcaseLibrary.id == NewTestCaseLibrary.id)  # 使用实际的唯一标识符字段
        .values(
            testLibrary_name=testLibraryNewName,
            testLibrary_detaills=testLibraryDetails,
            updated_by=testLibraryUpdateBy,
            updateTime=current_time
        )
    )

    # 执行UPDATE语句
    session.execute(stmt)
    session.commit()

def testDirectoryAddOne(session: CustomSession, NewTestCaseLibrary: TestcaseLibraryDao.TestcaseLibrary, currentNum: int):

    current_time = Unix_current_timestamp()

    # 构建UPDATE语句
    stmt = (
        update(TestcaseLibraryDao.TestcaseLibrary)
        .where(TestcaseLibraryDao.TestcaseLibrary.id == NewTestCaseLibrary.id)  # 使用实际的唯一标识符字段
        .values(
            testLibrary_num=currentNum+1
        )
    )

    # 执行UPDATE语句
    session.execute(stmt)
    session.commit()