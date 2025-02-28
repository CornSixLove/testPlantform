# creator: LiFree
# 编写时间： 2025/2/22 15:06
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .ModuleDao import Module
from db.mysqldb import Base

class Case(Base):
    __tablename__ = "case"
    __table_args__ = (
        Index('idx_case_module', 'module_id'),  # 外键字段建议加索引
        {'comment': '测试用例表'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    module_id = Column(
        Integer,
        ForeignKey('module.id', ondelete='CASCADE'),  # 级联删除
        nullable=False,
        comment='所属模块ID'
    )
    case_name = Column(String(100), nullable=False, comment='用例名称')
    api = Column(String(100), nullable=False, comment='接口地址')
    step_count = Column(Integer, default=0, comment='步骤数量')
    status = Column(Boolean, default=True, comment='状态: True-启用 False-禁用')
    version = Column(String(20), nullable=False, comment='版本号')
    case_weights = Column(Integer, default=0, comment='用例权重')
    update_time = Column(
        DateTime,
        server_default=func.now(),  # 默认值
        onupdate=func.now(),        # 更新时自动刷新
        comment='更新时间'
    )
    create_time = Column(
        DateTime,
        server_default=func.now(),
        comment='创建时间'
    )
    case_desc = Column(String(100), nullable=True, comment='用例描述')

    # 定义与 Module 的关联关系
    module = relationship(
        "Module",
        back_populates="cases",  # 需在 Module 模型中定义反向引用
        single_parent=True
    )

    steps = relationship(
        "Step",
        back_populates="case",  # 对应 Step 模型中的 case 字段
        cascade="all, delete-orphan",  # 级联删除所有关联步骤
        passive_deletes=True,  # 与数据库级联删除协同工作
        single_parent=True
    )

    def __repr__(self):
        return f"<Case(id={self.id}, name={self.case_name})>"