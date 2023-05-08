import os
import csv
from datetime import datetime
import queue


def get_live_chat_message_count_from_file(filename):
    timeframe_list = {}
    start_timestamp = -1

    i_file = open(filename, "r", encoding="utf-8")
    i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')
    n_header = next(i_csv_file)

    for row in i_csv_file:
        timestamp_secs = int(int(row[1]) / 1000)
        if row[2] == "-0:00":
            start_timestamp = timestamp_secs

        if start_timestamp != -1:
            norm_timestamp_secs = timestamp_secs - start_timestamp
            timeframe = norm_timestamp_secs // 15
            if timeframe_list.get(timeframe, -1) == -1:
                timeframe_list[timeframe] = [1, row[1]]
            else:
                timeframe_list[timeframe][0] += 1 

    timeframe_list_ret = []

    for k in timeframe_list:
        timeframe_list_ret.append(timeframe_list[k])

    return timeframe_list_ret


def get_live_chat_message_count_from_file_v2(filename):
    timeframe_list = {}
    start_timestamp = -1

    i_file = open(filename, "r", encoding="utf-8")
    i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')
    n_header = next(i_csv_file)

    for row in i_csv_file:
        timestamp_secs = int(int(row[1]) - (int(row[1]) % 15000))
        if row[2] == "-0:00":
            start_timestamp = timestamp_secs

        if start_timestamp != -1:
            norm_timestamp_secs = timestamp_secs - start_timestamp
            timeframe = norm_timestamp_secs // 15
            if timeframe_list.get(timeframe, -1) == -1:
                timeframe_list[timeframe] = [1, timestamp_secs]
            else:
                timeframe_list[timeframe][0] += 1 

    timeframe_list_ret = []

    for k in timeframe_list:
        timeframe_list_ret.append(timeframe_list[k])

    return timeframe_list_ret


#print(get_live_chat_message_count_from_file("call_download_3TCBoRzNC5I_only_text20230113140536.csv"))
print(str(get_live_chat_message_count_from_file_v2("call_download_3TCBoRzNC5I.3TCBoRzNC5I_timestamps.csv")).replace("[", "\n").replace("],","").replace("]]", "").replace(", ", ","), file=open("my_gen.csv", "w"))



        


# o_file = open(main_dir + "/" + filename + "_only_text" +  datetime.now().strftime("%Y%m%d%H%M%S") + ".csv", "w", encoding="utf-8")
# o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n', quotechar='"')
# o_csv_file.writerow(headers)
# ###
# o_csv_file.writerows(n_row)