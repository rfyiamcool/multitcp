#coding:utf-8
from connection import ClientConnection
try:
    from tcpyconfig import REQUEST_TIMEOUT
except:
    from default import REQUEST_TIMEOUT
from default import SERVER_DEFAULT, PORT_DEFAULT
from util import to_int


class TCPClient(object):

    def __init__(self, host=SERVER_DEFAULT, port=PORT_DEFAULT):
        self.host = host
        self.port = to_int(port)
        self._conn = ClientConnection(self.host, self.port, timeout=REQUEST_TIMEOUT)

    def connect(self):
        self._conn._connect()

    def send(self, data):
        self._conn.send(data)

    def recv(self):
        return self._conn.read()

    def disconnect(self):
        self._conn._disconnect()

    def execute(self, cmd, **params):
        params['cmd'] = cmd
        self.connect()
        self.send(params)
        res = self.recv()
        self.disconnect()
        return res
