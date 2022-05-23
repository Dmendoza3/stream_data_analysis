import pytchat

list_dic = "F:/(member_lists)/"
outf = open(list_dic + "gura_members2.csv","w", encoding="utf-8")

video_id = 'hD6LwW7Zkf8'
chat = pytchat.create(video_id=video_id)

member_list = {}
try:
    while chat.is_alive():
        for c in chat.get().items:
            if c.author.badgeUrl:
                member_list[c.author.name] = c.author.channelUrl
                print(len(member_list))
except :
    print("name,channel", file=outf)
    for k in member_list:
        print(k, member_list[k], sep=",",file=outf)
finally:
    print("name,channel", file=outf)
    for k in member_list:
        print(k, member_list[k], sep=",",file=outf)