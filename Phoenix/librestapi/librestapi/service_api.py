#/usr/bin/python3

from libbasemodel.stock_manager import StockBase
from libmysql_utils.header import REMOTE_HEADER
import pickle

def test(p):
    datahub = StockBase(REMOTE_HEADER)
    data = datahub.engine.execute("select version()").fetchall()
    result = pickle.dumps(data)
    return result

def stock_list(param):
    start_date = param['start_date']
    end_date = param['end_date']
    datahub = StockBase(REMOTE_HEADER)
    data = datahub.engine.execute(f"select trade_date,open_price,close_price,high_price,low_price from SH600000 where trade_date between '{start_date}' and '{end_date}'").fetchall()
    result = pickle.dumps(data)
    return result