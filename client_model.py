#!/usr/bin/python3
import socket
import time
import pickle

Server_setting = {"HOST": '127.0.0.1', "PORT": 9000}


class MsgFrame(object):
    def __init__(self, stock_code: str, start: str, end: str) -> None:
        self.stock_code = stock_code
        self.start_time = start
        self.end_time = end

    def __str__(self):
        return f"SELECT close_price from {self.stock_code} WHERE trade_date BETWEEN '{self.start_time}' and '{self.end_time}'"

    @property
    def sql(self):
        return self.__str__()

class Client(socket.socket):
    def __init__(self, HOST, PORT) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((HOST, PORT))
        self.FLAG = 1

    def send_msg(self, msg):
        self.send(msg)
        data = self.recv(102400)
        result = pickle.loads(data)
        return result

    def request(self):
        import json
        req = MsgFrame('SH600000', '2019-01-01', '2020-12-31')
        return pickle.dumps(req)

client = Client(**Server_setting)
for i in range(3):
    data = client.send_msg(client.request())
    print(data)
client.close()