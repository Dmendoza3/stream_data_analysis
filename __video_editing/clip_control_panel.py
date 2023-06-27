import unicodedata
import re

from datetime import timedelta

from cut_mp4 import cut_mp4
from convert_to_mp3 import convert_clip_mp3

import tkinter as tk
from tkinter import Label, Text, Button 

from download_yt import get_stream_current_duration, get_yt_video_url, download_yt_video
from get_current_live_stream import get_video_info



def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

class CustomWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "test"
        self.geometry('300x330')
        self.prefetched_url = ""
        self.stream_info = None

        self.elements = {}

    def add_textbox(self, name, n_text, pack_opt={}):
        self.elements[name] = (n_text, pack_opt)

    def add_label(self, name, n_label, pack_opt={}):
        self.elements[name] = (n_label, pack_opt)

    def add_button(self, name, n_button, pack_opt={}):
        self.elements[name] = (n_button, pack_opt)

    def start(self):
        for el in self.elements:
            element, pack_opts = self.elements[el]
            element.pack(**pack_opts)
        self.mainloop()

    def print_log(self, txt):
        self.get_element("logger").insert(tk.END, txt + "\n")

    def get_element(self, key):
        return self.elements[key][0]

    def get_stream_info(self):
        video_id = self.get_element("textbox_video_id").get("1.0", tk.END) 
        
        if len(video_id) < 11:
            self.print_log("Error: invalid id")
            return

        if not self.prefetched_url:
            self.print_log("Info: prefetched_url loaded")
            self.prefetched_url = get_yt_video_url(video_id)

        if not self.stream_info:
            self.print_log("Info: stream_info loaded")
            self.stream_info = get_video_info(video_id)

        duration_secs = int(float(get_stream_current_duration(video_id, prefetched_url=self.prefetched_url)))
        duration = timedelta(seconds=duration_secs)

        self.get_element("label_stream_start")["text"] = f"Stream time: {str(duration)}"
        self.get_element("label_stream_title")["text"] = f"Stream title: {self.stream_info[2]}"

    def get_clip(self, c_time=30, sup_clips=-1):
        video_id = self.get_element("textbox_video_id").get("1.0", tk.END) 
        
        if len(video_id) < 11:
            return
        
        if not self.prefetched_url:
            self.get_stream_info()


        self.print_log("generating clip...")

        duration_secs = int(float(get_stream_current_duration(video_id, prefetched_url=self.prefetched_url)))
        start_time = timedelta(seconds=duration_secs - 30)
        length = timedelta(seconds=c_time)

        video_name = slugify(self.stream_info[2])
        filename = video_name + "_" + str(start_time).replace(":","") + f"_{str(c_time)}"
        self.print_log(f"Generating {filename}, start_time: {start_time}, length: {length}")
        download_yt_video(self, start_time, length, filename, False, self.prefetched_url)

        if sup_clips > 0 and c_time >= 10:
            q_time = c_time / sup_clips
            start_time = 0
            for i in range(sup_clips):
                n_filename = video_name + f"_q{i}.mp4"
                cut_mp4(filename + ".mp4", start_time, q_time, n_filename, False)
                convert_clip_mp3(n_filename, False)

                start_time += q_time



window = CustomWindow()

##Video data loader
window.add_label("label_video_id", Label(window, text="video url:"), {"anchor":"w", "padx":5})
window.add_textbox("textbox_video_id", Text(window, height = 1, width = 11), {"anchor":"w", "padx":5})
window.add_button("button_video_data", Button(window, text="Load", command=lambda: window.get_stream_info()), {"anchor":"w", "padx":5})
window.add_button("button_clip_60s", Button(window, text="Clip 60s", command=lambda: window.get_clip(60)), {"anchor":"w", "padx":5})
window.add_button("button_clip_30s", Button(window, text="Clip 30s", command=lambda: window.get_clip(30)), {"anchor":"w", "padx":5})
window.add_button("button_clip_10s", Button(window, text="Clip 15s", command=lambda: window.get_clip(15)), {"anchor":"w", "padx":5})
window.add_button("button_clip_7s", Button(window, text="Clip 7s", command=lambda: window.get_clip(7)), {"anchor":"w", "padx":5})
window.add_button("button_clip_all", Button(window, text="Clip Multi", command=lambda: window.get_clip(30, sup_clips=4)), {"anchor":"w", "padx":5})


##Video data show
window.add_label("label_stream_start", Label(window, text="Stream time:"), {"anchor":"w", "padx":5})
window.add_label("label_stream_title", Label(window, text="Stream title:", wraplength=280), {"anchor":"w", "padx":5})

##logger
window.add_label("label_logger", Label(window, text="Log:"), {"anchor":"w", "padx":5})
window.add_textbox("logger", Text(window, height = 5, width = 52), {"anchor":"w", "padx":5})

window.start()