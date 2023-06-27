import os
import time
import threading, queue
from live_stream_status import get_current_status

def worker(name):
    print("w", name, "init...")
    while True:
        item = q.get()
        print("w", name, "started task...")
        ####

        print("w", w, ":", item)
        time.sleep(5)

        active_video_list.remove(item)
        ###
        print("w", name, "finished task...")
        q.task_done()


alive = True
active_video_list = set()
q = queue.Queue()
worker_amount = 10

# thread_list = []
for w in range(worker_amount):
    threading.Thread(target=worker, daemon=True, args=(w,)).start()

try:
    while alive:
        print("checking current status...")

        ongoing_streams = get_current_status(False)
        video_id = ""
        print("found:", len(ongoing_streams - active_video_list))

        for t in ongoing_streams:
            channel_video, channel_id, video_id, video_name = t
            if t not in active_video_list:
                q.put(t)
                active_video_list.add(t)

        time.sleep(15)
except KeyboardInterrupt:
    alive = False

q.join()

print("Finished")