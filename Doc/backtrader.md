# Backtrader笔记

[TOC]

## 待整理内容

## 模块说明

### calendar模块

定义了两个自定义数据结构_localized_day和_localized_month
日期的一些基本运算,如闰年判断，月份有多少天，某月的第一天是星期几以及该月有多少天，上一个月和下一个月
主要的模块，日历模块，字符型日历，html型日历
时区local功能，进入和离开时区并返回上一个时区
进一步衍生出带时区的日历
Calendar类的功能
初始化定义不同地区的firstweekday，有以monday开始的，有以sunday开始的。
iterweekdays用yield方法迭代每周7天
itermonthdays一共有4个方法，分别用来返回不同的迭代结果。其作用类似于生成一个日历结构，第一周从上个月接过来，并且最后一周包含下个月的几天
month2calendar生成仅含月份的日历
monthday2calendar则生成含日期的日历
还有按年度日期生成365日的日历的
Calendar只是生成一种日历的数据结构。

Text和Html则在Calendar基础上衍生出不同显示格式的日历，相当与可视化。

timegm将时间转换为秒用于某些计算

### 基类定义

MetaBase是一个基于Type的基类，定义了donew,doprenew等方法以及一个入口__call__
AutoInfoClass类
MetaParams基于MetaBase重新定义，并重载了donew方法
在MetaParams的new方法中,将基类与新类的'params'和'fparams'参数全都拼接起来，用于后面的派生类使用。生成一个cls.params对象，这个对象是一个AutoInfoClass，并调用了一次derive方法，将基类的cls转换为派生类的newcls。整体上是一种基础方法。

### timeseries模块

TimeFrame类，支持多种tick，从ms到y，这是一个基类，定义了返回tfname=tick类型的方法
DataSeries类基于LineSeries,其中最重要的getwritervalue根据前面的索引，按行逐个遍历列值后输出。
_Bar类定义了K线图上的bar

### Line

LineRoot 派生出LineSingle和LineMultiple
LineMultiple派生出MetaLineSeries,再派生LineSeries,最后派生出LineSeriesStub

### analyzer模块

通过类派生的方法定义了一个Analyzer和一个TimeSeriesAnalyzer

### comminfo模块

最后以CommInfo的方式输出交易费

### broker模块

broker定义了交易者，有以下接口
set_commoninfo,设定费率
get_value
get_cash
get_fundshare
get_fundvalue
get_position
submit
buy
sell
cancel

### position模块

仓位管理，通过设定仓位水平对持仓进行管理，包括set和update两个主要的接口

### 核心Strategy模块

通过lines保存策略数据
qbuffer用于内存管理
通过一系列notify_xxx方法来接收信息
strategy与broker绑定，通过操作broker直接下单，这种架构对broker的解耦不够彻底
定义了一系列交易方法
定义了一些方法来获取仓位信息

### Obeserver模块

Obeserver是一个监控模块，负责记录交易信息，然后实现绘图，与我之前的定义类似
