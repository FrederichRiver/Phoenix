#!/usr/bin/python3

"""
License: MIT
Author:  Fred Monster
Date:    2023-03-26
"""

# from upper directory import mysqlMeta
from ..mysql_utils import mysqlMeta, mysqlHeader
from .form import formStock
from datetime import datetime
from sqlalchemy import update, select

class StockORM(mysqlMeta):
    database = 'stock'
    table_name = 'stock_template'
    def __init__(self, header: mysqlHeader):
        super().__init__(header)

    def query(self, stock_code: str):
        formStock.__table__.name = stock_code
        sql = select(formStock.trade_date,formStock.stock_name,formStock.close_price)
        result = self.session.execute(sql).all()
        return result
    
    def update_factor(self, stock_code: str, trade_date: str, adjust_factor: float):
        formStock.__table__.name = stock_code
        sql = update(formStock).filter(formStock.trade_date==trade_date).values(adjust_factor=adjust_factor).execution_options(synchronize_session="fetch")
        self.execute(sql)

