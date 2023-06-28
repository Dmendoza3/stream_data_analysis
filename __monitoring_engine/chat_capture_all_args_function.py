import os
import sys
import pytchat
from datetime import datetime
import unicodedata
import re

##Get video name

def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '_', value).strip('-_')

def download_chat(parent_folder, video_name, video_id, overwrite=True, persistent=True, echo=True, fix_filename=False):
    os.makedirs(parent_folder, exist_ok=True)

    CHAT_HEADERS = ["type","id","message","timestamp","datetime","elapsedTime","amountValue","amountString","currency","bgColor","author.name","author.channelId","author.channelUrl","author.imageUrl","author.badgeUrl","author.isVerified","author.isChatOwner","author.isChatSponsor","author.isChatModerator"]

    if fix_filename:
        video_name = slugify(video_name)

    print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]", video_id, parent_folder, f"{video_name}.csv", file=open("yt_chat_downloads.log", "a"))

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

if __name__ == "__main__":
    if len(sys.argv) == 2:
        download_chat_timestamp("./", "call_download_" + sys.argv[1], sys.argv[1])
        #download_chat("./", "call_download_" + sys.argv[1], sys.argv[1])
    elif len(sys.argv) == 3:
        download_chat(sys.argv[1], "", sys.argv[2])
    elif len(sys.argv) == 4:
        download_chat(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        if sys.argv[4] == "-auto":
            download_chat(sys.argv[1], sys.argv[2], sys.argv[3], overwrite=False,persistent=False, echo=True, fix_filename=True)
    
    print(sys.argv)