import sys
import pytchat
from urllib.request import urlopen
from lxml.html import parse

##utils
def writeOnFile(ext):
    outf = open(list_dic + filename, "w", encoding="utf-8")
    print("name,channel", file=outf)
    for k in member_list:
        print('\"' + k + '\"', member_list[k] + ext, sep=",",file=outf)

##Constants
list_dic = "F:/(member_lists)/"
video_id = sys.argv[1]
youtube_url = 'https://www.youtube.com/watch?v='
url = youtube_url + video_id
page = urlopen(url)
p = parse(page)
filename = ("".join(list(filter(lambda ch: ord(ch) > 0 and ord(ch) < 127, p.find(".//title").text.replace(" - YouTube", ""))))).replace(" ", "_")



chat = pytchat.create(video_id=video_id)

member_list = {}
try:
    while chat.is_alive():
        for c in chat.get().items:
            if c.author.badgeUrl:
                member_list[c.author.name] = c.author.channelUrl
                print(c.datetime, len(member_list))
except :
    writeOnFile(".err.csv")
finally:
    writeOnFile(".csv")