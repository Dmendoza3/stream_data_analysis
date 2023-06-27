from get_current_live_stream import get_current_live_stream
import time

watch_list = []

status_dir = "status"
data_dir = "data"

def generate_status(ignore_free_chat=True):
    in_f = open(f"{data_dir}/watch_list.txt", "r")
    
    freechat_list = []
    if ignore_free_chat:
        in_f_freechat = open(f"{data_dir}/free_chat_list.txt", "r", encoding="utf-8")

        for line in in_f_freechat:
            name, channel_id, video_id, *title = line.split(",")
            freechat_list.append(video_id)

    print(freechat_list)

    timestamp = int(time.time())
    out_filename = f"{status_dir}/status.{timestamp}.txt"
    out_f = open(out_filename, "w", encoding="utf-8")

    status = []
    for line in in_f:
        channel_id, name = line.split(",")
        name = name.strip()
        video_id, video_url, title, description, keywords, scheduled_start_time = get_current_live_stream(channel_id)
        print("loading", name, "current stream data...")
        print(name, channel_id, video_id, scheduled_start_time, title, sep=",")
        print(video_id in freechat_list)
        if video_id != "-1" and video_id not in freechat_list:
            status.append((name, channel_id, video_id, title))
            print(name, channel_id, video_id, scheduled_start_time, f'"{keywords}"',f'"{title}"', sep=",", file=out_f)

    return status

        
generate_status()