#!/usr/bin/python3
# Filename: risk_manager.py

# 定义风控模型，接受上游订单，并产生订单给下游交易模块


from abc import ABCMeta, abstractmethod
import pickle
from hmmlearn.hmm import GaussianHMM

class AbstractRiskManager(metaclass=ABCMeta):
    """
    Risk Manager 基类
    """
    @abstractmethod
    def treat(self, *argv):
        raise(NotImplementedError())

    def save(self, mod_path: str):
        with open(mod_path, 'wb') as f:
            pickle.dump(self, f)

    def load(self, mod_path: str):
        with open(mod_path, 'rb') as f:
            pickle.load(f)
    

class HMMRiskManager(AbstractRiskManager):
    """
    基于HMM方法的Risk Manager.
    """
    def __init__(self, name: str, state=2) -> None:
        super().__init__()
        self._name = name if name else 'HMM_RM'
        self.hmm = GaussianHMM(
            n_components=state, covariance_type="full", n_iter=1000
            )
        self.TRAINED = False

    def train(self, data):
        self.hmm.fit(data)
        self.TRAINED = True

    def treat(self, x):
        regime = self.hmm.predict(x)
        return regime
