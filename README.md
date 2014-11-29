
###一个tcp的简单封装，这个是我们开发的分布式调度系统的通信组件，因为有更高性能的gevent的支持，所以这个组件算是废掉了， 现在算是开源了，基本是可以用的，开发的一些模式还是有点意思的，有兴趣的朋友可以看看

###This is client
```
from multitcp import TCPClient
import threading

def go():
    print TCPClient().execute(cmd="hello_world",info='aini')
for i in range(10):
    t = threading.Thread(target=go)
    t.start()
```


###THis is server
```
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

```
