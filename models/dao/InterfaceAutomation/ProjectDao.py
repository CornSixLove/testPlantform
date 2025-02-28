# creator: LiFree
# 编写时间： 2025/2/22 14:42
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from .ModuleDao import Module
from db.mysqldb import Base


# 项目表
class Project(Base):
    __tablename__ = "project"
    __table_args__ = {'comment': '项目表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    project_name = Column(String(20), nullable=False, comment='项目名称')
    project_desc = Column(String(200), nullable=True, comment='项目描述')
    status = Column(Boolean, default=True, comment='状态: True-启用 False-禁用')

    # 定义与 Modules 的一对多关系（重要！）
    modules = relationship(
        "Module",
        back_populates="project",
        cascade="all, delete-orphan",  # 级联删除关联模块
        passive_deletes=True  # 与数据库级联删除配合使用
    )

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.project_name})>"