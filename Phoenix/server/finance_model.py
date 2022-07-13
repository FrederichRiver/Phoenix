#!/usr/bin/python3

from libmysql_utils.header import REMOTE_HEADER
from libmysql_utils.mysql8 import mysqlQuery
from pandas import DataFrame, Series, Timestamp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FinanceModel(object):
    def __init__(self, stock_code: str) -> None:
        self.stock_code = stock_code

class FullCheck(mysqlQuery):
    def __init__(self, header):
        super().__init__(header)
        self.df = DataFrame()
    
    def query_data(self, stock_code: str, from_date, to_date) -> DataFrame:
        column = ['trade_date', 'close']
        query_string = 'trade_date,close_price'
        df = self.condition_select(stock_code, query_string, f"trade_date between '{from_date}' and '{to_date}'")
        if not df.empty:
            df.columns = column
            df[df['close'] == 0.0] = np.nan
            df.set_index('trade_date', inplace=True)
                
            df.index = pd.to_datetime(df.index)
            df.sort_index(axis=0, ascending=True, inplace=True) 
            df = df.fillna(method='ffill')

            df.dropna(axis=0,inplace=True)
            # print(df)
            self.df = df
            # print(f"{stock_code}:  {'%d.2%%' % float(df.loc[:, 'ROE'].values[-1])}")
        else:
            df = DataFrame()
        return df


    def query_stock(self, stock_code: str) -> DataFrame:
        alpha = 100000000
        column = ['trade_date', 'open', 'close', 'high', 'low', 'volume', 'turnover', 'adjust_factor']
        query_string = 'trade_date,open_price,close_price,high_price,low_price,volume,turnover,adjust_factor'
        df = self.select_values(stock_code, query_string)
        df.columns = column
        df[df['close'] == 0.0] = np.nan
        df.set_index('trade_date', inplace=True)
             
        df.index = pd.to_datetime(df.index)
        df.sort_index(axis=0, ascending=True, inplace=True) 
        df = df.fillna(method='ffill')

        df.dropna(axis=0,inplace=True)
        # print(df)
        self.df = df
        # print(f"{stock_code}:  {'%d.2%%' % float(df.loc[:, 'ROE'].values[-1])}")
        return df

    def query_stock2(self, stock_code: str) -> DataFrame:
        alpha = 100000000
        column = ['trade_date', 'open', 'close', 'high', 'low', 'volume', 'turnover', 'adjust_factor']
        query_string = 'trade_date,open_price,close_price,high_price,low_price,volume,turnover,adjust_factor'
        df1 = self.select_values(stock_code, query_string)
        df1.columns = column
        df1.set_index('trade_date', inplace=True)
        
        df2 = self.condition_select('company_stock_structure', 'report_date,total_stock', f"stock_code='{stock_code}'")
        df2.columns = ['trade_date', 'total']
        df2.set_index('trade_date', inplace=True)
        
        df3 = self.condition_select('income_statement', 'report_date,float_c37,float_c41', f"char_stock_code='{stock_code}'")
        df3.columns = ['trade_date', 'profit', 'net_profit']
        df3.set_index('trade_date', inplace=True)
        df3.loc[:, 'profit'] = df3.loc[:, 'profit'] / alpha
        df3.loc[:, 'net_profit'] = df3.loc[:, 'net_profit'] / alpha

        df4 = self.condition_select('balance_sheet', 'report_date,float_owner_equity', f"char_stock_code='{stock_code}'")
        df4.columns = ['trade_date', 'net_capital']
        df4.set_index('trade_date', inplace=True)
        df4.loc[:, 'net_capital'] = df4.loc[:, 'net_capital'] / alpha
        
        df = pd.concat([df1, df2, df3, df4], axis=0)
        df.index = pd.to_datetime(df.index)
        df.sort_index(axis=0, ascending=True, inplace=True) 
        df = df.fillna(method='ffill')
        df.loc[:, 'value'] = df.loc[:, 'close'] * df.loc[:, 'total'] / alpha
        df.loc[:, 'pe'] = df.loc[:, 'value'] / df.loc[:, 'profit']
        df.loc[:, 'ROE'] = 100 * df.loc[:, 'net_profit'] / df.loc[:, 'net_capital']

        df.dropna(axis=0,inplace=True)
        # print(df)
        self.df = df
        # print(f"{stock_code}:  {'%d.2%%' % float(df.loc[:, 'ROE'].values[-1])}")
        return df


class KLine(object):
    def __init__(self, stock_code: str, data: DataFrame) -> None:
        self.stock_code = stock_code
        self.df = data
        win_list = [5, 10, 20, 60]
        for w in win_list:
            self.df.loc[:, f'MA{w}'] = self.df.loc[:, 'close'].rolling(window=w).mean()
        # self.df.loc[:, 'flag'] = np.where(abs(self.df.loc[:, 'MA5']-self.df.loc[:, 'MA10'])/self.df.loc[:, 'MA5'] < 0.01, 100, 0)
        self.date_index = self.df.index.tolist()
        #self.df[['close', 'MA5', 'MA10', 'MA20', 'flag']].plot()
        #plt.show()

    @property
    def ma5(self) -> Series:
        return self.df.loc[:, 'MA5']

    @property
    def ma10(self) -> Series:
        return self.df.loc[:, 'MA10']

    @property
    def ma20(self) -> Series:
        return self.df.loc[:, 'MA20']

    @property
    def ma60(self) -> Series:
        return self.df.loc[:, 'MA60']
    
    def trade_date(self, trade_date: Timestamp, delta=1):
        """
        根据输入的delta, 返回以trade date为中心前后delta的时间。
        """
        if trade_date in self.date_index:
            idx = self.date_index.index(trade_date)
        else:
            idx = 0
        a = self.date_index[idx-delta] if idx - delta > 0 else None 
        b = self.date_index[idx+delta] if idx < len(self.date_index) else None
        return a, b

    def cross(self, trade_date: Timestamp, kline1: Series, kline2: Series):
        """
        判断两条k线交叉。
        """
        _, next_day = self.trade_date(trade_date)
        if kline1.loc[trade_date] < kline2.loc[trade_date] and kline1.loc[next_day] < kline2.loc[next_day]:
            return next_day
        else:
            return None
    
    def cross2(self, trade_date: Timestamp, kline1: Series, kline2: Series, kline3: Series):
        """
        计算在20日K线上, 5日与10日k线交叉。
        """
        _, next_day = self.trade_date(trade_date)
        if kline1.loc[trade_date] < kline2.loc[trade_date] and kline1.loc[next_day] < kline2.loc[next_day] and kline2.loc[next_day] > kline3.loc[next_day]:
            return next_day
        else:
            return None

    def criterion(self, ma5: Series, ma10: Series, ma20: Series):
        last_day = self.date_index[-1]
        if (ma5.loc[last_day] < 1.02 * ma10.loc[last_day]) and (ma5.loc[last_day] > ma10.loc[last_day]) and (ma10.loc[last_day] > ma20.loc[last_day]):
            return True
        else:
            return False 

def workflow_frame():
    # 获取股票列表
    DataEngine = FullCheck(REMOTE_HEADER)
    StQ = mysqlQuery(REMOTE_HEADER)
    stock_list = StQ.engine.execute("show tables like 'SH6%%'").fetchall()
    # 初始化数据
    df = None
    with open('/home/fred/Documents/dev/Phoenix/Phoenix/server/statistics.txt', 'a', buffering=1) as f:
        # f.write("Delta, Rate, Expect, Margin\n")
        for item in stock_list[14:]:
            stock = item[0]
            print(stock)
            try:
                df = DataEngine.query_stock(stock)
                # 读取数据
                if not df.empty:
                    f.write(f"Stock {stock}\n")
                    kl = KLine(stock, df)
                    param = range(1,30)
                    pos = 0
                    total = 0
                    ex = 0
                    margin = 0
                    for j in param:
                        for itm in kl.date_index:    
                            try:
                                if kl.cross(itm, kl.ma5, kl.ma10):
                                    _, d = kl.trade_date(itm, j)
                                    if d:
                                        """ x = kl.df.loc[d,'close']
                                        y = kl.df.loc[itm,'close']
                                        # print(f"{x},{y}") """
                                        profit = kl.df.loc[d,'close'] / kl.df.loc[itm,'close']
                                        total += 1
                                        if profit > 1:
                                            pos += 1
                                            ex += profit
                                    else:
                                        print(d)
                            except:
                                pass
                        rate = 100 * pos / total
                        ex = 100 * ex / pos
                        margin = (ex - 100)/ j
                        f.write(f"{j}, {'%.2f%%' % rate}, {'%.2f%%' % ex}, {'%.2f%%' % margin}\n")
                        pos = 0
                        total = 0
                        ex = 0
                else:
                    pass
            except:
                pass


def workflow_2():
    DataEngine = FullCheck(REMOTE_HEADER)
    StQ = mysqlQuery(REMOTE_HEADER)
    stock_list = StQ.engine.execute("select stock_code from stock_manager where flag='t'").fetchall()
    count = 0
    for item in stock_list:
        stock_code =  item[0]
        df = DataEngine.query_data(stock_code, '2022-05-01', '2022-06-29')
        # 读取数据
        if not df.empty:
            kl = KLine(stock_code, df)
            if flag := kl.criterion(kl.ma5, kl.ma10, kl.ma20):
                count += 1
                print(f"{stock_code},{count}")
    

if __name__ == '__main__':
    workflow_2()