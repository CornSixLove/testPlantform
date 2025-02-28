# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-20 16:55
---------
@summary: 
---------
@author: LiFree
"""

from fastapi import APIRouter, Depends, Request

from models.vo import testcaseDirectoryForm
from component import auth
from common import messages
from db.mysqldb import mysql_db, CustomSession
from models.dao import TestcaseLibraryDao, TestcaseDirectoryDao
from models.curd.curd_testCaseLibrary import testDirectoryAddOne
from models.response.response import ResponseModel
from service.testcaseService.testcaseDirectionService import search_directories_tree
from utils.tools import Unix_current_timestamp

from component.roleJwt import RoleChecker

router = APIRouter()


# @router.post("/createTestCaseDirectory", dependencies=[Depends(auth.access_token_validate)])
# 有关鉴权
@router.post("/createTestCaseDirectory", dependencies=[Depends(RoleChecker([0, 1, 3]))])
def createTestCaseDirectory(
        request: Request,
        forms: testcaseDirectoryForm.base.TestcaseDirectoryBody,
        session: CustomSession = Depends(mysql_db.get_db)):
    response = ResponseModel()

    query_result = session.query(TestcaseDirectoryDao.TestcaseDirectory).filter(
        TestcaseDirectoryDao.TestcaseDirectory.testDirectory_name == forms.testDirectoryName
    ).first()

    # 检查查询结果
    if query_result is not None:
        response.message = messages.MESSAGE_ADMIN_ERROR
        response.detail = "测试目录已经存在"
    else:
        # 创建新的测试用例库
        testcaseDirectory = TestcaseDirectoryDao.TestcaseDirectory()
        testcaseDirectory.testDirectory_name = forms.testDirectoryName
        # 把前端传来的currentDirectoryId作为创建目录的pid
        testcaseDirectory.pid = forms.currentDirectoryId
        testcaseDirectory.Library_Id = forms.currentLibraryId
        # 传入当前时间
        testcaseDirectory.createTime = Unix_current_timestamp()
        testcaseDirectory.testcase_num = 0
        testcaseDirectory.created_by = forms.createdBy
        testcaseDirectory.testDirectory_status = 1
        session.add(testcaseDirectory)
        session.commit()

        # 需要把测试用例库的旗下目录项目进行num+1
        LibraryOfDirectory = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
            TestcaseLibraryDao.TestcaseLibrary.id == forms.currentLibraryId
        ).first()
        testDirectoryAddOne(session, LibraryOfDirectory, LibraryOfDirectory.testLibrary_num)

        response.message = messages.MESSAGE_REGISTER_OK

    return response


@router.delete("/deleteTestCaseDirectory", dependencies=[Depends(RoleChecker([0, 1, 3]))])
def deleteTestCaseDirectory(
        request: Request,
        forms: testcaseDirectoryForm.base.DeleteTestcaseDirectoryBody,
        session: CustomSession = Depends(mysql_db.get_db)):
    response = ResponseModel()

    # 尝试获取要删除的目录记录
    query_result = session.query(TestcaseDirectoryDao.TestcaseDirectory).filter(
        TestcaseDirectoryDao.TestcaseDirectory.id == forms.currentDirectoryId,
        TestcaseDirectoryDao.TestcaseDirectory.Library_Id == forms.belongLibraryId
    ).with_for_update().first()  # 使用 with_for_update 防止并发问题

    if not query_result:
        response.message = messages.MESSAGE_ADMIN_ERROR
        response.detail = "该目录不存在"
        return response

    if forms.updatedBy != query_result.created_by:
        response.message = messages.MESSAGE_ADMIN_ERROR
        response.detail = "只有创建人才可以删除"
        return response

    try:
        # 获取对应的测试用例库
        library_of_directory = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
            TestcaseLibraryDao.TestcaseLibrary.id == forms.belongLibraryId
        ).with_for_update().first()

        if not library_of_directory:
            raise ValueError("对应的测试用例库未找到")

        # 删除目录记录
        session.delete(query_result)
        session.commit()

        # 更新测试用例库中的目录数量
        directory_count = session.query(TestcaseDirectoryDao.TestcaseDirectory).filter(
            TestcaseDirectoryDao.TestcaseDirectory.Library_Id == forms.belongLibraryId
        ).count()
        library_of_directory.testLibrary_num = directory_count-1

        # 提交事务
        session.commit()

        response.detail = "测试目录删除成功"
        response.message = messages.MESSAGE_REGISTER_OK
    except Exception as e:
        session.rollback()  # 出现异常时回滚事务
        response.message = messages.MESSAGE_ADMIN_ERROR
        response.detail = f"删除失败: {str(e)}"
        return response

    return response


@router.get("/directories/search", dependencies=[Depends(RoleChecker([0, 1, 3]))])
def search_directories(
        request: Request,
        name: str,
        session: CustomSession = Depends(mysql_db.get_db)):
    return search_directories_tree(session, name)


