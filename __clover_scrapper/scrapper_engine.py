import os
import time
import threading, queue
from palanq_search_scrapper import find_links_until

def config_control():
    print("config init...")
    while True:
        new_config_mod_time = os.path.getmtime("config.dat")
        #new_watch_list_prev_mod_time = os.path.getmtime("data/watch_list.dat")
        #new_permanent_watch_list_prev_mod_time = os.path.getmtime("data/permanent_video_watch_list.dat")
        if new_config_mod_time != config_prev_mod_time:
            config_prev_mod_time = new_config_mod_time
            in_f = open("config.dat", "r")
            n_config = {}
            for line in in_f:
                name, value = line.split("=")

                value_split = value.split(",")
                if len(value_split) > 1:
                    value = value_split

                config[name] = value
            in_f.close()
            config = n_config
            os.makedirs(config["save_location"], exist_ok=True)
        
        # if new_watch_list_prev_mod_time != watch_list_prev_mod_time:
        #     check_counter[0] = 0

        # if new_permanent_watch_list_prev_mod_time != permanent_watch_list_prev_mod_time:
        #     check_counter[0] = 0

        time.sleep(15)

##LOAD CONFIG
in_f = open("config.dat", "r")
config = {}
for line in in_f:
    name, value = line.split("=")

    value_split = value.split(",")
    if len(value_split) > 1:
        value = value_split

    config[name] = value
in_f.close()

os.makedirs(config["save_location"], exist_ok=True)

alive = True

check_counter = [1]
cap_wait_time = 20

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
        except Exception:
            print("error en la conexion")
        
        wait_time = 15 * check_counter[0]
        while wait_time:
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

print("Finished")