import os
import platform
import subprocess

def cut_mp4(filename, start_time, clip_length, clip_name, _async=True):
    base_filename = os.path.basename(filename)

    command = f"./ffmpeg -ss {start_time} -y -i {base_filename} -c copy -t {clip_length} {clip_name}  -nostats -loglevel error"
    
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

if __name__ == "__main__":
    cut_mp4("test_clip.mp4", 7.5, 12.5, "clip_0_30.mp4", False)
    #cut_mp4("test_clip.mp4", 30, 60, "clip_30_60.mp4", False)