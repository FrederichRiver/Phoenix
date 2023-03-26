#!/usr/bin/python3

"""
License: MIT
Author:  Fred Monster
Date:    2023-03-26
""" 

# from upper directory import mysqlMeta
from ..mysql_utils import mysqlMeta, mysqlHeader
from .form import formStockManager
from datetime import datetime
from sqlalchemy import update


class StockManagerORM(mysqlMeta):
    database = 'stock'
    table_name = 'stock_manager'
    def __init__(self, header: mysqlHeader):
        super().__init__(header)

    def init_stock(self, stock_code_list: list):
        for stock_code in stock_code_list:
            update_date = datetime.date.today().strftime('%Y-%m-%d')
            stock = formStockManager(stock_code=stock_code, create_date= update_date)
            self.session.add(stock)
            self.session.commit()
    
    def add_stock(self, stock_code: str, stock_name: str, orgId: str, short_code: str, flag: str):
        update_date = datetime.date.today().strftime('%Y-%m-%d')
        stock = formStockManager(
            stock_code=stock_code,
            stock_name=stock_name,
            orgId=orgId,
            short_code=short_code,
            flag=flag,
            create_date= update_date)
        self.session.add(stock)
        self.session.commit()
    
    def update_name(self, stock_code: str, stock_name: str):
        sql = update(formStockManager).where(formStockManager.stock_code==stock_code).values(stock_name=stock_name).execution_options(synchronize_session="fetch")
        self.execute(sql)

    def update_stock(self, stock_code: str, args: dict):
        """
        args keys: stock_name, orgId, short_code, flag
        """
        sql = update(formStockManager).where(formStockManager.stock_code==stock_code).values(args).execution_options(synchronize_session="fetch")
        self.execute(sql)
