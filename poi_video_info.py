import os
import sys
import csv
import requests
import time
import json
from datetime import datetime

def get_date(str_date):
    s_date, s_time = str_date.split(" ")
    s_year, s_month, s_day = s_date.split("-")
    s_hour, s_minute, s_seconds = s_time.split(":")
    start_unix = time.mktime(datetime(int(s_year), int(s_month), int(s_day), int(s_hour), int(s_minute), int(s_seconds)).timetuple()) * 1000

    return str(int(start_unix))

def superchat_poi(video_id, currency="₩"):
    url = f"https://holoapi.poi.cat/api/v4/live_chat/highlight?id={video_id}"

    response = requests.get(url)

    sum = 0
    for sc in response.json()["paid"]:
        if sc["amount"][0] == currency:
            value = sc["amount"][1:].replace(",", "")
            sum += float(value)
    return sum


def get_video_list_info_range_poi(channel_code, start_at = "", start_at_unix = 0, end_at = "", end_at_unix = 0):
    url = f"https://vt-api.poi.cat/api/v4/streams/ended?channelIds={channel_code}"

    if len(start_at) > 0:
        url += "&startAt=" + get_date(start_at)
    elif int(start_at_unix) > 0:
        url += "&startAt=" + str(start_at_unix)

    if len(end_at) > 0:
        url += "&endAt=" + get_date(end_at)
    elif int(end_at_unix) > 0:
        url += "&endAt=" + str(end_at_unix)


    response = requests.get(url)

    proccesed_list = []

    video_playlist = response.json()

    #json.dump(video_playlist, open("test_peko.txt", "w",encoding="utf-8"))
    if not len(video_playlist):
        print(url)
    else:
        for video_info in video_playlist:
            try:
                proccesed_list.append([
                    video_info["vtuberId"], #0
                    video_info["platformId"], #1
                    video_info["title"], #2
                    video_info.get("viewerAvg","-"), #3
                    video_info.get("viewerMax", "-"), #4
                    datetime.utcfromtimestamp(int(video_info["startTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.utcfromtimestamp(int(video_info.get("scheduleTime", 0)) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.utcfromtimestamp(int(video_info["endTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    video_info["startTime"], #8
                    video_info.get("scheduleTime", "0"), #9
                    video_info["endTime"], #10
                    #superchat_poi(video_info["streamId"])
                ])
            except:
                print(video_info)

    return proccesed_list


def get_video_list_info_all_poi_range(channel_code, start_at = "", start_at_unix = "", end_at = "", end_unix = ""):
    complete_list = []
    video_list = get_video_list_info_range_poi(channel_code, start_at = start_at, end_at=end_at)
    complete_list.extend(video_list)
    while len(video_list) > 0:
        last_unix_time = video_list[-1][-3] #endTime in video_list
        print("Downloading from",video_list[0][7],"to", video_list[-1][5])
        video_list = get_video_list_info_range_poi(channel_code, start_at=start_at, end_at_unix=last_unix_time)
        complete_list.extend(video_list)
    
    return complete_list

#print(str(get_video_list_info_range_poi("amelia", "2020-09-01", "2020-12-16")).replace("],", "]\n"))
def download_video_info(start_date, end_date, channel_list=[]):
    date_range = (start_date, end_date)#("2022-05-01 00:00:00", "2022-05-31 23:59:59")
    channel_code_list = [
        60,#usada-pekora
        #amelia
        #calliope
        #gura
        #inanis
        #kiara
        #irys
        #sana
        #ceres
        #ouro
        #mumei
        #hakos
    ] if len(channel_list) == 0 else channel_list

    file_label = "_" + date_range[0].split(" ")[0].replace("-", "_") + "-" + date_range[1].split(" ")[0].replace("-", "_")

    main_dir = "poi_channel_data/"
    os.makedirs(main_dir + "video_templates/", exist_ok=True)
    for channel_code in channel_code_list:
        os.makedirs(main_dir + "video_templates/" + channel_code, exist_ok=True)

        o_file = open(main_dir + channel_code + file_label + ".csv", "w", encoding="utf-8")
        o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n')

        video_list = get_video_list_info_all_poi_range(channel_code, start_at=date_range[0], end_at=date_range[1])

        headers = ["vtuberId", "streamId", "title", "averageViewerCount", "maxViewerCount", "startTime_f", "scheduleTime_f", "endTime_f", "startTime", "scheduleTime", "endTime"]
        o_csv_file.writerow(headers)
        o_csv_file.writerows(video_list)

        for video_data in video_list:
            clean_name = ("".join(list(filter(lambda ch: ord(ch) in range(1, 128) and (ch not in ".<>:\"/\\|?*&"), video_data[1])))).replace(" ", "_")
            open(main_dir + "video_templates/" + channel_code + "/" + clean_name + "." + video_data[0] + ".csv", "w")
        #print(str(get_video_list_info_all_poi(channel_code)).replace("],", "\n").replace("[", "").replace("]]", ""), file=o_csv_file)

if __name__ == "__main__":
    #print(superchat_poi("B_JOXosJVNo"))
    #print(get_video_list_info_range_poi("60", start_at="2024-01-01 00:00:00", end_at="2024-03-31 23:59:59"))
    download_video_info("2023-01-01 00:00:00", "2024-03-31 23:59:59", ["60"])
    # if len(sys.argv) == 3:
    #     start_date = sys.argv[1] + " 00:00:00"
    #     end_date = sys.argv[2] + " 23:59:59"
    #     download_video_info(start_date, end_date)
    # else:
    #     print("Arguments missing: start_date end_date")