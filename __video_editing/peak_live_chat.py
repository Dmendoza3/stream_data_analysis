import os
import sys
import requests
import random
from datetime import timedelta, datetime
from count_messages_by_time_frame_function import get_live_chat_message_count_from_file, get_word_count_periods

def time_formatted(time):
    return timedelta(seconds=time)

def get_live_chat_message_count_holostats_api(video_id):
    url = f"https://holoapi.poi.cat/api/v4/streams_report?ids={video_id}&metrics=youtube_live_chat_message"

    response = requests.get(url)

    json = response.json()
    return json

def get_average_message_count_holostats_api(video_id):
    # c_outliers = 2.56
    rows = get_live_chat_message_count_holostats_api(video_id)["reports"][0]["rows"]

    # outliers_list = []
    # start_time = -1
    # avg_messages = 0
    for i, row in enumerate(rows):
        if i == 0:
            start_time = row[0]
        #avg_messages += row[1]
        #print("frame:", i, "messages_total:", row[2])
    
    # avg_msg_count = avg_messages / len(rows)

    c_rows = rows[:]
    c_rows.sort(reverse=True, key=lambda x:x[1])

    # for i, row in enumerate(c_rows):
    #     if row[1] / c_outliers >= avg_msg_count:
    #         pass

    # print("start_time:", start_time)
    # print("total_messages:", avg_messages)
    # print("total_frames:", len(rows))
    # print("avg_messages:", avg_messages / len(rows))
    # print("max_messages:", max(rows, key=lambda x:x[1]))
    # print("max_messages[5]:", c_rows[0:5])

    return (start_time, c_rows)

def get_frames_holostats_api(video_id, frame_limit=-1):
    start_timestamp, count_per_frame = get_average_message_count_holostats_api(video_id)
    ret_list = []

    for i, frame in enumerate(count_per_frame):
        clip_avg_length = 90 #120 secs = 2 minutes
        plus_random_time = random.randint(11, 70)
        minus_random_start_time = random.randint(18, 24)

        ##TODO: overlap validation
        unix_diff = int(frame[0] / 1000) - int(start_timestamp / 1000)
        if unix_diff <= minus_random_start_time:
            minus_random_start_time = 0

        start_time = time_formatted(unix_diff - minus_random_start_time)
        length = time_formatted(clip_avg_length + plus_random_time)
        clip_name = f"frame_{i}_{video_id}"
        
        ret_list.append((video_id, str(start_time), str(length), clip_name))
        #print(video_id, start_time, length, clip_name, sep=", ")

        if len(ret_list) >= frame_limit and frame_limit > 0:
            break
    return ret_list

def get_average_message_count_by_file(filename, filter_word):
    rows = get_live_chat_message_count_from_file(filename, filter_word)

    start_time = -1
    # for i, row in enumerate(rows[:]):
    #     if i == 0:
    start_time = rows[0][0]
    

    c_rows = rows[:]
    c_rows.sort(reverse=True, key=lambda x:x[1])
    
    return (start_time, c_rows)

def get_frames_by_file(file, frame_limit=-1, filter_word="", padding_start=(18,24), padding_end=(11,70), avg_length=90, clip_dir="clips"):
    base_file = os.path.basename(file)
    name, video_id, extension = base_file.split(".")
    filename = name + "_" + video_id
    start_timestamp, count_per_frame = get_average_message_count_by_file(file, filter_word)
    ret_list = []

    for i, frame in enumerate(count_per_frame):
        clip_avg_length = avg_length #120 secs = 2 minutes
        plus_random_time = random.randint(padding_end[0], padding_end[1])
        minus_random_start_time = random.randint(padding_start[0], padding_start[1])

        ##TODO: overlap validation
        unix_diff = int(frame[0] / 1000) - int(start_timestamp / 1000)
        if unix_diff <= minus_random_start_time:
            minus_random_start_time = 0

        start_time = time_formatted(unix_diff - minus_random_start_time)
        length = time_formatted(clip_avg_length + plus_random_time)
        clip_label_extra = "no_filter"
        if filter_word:
            if type(filter_word)==str:
                clip_label_extra = filter_word
            if type(filter_word)==tuple:
                clip_label_extra = filter_word[0]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        clip_name = f"frame_{i}!{filename}_volume_({clip_label_extra})!" + timestamp
        
        ret_list.append((filename, str(start_time), str(length), clip_dir + "/" + clip_name))

        if len(ret_list) >= frame_limit and frame_limit > 0:
            break
    return ret_list

def get_frames_by_periods(file, frame_limit=-1, filter_word="", frequency_tolerance=3, min_length=5, offset_start=(10,10), padding_end=(0,0), clip_dir="clips", order_by="length"):
    base_file = os.path.basename(file)
    name, video_id, extension = base_file.split(".")
    filename = name + "_" + video_id
    start_timestamp, word_usage_periods_list = get_word_count_periods(file, frequency_tolerance, min_length, filter_word, order_by)
    ret_list = []

    for word, period_list in word_usage_periods_list:
        for i, periods in enumerate(period_list):
            timestamp_range_start, timestamp_range_end, timestamp_range_length, word_count, word_density = periods
            clip_length = timestamp_range_length
            plus_random_time = random.randint(padding_end[0], padding_end[1])
            minus_random_start_time = random.randint(offset_start[0], offset_start[1])

            offset_start_timestamp = timestamp_range_start - minus_random_start_time
            if offset_start_timestamp < 0:
                offset_start_timestamp = 0

            start_time = time_formatted(offset_start_timestamp)
            length = time_formatted(clip_length + plus_random_time)
            clip_label_extra = "no_filter"
            if filter_word:
                if type(filter_word)==str:
                    clip_label_extra = filter_word
                if type(filter_word)==tuple:
                    clip_label_extra = filter_word[0]

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            clip_name = f"frame_{i}!{filename}_period_{order_by}_({word})!" + timestamp
            
            ret_list.append((filename, str(start_time), str(length), clip_dir + "/" + clip_name))
            #print(video_id, start_time, length, clip_name, sep=", ")

            if len(ret_list) >= frame_limit and frame_limit > 0:
                break
    return ret_list[0:frame_limit]

if __name__=="__main__":
    if len(sys.argv) == 2:
        _, filename =  sys.argv
        word_filter = ""
        min_length = 1
        tolerance = 1
        # for tolerance in range(20, 100):
        #     print(f"Tolerance({word_filter}):", tolerance)
        #     print(get_frames_by_periods(filename, 2, word_filter, tolerance, min_length, (0,0), (0,0)))
        print(*get_frames_by_periods(filename, -1, frequency_tolerance=tolerance,filter_word=word_filter,min_length=1), sep="\n",file=open("periods.csv", "w", encoding="utf-8"))
        #print(*get_frames_by_file(filename, -1, word_filter), sep="\n",file=open("frames.csv", "w", encoding="utf-8"))
    #print(get_live_chat_message_count("3TCBoRzNC5I"))
    #print(get_live_chat_message_count_from_file("3TCBoRzNC5I.csv"))
    #print(get_frames_by_file("nQLfdu5KZSA.csv", 10, ("hic_test_recording", r"\bhic\b", ":_ameHic1::_ameHic2::_ameHic3:"), (0,0), (0,0), 8))
    #print(get_frames_by_periods("-msuiNLHMGk.csv", 5, "_irysBlush"))
    #print(get_frames("3TCBoRzNC5I", 5))
