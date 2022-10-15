#!/usr/bin/python38
import matplotlib.pyplot as plt
import os
from abc import ABC
import io
import mplfinance as mpf
import matplotlib.pyplot as plt
from libbasemodel.stock_model import StockBase, StockData
from libmysql_utils.mysql8 import mysqlHeader
from libmysql_utils.header import GLOBAL_HEADER, REMOTE_HEADER
from pandas import DataFrame
import pandas as pd
from dev_global.env import TIME_FMT
import datetime
from PIL import Image
"""
接收各种数据之后绘制图像。
"""

import pandas as pd
from dev_global.env import TIME_FMT
from libbasemodel.stock_model import StockBase
from pandas import DataFrame
"""
数据源用于获取各种数据，处理之后提交给graph方法来绘制图像用于可视化。
"""
class DataSource(StockBase):
    def get_shibor_data(self, length=60) -> DataFrame:
        df = self.select_values(
            "shibor", 'release_date,one_week')
        # data cleaning
        df.columns = ['Date', 'one_week']
        df['Date'] = pd.to_datetime(df['Date'], format=TIME_FMT)
        df.set_index('Date', inplace=True)
        df.dropna(axis=0, how='any', inplace=True)
        df = df[-length:].copy()
        return df

    def get_treasury_yield_data(self, length=60) -> DataFrame:
        df1 = self.select_values(
            "china_treasury_yield", 'report_date,ten_year')
        # data cleaning
        df1.columns = ['Date', 'China']
        df1['Date'] = pd.to_datetime(df1['Date'], format=TIME_FMT)
        df1.set_index('Date', inplace=True)
        df1.dropna(axis=0, how='any', inplace=True)
        df1 = df1[-length:].copy()

        df2 = self.select_values(
            "us_treasury_yield", 'report_date,ten_year')
        # data cleaning
        df2.columns = ['Date', 'US']
        df2['Date'] = pd.to_datetime(df2['Date'], format=TIME_FMT)
        df2.set_index('Date', inplace=True)
        df2.dropna(axis=0, how='any', inplace=True)
        df2 = df2[-length:].copy()
        df = pd.concat([df1, df2], axis=1)
        return df

class plot(ABC):
    def plot(self, title: str, df):
        """
        return a image buffer in memery.
        """
        buf = io.BytesIO()
        self.param_dict['savefig'] = {'fname':buf}
        self.param_dict['title'] = title
        mpf.plot(df, **self.param_dict)
        return buf

    def save(self, title:str, path:str, df):
        """
        Save image as .png image.
        """
        img_path = os.path.join(path, f"{title}.png")
        buf = self.plot(title, df)
        img = Image.open(buf)
        img.save(img_path)
        return True

class kPlot(plot):
    def __init__(self) -> None:
        usr_color = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')
        usr_style = mpf.make_mpf_style(marketcolors=usr_color)
        self.param_dict = {}
        self.param_dict['returnfig'] = True
        self.param_dict['type'] = 'candle'
        self.param_dict['mav'] = (5, 10, 20)
        self.param_dict['volume'] = True
        self.param_dict['title'] = 'STOCK'
        self.param_dict['style'] = usr_style
        self.param_dict['datetime_format'] = TIME_FMT
        self.param_dict['figscale'] = 1.0
        


class LinePlot(object):
    def __init__(self, xlabel: str, ylabel:str) -> None:
        self.param_dict = {}
        self.param_dict['returnfig'] = True
        self.param_dict['type'] = 'candle'
        self.param_dict['figure'] = (12, 4)
        self.param_dict['xlabel'] = 'X'
        self.param_dict['title'] = 'STOCK'
        self.param_dict['datetime_format'] = TIME_FMT
        self.param_dict['ylabel'] = 'Y'
        buf = io.BytesIO()
        self.param_dict['savefig'] = {'fname':buf}

    def plot(self, title: str, dfs, labels):
        """
        return a image buffer in memery.
        """
        buf = io.BytesIO()
        self.param_dict['title'] = title
        plt.figure(self.param_dict['figure'], dpi=72)
        plt.xlabel(self.param_dict['xlabel'])
        plt.title(title)
        plt.ylabel(self.param_dict['ylabel'])
        for i in range(len(dfs)):
            plt.plot(dfs[i], label=labels[i])
        plt.savefig(fname=buf)
        return buf

class Plot(object):
    def __init__(self, img_path: str) -> None:
        self.image_path = img_path

    def candle_plot_config(self, title='', plot_type='') -> dict:
        param_dict = {}
        if plot_type == "candle_plot":
            usr_color = mpf.make_marketcolors(up='red', down='green', edge='i', wick='i', volume='in')
            usr_style = mpf.make_mpf_style(marketcolors=usr_color)
            param_dict['returnfig'] = True
            param_dict['type'] = 'candle'
            param_dict['mav'] = (5, 10, 20)
            param_dict['volume'] = True
            param_dict['title'] = title
            param_dict['style'] = usr_style
            param_dict['datetime_format'] = TIME_FMT
            param_dict['figscale'] = 1.0
        return param_dict

    def plot_config(self, title='', plot_type='') -> plt:
        current_date = datetime.date.today().strftime(TIME_FMT)
        plt.figure(figsize=(12, 4), dpi=72)
        plt.xlabel("Date")
        if plot_type == 'shibor':    
            plt.title(f"View of Shibor on {current_date}")
            plt.ylabel("Rate in %")
        elif plot_type == 'treasury':
            plt.title(f"View of Treasury Yield on {current_date}")
            plt.ylabel("Yield in %")
        return plt

    def mpl_plot(self, df: DataFrame, param: dict):
        mpf.plot(df, **param)
        plt.show()

    def plot(self, df: DataFrame, param: dict, plot_type=''):
        plt = self.plot_config(plot_type=plot_type)
        if plot_type == 'shibor':
            plt.plot(df, label="7 days shibor")
            image_name = "shibor.png"
        elif plot_type == 'treasury':
            plt.plot(df['China'], label="China")
            plt.plot(df['US'], label="US")
            image_name = "treasury_yield.png"
        imgfile = os.path.join(self.image_path, image_name)
        plt.legend()
        plt.savefig(imgfile, format='png')


d = StockData(REMOTE_HEADER)
# df = d.condition_select('SH600000', 'close_price,open_price,high_price,low_price', "trade_date between '1999-12-19' and '2022-06-30'")
df = d.get_stock_data('SH600000', length=500)
df.ffill(inplace=True)
# print(df.head(5))
#p = Plot('/home/fred/Documents/dev/Phoenix/Phoenix/view')
#param = p.candle_plot_config('SH600000', 'candle_plot')
#p.mpl_plot(df, param)
p = kPlot()
buf = p.plot('SH600000', df)
img = Image.open(buf)
img.save('/home/fred/Documents/dev/Phoenix/Phoenix/view/SH600000.png')