#coding:utf-8
import logging
from multiprocessing.pool import ThreadPool
import signal
import socket

from handler import RequestHandler, HandlerFactory
try:
    from tcpyconfig import NUM_THREADS
except:
    from default import NUM_THREADS
try:
    from tcpyconfig import DEBUG
except:
    from default import DEBUG
from default import SERVER_DEFAULT, PORT_DEFAULT


logging.basicConfig()
logger = logging.getLogger("multitcp.TCPServer")
if DEBUG:
    logger.setLevel(logging.DEBUG)


class TCPServer(object):
    def __init__(self, host=None, port=None, **kwargs):
        self.host = host if host else SERVER_DEFAULT
        self.port = port if port else PORT_DEFAULT
        self.commands = kwargs.get("commands", {})
        threads = kwargs.get("threads", NUM_THREADS)
        self.request_queue = ThreadPool(threads)
        self.socket = None
        self.make_conn()
        self.start_signal_handler()

    def make_conn(self):
        """
        打开socket，绑定ip port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.listen(5)

    def signal_handler(self, signal, frame):
        self.request_queue.join()
        self.socket.close()

    def start_signal_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)

    def listen(self):
        print "TCPServer is listening at %s:%d!" % (self.host, self.port)
        hf = HandlerFactory(self.commands)
        while True:
            logging.debug("TCPServer accepting requests.")
            client_sock, client_addr = self.socket.accept()
            client_host, client_port = client_addr
            logging.debug("TCPServer handling request from %s:%s." % (client_host, client_port))
            handler = RequestHandler(hf,
                                     client_host,
                                     client_port,
                                     client_sock)
            self.request_queue.apply(handler.handle, ())
        self.socket.close()
