import os
import re
import csv
from datetime import datetime
import queue

from graph_to_image import plot_to_img

def string_found(string1, string2):
    if re.search(string1, string2, re.IGNORECASE):
        return True
    return False

def get_live_chat_message_count_from_file_v01(filename):
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

#xxx = open("log.log", "w")

def get_live_chat_message_count_from_file(filename, filter_word=""):
    timeframe_list = {}
    start_timestamp = -1

    i_file = open(filename, "r", encoding="utf-8")
    i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')
    n_header = next(i_csv_file)

    message_index = n_header.index("message")
    timestamp_index = n_header.index("timestamp")
    elapsedTime_index = n_header.index("elapsedTime")

    for csv_row in i_csv_file:
        row = [csv_row[message_index], csv_row[timestamp_index], csv_row[elapsedTime_index]]

        timestamp_secs = int(int(row[1]) - (int(row[1]) % 15000))
        if start_timestamp == -1:
            if row[2] in ("-0:00", "0:00", "0:01", "0:02"):
                start_timestamp = timestamp_secs
                timeframe_list[0] = [int(row[1]), 0]
            

        if filter_word:
            low_c_row = row[0].lower()
            if type(filter_word)==str:
                if not string_found(filter_word, low_c_row):
                    continue
            if type(filter_word)==tuple:
                found_c = 0
                for t in filter_word:
                    if string_found(t, low_c_row):
                        found_c += 1
                        
                if found_c == 0:
                    continue

        if start_timestamp != -1:
            norm_timestamp_secs = timestamp_secs - start_timestamp
            timeframe = norm_timestamp_secs // 15000
            if timeframe_list.get(timeframe, -1) == -1:
                timeframe_list[timeframe] = [timestamp_secs, 1]
            else:
                timeframe_list[timeframe][1] += 1 

    timeframe_list_ret = []

    for k in timeframe_list:
        timeframe_list_ret.append(timeframe_list[k])

    return timeframe_list_ret

def word_counter(filename, filter_word="", lower_all=True):
    word_list = {}
    start_timestamp = -1

    i_file = open(filename, "r", encoding="utf-8")
    i_csv_file = csv.reader(i_file, skipinitialspace=True, lineterminator='\n')
    n_header = next(i_csv_file)

    message_index = n_header.index("message")
    timestamp_index = n_header.index("timestamp")
    elapsedTime_index = n_header.index("elapsedTime")

    for csv_row in i_csv_file:
        row = [csv_row[message_index], csv_row[timestamp_index], csv_row[elapsedTime_index]]

        timestamp_secs = int(row[1])#int(int(row[1]) - (int(row[1]) % 15000))
        if start_timestamp == -1:
            if row[2] in ("-0:01", "-0:00", "0:00", "0:01", "0:02"):
                start_timestamp = timestamp_secs

        if filter_word:
            pass

        if start_timestamp != -1:
            norm_timestamp_secs = timestamp_secs - start_timestamp
            timeframe = norm_timestamp_secs // 1000
            
            corrected_row = row[0].replace("'","")
            word_split = re.split(r"\W+", corrected_row)

            for word in word_split:
                if lower_all:
                    word = word.lower()
                if word_list.get(word, -1) == -1:
                    word_list[word] = [word, [timeframe]]
                else:
                    word_list[word][1].append(timeframe)

    word_list_ret = []

    for k in word_list:
        if k:
            word_list_ret.append(word_list[k])

    return (start_timestamp, word_list_ret)

def word_usage_periods(word_list, frequency_tolerance=3, min_length = 5, filter_word="", order_by="length"):
    word_periods_list = dict()
    for word, timestamps in word_list:
        start_time = -1
        end_time = -1
        prev_time = -1
        count_per_period = 0
        periods = []

        if filter_word: ##word filter
            if word.lower() not in filter_word:
                continue
        
        for timestamp in timestamps:
            if start_time == -1:
                start_time = timestamp
                prev_time = start_time
                count_per_period = 1
                continue
            else:
                if timestamp - prev_time <= frequency_tolerance:
                    prev_time = timestamp
                    count_per_period += 1
                else:
                    end_time = prev_time
                    if end_time - start_time >= min_length:
                        periods.append((start_time, end_time, (end_time - start_time), count_per_period,((end_time - start_time) / count_per_period)))
                        #periods.append((start_time, end_time))## original
                    start_time = -1
                    end_time = -1
                    prev_time = -1
        if len(periods) > 0:
            word_periods_list[word] = periods
        
    word_periods_list_ret = []

    order_list = {"length": 2, "count": 3, "density": 4, "triple": -1}
    if order_by not in order_list.keys():
        order_by = "length"

    for k in word_periods_list:
        if order_by == "triple":
            word_periods_list[k].sort(reverse=True, key=lambda x: (x[3], x[2], x[4]))
        else:            
            word_periods_list[k].sort(reverse=True, key=lambda x: x[order_list[order_by]])
        word_periods_list_ret.append((k, word_periods_list[k])) 

    word_periods_list_ret.sort(reverse=True, key=lambda x: len(x[1]))
    
    return word_periods_list_ret
        
def get_word_count_periods(filename, frequency_tolerance=3, min_length = 5, filter_word="", order_by="length"):
    start_timestamp, word_count = word_counter(filename, filter_word)
    word_usage_periods_list = word_usage_periods(word_count, frequency_tolerance, min_length, filter_word, order_by)

    return (start_timestamp, word_usage_periods_list)

if __name__=="__main__":
    #print(get_live_chat_message_count_from_file_v2("-msuiNLHMGk.csv", (r"\bhic\b", ":_ameHic1::_ameHic2::_ameHic3:")))
    #print(str(word_counter("-msuiNLHMGk.csv")[1]).replace("[", "\n").replace("],","").replace("]]", "").replace(", ", ","), file=open("my_gen_w_corr_array.csv", "w", encoding="utf-8"))
    #plot_to_img(get_live_chat_message_count_from_file("powerwash.-fBlrjLNHuk.csv"))
    print(*(word_usage_periods(word_counter("powerwash.-fBlrjLNHuk.csv")[1], 3, 5, "")), sep="\n", file=open("word_periods.txt", "w",encoding="utf-8"))
    #print(word_counter("EDF5.QJRaAWNTw3g.csv"), file=open("word_counter.txt", "w", encoding="utf-8"))
    #print(str(get_live_chat_message_count_from_file("powerwash.-fBlrjLNHuk.csv")).replace("[", "\n").replace("],","").replace("]]", "").replace(", ", ","), file=open("my_gen.csv", "w"))
    

    # x = "this is a word not unlike random letters"
    # y = ngrams(x.split(), 3)
    # print(list(y))


    # o_file = open(main_dir + "/" + filename + "_only_text" +  datetime.now().strftime("%Y%m%d%H%M%S") + ".csv", "w", encoding="utf-8")
    # o_csv_file = csv.writer(o_file, skipinitialspace=True, lineterminator='\n', quotechar='"')
    # o_csv_file.writerow(headers)
    # ###
    # o_csv_file.writerows(n_row)