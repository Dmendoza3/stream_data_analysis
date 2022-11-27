import os
import csv
from datetime import datetime
import queue

main_dir = "."
list_parent_folders = os.listdir(main_dir)

headers = ["message", "timestamp", "elapsedTime"]

timeframe_list = {}
frame = 0
start_timestamp = -1

for index, file in enumerate(list_parent_folders):
    if len(file.split(".")) == 3:
        filename, id,ext = file.split(".")
        if ext == "csv":
            i_file = open(main_dir + "/" + file, "r", encoding="utf-8")
            i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')
            n_row = []
            n_header = next(i_csv_file)

            for index, row in enumerate(i_csv_file):
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
                


print(timeframe_list[max(timeframe_list, key=lambda x: timeframe_list[x][0])])
                    


        


# o_file = open(main_dir + "/" + filename + "_only_text" +  datetime.now().strftime("%Y%m%d%H%M%S") + ".csv", "w", encoding="utf-8")
# o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n', quotechar='"')
# o_csv_file.writerow(headers)
# ###
# o_csv_file.writerows(n_row)