import os
import threading, queue
from chat_capture_all_args_function import download_chat

def external_chat_capture(parent_folder, video_name, video_id):
    os.system("python chat_capture_all_args_function.py " + parent_folder + " " + video_name + " " + video_id)

def worker():
    while True:
        item = q.get()

        external_chat_capture(item[0], item[1], item[2])

        q.task_done()

parent_folder = "chat_archive"

list_parent_folders = os.listdir("./" + parent_folder)

video_list_params = []

for folder in list_parent_folders:
    if os.path.isdir("./chat_archive/" + folder):
        list_channel_files = os.listdir("./chat_archive/" + folder)
        for file in list_channel_files:
            if len(file.split(".")) == 3:
                video_name, video_id, ext = file.split(".")
                if ext == "csv":
                    video_list_params.append([parent_folder + "/" + folder, video_name, video_id])
                    #download_chat(parent_folder + "/" + folder, video_name, video_id)
                    #print(file)


q = queue.Queue()

# thread_list = []
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()
threading.Thread(target=worker, daemon=True).start()

for params in video_list_params:
    q.put(params)
    #thread_list.append(threading.Thread(target=external_chat_capture, name="id_" + params[2], args=params))

q.join()

print("Finished")


# for thr in thread_list:
#     thr.start()
