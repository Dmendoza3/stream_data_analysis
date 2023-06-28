import os
import time
import threading, queue
from live_stream_status import get_current_status
from chat_capture_all_args_function import download_chat

def external_chat_capture(parent_folder, video_name, video_id):
    os.system(f"python chat_capture_all_args_function.py {parent_folder} \"{video_name}\" {video_id} -auto")

def worker(name):
    print("w", name, "init...")
    worker_status[name] = "idle"
    while True:
        item, video_element = q.get()
        worker_status[name] = "working"
        ####

        parent_folder, video_name, video_id = item

        worker_status[name] = "downloading " + video_name[0:20] + "..."#video_id
        external_chat_capture(parent_folder, video_name, video_id)
        #download_chat(parent_folder, video_name, video_id, overwrite=False,persistent=False, echo=False, fix_filename=True)

        active_video_list.remove(video_element)
        ###
        worker_status[name] = "idle"
        q.task_done()
    worker_status[name] = "dead"


alive = True
active_video_list = set()
q = queue.Queue()
worker_amount = 10
worker_status = ["idle"] * worker_amount
parent_folder = "chat_archive"

check_counter = 1
cap_wait_time = 20

# thread_list = []
for w in range(worker_amount):
    threading.Thread(target=worker, daemon=True, args=(w,)).start()

try:
    while alive:
        print("checking current status...", end="")

        try:
            ongoing_streams = get_current_status(False)
            video_id = ""
            new_found = len(ongoing_streams - active_video_list)
            print("\b\b\b new found:", len(ongoing_streams - active_video_list))
            if new_found == 0 and check_counter <= cap_wait_time:
                check_counter += 1
            
            if new_found != 0:
                check_counter = 0

            for t in ongoing_streams:
                channel_name, channel_id, video_id, video_name = t
                if t not in active_video_list:
                    q.put(([parent_folder + "/" + channel_name, video_name, video_id], t))
                    active_video_list.add(t)
                #print(list(q.queue))
        except ConnectionError:
            print("error en la conexion")
        
        wait_time = 15 * check_counter
        while wait_time:
            print("checking again in ", wait_time, " " * 10, end="\r") 
            wait_time -= 1
            if wait_time % 15 == 0:
                print(*[(i,w) for i, w in enumerate(worker_status)], sep="\n")

            time.sleep(1)
except KeyboardInterrupt:
    alive = False

q.join()

print("Finished")