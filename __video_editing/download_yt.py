import os
import sys
import time
import platform
import subprocess
from datetime import timedelta, datetime
#from pytube import YouTube, Channel

dl_logs_dir = "dl_logs"

def get_yt_video_url(video_id, quality="18"):
    command = f"./yt-dlp -f {quality} -g 'https://www.youtube.com/watch?v={video_id}' --extractor-args youtube:player-skip=js" #+ " --list-formats"
    if platform.system() == "Windows":
        proc = "powershell"
        proc = subprocess.Popen([proc, command], stdout=subprocess.PIPE, shell=False)
        out = proc.stdout.read()
        return out.decode("utf-8")
    elif platform.system() == "Linux":
        proc = subprocess.Popen([command], shell=False)
        out = proc.stdout.read()
        return out.decode("utf-8")
    elif platform.system() == "Darwin": #MAC
        pass



def download_yt_video(video_id, start_time, clip_length, clip_name, _async=True, prefetched_url=""):
    print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]", video_id, start_time, clip_length, clip_name + ".mp4", file=open("yt_downloads.log", "a"))
    base_filename = os.path.basename(clip_name)

    command = ""
    if prefetched_url:
        command = f"./ffmpeg -ss {start_time} -y -i '{prefetched_url}' -t {clip_length} -c copy '{clip_name}.mp4' -progress './{dl_logs_dir}/{base_filename}.log' -nostats -loglevel error"#-progress - -nostats -loglevel error" #-progress ./{clip_name}.log"
    else:
        command = f"./ffmpeg -ss {start_time} -y -i $(./yt-dlp -f b -g 'https://www.youtube.com/watch?v={video_id}') -t {clip_length} -c copy '{clip_name}.mp4' -progress './{dl_logs_dir}/{clip_name}.log' -nostats -loglevel error"#-progress - -nostats -loglevel error" #-progress ./{clip_name}.log"
    if platform.system() == "Windows":
        proc = "powershell"
        if _async:
            proc = subprocess.Popen([proc, command], shell=False)
        else:
            proc = subprocess.call([proc, command], shell=False)
    elif platform.system() == "Linux":
        proc = subprocess.Popen([command], shell=False)
    elif platform.system() == "Darwin": #MAC
        pass

def get_stream_current_duration(video_id, prefetched_url="", formatted_time=False):
    command = ""
    if prefetched_url:
        command = f"./ffprobe -i '{prefetched_url}' -show_entries format=start_time -v quiet -of csv='p=0'"
    else:
        command = f"./ffprobe -i $(./yt-dlp -f b -g https://www.youtube.com/watch?v={video_id}) -show_entries format=start_time -v quiet -of csv='p=0'"

    command += " -sexagesimal" if formatted_time else ""
    if platform.system() == "Windows":
        proc = "powershell"
        proc = subprocess.Popen([proc, command], stdout=subprocess.PIPE, shell=False)
        out = proc.stdout.read()
        return out.decode("utf-8").strip()
    elif platform.system() == "Linux":
        proc = subprocess.Popen([command], shell=False)
        out = proc.stdout.read()
        return out.decode("utf-8").strip()
    elif platform.system() == "Darwin": #MAC
        pass

if __name__ == "__main__":
    video_id = "m0afm7Yn93M"
    start_time = "00:00:00"#"01:10:31"
    clip_length = "00:00:30"
    clip_name = f"clip_test_{video_id}"
    #print("result: ", get_yt_video_url(video_id))
    prefetch = get_yt_video_url(video_id, 18)
    print(prefetch)
    # while True:
    #     print("Time:", get_stream_current_duration(video_id, prefetched_url=prefetch,formatted_time=True), "\r", end="")

    #     time.sleep(4)
    download_yt_video(video_id, start_time, clip_length, clip_name, False, prefetch)