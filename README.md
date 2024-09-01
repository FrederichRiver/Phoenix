# Phoenix

Phoenix is a personal quantitive trading system.

[TOC]

## Environment

### Docker

Create data volume to separate data from container.

```bash
docker volume create data_volume
```

挂载数据卷

```bash
docker run -it -v data_volume:/data ubuntu
```

## Installation

TBD

## Report Module

Report module is a web application to show the result of backtest.
It is base on Django3.

### Strategy Report

Strategy report is a report for a strategy.
It contains the following information:

1. Strategy name
2. Net value chart
3. beta, alpha, sharpe ratio, max drawdown, max drawdown duration
