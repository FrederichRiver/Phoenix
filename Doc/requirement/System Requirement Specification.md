# System Specification

[TOC]

<div STYLE="page-break-after: always;"></div>

## System module



## Strategy module

### SRS_Strategy_001

|SRS_Strategy_001||
|--|:-|
|Description|django_report模块基于Django3实现。它包含3个接口：<br>1. 通过读取模板template_Report_001来实现策略的展示，该模板是一个html模板。<br>2. 读取图像的IO接口。<br>3. 策略的其它信息，通过json传递。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material|SRS_Strategy_00101,SRS_Strategy_00102,SRS_Strategy_00103|

### SRS_Strategy_00101

|SRS_Strategy_00101||
|--|:-|
|Description|定义了SRS_Strategy_001中的模板，通过template_report_001实现。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material|template_Report_001|

### SRS_Strategy_00102

|SRS_Strategy_00102||
|--|:-|
|Description|描述SRS_Strategy_001中关于图像IO的要求。该接口以list方式实现。既可以接受基于base64的图像IO对象，也可以接受静态地址，或是上述的混合。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_00103

|SRS_Strategy_00103||
|--|:-|
|Description|描述SRS_Strategy_001中关于报告参数的要求，通过json传递。包括：报告类型、图片数量、关键参数描述(根据不同报告具有不同的参数)|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_002

|SRS_Strategy_002||
|--|:-|
|Description|规范image_engine具有根据需求输出图片的功能。可以设定输出到指定的url，或者输出为一个IO流。它具有3个接口：<br>1. 输出到的url<br>2.生成图片的内部模板参数<br>3. 图片所必须的数据，以json格式传入。 |
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_00201

|SRS_Strategy_00201||
|--|:-|
|Description|非关键需求。在图片中增加水印|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_003

|SRS_Strategy_003||
|--|:-|
|Description|针对账户的结算功能模块settle center的需求。根据给定的账户名称，读取历史净值数据，输出净值曲线数据和结算结果。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material|SRS_Strategy_003001|

### SRS_Strategy_003001

|SRS_Strategy_003001||
|--|:-|
|Description|对SRS_Strategy_003中净值结算的详细描述：<br>1. 收益率profit;<br>2. 年化收益率annualized return;<br>3. 最大回撤max draw;<br>4. sharpe ratio;<br>5. sotino ratio;<br>6. alpha系数;<br>7. beta系数<br>每一个数据分解为一个函数实现|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_003002

|SRS_Strategy_003002||
|--|:-|
|Description|每一个settle都要有hash及属性，对于已经存在的settle，直接从本地读取。不存在的settle再从datahub中获取。settle通过redis进行管理。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_003003

|SRS_Strategy_003003||
|--|:-|
|Description|每次settle请求保存在redis数据库中1d的时间。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_003004

|SRS_Strategy_003004||
|--|:-|
|Description|对于settle保存的数据结构进行定义。TBD|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_004

|SRS_Strategy_004||
|--|:-|
|Description|order center从strategy engine接收买卖指令，并向risk manager发送请求。risk manager返回仓位建议。order center根据risk manager给出的仓位建议p%，对acc进行操作，核算所产生的下单量，并根据当前价格生成订单。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_005

|SRS_Strategy_005||
|--|:-|
|Description|risk manager是一个复杂系统，能根据市场环境给出仓位建议，包括总仓位建议和标的仓位建议。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_005001

|SRS_Strategy_005001||
|--|:-|
|Description|最简单的风险管理策略为定额仓位管理，即特定仓位比例。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_005002

|SRS_Strategy_005002||
|--|:-|
|Description|每个账户在risk manager里注册后，使用特定的仓位策略，以及其参数。除非通过特定的流程修改，该账户将一直使用这个仓位策略。|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_006

|SRS_Strategy_006||
|--|:-|
|Description|strategy engine，关于strategy的基本需求：它是一个独立运行的app进程，通过接收cmd来反馈策略信号，并且可以自由组合各种策略。其它TBD|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_006001

|SRS_Strategy_006001||
|--|:-|
|Description|关于strategy的基本需求：它是一个独立运行的app进程，通过接收cmd来反馈策略信号，并且可以自由组合各种策略。其它TBD|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

### SRS_Strategy_006011

|SRS_Strategy_006011||
|--|:-|
|Description|strategy engine的第一个策略，即根据K线形态来判断买入点和卖出点|
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||

## template table

|||
|--|:-|
|Description||
|Rationale||
|Use Case||
|Dependencies||
|Supporting Material||
