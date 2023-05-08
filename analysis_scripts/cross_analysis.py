import sys
import csv

channel_name = sys.argv[1]

i_file_1 = open("./cross_analysis/" + channel_name + "_member_count_by_video.csv", "r", encoding="utf-8")
i_csv_file_1 = csv.reader(i_file_1, skipinitialspace=True)

i_file_2 = open("./cross_analysis/" + channel_name + "_view_count.csv", "r", encoding="utf-8")
i_csv_file_2 = csv.reader(i_file_2, skipinitialspace=True)

headers_1 = []
headers_2 = []

chatter_count = {}
view_count = {}

for sub_i, row in enumerate(i_csv_file_1):
    if sub_i == 0:
        headers_1 = row
    else:
        chatter_count[row[0]] = row
    

for sub_i, row in enumerate(i_csv_file_2):
    if sub_i == 0:
        headers_2 = row
    else:
        view_count[row[0]] = row


#video_id,video_name,date,total_users,members,msg/sec #chatter_count
#streamId,title,averageViewerCount,maxViewerCount,startTime_f,scheduleTime_f,endTime_f,startTime,scheduleTime,endTime #view_count

o_file = open("./cross_analysis/" + channel_name + "_cross.csv", "w", encoding="utf-8")
o_csv_file = csv.writer(o_file, lineterminator='\n')

cross_header = ["video_id", "title","total_users", "members", "msg/sec", "averageViewerCount", "maxViewerCount", "startTime_f", "length","ratio_avg", "ratio_total", "ratio_mem_avg", "ratio_mem_total", "ratio_chat_p_sec_avg"]

o_csv_file.writerow(cross_header)

for key in chatter_count:
    if view_count.get(key, -1) != -1:
        if view_count[key][2] == "-":
            continue

        new_row = [
            chatter_count[key][0],
            view_count[key][1],
            chatter_count[key][3],
            chatter_count[key][4],
            chatter_count[key][5],
            view_count[key][2],
            view_count[key][3],
            view_count[key][4],
            str((int(view_count[key][9]) - int(view_count[key][7])) / 1000),
            str((int(chatter_count[key][3]) / int(view_count[key][2])) * 100), 
            str((int(chatter_count[key][3]) / int(view_count[key][3])) * 100),
            str((int(chatter_count[key][4]) / int(view_count[key][2])) * 100),
            str((int(chatter_count[key][4]) / int(view_count[key][3])) * 100),
            str(int(chatter_count[key][3]) / ((int(view_count[key][9]) - int(view_count[key][7])) / 1000))
        ]
        o_csv_file.writerow(new_row)



    
