"""
@ Created on 2025-01-14 17:23
---------
@summary:
---------
@author: LiFree
"""

from pydantic import BaseModel, Field


class PageBase(BaseModel):
    page: int = Field(default=1, description="")
    size: int = Field(default=20, description="")


class TestcaseDirectoryBody(BaseModel):
    currentDirectoryId: int = Field(default=0, description="当前目录的id即父目录id")
    currentLibraryId: int = Field(default=0, description="当前目录所属项目的id")
    testDirectoryName: str = Field(default=..., description="测试目录名称")
    createdBy: str = Field(default=None, description="创建人")

class DeleteTestcaseDirectoryBody(BaseModel):
    currentDirectoryId: int = Field(default=0, description="当前目录的id即要删除的目录id")
    belongLibraryId: int = Field(default=0, description="当前目录所属项目id")
    updatedBy: str = Field(default=..., description="更改人")


class UpdateCaseBody(BaseModel):
    testLibraryName: str = Field(default=..., description="更改前测试库名称")
    testLibraryNewName: str = Field(default=..., description="更改后测试库名称")
    testLibraryCode: str = Field(default=..., description="测试库编号")
    testLibraryDetaills: str = Field(default=None, description="用例库描述")
    updatedBy: str = Field(default=..., description="更改人")


