import os
import download_yt
import peak_live_chat
import threading, queue
from datetime import timedelta
from convert_to_mp3 import convert_clips_mp3
from convert_to_webm import convert_clips_webm
from convert_to_webm import mute_all

q = queue.Queue()
def worker():
    while True:
        item = q.get()

        #print(item[0], item[1], item[2], item[3], item[4], item[5])
        print(f"downloading {item[0]} start_time:{item[1]} total lenght:{item[2]} saved to: {item[3]}.mp4")
        base_filename = os.path.basename(item[3])
        dir_name = os.path.dirname(item[3])
        _, filename, timestamp = base_filename.split("!")
        new_dir = dir_name + "/" + filename

        if not os.path.exists(new_dir):
            try:
                os.mkdir(new_dir)
            except:
                pass

        new_file = new_dir + "/" + base_filename

        #download_yt.download_yt_video(item[0], item[1], item[2], item[3], item[4], item[5])
        download_yt.download_yt_video(item[0], item[1], item[2], new_file, item[4], item[5])

        q.task_done()

##first version 
def generate_clips_holostats_api(video_id, clip_count=1):
    frames = peak_live_chat.get_frames_holostats_api(video_id, clip_count)

    for _, start_time, clip_length, clip_name in frames:
        print(f"downloading {video_id} total lenght:{clip_length} saved to: {clip_name}.mp4")
        download_yt.download_yt_video(video_id, start_time, clip_length, clip_name, False)

##Generates clips by amount of messages per frame of 15 secods
def generate_clips_by_volume(filename, clip_count=1, filter_word="", offset_start=(18,24), padding_end=(11, 70), avg_length=90):
    video_name, video_id, extension = filename.split(".")
    frames = peak_live_chat.get_frames_by_file(filename, clip_count, filter_word, offset_start, padding_end, avg_length)

    prefetched_url = download_yt.get_yt_video_url(video_id)
    
    for _, start_time, clip_length, clip_name in frames:
        q.put([video_id, start_time, clip_length, clip_name, False, prefetched_url])
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=worker, daemon=True).start()

    q.join()

##Generates clips by periods of continuous text 
def generate_clips_by_periods(filename, clip_count=1, filter_word="", frequency_tolerance=3, min_length=5, offset_start=(10,10), padding_end=(0, 0), order_by="length"):
    """
    Creates an N amount of mp4 video clips of a live stream on youtube based on periods of a used word found in the logs of the file specified
    """
    video_name, video_id, extension = filename.split(".")
    
    frames = peak_live_chat.get_frames_by_periods(filename, clip_count, filter_word, frequency_tolerance, min_length, offset_start, padding_end, "clips", order_by)

    prefetched_url = download_yt.get_yt_video_url(video_id)
    
    print("frames found:", len(frames))
    for _, start_time, clip_length, clip_name in frames:
        q.put([video_id, start_time, clip_length, clip_name, False, prefetched_url])
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=worker, daemon=True).start()
    threading.Thread(target=worker, daemon=True).start()

    q.join()

def generate_clips_last_n_seconds(self, video_id, name,c_time=30, prefetched_url=""):
    """
    Creates a mp4 video clip of the last N seconds of a live stream on youtube
    """
    if len(video_id) < 11 and c_time > 1:
        return
    
    if len(prefetched_url) == 0:
        prefetched_url = download_yt.get_yt_video_url(video_id)

    duration_secs = int(float(download_yt.get_stream_current_duration(video_id, prefetched_url=prefetched_url)))
    start_time = timedelta(seconds=duration_secs - 30)
    length = timedelta(seconds=c_time)

    filename = name + "_" + str(start_time).replace(":","") + f"_{str(c_time)}"
    download_yt.download_yt_video(self, start_time, length, filename, False, prefetched_url)


if __name__ == "__main__":
    clip_amount = 3
    text_filter = ("_iryslaugh", "¿")
    offset_start = (10,10)
    padding_end = (0,0)
    min_length = 4
    avg_length = 15
    frequency_tolerance = 3

    file = "EuroTruck.neZyTON6Ff0.csv"
    name, id, ext = file.split(".")

    clip_folder = lambda x,y: f"clips/{name}_{id}_{x}_{y}_({text_filter[0]})"


    generate_clips_by_periods(file, clip_amount, text_filter, offset_start=offset_start, padding_end=padding_end, min_length=min_length,frequency_tolerance=frequency_tolerance, order_by="triple")
    convert_clips_mp3(clip_folder("period", "triple"), False)

    # generate_clips_by_periods(file, clip_amount, text_filter, offset_start=offset_start, padding_end=padding_end, min_length=min_length,frequency_tolerance=frequency_tolerance, order_by="length")
    # convert_clips_mp3(clip_folder("period", "length"), False)

    # generate_clips_by_periods(file, clip_amount, text_filter, offset_start=offset_start, padding_end=padding_end, min_length=min_length,frequency_tolerance=frequency_tolerance, order_by="count")
    # convert_clips_mp3(clip_folder("period", "count"), False)

    # generate_clips_by_periods(file, clip_amount, text_filter, offset_start=offset_start, padding_end=padding_end, min_length=min_length,frequency_tolerance=frequency_tolerance, order_by="density")
    # convert_clips_mp3(clip_folder("period", "density"), False)

    #generate_clips_by_volume(file, clip_amount, text_filter, offset_start, padding_end, avg_length)
    #convert_clips_mp3(clip_folder("volume"), False)
    #convert_clips_webm(clip_folder, True, False)

    #convert_clips_webm("compilation", True, False)


#generate_clips_by_periods("cod.5ptxXv3fl1U.csv", 5, ("_iryslaugh", "-1"), offset_start=(10,10), padding_end=(0,0), min_length=4,frequency_tolerance=3)
#generate_clips_by_periods("cod.5ptxXv3fl1U.csv", 5, ("_irysdevil", "-1"), offset_start=(10,10), padding_end=(0,0), min_length=4,frequency_tolerance=3)
#generate_clips_by_periods("cod.5ptxXv3fl1U.csv", 5, ("_iryssurprised", "-1"), offset_start=(10,10), padding_end=(0,0), min_length=4,frequency_tolerance=3)
#generate_clips_by_periods("cod.5ptxXv3fl1U.csv", 5, ("_irysheart2", "-1"), offset_start=(10,10), padding_end=(0,0), min_length=4,frequency_tolerance=3)
#generate_clips_by_periods("cod.5ptxXv3fl1U.csv", 5, ("_iryspien", "-1"), offset_start=(10,10), padding_end=(0,0), min_length=4,frequency_tolerance=3)

# generate_clips_by_file("cod.5ptxXv3fl1U.csv", 5, ("_iryslaugh","-1"), (0,0), (0,0), 15)
# generate_clips_by_file("cod.5ptxXv3fl1U.csv", 5, ("_irysdevil","-1"), (0,0), (0,0), 15)
# generate_clips_by_file("cod.5ptxXv3fl1U.csv", 5, ("_iryssurprised","-1"), (0,0), (0,0), 15)
# generate_clips_by_file("cod.5ptxXv3fl1U.csv", 5, ("_irysheart2","-1"), (0,0), (0,0), 15)
# generate_clips_by_file("cod.5ptxXv3fl1U.csv", 5, ("_iryspien","-1"), (0,0), (0,0), 15)

# convert_clips_mp3("clips/cod_by_period_download/cod_5ptxXv3fl1U_(_iryslaugh)", False)
# convert_clips_mp3("clips/cod_by_period_download/cod_5ptxXv3fl1U_(_irysdevil)", False)
# convert_clips_mp3("clips/cod_by_period_download/cod_5ptxXv3fl1U_(_iryssurprised)", False)
# convert_clips_mp3("clips/cod_by_period_download/cod_5ptxXv3fl1U_(_irysheart2)", False)
# convert_clips_mp3("clips/cod_by_period_download/cod_5ptxXv3fl1U_(_iryspien)", False)
#convert_clips_mp3("clips/cod2_m0afm7Yn93M_(_iryslaugh)", False)
#convert_clips_webm("clips/cod2_m0afm7Yn93M_(_iryslaugh)", True, False)
#mute_all("clips/cod2_m0afm7Yn93M_(_iryslaugh)", "mp4", False)

# convert_clips_mp3("clips/cod_by_file_download/cod_5ptxXv3fl1U_(_iryslaugh)", False)
# convert_clips_mp3("clips/cod_by_file_download/cod_5ptxXv3fl1U_(_irysdevil)", False)
# convert_clips_mp3("clips/cod_by_file_download/cod_5ptxXv3fl1U_(_iryssurprised)", False)
# convert_clips_mp3("clips/cod_by_file_download/cod_5ptxXv3fl1U_(_irysheart2)", False)
# convert_clips_mp3("clips/cod_by_file_download/cod_5ptxXv3fl1U_(_iryspien)", False)

