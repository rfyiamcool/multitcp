from multitcp import TCPServer, TCPHandler
import time


class HelloWorldHandler(TCPHandler):
    def __init__(self, cmd=None, info=None):
        self.info = info
    def execute(self):
        print self.info
        time.sleep(5)
        return self.success(message=self.info)

if __name__ == "__main__":
    server = TCPServer()
    server.commands = {
        'hello_world': HelloWorldHandler
    }
    server.listen()
