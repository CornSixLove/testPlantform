# creator: LiFree
# 编写时间： 2025/2/25 21:44
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Index
from sqlalchemy.sql import func
from StepDao import Step
from sqlalchemy.orm import relationship
from .ModuleDao import Module  # 假设Module模型在ModuleDao中定义
from db.mysqldb import Base

class Sql(Base):
    __tablename__ = "sql"
    __table_args__ = (
        Index('idx_sql_step', 'step_id'),  # 外键字段加索引
        {'comment': 'SQL操作表'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    step_id = Column(
        Integer,
        ForeignKey(' step.id', ondelete='CASCADE'),  # 级联删除
        nullable=False,
        comment='所属步骤ID'
    )
    db = Column(String(40), default="", comment='数据库名称')
    db_remark = Column(String(100), default="", comment='数据库备注')
    sql_condition = Column(Integer, nullable=False, comment='SQL条件')
    is_select = Column(Boolean, nullable=False, comment='是否查询语句')
    variable = Column(String(200), nullable=False, comment='变量名')
    sql = Column(Text, nullable=False, comment='SQL语句')
    remark = Column(String(200), default="", comment='备注')
    status = Column(Boolean, default=True, comment='状态: True-启用 False-禁用')

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

    step = relationship(
        "Step",
        back_populates="sql_operations",  # 需要在 Step 模型中定义反向引用
        single_parent=True
    )

    def __repr__(self):
        return f"<Sql(id={self.id}, step_id={self.step_id}, sql={self.sql[:50]})>"