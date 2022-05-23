import re
import sys
import csv
from urllib.request import urlopen
from lxml.html import parse

##Constants
disc = "C:\\Users\\dario.mendoza\\Downloads"
list_dic = disc + "\(member_lists)\\"
filename = sys.argv[1]
full_filename = list_dic + filename
chat_ext = ".chat.csv"
chatter_ext = ".chatters.csv"

chat_list = []
chatter_list = []

with open(full_filename + chat_ext, "r", encoding="utf-8") as csv_chat:
    reader = csv.reader(csv_chat, delimiter=",", quotechar='"')
    for row in reader:
        chat_list.append(row)

with open(full_filename + chatter_ext, "r", encoding="utf-8") as csv_chat:
    reader = csv.reader(csv_chat, delimiter=",", quotechar='"')
    for row in reader:
        chatter_list.append(row)


chat_headers = chat_list[0]
chatter_headers = chatter_list[0]

#
list_sc =  list(filter(lambda row: row[chat_headers.index("type")] == "superChat", chat_list))
list_chatModerator = list(filter(lambda row: row[chat_headers.index("author.isChatModerator")] == "True", chat_list))
list_chatOwner = list(filter(lambda row: row[chat_headers.index("author.isChatOwner")] == "True", chat_list))
list_isVerified = list(filter(lambda row: row[chat_headers.index("author.isVerified")] == "True", chat_list))
#
list_members = list(filter(lambda row: row[chatter_headers.index("isChatSponsor")] == "True", chatter_list))

##Analisys
total_msgs = len(chat_list) - 1
stream_duration = chat_list[-1][chat_headers.index("elapsedTime")].split(":")
stream_duration = int(stream_duration[0]) * 3600 + int(stream_duration[1]) * 60 + int(stream_duration[2])
msg_per_second = total_msgs / stream_duration
sc_per_minute= len(list_sc) / (stream_duration / 60)
#todo: total superchat (values)
total_chatters = len(chatter_list) - 1
#todo: total members per badge
total_chatModerator = len(list_chatModerator)


user_analisys = {}
for msg in chat_list:
    userId = msg[chat_headers.index("author.channelId")]
    msgId = msg[chat_headers.index("id")]
    msgType = msg[chat_headers.index("type")]
    msgContent = msg[chat_headers.index("message")]
    if not user_analisys.get(userId, False):
        user_analisys[userId] = {'firstMessage': msgId, 'lastMessage':msgId, 'chatCount': 1, 'scAmount':1 if msgType=='superChat' else 0, 'wordlist':{}, 'stickerList':{}}
    else:
        user_analisys[userId]['lastMessage'] = msgId
        user_analisys[userId]['chatCount'] += 1 
        user_analisys[userId]['scAmount'] += 1 if msgType=='superChat' else 0
    
    msgNoSticker = re.sub(r'\s+',' ',re.sub(r':_[a-zA-Z0-9]*:', ' ',msgContent)).strip().split(" ")
    msgOnlySticker = re.findall(r':_[a-zA-Z0-9]*:',msgContent)
    #user_analisys[userId]['wordlist'] = ''
    #print(msgNoSticker)
    #user_analisys[userId]['stickerList'] = ''
    if msgNoSticker:
        print(msgNoSticker, end='\n\n')


#for k in user_analisys:
#    print(k)

print(user_analisys[max(list(user_analisys), key=lambda x: user_analisys[x]['chatCount'])])


##Message analisys
#list of sticker uses (1, groups of 2, 3) (by user)
#list of words (1, groups of 2, 3) (by user)
