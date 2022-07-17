#!/usr/bin/python3
from .order import TradeOrder


class FeeBase(object):
    """
    费用类
    """
    def __init__(self, ratio: float) -> None:
        self.ratio = ratio


class CommissionBase(FeeBase):
    def __init__(self) -> None:
        super().__init__(0.0003)


class StockCommission(CommissionBase):
    """
    佣金：0.0003或5元
    """
    def __call__(self, vol: float) -> float:
        return max(round(abs(vol * self.ratio), 2), 5.0)


class TransferFee(FeeBase):
    """
    过户费：0.00002
    """
    def __init__(self) -> None:
        super().__init__(0.00002)

    def __call__(self, vol: float) -> float:
        return abs(round(vol * self.ratio, 2))


class StampTax(FeeBase):
    """
    印花税：0.001
    """
    def __init__(self) -> None:
        super().__init__(0.001)

    def __call__(self, vol: float):
        return abs(round(vol * self.ratio, 2))


class AssetBase(object):
    def __init__(self, stock_code: str, cash=0.0) -> None:
        self.stock_code = stock_code
        self.unit = 'CNY'
        self._price = 0.0
        self._volume = 0.0

    @property
    def value(self) -> float:
        return self.price * self._volume

    @property
    def price(self) -> float:
        return self._price

    def update(self, price: float):
        self._price = price

    def long(self, price: float, vol: int):
        self._volume += vol
        self.update(price)

    def short(self, price: float, vol: int):
        self._volume -= vol
        self.update(price)

class StockAsset(AssetBase):
    pass

class FutureAsset(AssetBase):
    pass

class OptionAsset(AssetBase):
    pass

class FundAsset(AssetBase):
    pass

class ETFAsset(AssetBase):
    pass


def buy(asset: AssetBase, price: float, vol: int):
    """
    return: [0]总成本, [1]直接成本, [2]余额, [3]税费, [4]过户费, [5]交易费
    """
    asset.vol += vol
    # 印花税
    t = 0.0
    # 过户费
    f1 = 0.0
    # 交易费
    f2 = 0.0
    cost = price * vol
    cost2 = cost + t + f1 + f2
    asset.long(price, vol)
    # 总成本, 直接成本, 余额, 税费, 过户费, 交易费 
    return cost2, cost, 0.0, t, f1, f2


def sell(asset: AssetBase, price: float, vol: int):
    """
    return: [0]总成本, [1]直接成本, [2]余额, [3]税费, [4]过户费, [5]交易费
    """
    asset.vol -= vol
    # 印花税
    t = 0.0
    # 过户费
    f1 = 0.0
    # 交易费
    f2 = 0.0
    cost = price * vol
    cost2 = cost + t + f1 + f2
    asset.short(price, vol)
    # 总成本, 直接成本, 余额, 税费, 过户费, 交易费 
    return cost2, cost, 0.0, t, f1, f2

def settle(asset: AssetBase, price: float, vol: int):
    """
    return: [0]总成本, [1]直接成本, [2]余额, [3]税费, [4]过户费, [5]交易费
    """
    
    # 印花税
    t = 0.0
    # 过户费
    f1 = 0.0
    # 交易费
    f2 = 0.0
    cost = price * vol
    cost2 = cost + t + f1 + f2
    asset.short(price, asset.vol)
    # 总成本, 直接成本, 余额, 税费, 过户费, 交易费 
    return cost2, cost, 0.0, t, f1, f2

def xrdr(asset: AssetBase, x1, x2, x3):
    # 总成本, 直接成本, 余额, 税费, 过户费, 交易费 
    return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0




