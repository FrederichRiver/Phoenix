#!/usr/bin/python3

"""
Data Hub is a engine to manage data and provide data service.
"""
import os
import time
from typing import List
from sqlalchemy import select
from pandas import DataFrame
from mysql_utils.orm import form
from mysql_utils.orm.form import formStock
from mysql_utils.mysql_utils import mysqlMeta

class DataHub(object):
    """
    Data hub provide basic function of data hub.
    usage:
    1. mysql_db is a dict, key is db name, value is mysqlMeta object.
    2. DBs is a list, which contains all db names.
    """
    def __init__(self, header, dblist: List) -> None:
        # for each db in db_list, create a mysqlMeta object which db is None, then set the db of header equals db.
        # add the mysqlMeta object to self.mysql_db.
        # self.mysql_db is a dict, key is db name, value is mysqlMeta object.
        self.mysql_db = {}
        self.DBs = []
        self.header = header
        if dblist:
            for db in dblist:
                header.set_db(db)
                self.mysql_db[db] = mysqlMeta(header)
                self.DBs.append(db)
    
    # use this method to re_init mysql_db and DBs.
    def init_mysql(self, dblist: list):
        self.mysql_db = {}
        self.DBs = []
        if dblist:
            for db in dblist:
                self.header.set_db(db)
                self.mysql_db[db] = mysqlMeta(self.header)
                self.DBs.append(db)

class DataHubManageService(DataHub):
    """
    DataHubManageService provide admin services base on DataHub.
    login using root user.
    """
    # add_table is a function to add a table to a database.
    def add_table(self, table_name: str, database: str):
        # table_obj is the name of table in str
        # import the table object from mysql_utils.orm.form
        # from mysql_utils.orm import form
        # table_name are as 'form.formStock'
        # translate the name into object using eval.
        table_obj = eval(f"form.{table_name}")
        self.mysql_db[database].session.add(table_obj)
        self.mysql_db[database].session.commit()

    # database backup
    def backup_database(self, user: str, pw: str, database: str, file_path: str):
        # output a tar.gz file, which name is database_yyyy_mm_dd_HH_MM_SS.tar.gz
        # check whether file_path exists, if not, create it.
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        # file_name is file_path/database_yyyy_mm_dd_HH_MM_SS.tar.gz
        file_name = os.path.join(file_path, f"{self.mysql_db[database].database}_{time.strftime('%Y_%m_%d_%H_%M_%S')}")
        os.system(f"mysqldump -u {user} -p {pw} {self.mysql_db[database].database} > {file_name}.sql")
        os.system(f"tar -zcvf {file_name}.tar.gz {file_name}.sql")
        # remove the sql file
        os.remove(f"{file_name}.sql")
    
    def restore_database(self, user: str, pw: str,  sql_file_name: str):
        # restore database from a sql file.
        os.system(f"mysql -u {user} -p {pw} < {sql_file_name}")
        

class DataHubPubService(DataHub):
    """
    DataHubPubService provide services base on DataHub.
    basic service:
    1. provide data service
    """
    def api_stock_list(self) -> List[str]:
        """
        Return stock_list as List.
        """
        result = self.mysql_db['stock'].session.execute(select(formStock.stock_code)).all()

        return list(result)

    def api_get_stock_data(self, stock_code: str, start_date: str, end_date: str) -> DataFrame:
        """
        Return stock data as List.
        """
        # replace the __tablename__ in formStock
        formStock.__table__.name = stock_code
        result = self.mysql_db['stock'].session.execute(select(formStock).filter(formStock.stock_code == stock_code, formStock.date >= start_date, formStock.date <= end_date)).all()
        df = DataFrame(result)
        return df