# -*- coding: utf-8 -*-
"""
@ Created on 2024-06-14 12:32
---------
@summary:
---------
@author: LiFree
"""
import time
from typing import Generator, Optional, List

import pymysql
from sqlalchemy import create_engine, exc, engine
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Query

from env import test as settings
from log import logger
from utils.tools import print_parent_caller


def as_dict_decorator(cls):
    """
    orm模型装饰器
    为SQL alchemy orm模型设置反序列化函数
        该方法只能对于全表查询对象生效

    @as_dict_decorator
    class ormModel(Base):
        ...
    query = session.query(ormModel).all() =>
    result = [obj.to_dict for obj in query]  -> [{field: value}]

    """

    def to_dict(self, exclude: list = None):
        if exclude:
            return {c.name: getattr(self, c.name) for c in self.__table__.columns if c not in exclude}

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    setattr(cls, 'to_dict', to_dict)

    return cls


class CustomSession(Session):
    @staticmethod
    def sql_to_dict(query):
        """
        将SQL alchemy的orm查询结果转为dict对象
            query = session.query(User)
            result = sql_to_dict(query.all()) or sql_to_dict(query.first())

        return [{field: value}] or {field: value}
        """

        def convert_to_dict(obj):
            if isinstance(obj, engine.row.Row):  # 判断是否为 Row 对象
                return dict(zip(obj.keys(), obj))
            else:
                return obj.to_dict()

        if isinstance(query, list):
            return [convert_to_dict(obj) for obj in query]
        else:
            return convert_to_dict(query)

    @staticmethod
    @print_parent_caller(types=True)
    def print_sql(query, output: bool = True, is_params: bool = False):
        """ 打印输出orm映射的原生SQL """
        try:

            sql = query.statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
        except Exception as e:
            logger.error(e)
            sql = query.statement

        if output:
            logger.info(sql)
            if is_params:
                logger.info(query.statement.compile().params)
        return sql

    @staticmethod
    def limit_offset(obj: Query, page: int = 1, limit: int = 3) -> Query:
        """ 分页器 """
        return obj.limit(limit).offset((page - 1) * limit)

    def get_connection(self):
        conn = self.bind.raw_connection()
        cursor = conn.cursor()

        return conn, cursor

    @staticmethod
    def close_connection(conn, cursor) -> None:
        if conn:
            conn.close()
        if cursor:
            cursor.close()

    def add_batch(self, sql, datas: List[List]):
        """
        @summary: 批量添加数据
        ---------
        @ param sql: insert ignore into (xxx,xxx,xxx) values (%s, %s, %s)
        @ param datas: 列表 [[v1,v2,v3], [v1,v2,v3]]
                       列表里的值要和插入的key的顺序对应上
        ---------
        @result: 添加行数
        """
        affect_count = None
        conn, cursor = None, None

        try:
            conn, cursor = self.get_connection()
            affect_count = cursor.executemany(sql, datas)
            logger.debug(f"\n{sql.strip()} \n Affected rows: {affect_count}")
            conn.commit()

        except Exception as e:
            logger.error(
                """
                error:%s
                sql:  %s
                """
                % (e, sql)
            )
        finally:
            self.close_connection(conn, cursor)

        return affect_count


class MySQLPool:
    def __init__(
            self,
            user: str = None,
            port: int = None,
            db: str = None,
            user_pass: str = None,
            host: str = None,
            pool_size=15,
            max_overflow=500,
            pool_recycle=3600
    ):
        db = db or settings.MYSQL_DB
        host = host or settings.MYSQL_IP
        port = port or settings.MYSQL_PORT
        user = user or settings.MYSQL_USER_NAME
        user_pass = user_pass or settings.MYSQL_USER_PASS
        sqlalchemy_url = f"mysql+pymysql://{user}:{user_pass}@{host}:{port}/{db}"

        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        self.engine = create_engine(
            sqlalchemy_url,
            # echo=True,  # 是否输出sql语句
            # encoding="utf-8",
            pool_size=self.pool_size,
            pool_recycle=self.pool_recycle,
            max_overflow=self.max_overflow
        )
        self.Session = sessionmaker(autoflush=False, bind=self.engine, class_=CustomSession)
        logger.debug("连接到mysql数据库 %s : %s" % (host, db))

    def get_db(self) -> Generator[Session, None, None]:
        max_retries = 3
        retries = 0
        while retries <= max_retries:
            db: Optional[Session] = None
            try:
                db: Session = self.Session()
                yield db
                break
            except pymysql.err.OperationalError as ee:
                logger.error(f"pymysql.err.OperationalError: {ee}")
                if db:
                    db.rollback()

                time.sleep(0.3)
                continue
            except pymysql.err.IntegrityError as IntegrityError:
                logger.error(f"pymysql.err.OperationalError: {IntegrityError}")
                if db:
                    db.rollback()
            except exc.SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
                if db:
                    db.rollback()
                break
            finally:
                if db:
                    db.close()

            retries += 1

    def update(self, statement):
        try:
            with self.Session() as session:
                session.execute(statement)
                session.commit()
        except Exception as e:
            logger.error(
                """
                error:%s
                sql:  %s
            """
                % (e, statement)
            )
            return False
        else:
            return True


mysql_db = MySQLPool()
Base = declarative_base()

"""
根据数据库现有的表生成 数据表模型
sqlacodegen mysql+pymysql://user:password@host:port/db --outfile=model.py --tables table1,table2
"""
