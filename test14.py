id_list = []

id_list = [line.split(",")[0] for line in open("channel_names.txt", "r", encoding="utf-8")]

print(id_list)