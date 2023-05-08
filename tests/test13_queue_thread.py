import logging
import threading, queue
import time

q = queue.Queue()

def worker(name):
    while True:
        item = q.get()
        print(name, "is working", end="")
        wait_print(item[0], item[1])

        q.task_done()
        print(name, "finished")

def wait_print(msg,secs):
    time.sleep(secs)
    print(msg, flush=True, end="")


l_args = [6,7,9,5,1,2,8,4,3,1,2,8,4,7,9,5,4,3,1,2,8,4,7,]

l_threads = []

threading.Thread(target=worker, args=["w_1"],daemon=True).start()
threading.Thread(target=worker, args=["w_2"], daemon=True).start()
threading.Thread(target=worker, args=["w_3"], daemon=True).start()

for arg in l_args:
    args = (arg, arg)
    q.put(args)

q.join()

print("finish")