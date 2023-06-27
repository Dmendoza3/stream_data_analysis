import os
import sys
import time
import platform
import subprocess

def convert_clips_webm(main_dir="clips", mute = False, _async = True):
    list_parent_folders = os.listdir(main_dir)

    for index, file in enumerate(list_parent_folders):
        f1 = ""
        if len(file.split(".")) == 2:
            filename, ext = file.split(".")
        elif len(file.split(".")) == 3:
            f1, filename, ext = file.split(".")
        complete_filename = main_dir + "/" + ((f1 + ".") if f1 else "") + filename

        if ext == "mp4":    
            print(f"converting to webm {filename}...")

            mute_option = "-an" if mute else ""
            command = f"./ffmpeg -i '{complete_filename}.mp4' -c:v libvpx-vp9 -crf 40 -b:v 0 -b:a 128k -c:a libopus {mute_option} '{complete_filename}.webm' -n -nostats -loglevel error"
            #f"./ffmpeg -i '{complete_filename}.mp4' -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 1 -an -deadline best -row-mt 1 -f null /dev/null && ./ffmpeg -i input.file -c:v libvpx-vp9 -b:v 0 -crf 30 -pass 2 -deadline best -row-mt 1 -c:a libopus -b:a 96k -ac 2 '{complete_filename}.webm'"
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

def convert_clip_webm(filename, mute = False ,_async = True):
    base_filename = os.path.basename(filename)

    mute_option = "-an" if mute else ""

    command = f"./ffmpeg -i '{base_filename}' -c:v libvpx-vp9 -crf 63 -b:v 0 -b:a 128k {mute_option} -c:a libopus '{base_filename}.webm' -n -nostats -loglevel error"
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

def mute_all(main_dir="clips", extension = "mp4", _async = True):
    list_parent_folders = os.listdir(main_dir)

    for index, file in enumerate(list_parent_folders):
        f1 = ""
        if len(file.split(".")) == 2:
            filename, ext = file.split(".")
        elif len(file.split(".")) == 3:
            f1, filename, ext = file.split(".")
        complete_filename = main_dir + "/" + ((f1 + ".") if f1 else "") + filename

        if ext == extension:
            print(f"converting {complete_filename}...")
            command = f"./ffmpeg -i '{complete_filename}.{ext}' -c copy -an '{complete_filename}_muted.{ext}'"
            print("command: ", command)
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
if __name__ == "__main__":
    print("converting:", sys.argv[1])
    convert_clip_webm(sys.argv[1])