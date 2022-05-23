import keyboard
import threading
import time


def print_time( threadName, delay):
   count = 0
   while count < 50:
      count += 1
      print ("%s: %s" % (count, time.ctime(time.time())))
      time.sleep(delay)


t = threading.Thread(target=print_time, args=("THREAD", 3.5, ))
t.start()

keyboard.add_hotkey('ctrl+s', t.stop)