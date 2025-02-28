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


class TestCaseBody(BaseModel):
    testLibraryName: str = Field(default=..., description="测试库名称")
    testLibraryDetaills: str = Field(default=None, description="用例库描述")
    testLibraryIcon: str = Field(default=None, description="用例库icon")
    createdBy: str = Field(default=None, description="创建人")

class DeleteTestCaseBody(BaseModel):
    testLibraryName: str = Field(default=..., description="测试库名称")
    testLibraryCode: str = Field(default=..., description="测试库编号")
    createdBy: str = Field(default=None, description="创建人")
    updatedBy: str = Field(default=..., description="更改人")


class UpdateCaseBody(BaseModel):
    testLibraryName: str = Field(default=..., description="更改前测试库名称")
    testLibraryNewName: str = Field(default=..., description="更改后测试库名称")
    testLibraryCode: str = Field(default=..., description="测试库编号")
    testLibraryDetaills: str = Field(default=None, description="用例库描述")
    updatedBy: str = Field(default=..., description="更改人")


