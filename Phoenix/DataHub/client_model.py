#!/usr/bin/python3
import socket
import time
import pickle
from libbasemodel.message_model import MsgFrame

HOST = '127.0.0.1'    # The remote host
PORT = 9000              # The same port as used by the server



class Client(object):
    """
    此类早期开发用，待成熟后取消。
    """
    def __init__(self, host, port) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 补充对host和port的格式转换
        self.client.connect((host, port))
        self.FLAG = 1

    def send(self, msg):
        self.client.send(msg)
        data = self.client.recv(102400)
        result = pickle.loads(data)
        return result

    def close(self):
        self.client.close()
        self.FLAG = 0

    def request(self):
        req = MsgFrame('test', p1=5, p2=10)
        return pickle.dumps(req)

class DataHubDecorator(object):
    def __init__(self, host, port) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 补充对host和port的格式转换
        self.client.connect((host, port))

    def __call__(self, func):
        def wapper(msg):
            self.client.send(msg)
            data = self.client.recv(102400)
            result = pickle.loads(data)
            func(result)
        return wapper

    def __close__(self):
        self.client.close()



req = MsgFrame('test', p1=5, p2=10)
req = MsgFrame('stock_list', start_date='2020-01-01', end_date='2022-07-09')
msg = pickle.dumps(req)


@DataHubDecorator(HOST, PORT)
def test_print(data):
    print(data)

test_print(msg)
