import csv
import requests
import time
from datetime import datetime

def get_date(str_date):
    s_year, s_month, s_day = str_date.split("-")
    start_unix = time.mktime(datetime(int(s_year), int(s_month), int(s_day)).timetuple()) * 1000

    return str(int(start_unix))

def get_video_list_info_range_poi(channel_code, start_date = "", end_date = ""):
    start_unix = get_date(start_date)
    end_unix = get_date(end_date)

    url = "https://holoapi.poi.cat/api/v4/youtube_streams?ids=" + channel_code + "&status=live,ended&startAt=" + start_unix + "&endAt=" + end_unix + "&orderBy=start_time:asc"
    response = requests.get(url)

    proccesed_list = []

    video_playlist = response.json()
    for video_info  in video_playlist["streams"]:
        proccesed_list.append([
            video_info["title"], 
            datetime.utcfromtimestamp(int(video_info["startTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(int(video_info["scheduleTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(int(video_info["endTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            video_info.get("averageViewerCount","-"),
            video_info.get("maxViewerCount", "-") 
        ])
        #print(video_info["title"])

    return proccesed_list

def get_video_list_info_starting_at_poi(channel_code, start_at = "", start_at_unix = 0):
    url = "https://holoapi.poi.cat/api/v4/youtube_streams?ids=" + channel_code + "&status=live,ended&orderBy=start_time:asc" 

    if len(start_at) > 0:
        url += "&startAt=" + get_date(start_at)
    elif int(start_at_unix) > 0:
        url += "&startAt=" + str(start_at_unix)
    response = requests.get(url)

    proccesed_list = []

    video_playlist = response.json()
    for video_info  in video_playlist["streams"]:
        proccesed_list.append([
            video_info["streamId"], 
            video_info["title"], 
            video_info.get("averageViewerCount","-"),
            video_info.get("maxViewerCount", "-"),
            datetime.utcfromtimestamp(int(video_info["startTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(int(video_info.get("scheduleTime", 0)) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(int(video_info["endTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            video_info["startTime"],
            video_info.get("scheduleTime", "0"),
            video_info["endTime"]
        ])
        #print(video_info["title"])

    return proccesed_list

def get_video_list_info_all_poi(channel_code, start_at = "", start_at_unix = ""):
    complete_list = []
    video_list = get_video_list_info_starting_at_poi(channel_code, start_at = start_at)
    complete_list.extend(video_list)
    while len(video_list) > 0:
        last_unix_time = video_list[-1][-1]
        print("Downloading from",video_list[0][4],"to",video_list[-1][6])
        video_list = get_video_list_info_starting_at_poi(channel_code, start_at_unix=last_unix_time)
        complete_list.extend(video_list)
    
    return complete_list

#print(str(get_video_list_info_range_poi("amelia", "2020-09-01", "2020-12-16")).replace("],", "]\n"))
channel_code = "kiara"
o_file = open(channel_code + ".csv", "w", encoding="utf-8")
o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n')

headers = ["streamId", "title", "averageViewerCount", "maxViewerCount", "startTime_f", "scheduleTime_f", "endTime_f", "startTime", "scheduleTime", "endTime"]
o_csv_file.writerow(headers)
o_csv_file.writerows(get_video_list_info_all_poi(channel_code))
#print(str(get_video_list_info_all_poi(channel_code)).replace("],", "\n").replace("[", "").replace("]]", ""), file=o_csv_file)
