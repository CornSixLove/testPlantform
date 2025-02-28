# -*- coding: utf-8 -*-
"""
@ Project: python_code
@ AutoName: LiFree
@ ProName: redisdb.py
@ Time: 2024-11-16 16:25
@summary: 操作redis数据库
"""
import time
from typing import Generator

import redis
from redis.exceptions import ConnectionError

from env import test as settings


class RedisPool:
    """ redis连接池 """

    def __init__(self, host, port, max_connections, timeout=2, password=None):
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            max_connections=max_connections,
            socket_connect_timeout=timeout,
            password=password,
            decode_responses=True
        )
        self.conn = redis.StrictRedis(connection_pool=self.pool)

    def get_conn(self):
        try:
            self.conn.ping()
        except ConnectionError:
            self.reconnect()
        return self.conn

    def get_redis(self) -> Generator[redis.Redis, None, None]:
        try:
            self.conn.ping()
            yield self.conn
        except ConnectionError:
            self.reconnect()
        finally:
            self.conn.close()

    def reconnect(self):
        self.pool.disconnect()
        self.conn = redis.StrictRedis(connection_pool=self.pool)

    def check_conn(self):
        count = 0
        while True:
            count += 1
            try:
                if not self.conn.ping():
                    raise ConnectionError("unable to connect to redis")
                else:
                    return True
            except ConnectionError:
                self.reconnect()
            time.sleep(2)


rdp = RedisPool(
    settings.REDIS_HOST,
    settings.REDIS_PORT,
    settings.POOL_MAX_CONNECTIONS,
    password=settings.REDIS_PASS
)

rdc = rdp.get_conn()
redis_obj = rdp.get_redis
