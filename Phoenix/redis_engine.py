#!/usr/bin/python3
# file: Phoenix\redis_engine.py
"""
License: MIT
Author:  Fred Monster
Date:    2023-03-25
Purpose: Define a redis engine, which can connect to redis database\n
"""

import redis

class redis_engine(object):
    # init
    def __init__(self, host: str, port: int, password: str, db: int=0) -> None:
        self.host = host
        self.port = port
        self.password = password
        self.redis = redis.Redis(host=self.host, port=self.port, password=self.password, db=db)
    
    # redis string set
    def set_string(self, key: str, value: str):
        self.redis.set(key, value)
    
    # redis string get
    def get_string(self, key: str) -> str:
        return self.redis.get(key)
    
    # redis hash hmset
    def set_hash(self, key: str, value: dict):
        for k, v in value:
            self.redis.hset(key, k, v)

    # redis hash hmget
    def get_hash(self, key: str) -> dict:
        return self.redis.hgetall(key)

    # redis list set
    def set_list(self, key: str, value: str):
        self.redis.lpush(key, value)

    # redis list get
    def get_list(self, key: str) -> list:
        return self.redis.lrange(key, 0, -1)
    
    # shutdown
    def shutdown(self):
        self.redis.connection_pool.disconnect()
