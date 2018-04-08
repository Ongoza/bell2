import threading
import time

theVar = 0
threads = []


class MyThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, n, ip):
        print("start " + ip)
        self.n = n
        self.ip = ip
        threading.Thread.__init__(self)

    def kill(self):
        print('kill:', self.ip)
        self.killed = True


for x in range(5):
    threads.append(MyThread("task1", str(x)).start())
    for t in threading.enumerate():
        print("name=", t.getName())


size = len(threads) - 1
for x in range(size, -1, -1):
    print("x=", x)
    if(threads[x]):
        threads[x].join()
        del threads[x]
    else:
        del threads[x]
print("sum=", len(threads))
