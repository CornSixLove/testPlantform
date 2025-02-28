# -*- coding: utf-8 -*-
"""
@ Created on 2025-01-14 16:55
---------
@summary: 
---------
@author: LiFree
"""
from http.client import HTTPException

from fastapi import APIRouter, Depends, Request

from core.custom_exception import RequestCheckException, SQLException
from models.dao.TestcaseDirectoryDao import TestcaseDirectory
from models.vo import testcaseForm
from component import auth
from common import messages, status
from db.mysqldb import mysql_db, CustomSession
from models.dao import TestcaseLibraryDao, TestcaseDirectoryDao
from models.curd.curd_testCaseLibrary import changeTestLibrary
from models.response.TestcaseLibraryResponse import TestcaseLibraryResponse
from models.response.response import ResponseModel
from utils.tools import random_HubCode, Unix_current_timestamp

router = APIRouter()

# @router.post("/createTestCaseLibrary")
@router.post("/createTestCaseLibrary", dependencies=[Depends(auth.access_token_validate)])
def createTestCaseLibrary(
        request: Request,
        forms: testcaseForm.base.TestCaseBody,
        session: CustomSession = Depends(mysql_db.get_db)):
    response = ResponseModel()

    # 得到一个有序的随机数作为测试用例编号
    testLibraryCode = random_HubCode()

    continue_looping = True

    while continue_looping:
        # 执行查询
        query_result = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
            TestcaseLibraryDao.TestcaseLibrary.testLibrary_code == testLibraryCode
        ).first()

        # 检查查询结果
        if query_result is not None:
            testLibraryCode = random_HubCode()
        else:
            # 如果查询没有结果，设置标志以退出循环
            continue_looping = False

    # 创建新的测试用例库
    testCaseLibrary = TestcaseLibraryDao.TestcaseLibrary()
    testCaseLibrary.testLibrary_name = forms.testLibraryName
    testCaseLibrary.testLibrary_code = testLibraryCode
    # 传入当前时间
    testCaseLibrary.createTime = Unix_current_timestamp()
    testCaseLibrary.testLibrary_num = 0
    testCaseLibrary.created_by = forms.createdBy
    testCaseLibrary.testLibrary_detaills = forms.testLibraryDetaills
    testCaseLibrary.testLibrary_status = 1
    session.add(testCaseLibrary)
    session.commit()

    # 创建一个testcaseDirectory名为”全部测试用例“的根目录,初始化项目内的目录
    # 创建新的测试用例库
    testcaseDirectory = TestcaseDirectoryDao.TestcaseDirectory()
    testcaseDirectory.testDirectory_name = "全部测试用例"
    # pid和Library_Id=-1代表的是根节点
    testcaseDirectory.pid = -1
    testcaseDirectory.Library_Id = testCaseLibrary.id
    # 传入当前时间
    testcaseDirectory.createTime = Unix_current_timestamp()
    testcaseDirectory.testcase_num = 0
    testcaseDirectory.created_by = forms.createdBy
    testcaseDirectory.testDirectory_status = 1
    session.add(testcaseDirectory)
    session.commit()

    response.message = messages.MESSAGE_REGISTER_OK
    return response

@router.delete("/deleteTestCaseLibrary", dependencies=[Depends(auth.access_token_validate)])
def deleteTestCaseLibrary(
        request: Request,
        forms: testcaseForm.base.DeleteTestCaseBody,
        session: CustomSession = Depends(mysql_db.get_db)):

    response = ResponseModel()

    try:
        # 开始事务
        with session.begin():
            query_result = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
                TestcaseLibraryDao.TestcaseLibrary.testLibrary_code == forms.testLibraryCode
            ).first()

            if query_result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="该目录不存在")

            if forms.updatedBy != query_result.created_by:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只有创建人才可以删除")

            # 删除相关联的TestcaseDirectory记录
            session.query(TestcaseDirectory).filter(
                TestcaseDirectory.Library_Id == query_result.id
            ).delete(synchronize_session=False)

            # 删除TestcaseLibrary记录
            session.delete(query_result)

        # 如果一切正常，则设置成功消息
        response.message = messages.MESSAGE_REGISTER_OK

    except HTTPException as http_exc:
        # 直接抛出HTTP异常让FastAPI处理
        raise http_exc
    except Exception as e:
        # 捕捉并处理未预见的异常
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

    return response


@router.post("/updateTestCaseLibrary", dependencies=[Depends(auth.access_token_validate)])
def updateTestCaseLibrary(
        request: Request,
        forms: testcaseForm.base.UpdateCaseBody,
        session: CustomSession =Depends(mysql_db.get_db)):
    response = ResponseModel()

    # 执行查询找到对应的测试用例库
    NewTestCaseLibrary = session.query(TestcaseLibraryDao.TestcaseLibrary).filter(
        TestcaseLibraryDao.TestcaseLibrary.testLibrary_code == forms.testLibraryCode,
        TestcaseLibraryDao.TestcaseLibrary.testLibrary_name == forms.testLibraryName,
    ).first()

    # 已经存在，可以进行修改
    if NewTestCaseLibrary is not None:
        changeTestLibrary(session,NewTestCaseLibrary,forms.testLibraryNewName,forms.testLibraryDetaills,forms.updatedBy)
    else:
        # 不存在报错
        response.message = messages.MESSAGE_ADMIN_ERROR
        response.detail = "修改测试用例库报错"

    return response


@router.get("/home", dependencies=[Depends(auth.access_token_validate)])
def selectAllTestCaseLibrary(request: Request, session: CustomSession = Depends(mysql_db.get_db)):
    response = ResponseModel()

    TestCaseLibrary = session.query(TestcaseLibraryDao.TestcaseLibrary).all()

    # 序列化所有数据
    testcase_library_responses = [TestcaseLibraryResponse.from_orm(tc) for tc in TestCaseLibrary]

    response.data = testcase_library_responses

    return response


@router.get("/getTestCaseLibraryByPage", dependencies=[Depends(auth.access_token_validate)])
def getTestCaseLibraryByPage(
        request: Request,
        forms: testcaseForm.base.PageBase,
        session: CustomSession = Depends(mysql_db.get_db)
):
    response = ResponseModel()

    offset = (forms.page - 1) * forms.size
    # 执行分页查询
    TestCaseLibrary = session.query(TestcaseLibraryDao.TestcaseLibrary).offset(offset).limit(forms.size).all()
    # 序列化所有数据
    testcase_library_responses = [TestcaseLibraryResponse.from_orm(tc) for tc in TestCaseLibrary]
    response.data = testcase_library_responses

    return response