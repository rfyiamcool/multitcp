#coding:utf-8
import logging

from connection import ServerConnection


logging.basicConfig()
logger = logging.getLogger(__name__)


class TCPHandler(object):

    def __init__(self, **kwargs):
        self.conn = None

    def send(self, data):
        self.conn.send(data)

    def recv(self):
        return self.conn.read()

    def execute(self):
        raise NotImplementedError()

    def success(self, **kwargs):
        res = {
            'success': True,
        }
        res.update(kwargs)
        return res

    def error(self, message, **kwargs):
        res = {
            'error': True,
            'message': message
        }
        res.update(kwargs)
        return res


class HandlerFactory(object):
    def __init__(self, commands):
        self.commands = commands

    def make_handler(self, cmd=None, **kwargs):
        if not cmd or cmd not in self.commands:
            raise Exception("Invalid command %s!" % cmd)
        print 22
        print kwargs

        return self.commands.get(cmd)(**kwargs)


class RequestHandler(object):
    def __init__(self, factory, host, port, sock):
        self.factory = factory
        self.conn = ServerConnection(sock)

    def handle(self):
        try:
            data = self.conn.read()
            print data
            handler = self.factory.make_handler(**data)
            handler.conn = self.conn
            res = handler.execute()
        except Exception as e:
            logger.error(e.message)
            res = {"error": True, "message": e.message}
        self.conn.send(res)
