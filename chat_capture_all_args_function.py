import sys
import pytchat

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

def download_chat(parent_folder, video_name, video_id):
    HEADERS = ["name","channelId","channelUrl","imageUrl","badgeUrl","isVerified","isChatOwner","isChatSponsor","isChatModerator"]
    CHAT_HEADERS = ["type","id","message","timestamp","datetime","elapsedTime","amountValue","amountString","currency","bgColor","author.name","author.channelId","author.channelUrl","author.imageUrl","author.badgeUrl","author.isVerified","author.isChatOwner","author.isChatSponsor","author.isChatModerator"]

    chatter_list = {}
    chatoutf = open(parent_folder + "/" + video_name + "." + video_id + ".csv", "w", encoding="utf-8")
    print(*CHAT_HEADERS, sep=",", file=chatoutf)

    chat = pytchat.create(video_id=video_id)

    # try:
    print("Downloading", video_id,"...", end="")
    while chat.is_alive():
        for c in chat.get().items:
            try:
                message = [c.type,c.id, '"' + c.message.replace('"',"'") + '"',c.timestamp,c.datetime,'"' + c.elapsedTime + '"','"' + str(c.amountValue) + '"','"' + c.amountString + '"','"' + c.currency + '"', c.bgColor, '"' + c.author.name + '"',c.author.channelId, c.author.channelUrl,c.author.imageUrl,c.author.badgeUrl,c.author.isVerified,c.author.isChatOwner,c.author.isChatSponsor,c.author.isChatModerator]
                chatter_list[c.author.name] = [c.author.channelId,c.author.channelUrl,c.author.imageUrl,c.author.badgeUrl,c.author.isVerified,c.author.isChatOwner,c.author.isChatSponsor,c.author.isChatModerator]
                #print("\rDownloading", video_id,"..." ,len(chatter_list), end="")
                print(*message, sep=",", file=chatoutf)
            except:
                pass

    # except :
    #     writeOnFile(parent_folder + "/" + video_name + "." + video_id + ".chatters.err.csv", chatter_list, HEADERS)
    # finally:
    #     writeOnFile(parent_folder + "/" + video_name + "." + video_id + ".chatters.csv", chatter_list, HEADERS)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        download_chat(sys.argv[1], "", sys.argv[2])
    else:
        if len(sys.argv) > 2:
            download_chat(sys.argv[1],sys.argv[2],sys.argv[3])
    