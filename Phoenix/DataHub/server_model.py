#!/usr/bin/python3
import socket
import threading
import pickle
from libbasemodel.message_model import MsgFrame
from librestapi.service_api import test, stock_list


class DataHub(object):
    """
    DataHub is a RESTFUL server used for querying data and basic dealing. 
    """
    def __init__(self):
        # AF_INET is standard socket protcol.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 9000))
        self.server.listen(5)
        self.pool = []

    def add_connection(self, client: threading.Thread):
        self.pool.append(client)
        client.start()

    def remove_connection(self, conn):
        # 暂时无用途
        self.pool.remove(conn)

    def run(self):
        """
        Start to listen from ports and manage querying thread.
        """
        while True:
            conn, addr = s.server.accept()
            t = SocketConnection(client= conn)
            t.start()


class SocketConnection(threading.Thread):
    """
    """
    Buffer_size = 102400
    def __init__(self, client: socket.socket) -> None:
        super().__init__()
        self.client = client
        self.setDaemon(True)
    
    def run(self):
        data = self.client.recv(self.Buffer_size)
        if data:
            msg = pickle.loads(data)
            data = self.request_solve(msg)
            self.client.send(data)
        self.client.close()

    def request_solve(self, req: MsgFrame):
        func = eval(req.msg_type)
        result = func(req.param)
        return result

s = DataHub()
s.run()
