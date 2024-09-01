#/usr/local/bin/python3

from data_hub.data_utils import DataHubManageService
from mysql_utils.mysql_utils import mysqlHeader
from mysql_utils.orm.form import formStock

# all function present a service.
# each of them start with service_ prefix.

# 1 service init mysql database
# data structure:
# input is a dict, key is db name, value is a list of table names.
# for each db, create tables in the mysqlMeta object.

def service_init_mysql_database():
    import json
    from mysql_utils.mysql_header import root_stock_header
    # table_dict is read from a json file named 'table_dict.json'
    table_dict = json.loads(open('table_dict.json', 'r').read())
    # init DataHubManageService object.
    dhms = DataHubManageService(root_stock_header)
    for db in table_dict.keys():
        # create tables.
        for table in table_dict[db]:
            # create table.
            dhms.add_table(table, db)