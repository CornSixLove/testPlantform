from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional


class TestcaseLibraryResponse(BaseModel):
    id: int
    testLibrary_name: str
    testLibrary_code: str
    testLibrary_detaills: str
    testLibrary_num: int
    testLibrary_status: int
    createTime: int
    updateTime: Optional[int]  # 允许为 None
    updated_by: Optional[str]  # 允许为 None
    created_by: str

    class Config:
        from_attributes = True
        orm_mode = True  # 这允许直接从 SQLAlchemy 模型实例化 Pydantic 模型
