from multitcp import TCPClient
import threading   

def go():
    print TCPClient().execute(cmd="hello_world",info='aini')
for i in range(10):
    t = threading.Thread(target=go)
    t.start()
