import os
import sys
import csv
import math
import shutil
from datetime import datetime
#import threading, queue

def generate_chatter_list(row=[], video_id="", only_members=False):
    if len(row) > 0:
        if only_members:
            if row[17] != "True":
                return

        if chatter_list.get(row[11], -1) == -1:
            chatter_list[row[11]] = {
                "author.name": row[10], 
                "first_message_timestamp": row[3], 
                "last_message_timestamp": row[3],
                "first_message_content": row[2],
                "last_message_content": row[2],
                "first_message_video_id": video_id,
                "last_message_video_id": video_id,
                "message_count": 1,
                "text_msg_count": 1 if row[0] == "textMessage" else 0,
                "sc_count": 1 if row[0] == "superChat" else 0,
                "ss_count": 1 if row[0] == "superSticker" else 0,
                "first_member_timestamp": row[3] if row[17] == "True" else 2**42,
                "last_member_timestamp": row[3] if row[17] == "True" else -(2**42),
                "first_member_video_id": video_id if row[17] == "True" else "",
                "last_member_video_id": video_id if row[17] == "True" else "",
                "lastest_member_badge": row[14],
                "currencies": {row[8],} if row[0] == "superChat" else {'',},
                "currencies_values": {row[8]: float(row[6])} if row[0] == "superChat" else {}
            }
        else:
            if row[3] < chatter_list[row[11]]["first_message_timestamp"]:
                chatter_list[row[11]]["first_message_timestamp"] = row[3]
                chatter_list[row[11]]["first_message_content"] = row[2]
                chatter_list[row[11]]["first_message_video_id"] = video_id
                if row[17] == "True":
                    if int(row[3]) < int(chatter_list[row[11]]["first_member_timestamp"]):
                        chatter_list[row[11]]["first_member_timestamp"] = row[3]
                        chatter_list[row[11]]["first_member_video_id"] = video_id
            
            if row[3] >= chatter_list[row[11]]["last_message_timestamp"]:
                chatter_list[row[11]]["last_message_timestamp"] = row[3]
                chatter_list[row[11]]["last_message_content"] = row[2]
                chatter_list[row[11]]["last_message_video_id"] = video_id
                if row[17] == "True":
                    chatter_list[row[11]]["last_member_timestamp"] = row[3]
                    chatter_list[row[11]]["lastest_member_badge"] = row[14]
                    chatter_list[row[11]]["last_member_video_id"] = video_id

            chatter_list[row[11]]["message_count"] += 1
            if row[0] == "textMessage":
                chatter_list[row[11]]["text_msg_count"] += 1
            elif row[0] == "superChat":
                chatter_list[row[11]]["sc_count"] += 1
            elif row[0] == "superSticker":
                chatter_list[row[11]]["ss_count"] += 1

            if row[8]:
                chatter_list[row[11]]["currencies"].add(row[8])
                if chatter_list[row[11]]["currencies_values"].get(row[8], -1) == -1:
                    chatter_list[row[11]]["currencies_values"][row[8]] = float(row[6])
                else:
                    chatter_list[row[11]]["currencies_values"][row[8]] += float(row[6])

    else:
        o_filename = destination_folder + "/processed/" + file_alias + "_processed_" + datetime.now().strftime("%Y%m%d%H%M%S") + ("-only-members" if only_members else "") + ".csv"
        o_file = open(o_filename, "w", encoding="utf-8")

        print("creating", o_filename,"...")
        print("author.id", 
            "author.name", 
            "first_message_content",
            "last_message_content",
            "first_message_timestamp", 
            "last_message_timestamp",
            "msg_date_difference", 
            "first_message_video_id",
            "last_message_video_id",
            "first_date_formatted", 
            "last_date_formatted", 
            "message_count",
            "text_msg_count",
            "sc_count",
            "ss_count",
            "first_member_timestamp",
            "last_member_timestamp",
            "first_membership_date",
            "last_membership_date",
            "first_member_video_id",
            "last_member_video_id",
            "lastest_member_badge",
            "currencies",
            "currencies_values",
            sep=",", file=o_file)
        for chatter in chatter_list:
            try:
                first_message_date = datetime.utcfromtimestamp(int(chatter_list[chatter]["first_message_timestamp"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                last_message_date = datetime.utcfromtimestamp(int(chatter_list[chatter]["last_message_timestamp"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

                first_membership_date = datetime.utcfromtimestamp(int(chatter_list[chatter]["first_member_timestamp"]) / 1000).strftime('%Y-%m-%d %H:%M:%S') if chatter_list[chatter]["first_member_timestamp"] != 2**42 else "no date"
                last_membership_date = datetime.utcfromtimestamp(int(chatter_list[chatter]["last_member_timestamp"]) / 1000).strftime('%Y-%m-%d %H:%M:%S') if chatter_list[chatter]["last_member_timestamp"] != -(2**42) else "no date"

                if len(chatter_list[chatter]["currencies"]) > 1:
                    chatter_list[chatter]["currencies"].remove('')

                currency_list = '"' + str(chatter_list[chatter]["currencies"]).replace('"', "'").replace('{','').replace('}','').replace("\\xa0", "") + '"'
                currencies_values_list = '"' + str(chatter_list[chatter]["currencies_values"]).replace('"', "'").replace('{','').replace('}','').replace("\\xa0", "") + '"'

                print(chatter, 
                '"' + chatter_list[chatter]["author.name"].replace('"',"") + '"', 
                '"' + chatter_list[chatter]["first_message_content"].replace('"',"") + '"', 
                '"' + chatter_list[chatter]["last_message_content"].replace('"',"") + '"', 
                chatter_list[chatter]["first_message_timestamp"], 
                chatter_list[chatter]["last_message_timestamp"],
                int(chatter_list[chatter]["last_message_timestamp"]) - int(chatter_list[chatter]["first_message_timestamp"]),
                chatter_list[chatter]["first_message_video_id"], 
                chatter_list[chatter]["last_message_video_id"],
                first_message_date,
                last_message_date,
                chatter_list[chatter]["message_count"],
                chatter_list[chatter]["text_msg_count"],
                chatter_list[chatter]["sc_count"],
                chatter_list[chatter]["ss_count"],
                chatter_list[chatter]["first_member_timestamp"],
                chatter_list[chatter]["last_member_timestamp"],
                first_membership_date,
                last_membership_date,
                chatter_list[chatter]["first_member_video_id"],
                chatter_list[chatter]["last_member_video_id"],
                chatter_list[chatter]["lastest_member_badge"],
                currency_list,
                currencies_values_list,
                sep=",", file=o_file)
            except:
                print("before_error:", chatter_list[chatter]["first_message_timestamp"])
            
def generate_members_by_date_list(row=[], video_id=""):
    if len(row) > 0:
        date_key = datetime.utcfromtimestamp(int(row[3]) / 1000).strftime('%Y-%m')
        
        if members_by_date_list.get(date_key, -1) == -1:
            s = set()
            s_m = set()
            s.add(row[11])
            if row[17]=="True":
                s_m.add(row[11])
            members_by_date_list[date_key] = {
                "count":s,
                "count_members":s_m,
                "video_id": {video_id,}
            }
        else:
            members_by_date_list[date_key]["count"].add(row[11])
            members_by_date_list[date_key]["video_id"].add(video_id)
            if row[17]=="True":
                members_by_date_list[date_key]["count_members"].add(row[11])
    else:
        o_filename = "proccessed/" + file_alias + "_member_count_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
        o_file = open(o_filename, "w", encoding="utf-8")

        print("creating", o_filename,"...")
        print("date", "total_users", "members", "video_id",sep=",", file=o_file)
        for date_key in members_by_date_list:
            video_id_list = '"' + str(members_by_date_list[date_key]["video_id"]).replace('"', "'").replace('{','').replace('}','') + '"'
            try:
                print(date_key, 
                len(members_by_date_list[date_key]["count"]),
                len(members_by_date_list[date_key]["count_members"]),
                video_id_list,
                sep=",", file=o_file)
            except:
                print("before_error:", members_by_date_list[date_key]["first_message_timestamp"])

def generate_chatters_by_video_list(row=[], video_id="", video_name=""):
    if len(row) > 0:
        if members_by_video_list.get(video_id, -1) == -1:
            date_key = datetime.utcfromtimestamp(int(row[3]) / 1000).strftime('%Y-%m-%d')
            s = set()
            s_m = set()
            s.add(row[11])
            if row[17]=="True":
                s_m.add(row[11])
            members_by_video_list[video_id] = {
                "video_name": video_name,
                "date": date_key,
                "count": s,
                "count_members": s_m,
                "period_sum_first": row[3],
                "period_sum_last": [1],
                "timestamp_count": 1
                #"timestamp_list": [row[3]]
            }

        else:
            members_by_video_list[video_id]["count"].add(row[11])
            members_by_video_list[video_id]["period_sum_last"] = row[3]
            #members_by_video_list[video_id]["timestamp_list"].append(row[3])
            members_by_video_list[video_id]["timestamp_count"] += 1

            if row[17]=="True":
                members_by_video_list[video_id]["count_members"].add(row[11])                
    else:
        o_filename = "proccessed/" + file_alias + "_member_count_by_video_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
        o_file = open(o_filename, "w", encoding="utf-8")

        print("creating", o_filename,"...")
        print("video_id", "video_name", "date", "total_users", "members", "msg/sec", sep=",", file=o_file)
        for video_id in members_by_video_list:
            try:
                msg_per_second = int(members_by_video_list[video_id]["timestamp_count"]) / ((int(members_by_video_list[video_id]["period_sum_last"]) - int(members_by_video_list[video_id]["period_sum_first"])) / 1000)
                #calc_period(members_by_video_list[video_id]["period_sum_first"], members_by_video_list[video_id]["period_sum_last"], members_by_video_list[video_id]["timestamp_list"])

                print(video_id,
                '"' + members_by_video_list[video_id]["video_name"] + '"',
                members_by_video_list[video_id]["date"],
                len(members_by_video_list[video_id]["count"]),
                len(members_by_video_list[video_id]["count_members"]),
                msg_per_second,
                sep=",", file=o_file)
            except:
                print("before_error:", members_by_video_list[video_id]["first_message_timestamp"])

def count_row_sizes(row=[]):
    if len(row) > 0:
        if sizes.get(len(row), -1) == -1:
            sizes[len(row)] = 1
        else:
            sizes[len(row)] += 1
    else:
        print("File Sizes", sizes)

def move_corrupt_files(file=""):
    if file:
        move_list.add(file)
    else:
        for file in move_list:
            shutil.move(parent_folder + "/" + file, parent_folder + "/long/" + file)

def calc_period(p_start, p_end, timestamp_list):
    period_1_sec = (int(p_end) - int(p_start)) / 1000
    # period_15 = (int(p_end) - int(p_start)) / 15000
    # period_30 = (int(p_end) - int(p_start)) / 30000
    # period_60 = (int(p_end) - int(p_start)) / 60000

    #separate list by periods
    # periods_list_15 = [0] * int(period_15)
    # periods_list_30 = [0] * int(period_30)
    # periods_list_60 = [0] * int(period_60)

    # for timestamp in timestamp_list:
    #     t_int = int(timestamp)
    #     periods_list_15[t_int % period_15] += 1
    #     periods_list_30[t_int % period_30] += 1
    #     periods_list_60[t_int % period_60] += 1
    total_timestamps = len(timestamp_list)

    # return (total_timestamps / period_15, total_timestamps / period_30, total_timestamps / period_60)
    return (total_timestamps / period_1_sec)

HEADERS = [
    "type", #0
    "id", #1
    "message", #2
    "timestamp", #3
    "datetime", #4
    "elapsedTime", #5
    "amountValue", #6
    "amountString", #7
    "currency", #8
    "bgColor", #9
    "author.name", #10
    "author.channelId", #11
    "author.channelUrl", #12
    "author.imageUrl", #13
    "author.badgeUrl", #14
    "author.isVerified", #15
    "author.isChatOwner", #16
    "author.isChatSponsor", #17
    "author.isChatModerator" #18
]

parent_folder = sys.argv[1]
destination_folder = sys.argv[2]
file_alias = sys.argv[3]
list_parent_folders = os.listdir("./" + parent_folder)

chatter_list = {}

members_by_date_list = {}

members_by_video_list = {}

list_size = len(list_parent_folders)

sizes = {}

move_list = set()

for index, file in enumerate(list_parent_folders):
    print("processing file(", index + 1, "/", list_size, ")", sep="", end="\r")
    if len(file.split(".")) == 3:
        video_name, video_id, ext = file.split(".")
        if ext == "csv":
            i_file = open(parent_folder + "/" + file, "r", encoding="utf-8")
            i_csv_file = csv.reader(i_file, skipinitialspace=True)
            #next(i_csv_file) #read headers
            try:
                for sub_i, row in enumerate(i_csv_file):
                    if sub_i > 0:
                        if len(row) > 0:
                            generate_chatter_list(row,video_id)
                            #generate_members_by_date_list(row, video_id)
                            #generate_chatters_by_video_list(row, video_id, video_name)
                    #count_row_sizes(row)
                    # if len(row) > 19:
                        #move_corrupt_files(file)
            except:
                print("error on file:", file, end="\n\n")
                

#count_row_sizes()
generate_chatter_list()
#generate_members_by_date_list()
#generate_chatters_by_video_list()
