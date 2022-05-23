import os
import sys
import pytchat
import keyboard
from urllib.request import urlopen
from lxml.html import parse

##utils
def quickWriteOnFile():
    try:
        outf = open(list_dic + filename + ".chatters.quick.csv", "w", encoding="utf-8")
        print(*headers, sep=",", file=outf)
        for k in chatter_list:
            print('\"' + k + '\"', *chatter_list[k], sep=",",file=outf)
    except:
        pass

def writeOnFile(filename, slist, headers):
    outf = open(filename, "w", encoding="utf-8")
    print(*headers,sep=",", file=outf)
    for k in slist:
        print('\"' + k + '\"', *slist[k], sep=",",file=outf)


##Constants
disc = "C:\\Users\\dario.mendoza\\Downloads"
list_dic = disc + "\(member_lists)\\"
os.system("if exist " + list_dic + "mkdir " + list_dic)
headers = ["name","channelId","channelUrl","imageUrl","badgeUrl","isVerified","isChatOwner","isChatSponsor","isChatModerator"]
chatter_list = {}

##Get video name
video_id = sys.argv[1]
youtube_url = 'https://www.youtube.com/watch?v='
url = youtube_url + video_id
# page = urlopen(url)
# p = parse(page)
# filename = ("".join(list(filter(lambda ch: ord(ch) in range(1, 128) and (ch not in "<>:\"/\\|?*"), p.find(".//title").text.replace(" - YouTube", ""))))).replace(" ", "_")
filename = "test"


chat = pytchat.create(video_id=video_id)


keyboard.add_hotkey('g', quickWriteOnFile)

try:
    while chat.is_alive():
        for c in chat.get().items:
            chatter_list[c.author.name] = [c.author.channelId,c.author.channelUrl,c.author.imageUrl,c.author.badgeUrl,c.author.isVerified,c.author.isChatOwner,c.author.isChatSponsor,c.author.isChatModerator]
            print(c.datetime, len(chatter_list))
                
except :
    writeOnFile(list_dic + filename + ".chatters.err.csv", chatter_list, headers)
finally:
    writeOnFile(list_dic + filename + ".chatters.csv", chatter_list, headers)