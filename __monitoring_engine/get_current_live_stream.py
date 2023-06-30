import requests
from html.parser import HTMLParser

class currentLiveParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.video_id = ""
        self.video_url = ""
        self.title = ""
        self.description = ""
        self.keywords = ""
        self.scheduled_start_time = '-1'

        self.first_script = 0

    def handle_starttag(self, tag, attrs):
        if tag == "link":
            if attrs[0][1] == "canonical":
                self.video_url = attrs[1][1]
                if "watch" in self.video_url:
                    self.video_id = self.video_url.split("v=")[1]
                else:
                    self.video_id = "-1"

        if tag == "script" and self.first_script == 0:
            self.first_script = 1

        if self.video_id != "-1":
            if tag == "meta":
                if attrs[0][1] == "title":
                    self.title = attrs[1][1]

                if attrs[0][1] == "description":
                    self.description = attrs[1][1]

                if attrs[0][1] == "keywords":
                    self.keywords = attrs[1][1]

    def handle_endtag(self, tag):
        if tag=="script" and self.first_script == 1:
            self.first_script = 0

    def handle_data(self, data):
        if self.first_script == 1:
            scheduledStartTime_pos = data.find("scheduledStartTime")
            if scheduledStartTime_pos > 0:
                self.scheduled_start_time = data[scheduledStartTime_pos + 21:scheduledStartTime_pos + 31]
                self.first_script = -1
            #print("found time:", data.find("scheduledStartTime"))
    
    def get_video_data(self):
        return (self.video_id, self.video_url, self.title, self.description, self.keywords, self.scheduled_start_time)


def get_current_live_stream(channel_id):
    url = f"https://www.youtube.com/channel/{channel_id}/live"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"})
    #response = requests.get(url, headers={"User-Agent": "Test App (v0.0.1)"})

    txt = response.text

    parser = currentLiveParser()
    parser.feed(txt)

    #print(txt, file=open("raw.html","w", encoding="utf-8"))

    return parser.get_video_data()

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"}) #desktop
    #response = requests.get(url, headers={"User-Agent": "Test App (v0.0.1)"}) #test app

    txt = response.text

    #print(txt, file=open("raw.html","w", encoding="utf-8"))

    parser = currentLiveParser()
    parser.feed(txt)

    return parser.get_video_data()


if __name__=="__main__":
    ##IRyS
    channelID = "UC8rcEBzJSleTkf_-agPM20g"

    #channelID = "UCHsx4Hqa-1ORjQTh9TYDhww"
    
    print(get_current_live_stream(channelID))


    #print(get_video_info("2J-PNiBCT24"))
