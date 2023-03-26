#!/usr/bin/python3

"""
License: MIT
Author:  Fred Monster
Date:    2023-03-26
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine as _create_engine

# mysqlHeader is a header class
class mysqlHeader(object):
    # init mysql_utils
    def __init__(self, host: str, port: int, user: str, password: str, db: str, charset: str='utf8') -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    # str method
    def __str__(self) -> str:
        # mysql_url = (f"mysql+pymysql://{account}:{password}@{host}:{port}/{database}")
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
    
    @property
    def url(self) -> str:
        return self.__str__()

    @property
    def charset(self) -> str:
        return self.charset

# mysqlMeta is a meta class
class mysqlMeta(object):
    # init
    def __init__(self, header: mysqlHeader) -> None:
        self.header = header
        # self.engine is generated from _create_engine  in sqlalchemy
        self.engine = _create_engine(self.header.url, encoding=self.header.charset, echo=False)
        # self.session is generated from sessionmaker in sqlalchemy
        self.session = sessionmaker(bind=self.engine)()
    
    def __str__(self) -> str:
        version = self.engine.execute("SELECT VERSION()").fetchone()
        return version[0]
    
    @property
    def version(self) -> str:
        return self.__str__()
    
    def execute(self, sql: str) -> None:
        self.session.execute(sql)
        self.session.commit()
