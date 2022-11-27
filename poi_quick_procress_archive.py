import os

if not os.path.isdir("./poi_channel_data/processed/"):
    os.mkdir("./poi_channel_data/processed/")

if not os.path.isdir("./poi_channel_data/processed/_intersections"):
    os.mkdir("./poi_channel_data/processed/_intersections")

def external_chat_download(channel_code):
    os.system("python process_archive.py poi_channel_data/video_templates/" + channel_code + " poi_channel_data " + channel_code)


#channel_code_list = ["amelia","calliope","gura","inanis","kiara","irys","sana","ceres","ouro","mumei","hakos"]
channel_code_list = ["gura"]

for c in channel_code_list:
    external_chat_download(c)