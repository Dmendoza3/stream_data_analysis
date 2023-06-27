import os
import time
import platform
import subprocess


def convert_clips_mp3(main_dir="clips", _async = True):
    list_parent_folders = os.listdir(main_dir)

    for index, file in enumerate(list_parent_folders):
        f1 = ""
        if len(file.split(".")) == 2:
            filename, ext = file.split(".")
        elif len(file.split(".")) == 3:
            f1, filename, ext = file.split(".")
        complete_filename = main_dir + "/" + ((f1 + ".") if f1 else "") + filename

        if ext == "mp4":    
            print(f"converting to mp3 {f1}.{filename}...")
            command = f"./ffmpeg -i '{complete_filename}.mp4' '{complete_filename}.mp3' -n -nostats -loglevel error"
            if platform.system() == "Windows":
                proc = "powershell"
                if _async:
                    proc = subprocess.Popen([proc, command], shell=False)
                    time.sleep(0.333)
                else:
                    proc = subprocess.call([proc, command], shell=False)
            elif platform.system() == "Linux":
                proc = subprocess.Popen([command], shell=False)
            elif platform.system() == "Darwin": #MAC
                pass

def convert_clip_mp3(filename, _async = True):
    base_filename = os.path.basename(filename)

    command = f"./ffmpeg -i '{base_filename}' '{base_filename}.mp3' -n -nostats -loglevel error"
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

if __name__  == "__main__":
    convert_clips_mp3()