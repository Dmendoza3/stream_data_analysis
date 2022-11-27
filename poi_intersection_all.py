import os
import csv
from datetime import datetime
from itertools import combinations 

main_dir = "./poi_channel_data/processed"
list_parent_folders = os.listdir(main_dir)

channel_code_list = ["amelia","calliope","gura","inanis","kiara","irys","sana","ceres","ouro","mumei","hakos"]
channel_code_list = ["amelia","irys"]
chatter_list = dict()
chatter_list_complete = dict()

chatter_headers = []

for index, file in enumerate(list_parent_folders):
    if len(file.split(".")) == 2:
        filename, ext = file.split(".")
        channel_code, proccessed, timestamp = filename.split("_")

        chatter_list[channel_code] = set()
        chatter_list_complete[channel_code] = dict()
        print("loading chatters from " + channel_code, sep="")
        if ext == "csv" and channel_code in channel_code_list:
            i_file = open(main_dir + "/" + file, "r", encoding="utf-8")
            i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')
            lines = set()
            for index, row in enumerate(i_csv_file):
                if index == 0:
                    chatter_headers = row
                if index > 0 and len(row) == 19:
                    lines.add(len(row))
                    chatter_list[channel_code].add(row[0])
                    chatter_list_complete[channel_code][row[0]] = row

##Generate intersection list
intersection_list = []
for l in range(1,len(channel_code_list) + 1):
    for cb in list(combinations(channel_code_list, l)):
        ch_first = chatter_list[cb[0]]
        ch_rest = []
        for ch_i in cb[1:]:
            ch_rest.append(chatter_list[ch_i])
        intersection_list.append((cb, len(ch_first.intersection(*ch_rest)), ch_first.intersection(*ch_rest)))

##Generate intersection files
headers = ["intersection", "count", "ratio"]
o_all_file = open(main_dir + "/_intersections/all_intersections_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv", "w", encoding="utf-8")
o_all_csv_file = csv.writer(o_all_file, skipinitialspace=True, lineterminator='\n')

o_all_csv_file.writerow(headers)
for ch_c in channel_code_list:
    print("counting:", ch_c, "...")
    o_file = open(main_dir + "/_intersections/" + ch_c + "_intersections" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv", "w", encoding="utf-8")
    o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n')

    row = []
    headers = ["intersection", "count", "ratio"]
    for inter in intersection_list:
        if ch_c in inter[0]:
            #print(ch_c, inter[0])
            row.append([
                inter[0],
                inter[1],
                (inter[1] / len(chatter_list[ch_c])) * 100
            ])
    o_csv_file.writerow(headers)
    o_csv_file.writerows(row)
    o_all_csv_file.writerows(row)

##chatters in all chats

for ch_c in channel_code_list:
    o_file = open(main_dir + "/_intersections/unity_chatters_" + ch_c + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv", "w", encoding="utf-8")
    o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n')
    rows = []
    for u_id in intersection_list[-1][2]:
        rows.append(chatter_list_complete[ch_c][u_id])

    o_csv_file.writerow(chatter_headers)
    o_csv_file.writerows(rows)