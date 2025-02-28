# creator: LiFree
# 编写时间： 2025/2/25 17:36
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func, Index
from sqlalchemy.orm import relationship
from StepDao import Step
from .StepDao import Step  # 假设Step模型在StepDao模块中定义
from db.mysqldb import Base

class ReferenceStep(Base):
    __tablename__ = "reference_step"
    __table_args__ = (
        Index('idx_reference_step', 'step_id'),  # 索引用于加速查询
        {'comment': '步骤依赖表'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    step_id = Column(
        Integer,
        ForeignKey('step.id', ondelete='CASCADE'),  # 外键关联至Step表，并设置级联删除
        nullable=False,
        comment='所属步骤ID'
    )
    step_name = Column(String(100), default="", comment='步骤名称')
    path = Column(String(100), default="", comment='路径')
    reference_step_name = Column(String(100), default="", comment='引用步骤名称')
    variable = Column(String(200), nullable=False, comment='变量')

    # 自动管理的时间字段
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

    # 定义与Step的关系
    step = relationship(
        "Step",
        back_populates="references",  # 需要在Step模型中定义反向引用
        single_parent=True
    )

    def __repr__(self):
        return f"<ReferenceStep(id={self.id}, name={self.step_name})>"