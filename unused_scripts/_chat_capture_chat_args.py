import os
import sys
import pytchat
import keyboard
from urllib.request import urlopen
from lxml.html import parse


##Constants
disc = "D:"
list_dic = disc + "\(member_lists)\\"
os.system("if exist " + list_dic + "mkdir " + list_dic)
headers = ["type","id","message","timestamp","datetime","elapsedTime","amountValue","amountString","currency","bgColor","author.name","author.channelId","author.channelUrl","author.imageUrl","author.badgeUrl","author.isVerified","author.isChatOwner","author.isChatSponsor","author.isChatModerator"]
chatter_list = []

##Get video name
video_id = sys.argv[1]
youtube_url = 'https://www.youtube.com/watch?v='
url = youtube_url + video_id
page = urlopen(url)
p = parse(page)
filename = ("".join(list(filter(lambda ch: ord(ch) in range(1, 128) and (ch not in "<>:\"/\\|?*"), p.find(".//title").text.replace(" - YouTube", ""))))).replace(" ", "_")

outf = open(list_dic + filename + ".chat.csv", "w", encoding="utf-8")
print(*headers, sep=",", file=outf)


chat = pytchat.create(video_id=video_id)


while chat.is_alive():
    for c in chat.get().items:
        message = [c.type,c.id, '"' + c.message.replace('"',"'") + '"',c.timestamp,c.datetime,'"' + c.elapsedTime + '"','"' + str(c.amountValue) + '"','"' + c.amountString + '"','"' + c.currency + '"', '"' + c.author.name + '"',c.bgColor,c.author.channelId,c.author.channelUrl,c.author.imageUrl,c.author.badgeUrl,c.author.isVerified,c.author.isChatOwner,c.author.isChatSponsor,c.author.isChatModerator]
        #print(*message, sep=",")
        if int(c.elapsedTime.split(":")[-1]) % 30 == 0:
            print(c.elapsedTime)
        print(*message, sep=",", file=outf)