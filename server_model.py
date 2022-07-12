#!/usr/bin/python3
import socket
import threading
import pickle
from libbasemodel.stock_manager import StockBase
from libmysql_utils.header import REMOTE_HEADER
from .server_utils import MsgFrame


class Server(socket.socket):
    def __init__(self, HOST, PORT) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((HOST, PORT))
        self.listen(5)
        self.pool = []


    def add_connection(self, client: threading.Thread) -> bool:
        # 创建一个线程，用于专门处理连接请求。
        try:
            self.pool.append(client)
            client.start()
            status = True
        except Exception:
            status = False
        return status

    def remove_connection(self, client: threading.Thread):
        # 从进程池当中去除一个连接。
        self.pool.remove(client)

    def run(self):
        while True:
            conn, addr = s.accept()
            c = SocketConnection(client= conn)
            self.add_connection(c)


class SocketConnection(threading.Thread):
    Buffer_size = 102400
    def __init__(self, client: socket.socket) -> None:
        super().__init__()
        self.client = client
        self.setDaemon(True)
    
    def run(self):
        while self.client:
            data = self.client.recv(self.Buffer_size)
            if data:
                msg = pickle.loads(data)
                data = self.request_solve(msg)
                self.client.send(data)
        self.client.close()

    def request_solve(self, req: MsgFrame):
        datahub = StockBase(REMOTE_HEADER)
        data = datahub.engine.execute(req.sql).fetchall()
        result = pickle.dumps(data)
        return result

