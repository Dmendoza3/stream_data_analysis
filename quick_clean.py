import re

i_file = open("members.txt", "r", encoding="utf-8")
o_file = open("members.clean.txt", "w", encoding="utf-8")

for line in i_file:
    line_clean = re.sub(r':.*:', '', line)
    line_clean = line_clean.replace("\n", "") #.replace(".", "").replace(",","").replace('"', "").replace("’","").replace("'","").replace("!")
    line_clean = re.sub(r'[^a-zA-Z\d\s]', '', line_clean)

    if line_clean == " ":
        line_clean = ""

    if len(line_clean):
        try:
            print(line_clean, file=o_file)
        except:
            print("error parse")