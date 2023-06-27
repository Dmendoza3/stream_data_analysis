import time
import os

def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line

main_dir = "./clips"
list_parent_folders = os.listdir(main_dir)
_async = True

for index, file in enumerate(list_parent_folders):
    if len(file.split(".")) == 2:
        filename, ext = file.split(".")

        complete_filename = main_dir + "/" + filename

        if ext == "log":    
            in_f = open(complete_filename, "r")
            for l in follow(in_f):
                pr = ""
                if "frame=" in l:
                    pr += l.replace("\n", "") + "|"
                if "out_time=" in l:
                    pr += l.replace("\n", "") + "|"
                    
                if pr:
                    print(pr)