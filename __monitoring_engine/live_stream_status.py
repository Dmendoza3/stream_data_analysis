from get_current_live_stream import get_current_live_stream
import time
import threading, queue

status_dir = "status"
data_dir = "data"
q = queue.Queue()

def worker(id, ret_list):
    while True:
        item = q.get()
        ret_list.append(get_current_live_stream(item))
        q.task_done()

def get_current_status(ignore_free_chat=True):
    in_f = open(f"{data_dir}/watch_list.txt", "r")
    in_permanent_f = open(f"{data_dir}/permanent_video_watch_list.txt", "r", encoding="utf-8")
    watch_list = [tuple(line.split(",")) for line in in_f.read().split("\n")]
    permanent_video_watch_list = [tuple(line.split(",")) for line in in_permanent_f.read().split("\n")]
    
    freechat_list = []
    if ignore_free_chat:
        in_f_freechat = open(f"{data_dir}/free_chat_list.txt", "r", encoding="utf-8")

        for line in in_f_freechat:
            name, channel_id, video_id, *title = line.split(",")
            freechat_list.append(video_id)

    timestamp = int(time.time())
    out_filename = f"{status_dir}/status.{timestamp}.txt"
    out_f = open(out_filename, "w", encoding="utf-8")

    status = set()
    for channel_id, name in watch_list:
        name = name.strip()
        video_id, video_url, title, description, keywords, scheduled_start_time = get_current_live_stream(channel_id)
        #print("loading", name, "current stream data...")
        #print(name, channel_id, video_id, scheduled_start_time, title, sep=",")
        if video_id != "-1" and video_id not in freechat_list:
            status.add((name, channel_id, video_id, title))
            print(name, channel_id, video_id, scheduled_start_time, f'"{keywords}"', f'"{title}"', sep=",", file=out_f)

    #add permanent watched videos
    for name, channel_id, video_id, title in permanent_video_watch_list:
        status.add((name, channel_id, video_id, title))

    return status

def get_current_status_threaded(ignore_free_chat=True, threads=10):
    in_f = open(f"{data_dir}/watch_list.txt", "r")
    watch_list = [tuple(line.split(",")) for line in in_f.read().split("\n")]
    
    freechat_list = []
    if ignore_free_chat:
        in_f_freechat = open(f"{data_dir}/free_chat_list.txt", "r", encoding="utf-8")

        for line in in_f_freechat:
            name, channel_id, video_id, *title = line.split(",")
            freechat_list.append(video_id)

    timestamp = int(time.time())
    out_filename = f"{status_dir}/status.{timestamp}.txt"
    out_f = open(out_filename, "w", encoding="utf-8")

    status = set()
    ret_list = [None] * threads
    t_list = []
    for t in range(threads):
        t_list.append(threading.Thread(target=worker, daemon=True, args=(t,ret_list,)))
        t_list[-1].start()

    for channel_id, name in watch_list:
        name = name.strip()
        q.put(channel_id)
        q.join()
        # for t in t_list:
        #     t.stop()
        #print("loading", name, "current stream data...")
        #print(name, channel_id, video_id, scheduled_start_time, title, sep=",")

    for video_id, video_url, title, description, keywords, scheduled_start_time in ret_list:
        if video_id != "-1" and video_id not in freechat_list:
            status.add((name, channel_id, video_id, title))
            print(name, channel_id, video_id, scheduled_start_time, f'"{keywords}"', f'"{title}"', sep=",", file=out_f)

    return status

if __name__ == "__main__":
    print(get_current_status_threaded(False))