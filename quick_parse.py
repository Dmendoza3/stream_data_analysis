i_file = open("members.clean.txt", "r", encoding="utf-8")
o_file = open("members.parsed.csv", "w", encoding="utf-8")

count_dict = {}

for line in i_file:
    for word in line.split(" "):
        k_word = word.replace("\n", "")
        if not count_dict.get(k_word, False):
            count_dict[k_word] = 1
        else:
            count_dict[k_word] += 1

print("word,count", file=o_file)

for k in count_dict:
    print(k, count_dict[k], sep=",", file=o_file)