import os
import sys
import pytchat
import unicodedata
import re

##utils
def writeOnFile(filename, slist, headers):
    outf = open(filename, "w", encoding="utf-8")
    print(*headers,sep=",", file=outf)
    for k in slist:
        print('\"' + k + '\"', *slist[k], sep=",",file=outf)

##Constants
# if len(sys.argv) > 1:
#     list_dic = sys.argv[1]
#     video_name = sys.argv[2]
#     video_id = sys.argv[3]

##Get video name

def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def download_chat(parent_folder, video_name, video_id, overwrite=True, persistent=True, echo=True, slugify=False):
    os.makedirs(parent_folder, exist_ok=True)

    CHAT_HEADERS = ["type","id","message","timestamp","datetime","elapsedTime","amountValue","amountString","currency","bgColor","author.name","author.channelId","author.channelUrl","author.imageUrl","author.badgeUrl","author.isVerified","author.isChatOwner","author.isChatSponsor","author.isChatModerator"]

    if slugify:
        video_name = slugify(video_name)

    new_filename = parent_folder + "/" + video_name + "." + video_id + ".csv"

    write_mode = "w" if overwrite else "a+"
    exist_flag = os.path.exists(new_filename)

    chatoutf = open(new_filename, write_mode, encoding="utf-8")

    if not exist_flag and write_mode == "a+":
        print(*CHAT_HEADERS, sep=",", file=chatoutf)

    chat = pytchat.create(video_id=video_id)

    retries = 10

    # try:
    dled_messages = 0
    if echo:
        print("Downloading", video_id,"...")
    while True:
        while chat.is_alive():
            for c in chat.get().items:
                try:
                    dled_messages += 1

                    message = [c.type,c.id, '"' + c.message.replace('"',"'") + '"',c.timestamp,c.datetime,'"' + c.elapsedTime + '"','"' + str(c.amountValue) + '"','"' + c.amountString + '"','"' + c.currency + '"', c.bgColor, '"' + c.author.name + '"',c.author.channelId, c.author.channelUrl,c.author.imageUrl,c.author.badgeUrl,c.author.isVerified,c.author.isChatOwner,c.author.isChatSponsor,c.author.isChatModerator]
                    print(*message, sep=",", file=chatoutf)
                    
                    #print("Elapsed Time:", c.elapsedTime, "Downloaded messages: ", dled_messages, " " * 15, end="\r")
                except:
                    pass
        if persistent and retries >= 0:
            if echo:
                print("restarting", video_id)
            retries -= 1
        else:
            return

def download_chat_timestamp(parent_folder, video_name, video_id):
    CHAT_HEADERS = ["message","timestamp","elapsedTime"]

    chatoutf = open(parent_folder + "/" + video_name + "." + video_id + "_timestamps.csv", "w", encoding="utf-8")
    print(*CHAT_HEADERS, sep=",", file=chatoutf)

    chat = pytchat.create(video_id=video_id)

    # try:
    print("Downloading (timestamp only)", video_id,"...")
    dled_messages = 0
    while chat.is_alive():
        for c in chat.get().items:
            try:
                dled_messages += 1
                message = ['"' + c.message.replace('"',"'") + '"',c.timestamp,c.elapsedTime]
                print(*message, sep=",", file=chatoutf)
                print("Elapsed Time:", c.elapsedTime, "Downloaded messages: ", dled_messages, " " * 15, end="\r")
            except:
                pass

    # except :
    #     writeOnFile(parent_folder + "/" + video_name + "." + video_id + ".chatters.err.csv", chatter_list, HEADERS)
    # finally:
    #     writeOnFile(parent_folder + "/" + video_name + "." + video_id + ".chatters.csv", chatter_list, HEADERS)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        download_chat_timestamp("./", "call_download_" + sys.argv[1], sys.argv[1])
        #download_chat("./", "call_download_" + sys.argv[1], sys.argv[1])
    if len(sys.argv) == 3:
        download_chat(sys.argv[1], "", sys.argv[2])
    else:
        if len(sys.argv) > 2:
            download_chat(sys.argv[1],sys.argv[2],sys.argv[3])
    