import os
import sys
import poi_video_info

start_date, end_date = ("2020-06-12 00:00:00", "2023-10-12 23:59:59")

poi_video_info.download_video_info(start_date, end_date, ["calliope"]) ##download channel videolist

#os.system("python chat_process_all_file.py ./poi_channel_data/video_templates") ##download all chatlogs

#os.system("python poi_quick_procress_archive.py") ##extract chatter info

#os.system("python poi_intersection_all.py")
