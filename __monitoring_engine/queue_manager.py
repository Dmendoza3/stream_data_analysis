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

        worker_status[name] = "downloading " + video_name[0:20] + "... " + video_id
        try:
            external_chat_capture(parent_folder, video_name, video_id)
        finally:
            check_counter[0] = 0
            print("error on w", name)    
        #download_chat(parent_folder, video_name, video_id, overwrite=False,persistent=False, echo=False, fix_filename=True)

        active_video_list.remove(video_element)
        print("removed:", video_element, " current active:", len(active_video_list))
        ###
        worker_status[name] = "idle"
        q.task_done()
    worker_status[name] = "dead"

def config_control():
    print("config init...")
    config_prev_mod_time = os.path.getmtime("config.dat")
    watch_list_prev_mod_time = os.path.getmtime("data/watch_list.dat")
    permanent_watch_list_prev_mod_time = os.path.getmtime("data/permanent_video_watch_list.dat")

    while True:
        new_config_mod_time = os.path.getmtime("config.dat")
        new_watch_list_prev_mod_time = os.path.getmtime("data/watch_list.dat")
        new_permanent_watch_list_prev_mod_time = os.path.getmtime("data/permanent_video_watch_list.dat")
        if new_config_mod_time != config_prev_mod_time:
            config_prev_mod_time = new_config_mod_time
            in_f = open("config.dat", "r")
            n_config = {}
            for line in in_f:
                name, value = line.split("=")
                config[name] = value
            config = n_config
            in_f.close()
        
        if new_watch_list_prev_mod_time != watch_list_prev_mod_time:
            check_counter[0] = 0

        if new_permanent_watch_list_prev_mod_time != permanent_watch_list_prev_mod_time:
            check_counter[0] = 0

        time.sleep(15)


config = {}
in_f = open("config.dat", "r")
for line in in_f:
    name, value = line.split("=")
    config[name] = value

in_f.close()

server_mode = int(config["server"]) == 1
alive = True
active_video_list = set()
q = queue.Queue()
worker_amount = 15
worker_status = ["idle"] * worker_amount
parent_folder = config["archive_location"]

prev_status = ""

check_counter = [1]
check_again = [False]
cap_wait_time = 20

thread_list = []
for w in range(worker_amount):
    thread_list.append(threading.Thread(target=worker, daemon=True, args=(w,)))
    thread_list[-1].start()

#master thread
config_thread = threading.Thread(target=config_control, daemon=True)
config_thread.start()

try:
    while alive:
        print("checking current status...", end="\r")

        try:
            ongoing_streams = get_current_status(True)
            video_id = ""
            new_found = len(ongoing_streams - active_video_list)
            print("new found:", len(ongoing_streams - active_video_list), " "*22, end="\r")
            if new_found == 0 and check_counter[0] <= cap_wait_time:
                check_counter[0] += 1
            
            if new_found != 0:
                check_counter[0] = 0

            for t in ongoing_streams:
                channel_name, channel_id, video_id, video_name = t
                if t not in active_video_list:
                    q.put(([parent_folder + "/" + channel_name, video_name, video_id], t))
                    active_video_list.add(t)
                #print(list(q.queue))
        except Exception as e:
            print("error en la conexion", e)
        
        wait_time = 15 * check_counter[0]
        if server_mode:
            print("checking again in ", wait_time, " " * 10, end="\r")
        while wait_time:
            if not server_mode:
                print("checking again in ", wait_time, " " * 10, end="\r")
            wait_time -= 1
            if wait_time % 15 == 0:
                new_status = [(i, w) for i, w in enumerate(worker_status)]
                if str(new_status) != prev_status:
                    print("_"*22, *new_status, sep="\n")
                    prev_status = str(new_status)

            if check_counter[0] == 0:
                break
            
            time.sleep(1)
except KeyboardInterrupt:
    alive = False

q.join()

print("Finished")