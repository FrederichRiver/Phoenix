#!/usr/local/bin/python3.8
#coding=utf-8
"""
Created on 2023-04-18 22:59:36
"""

from mysql_utils.mysql_utils import mysqlHeader

HOST = 'localhost'
PORT = 3306

root_stock_header = mysqlHeader(HOST, PORT, 'root', 'mysql14great', 'stock')