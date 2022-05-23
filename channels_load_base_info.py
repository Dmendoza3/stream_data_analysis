import os
from tinydb import TinyDB
from pathlib import Path
from datetime import date
from channel_video_list import get_channel_video_info_id, get_video_info

archive_path = "chat_archive"

base_dir =  archive_path

db = TinyDB(archive_path + '/full_channel_info.json')
#db.truncate()

Path(archive_path).mkdir(parents=True, exist_ok=True)

#get channel id list from txt
channel_list = [line.split(",") for line in open("channel_names.txt", "r", encoding="utf-8")]

for channel_id, channel_name_local in channel_list:
    channel_name, video_list = get_channel_video_info_id(channel_id)
    channel_table = db.table(channel_name_local.replace("\n",""))
    db.insert({ "channel_id": channel_id, "channel_name":channel_name_local.replace("\n","") })

    channel_dir = base_dir + "\\" + channel_name.replace(" ", "_").replace(".", "_")
    Path(channel_dir).mkdir(parents=True, exist_ok=True)

    i_filename = "video_list_" + str(date.today()) + ".txt"
    i_file = open(channel_dir + "\\" + i_filename, "w", encoding="utf-8")

    print("loading ", channel_name,"...", sep="")
    for video in video_list:
        video_info = get_video_info(video)
        channel_table.insert(video_info)
        if video_info["start_time"]:
            open(channel_dir + "\\" + video_info["clean_name"] + "." + video + ".csv", "a")
        print(video, file=i_file)
    

