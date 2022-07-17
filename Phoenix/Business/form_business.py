#!/usr/bin/python3

from sqlalchemy import Column, ForeignKey 
from sqlalchemy import String as mString
from sqlalchemy import Integer as mInteger
from sqlalchemy import Float as mFloat
from sqlalchemy import DateTime as mDateTime
from sqlalchemy.ext.declarative import declarative_base
from libmysql_utils.orm.form import formStockManager


Base = declarative_base()

class StockPool(Base):
    __tablename__ = 'template_stock_pool'
    idx = Column(mString(12), primary_key=True)
    stock_code = Column(mString(10), ForeignKey=formStockManager.stock_code)
    stock_name = Column(mString(20))

class StockPoolSet(Base):
    """
    A set of forms, these forms are created from StockPool.
    """
    __tablename__ = 'stock_pool_set'
    idx = Column(mString(12), primary_key=True)
    form_name = Column(mString(20))
    create_time = Column(mDateTime)
    description = Column(mString(100))
