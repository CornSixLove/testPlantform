# creator: LiFree
# 编写时间： 2025/2/22 14:43
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from .ProjectDao import Project
from .CaseDao import Case
from db.mysqldb import Base  # 假设这是你的 Base 类所在位置

# 模块表
class Module(Base):
    __tablename__ = "module"
    __table_args__ = {'comment': '模块表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    project_id = Column(
        Integer,
        ForeignKey('project.id', ondelete='CASCADE'),  # 数据库级联删除
        nullable=False,
        comment='所属项目ID'
    )
    module_name = Column(String(20), nullable=False, comment='模块名称')
    developer = Column(String(100), nullable=True, comment='开发人员')
    module_desc = Column(String(200), nullable=True, comment='模块描述')
    status = Column(Boolean, default=True, comment='状态: True-启用 False-禁用')

    # 定义与 Project 的多对一关系（重要！）
    project = relationship(
        "Project",
        back_populates="modules",
        single_parent=True  # 强化父子关系约束
    )

    # 新增与 Case 的一对多关系（关键修改！）
    cases = relationship(
        "Case",  # 确保 Case 类已导入或使用字符串形式 "your_module.models.Case"
        back_populates="module",  # 对应 Case 模型中的 module 字段
        cascade="all, delete-orphan",  # 级联删除关联的用例
        passive_deletes=True,  # 与数据库级联删除配合使用
        single_parent=True  # 确保一个用例只属于一个模块
    )

    def __repr__(self):
        return f"<Module(id={self.id}, name={self.module_name})>"