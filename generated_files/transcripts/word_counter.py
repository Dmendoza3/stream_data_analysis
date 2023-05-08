in_f = open("transcript_join.csv", "r")
out_f = open("word_count.csv", "w")

word_count = {}

for line in in_f:
    for word in line.replace("\n","").split(" "):
        if word_count.get(word, -1) == -1:
            word_count[word] = 1
        else:
            word_count[word] += 1

print("word,count", file=out_f)
for k in word_count:
    print(f"{k},{word_count[k]}", file=out_f)
