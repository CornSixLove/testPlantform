# creator: LiFree
# 编写时间： 2025/2/22 18:01


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Index, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ReferenceStepDao import ReferenceStep
from .ModuleDao import Module
from db.mysqldb import Base

class Step(Base):
    __tablename__ = "step"
    __table_args__ = (
        Index('idx_step_case', 'case_id'),  # 外键字段加索引
        {'comment': '测试步骤表'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    case_id = Column(
        Integer,
        ForeignKey('case.id', ondelete='CASCADE'),  # 级联删除
        nullable=False,
        comment='所属用例ID'
    )
    step_name = Column(String(100), nullable=False, comment='步骤名称')
    step_desc = Column(String(100), nullable=True, comment='步骤描述')
    step_level = Column(String(10), nullable=False, comment='步骤级别')  # 原 Django 的 steplevel
    method = Column(String(10), nullable=False, comment='请求方法 (GET/POST等)')

    # 长文本字段使用 Text 类型（替代 Django 的 CharField）
    params = Column(Text, nullable=True, comment='请求参数 (JSON字符串)')
    headers = Column(Text, nullable=True, comment='请求头 (JSON字符串)')
    files = Column(Text, nullable=True, comment='上传文件 (JSON字符串)')
    assert_response = Column(Text, nullable=True, comment='断言规则 (JSON字符串)')
    api_dependency = Column(Text, nullable=True, comment='依赖接口 (JSON字符串)')

    sql_count = Column(Integer, default=0, comment='SQL操作次数')  # 原 Django 的 sqlCount
    nosql_count = Column(Integer, default=0, comment='NoSQL操作次数')  # 原 nosqlCount
    step_weights = Column(Integer, default=0, comment='步骤权重')
    status = Column(Boolean, default=True, comment='状态: True-启用 False-禁用')

    # 时间字段自动管理
    update_time = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )
    create_time = Column(
        DateTime,
        server_default=func.now(),
        comment='创建时间'
    )

    # 定义与 Case 的关联关系
    case = relationship(
        "Case",
        back_populates="steps",  # 需在 Case 模型中定义反向引用
        single_parent=True
    )

    # 在Step模型中添加以下内容
    references = relationship(
        "ReferenceStep",
        back_populates="step",
        cascade="all, delete-orphan",  # 级联删除所有关联的ReferenceStep记录
        passive_deletes=True,  # 支持数据库级别的级联删除
        single_parent=True
    )

    sql_operations = relationship(
        "Sql",
        back_populates="step",
        cascade="all, delete-orphan",  # 级联删除所有关联的Sql记录
        passive_deletes=True,  # 支持数据库级别的级联删除
        single_parent=True
    )

    def __repr__(self):
        return f"<Step(id={self.id}, name={self.step_name})>"