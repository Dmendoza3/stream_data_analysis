import os
import csv
from datetime import datetime
import queue

main_dir = "./poi_channel_data/_archive/irys_2023_05_31-2023_06_20/1"
list_parent_folders = os.listdir(main_dir)

headers = ["message", "timestamp", "elapsedTime"]

for index, file in enumerate(list_parent_folders):
    if len(file.split(".")) == 3:
        filename, id,ext = file.split(".")
        if ext == "csv":
            i_file = open(main_dir + "/" + file, "r", encoding="utf-8")
            i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')

            o_file = open(main_dir + "/" + filename + "_only_text" +  datetime.now().strftime("%Y%m%d%H%M%S") + "."  + id + ".csv", "w", encoding="utf-8")
            o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n', quotechar='"')
            o_csv_file.writerow(headers)

            n_row = []
            for index, row in enumerate(i_csv_file):
                if index > 0 and len(row) == 19:
                    n_row.append([row[2], row[3], row[5]])
            o_csv_file.writerows(n_row)