import os
import threading

def open_notepad():
    os.system("notepad")

l = [None] * 5 

for n in range(4):
    l[n] = threading.Thread(target=open_notepad, name="note" + str(n))
    l[n].start()
